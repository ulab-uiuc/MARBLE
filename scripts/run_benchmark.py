#!/usr/bin/env python
"""
Run MultiAgentBench tasks end to end with a single command.

Examples (run from anywhere)::

    # 3 research tasks with an OpenAI model
    python scripts/run_benchmark.py --scenario research --model gpt-4o-mini --limit 3

    # specific bargaining tasks with Gemini through OpenRouter, tree coordination
    python scripts/run_benchmark.py --scenario bargaining \
        --model openrouter/google/gemini-2.5-flash \
        --task_ids 1,2,3 --coordinate_mode tree

    # only recompute the summary of an earlier run
    python scripts/run_benchmark.py --scenario research --model gpt-4o-mini --summary_only

For every task the script fills in the blanks of the benchmark record
(model, environment, coordination mode, output path), saves the resulting YAML
config next to the results, runs the engine and appends one JSON line per task
to ``<output_dir>/<scenario>/<model>/results.jsonl``. Finished tasks are skipped
when the command is run again, so interrupted runs can simply be restarted.
"""

import argparse
import copy
import json
import os
import shutil
import sys
import time
import traceback
from typing import Any, Dict, Iterable, List, Optional

import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

BENCHMARK_DIR = os.path.join(REPO_ROOT, "multiagentbench")

# Blanks left in the benchmark JSONL records are filled with these values.
SCENARIO_DEFAULTS: Dict[str, Dict[str, Any]] = {
    "research": {
        "coordinate_mode": "graph",
        "environment": {
            "type": "Research",
            "name": "Research Collaboration Environment",
            "max_iterations": 5,
        },
    },
    "bargaining": {
        "coordinate_mode": "graph",
        "environment": {
            "type": "WorldSimulation",
            "name": "World Simulation Environment",
            "max_iterations": 3,
        },
    },
    "coding": {
        "coordinate_mode": "graph",
        "environment": {
            "type": "Coding",
            "name": "Coding Environment",
            "max_iterations": 5,
        },
    },
    "database": {
        "coordinate_mode": "graph",
        "environment": {
            "type": "DB",
            "name": "DB Simulation Environment",
            "max_iterations": 5,
        },
    },
    "minecraft": {
        "coordinate_mode": "graph",
        "environment": {
            "type": "Minecraft",
            "name": "Minecraft Environment",
            "max_iterations": 20,
        },
    },
}

COORDINATE_MODES = ["graph", "star", "tree", "chain"]


def log(message: str) -> None:
    """Print progress immediately, even when stdout is redirected to a file."""
    print(message, flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run MultiAgentBench scenarios and aggregate their scores.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--scenario",
        required=True,
        choices=sorted(SCENARIO_DEFAULTS),
        help="Benchmark scenario to run.",
    )
    parser.add_argument(
        "--model",
        required=True,
        help="Agents' model, as a LiteLLM model name (e.g. gpt-4o-mini, "
        "openrouter/google/gemini-2.5-flash, together_ai/meta-llama/...).",
    )
    parser.add_argument(
        "--eval_model",
        default=None,
        help="Judge model used by the evaluator. Defaults to --model.",
    )
    parser.add_argument(
        "--task_ids",
        default=None,
        help="Comma separated task ids and/or ranges, e.g. '1,2,10-20'. "
        "Defaults to every task of the scenario.",
    )
    parser.add_argument(
        "--limit", type=int, default=None, help="Run at most this many tasks."
    )
    parser.add_argument(
        "--coordinate_mode",
        choices=COORDINATE_MODES,
        default=None,
        help="Coordination protocol. Defaults to the value in the benchmark "
        "record, or 'graph' when it is blank.",
    )
    parser.add_argument(
        "--max_iterations",
        type=int,
        default=None,
        help="Override the maximum number of iterations per task.",
    )
    parser.add_argument(
        "--planning_method",
        choices=["naive", "cot", "group_discuss", "cognitive_evolve"],
        default=None,
        help="Planner strategy used in star coordination.",
    )
    parser.add_argument(
        "--minecraft_host",
        default="localhost",
        help="Host of the Minecraft server (minecraft scenario only).",
    )
    parser.add_argument(
        "--minecraft_port",
        type=int,
        default=25565,
        help="Port of the Minecraft server (minecraft scenario only).",
    )
    parser.add_argument(
        "--output_dir",
        default="results",
        help="Directory where configs, results and summaries are written.",
    )
    parser.add_argument(
        "--input_file",
        default=None,
        help="Benchmark JSONL file. Defaults to "
        "multiagentbench/<scenario>/<scenario>_main.jsonl.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Re-run tasks that already have a result instead of skipping them.",
    )
    parser.add_argument(
        "--summary_only",
        action="store_true",
        help="Do not run anything; only aggregate the existing results.",
    )
    return parser.parse_args()


def parse_task_ids(spec: Optional[str]) -> Optional[List[int]]:
    """Turn '1,2,10-12' into [1, 2, 10, 11, 12]."""
    if not spec:
        return None
    task_ids: List[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = part.split("-", 1)
            task_ids.extend(range(int(start), int(end) + 1))
        else:
            task_ids.append(int(part))
    return task_ids


def load_tasks(input_file: str) -> List[Dict[str, Any]]:
    """Load benchmark records, assigning task ids to records that lack one."""
    tasks: List[Dict[str, Any]] = []
    with open(input_file, "r", encoding="utf-8") as f:
        for index, line in enumerate(line for line in f if line.strip()):
            record = json.loads(line)
            if record.get("task_id") is None:
                # Minecraft records keep their id inside the environment block.
                record["task_id"] = record.get("environment", {}).get("task_id", index)
            tasks.append(record)
    return tasks


def safe_name(name: str) -> str:
    return "".join(c if c.isalnum() or c in "-_." else "_" for c in name)


def build_config(
    record: Dict[str, Any], args: argparse.Namespace, run_dir: str
) -> Dict[str, Any]:
    """Fill the blanks of a benchmark record and apply command-line overrides."""
    config = copy.deepcopy(record)
    scenario = args.scenario
    defaults = SCENARIO_DEFAULTS[scenario]
    task_id = config["task_id"]

    config["scenario"] = scenario
    config["llm"] = args.model
    for agent in config.get("agents", []):
        agent.pop("llm", None)

    config["coordinate_mode"] = (
        args.coordinate_mode
        or config.get("coordinate_mode")
        or defaults["coordinate_mode"]
    )

    environment = config.setdefault("environment", {})
    for key, value in defaults["environment"].items():
        if environment.get(key) in (None, ""):
            environment[key] = value
    if args.max_iterations is not None:
        environment["max_iterations"] = args.max_iterations
    environment["max_iterations"] = int(environment["max_iterations"])
    if scenario == "coding":
        # One workspace per task: a leftover solution.py from another task
        # would otherwise be picked up (and judged) as this task's solution.
        environment["workspace_dir"] = os.path.join(
            run_dir, "workspace", f"task_{task_id}"
        )

    if scenario == "minecraft":
        # The benchmark records spread tasks over several servers/ports for
        # parallel runs; this runner is sequential and uses a single server.
        environment["host"] = args.minecraft_host
        environment["port"] = args.minecraft_port
        for offset, agent in enumerate(config.get("agents", [])):
            agent["agent_port"] = 5000 + offset

    relationships = config.setdefault("relationships", [])
    agent_ids = [agent["agent_id"] for agent in config.get("agents", [])]
    if (
        config["coordinate_mode"] == "tree"
        and agent_ids
        and not any(len(rel) == 3 and rel[2] == "parent" for rel in relationships)
    ):
        # Tree coordination needs a hierarchy, which most benchmark records do
        # not define. Without it only the first agent would ever act, so use
        # the first agent as the root and every other agent as its child.
        log(
            f"[run_benchmark] task {task_id}: no 'parent' relationship defined; "
            f"using '{agent_ids[0]}' as the root of the tree."
        )
        for child_id in agent_ids[1:]:
            relationships.append([agent_ids[0], child_id, "parent"])

    memory = config.setdefault("memory", {})
    if not memory.get("type"):
        memory["type"] = "SharedMemory"

    metrics = config.setdefault("metrics", {})
    metrics["evaluate_llm"] = args.eval_model or args.model

    engine_planner = config.setdefault("engine_planner", {})
    engine_planner.setdefault("initial_progress", "Starting the simulation.")
    if args.planning_method:
        engine_planner["planning_method"] = args.planning_method

    output = config.setdefault("output", {})
    output["format"] = "jsonl"
    output["file_path"] = os.path.join(run_dir, "results.jsonl")
    return config


def read_results(results_path: str) -> List[Dict[str, Any]]:
    if not os.path.isfile(results_path):
        return []
    results = []
    with open(results_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                results.append(json.loads(line))
            except json.JSONDecodeError:
                log(f"[run_benchmark] Skipping malformed line in {results_path}")
    return results


def rewrite_results_without(results_path: str, task_ids: Iterable[Any]) -> None:
    """Drop earlier records of the given tasks (used with --overwrite)."""
    drop = {str(task_id) for task_id in task_ids}
    kept = [r for r in read_results(results_path) if str(r.get("task_id")) not in drop]
    with open(results_path, "w", encoding="utf-8") as f:
        for record in kept:
            f.write(json.dumps(record, default=str) + "\n")


def is_complete(record: Dict[str, Any]) -> bool:
    """A record counts as finished when the engine reached its final bookkeeping."""
    return "token_usage" in record and not record.get("error")


def run_task(config: Dict[str, Any], config_path: str) -> Optional[str]:
    """Run one task in-process. Returns an error message, or None on success."""
    from marble.configs.config import Config
    from marble.engine.engine import Engine

    try:
        engine = Engine(Config.load(config_path))
        engine.start()
        return None
    except KeyboardInterrupt:
        raise
    except Exception as e:  # keep going with the remaining tasks
        traceback.print_exc()
        return f"{type(e).__name__}: {e}"


def _mean(values: Iterable[float]) -> Optional[float]:
    values = list(values)
    return round(sum(values) / len(values), 4) if values else None


def _valid_scores(scores: Any) -> List[float]:
    """Scores of -1 mean "nothing to evaluate" and are left out of averages."""
    if not isinstance(scores, list):
        return []
    return [s for s in scores if isinstance(s, (int, float)) and s >= 0]


def summarize(results: List[Dict[str, Any]], scenario: str) -> Dict[str, Any]:
    """Aggregate per-task records into benchmark-level numbers."""
    completed = [r for r in results if is_complete(r)]
    summary: Dict[str, Any] = {
        "scenario": scenario,
        "num_tasks": len(results),
        "num_completed": len(completed),
        "num_failed": len(results) - len(completed),
    }
    if not completed:
        return summary

    planning = [_mean(_valid_scores(r.get("planning_scores"))) for r in completed]
    communication = [
        _mean(_valid_scores(r.get("communication_scores"))) for r in completed
    ]
    planning = [p for p in planning if p is not None]
    communication = [c for c in communication if c is not None]
    summary["planning_score"] = _mean(planning)
    summary["communication_score"] = _mean(communication)
    # Coordination score (CS in the paper): mean of planning and communication.
    coordination = []
    for r in completed:
        parts = [
            _mean(_valid_scores(r.get("planning_scores"))),
            _mean(_valid_scores(r.get("communication_scores"))),
        ]
        parts = [p for p in parts if p is not None]
        if parts:
            coordination.append(sum(parts) / len(parts))
    summary["coordination_score"] = _mean(coordination)
    summary["avg_milestones"] = _mean(
        r.get("total_milestones", 0) or 0 for r in completed
    )
    summary["avg_token_usage"] = _mean(r.get("token_usage", 0) or 0 for r in completed)
    summary["avg_iterations"] = _mean(len(r.get("iterations", [])) for r in completed)

    task_scores: Dict[str, List[float]] = {}

    def collect(prefix: str, value: Any) -> None:
        if isinstance(value, dict):
            for key, sub_value in value.items():
                collect(f"{prefix}.{key}" if prefix else key, sub_value)
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            if value >= 0:  # -1 marks an unparsable judge answer
                task_scores.setdefault(prefix, []).append(float(value))

    for r in completed:
        if scenario == "coding":
            collect("code_quality", r.get("code_quality") or {})
        elif scenario == "database":
            evaluation = r.get("task_evaluation") or {}
            if isinstance(evaluation, dict) and "accuracy" in evaluation:
                collect("accuracy", evaluation["accuracy"])
        elif scenario == "minecraft":
            collect("block_hit_rate_x5", r.get("task_evaluation"))
        else:
            collect("", r.get("task_evaluation") or {})

    summary["task_scores"] = {key: _mean(values) for key, values in task_scores.items()}
    all_task_values = [
        sum(values) / len(values) for values in task_scores.values() if values
    ]
    # Task score (TS): mean over the scenario's task-level criteria.
    summary["task_score"] = _mean(all_task_values)
    return summary


def print_summary(summary: Dict[str, Any], results_path: str) -> None:
    print("\n" + "=" * 70)
    print(f"MultiAgentBench summary: {summary['scenario']}")
    print("=" * 70)
    for key, value in summary.items():
        if key == "task_scores":
            print("task_scores:")
            for name, score in (value or {}).items():
                print(f"  {name:<45} {score}")
        else:
            print(f"{key:<24} {value}")
    print(f"\nPer-task records: {results_path}")
    print("=" * 70)


def main() -> None:
    args = parse_args()

    # Load .env (API keys) before anything talks to a provider.
    from marble.main import load_env_files

    load_env_files()

    run_dir = os.path.abspath(
        os.path.join(args.output_dir, args.scenario, safe_name(args.model))
    )
    config_dir = os.path.join(run_dir, "configs")
    results_path = os.path.join(run_dir, "results.jsonl")
    summary_path = os.path.join(run_dir, "summary.json")
    os.makedirs(config_dir, exist_ok=True)

    if not args.summary_only:
        input_file = args.input_file or os.path.join(
            BENCHMARK_DIR, args.scenario, f"{args.scenario}_main.jsonl"
        )
        tasks = load_tasks(input_file)
        wanted = parse_task_ids(args.task_ids)
        if wanted is not None:
            tasks = [t for t in tasks if t["task_id"] in wanted]
        if args.limit is not None:
            tasks = tasks[: args.limit]
        if not tasks:
            log("[run_benchmark] No tasks selected.")
            sys.exit(1)

        if args.overwrite:
            rewrite_results_without(results_path, [t["task_id"] for t in tasks])
        done = {
            str(r.get("task_id")) for r in read_results(results_path) if is_complete(r)
        }

        for index, record in enumerate(tasks, start=1):
            task_id = record["task_id"]
            if str(task_id) in done:
                log(f"[run_benchmark] ({index}/{len(tasks)}) task {task_id}: done, skipping")
                continue
            log(f"[run_benchmark] ({index}/{len(tasks)}) task {task_id}: running")
            # Drop a previous failed attempt so each task has a single record.
            rewrite_results_without(results_path, [task_id])

            config = build_config(record, args, run_dir)
            workspace_dir = config["environment"].get("workspace_dir")
            if args.scenario == "coding" and workspace_dir:
                shutil.rmtree(workspace_dir, ignore_errors=True)
            config_path = os.path.join(config_dir, f"task_{task_id}.yaml")
            with open(config_path, "w", encoding="utf-8") as f:
                yaml.safe_dump(config, f, allow_unicode=True, sort_keys=False)

            started = time.time()
            error = run_task(config, config_path)
            elapsed = round(time.time() - started, 1)
            if error:
                log(f"[run_benchmark] task {task_id} FAILED after {elapsed}s: {error}")
                if not any(
                    str(r.get("task_id")) == str(task_id) for r in read_results(results_path)
                ):
                    with open(results_path, "a", encoding="utf-8") as f:
                        f.write(
                            json.dumps(
                                {
                                    "scenario": args.scenario,
                                    "task_id": task_id,
                                    "llm": args.model,
                                    "error": error,
                                }
                            )
                            + "\n"
                        )
            else:
                log(f"[run_benchmark] task {task_id} finished in {elapsed}s")

    summary = summarize(read_results(results_path), args.scenario)
    summary["model"] = args.model
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print_summary(summary, results_path)


if __name__ == "__main__":
    main()
