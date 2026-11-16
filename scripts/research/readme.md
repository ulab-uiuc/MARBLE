# Research Collaboration Simulation Environment

This repository provides a configurable environment for simulating multiagent research collaboration tasks. The environment facilitates knowledge exchange among AI agents to generate novel research ideas using a structured approach.

## Features

- **Multiagent Collaboration:** Agents interact in a fully connected network to exchange expertise and ideas.
- **Research Tools Integration:** Built-in functions to fetch related papers, recent publications, co-author networks, and more.
- **Curated Benchmark Dataset:** Utilizes 100 curated ML/AI papers from the ResearchTown project, categorized into 33 easy, 34 medium, and 33 hard tasks.
- **Structured Idea Generation:** Generates research ideas using a standardized 5q format.
- **Configurable Environment:** Easily adjustable simulation parameters and evaluation metrics through configuration files.

---


## Execution Steps

Set the API key of your provider (see the main README), then run from any directory:

```bash
# all 100 research tasks
python scripts/run_benchmark.py --scenario research --model gpt-4o-mini

# first 5 tasks with another model and judge
python scripts/run_benchmark.py --scenario research \
    --model openrouter/google/gemini-2.5-flash --eval_model gpt-4o --limit 5
```

`bash scripts/research/run_simulation.sh` is a thin wrapper around the same command
(`MODEL=... bash scripts/research/run_simulation.sh --limit 5`).

The runner fills in the blanks of each benchmark record with these defaults, all of which can be
overridden on the command line:

| Setting | Default | Option |
|---------|---------|--------|
| Coordination mode | `graph` | `--coordinate_mode {graph,star,tree,chain}` |
| Maximum iterations | `5` | `--max_iterations` |
| Agents' model | (required) | `--model` |
| Judge model | same as `--model` | `--eval_model` |
| Output folder | `results/` | `--output_dir` |

Results are written to `results/research/<model>/`: `results.jsonl` holds one record per task
(including the 5q research idea of every iteration and the `task_evaluation` scores for innovation,
safety and feasibility) and `summary.json` the averages.

### Generating YAML configs manually

If you prefer one YAML file per task, `multiagentbench/jsonl2yaml.py` converts the benchmark file
(see `multiagentbench/runjsonl2yaml.sh` for the available defaults). Each generated file can then be
run with `python marble/main.py --config_path <file>`.
