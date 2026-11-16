"""Sanity checks for the benchmark data and the unified runner."""

import argparse
import importlib.util
import json
import os
from typing import Any, Dict, List

import pytest

from marble.environments.minecraft_env import (
    REQUIRED_MINECRAFT_ASSETS,
    MinecraftEnvironment,
)
from marble.utils.paths import DATA_DIR, REPO_ROOT

SCENARIOS = ["research", "bargaining", "coding", "database", "minecraft"]


def load_records(scenario: str) -> List[Dict[str, Any]]:
    path = os.path.join(REPO_ROOT, "multiagentbench", scenario, f"{scenario}_main.jsonl")
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def load_runner():  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(
        "run_benchmark", os.path.join(REPO_ROOT, "scripts", "run_benchmark.py")
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_each_scenario_has_100_distinct_tasks(scenario: str) -> None:
    records = load_records(scenario)
    assert len(records) == 100
    assert len({record["task_id"] for record in records}) == 100
    assert all(record["scenario"] == scenario for record in records)


def test_minecraft_assets_are_present_and_cover_every_task() -> None:
    # Issues #222 / #243: these files were missing from the repository.
    for name in REQUIRED_MINECRAFT_ASSETS:
        assert os.path.isfile(os.path.join(DATA_DIR, name)), name
    MinecraftEnvironment.check_assets()

    with open(os.path.join(DATA_DIR, "blueprint_description_all.json")) as f:
        descriptions = json.load(f)
    with open(os.path.join(DATA_DIR, "building_blue_print.json")) as f:
        blueprints = json.load(f)

    records = load_records("minecraft")
    environment_ids = [record["environment"]["task_id"] for record in records]
    assert sorted(environment_ids) == list(range(100))
    for record in records:
        task_id = record["environment"]["task_id"]
        assert f"task_{task_id}" in descriptions
        assert task_id < len(blueprints)
        blueprint_text = json.dumps(descriptions[f"task_{task_id}"], indent=4)
        assert record["task"]["content"].endswith(blueprint_text)


def runner_args(**overrides: Any) -> argparse.Namespace:
    values = dict(
        scenario="research",
        model="my/model",
        eval_model=None,
        coordinate_mode=None,
        max_iterations=None,
        planning_method=None,
        minecraft_host="localhost",
        minecraft_port=25565,
    )
    values.update(overrides)
    return argparse.Namespace(**values)


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_runner_fills_in_a_runnable_config(scenario: str, tmp_path) -> None:  # type: ignore[no-untyped-def]
    runner = load_runner()
    record = load_records(scenario)[0]
    config = runner.build_config(record, runner_args(scenario=scenario), str(tmp_path))

    assert config["llm"] == "my/model"
    assert config["metrics"]["evaluate_llm"] == "my/model"
    assert config["coordinate_mode"] in runner.COORDINATE_MODES
    assert config["environment"]["type"] == runner.SCENARIO_DEFAULTS[scenario]["environment"]["type"]
    assert isinstance(config["environment"]["max_iterations"], int)
    assert config["output"]["file_path"] == os.path.join(str(tmp_path), "results.jsonl")
    assert config["memory"]["type"]
    if scenario == "coding":
        assert config["environment"]["workspace_dir"].startswith(str(tmp_path))


def test_runner_builds_a_hierarchy_for_tree_mode(tmp_path) -> None:  # type: ignore[no-untyped-def]
    runner = load_runner()
    record = load_records("research")[0]
    config = runner.build_config(
        record, runner_args(coordinate_mode="tree"), str(tmp_path)
    )
    parents = [rel for rel in config["relationships"] if rel[2] == "parent"]
    assert [rel[0] for rel in parents] == ["agent1"] * (len(config["agents"]) - 1)


def test_runner_summary_ignores_unscored_iterations() -> None:
    runner = load_runner()
    results = [
        {
            "task_id": 1,
            "token_usage": 100,
            "planning_scores": [4, -1],
            "communication_scores": [-1, -1],
            "total_milestones": 3,
            "iterations": [{}, {}],
            "task_evaluation": {"innovation": 4, "safety": 5, "feasibility": 3},
        },
        {"task_id": 2, "error": "boom"},
    ]
    summary = runner.summarize(results, "research")
    assert summary["num_completed"] == 1 and summary["num_failed"] == 1
    assert summary["planning_score"] == 4.0
    assert summary["communication_score"] is None
    assert summary["task_score"] == 4.0
    assert runner.parse_task_ids("1,3-5") == [1, 3, 4, 5]
