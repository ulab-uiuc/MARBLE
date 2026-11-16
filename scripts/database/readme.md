# Database Diagnosis Environment

This environment is designed to simulate a multiagent system where agents collaborate to diagnose database issues. It is based on [DB-GPT](https://github.com/TsinghuaDatabaseGroup/DB-GPT).

## Features
- **Multiagent Collaboration:** Agents interact in a fully connected network to exchange expertise and ideas.
- **Database Diagnosis Tools Integration:** Agents have full access to PostgreSQL databases, where they retrieve from tables such as `pg_stat_activity`, `pg_locks`, and `pg_stat_database`, to diagnose database issues.
- **Curated Benchmark Dataset:** Utilizes 100 curated database diagnosis cases based on 10 scenarios.
- **Configurable Environment:** Easily adjustable simulation parameters and evaluation metrics through configuration files.

## Execution Steps

You need `docker` with the compose plugin; follow the instructions on the
[official website](https://docs.docker.com/compose/install/). The environment is light enough to
run on a laptop. `sudo` is only used if your user cannot talk to the Docker daemon directly.

Each task starts a fresh PostgreSQL (pinned to version 17), Prometheus and two exporters from
`marble/environments/db_env_docker/docker-compose.yml`, injects the anomalies of the task, lets the
agents diagnose it, and removes the containers again when the task is finished. Ports 5432, 9090,
9100 and 9187 must be free.

Run the benchmark from any directory (set the API key of your provider first, see the main README):

```bash
# all 100 database tasks
python scripts/run_benchmark.py --scenario database --model gpt-4o-mini

# a few tasks with another model
python scripts/run_benchmark.py --scenario database --model openrouter/google/gemini-2.5-flash --task_ids 1-5
```

`bash scripts/database/run_simulation.sh` is a thin wrapper around the same command
(`MODEL=... bash scripts/database/run_simulation.sh --limit 5`).

## Results

Results are written to `results/database/<model>/`. Every record in `results.jsonl` contains

- `task_evaluation.root_cause`: the gold root cause(s),
- `task_evaluation.predicted`: the agents' final answer (free text),
- `task_evaluation.predicted_labels` and `task_evaluation.accuracy`: the labels the judge model
  extracted from that answer and the fraction of gold root causes among them,

and `summary.json` reports the mean accuracy together with the coordination scores.

`batch_eval.py` is the original offline scorer for results stored as one JSON file per task; it is
kept for reproducing older runs and is not needed with `run_benchmark.py`.

The pre-generated per-model configs in `marble/configs/test_config_database` can still be run one
by one with `python marble/main.py --config_path <config>`.
