# Database Diagnosis Environment

This environment is designed to simulate a multiagent system where agents collaborate to diagnose database issues. It is based on [DB-GPT](https://github.com/TsinghuaDatabaseGroup/DB-GPT).

## Features
- **Multiagent Collaboration:** Agents interact in a fully connected network to exchange expertise and ideas.
- **Database Diagnosis Tools Integration:** Agents have full access to PostgreSQL databases, where they retrieve from tables such as `pg_stat_activity`, `pg_locks`, and `pg_stat_database`, to diagnose database issues.
- **Curated Benchmark Dataset:** Utilizes 100 curated database diagnosis cases based on 10 scenarios.
- **Configurable Environment:** Easily adjustable simulation parameters and evaluation metrics through configuration files.

## Execution Steps

You will need `docker` and `docker-compose` installed to run the simulation. To prepare the environment on a Linux system, you will need sudo privileges. It is generally not recommended to run it on a shared server, as it is light enough to operate on your own laptop.

To install docker and docker-compose, you can follow the instructions on the [official website](https://docs.docker.com/compose/install/).

The config files are in `marble/configs/test_config_database`. I have used OpenAI and Fireworks AI API so you would need to set up these environments: `OPENAI_API_KEY` and `FIREWORKS_AI_API_KEY`.

In `marble/result/`, you will also need to set up these folders

```
result_gpt-3.5-turbo/
result_gpt-4o-mini/
result-llama-3.1-8b/
result-llama-3.1-70b/
result-llama-3.3-70b/
```

Run `bash run_simulation.sh` to execute the example code. You could tweak the prompt to run all other benchmark cases. This particular example will save to `result_gpt-3.5-turbo/`.

To run evaluation, place `batch_eval.py` into the `marble/result/` folder and execute.