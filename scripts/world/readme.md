# Bargaining (World Simulation) Environment

Buyers and sellers negotiate over a product with the tools of the environment (`offer_price`,
`reject_and_counter`, `provide_information`, `accept_offer`, ...).

Set the API key of your provider (see the main README), then run from any directory:

```bash
# all 100 bargaining tasks
python scripts/run_benchmark.py --scenario bargaining --model gpt-4o-mini

# a few tasks with another model
python scripts/run_benchmark.py --scenario bargaining --model openrouter/google/gemini-2.5-flash --task_ids 1-5
```

`bash scripts/world/run.sh` is a thin wrapper around the same command
(`MODEL=... bash scripts/world/run.sh --limit 5`).

Results are written to `results/bargaining/<model>/`. The negotiation is judged from both sides:
`task_evaluation.buyer` and `task_evaluation.seller` each hold the scores for effectiveness of
strategies, progress and outcome, and interaction dynamics (the prompt no longer has to be switched
by hand in `evaluator.py`).
