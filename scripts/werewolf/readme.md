# Werewolf Game Simulation Environment

This repository provides a configurable environment for simulating Werewolf (Mafia) games with AI agents. Key features include full-game simulation, checkpoint loading, and evaluation modes.

## Installation

Install MARBLE as described in the main README (`poetry install`); no extra packages are needed.

## Configuration

Modify game settings in `marble/configs/test_config/werewolf_config/werewolf_config.yaml`:

```yaml
roles: # List of roles in the game
  - wolf
  - villager
  - seer
  - witch
  - guard
  ...
randomize_roles: True  # Shuffle role order
use_random_names: True  # Assign random names to agents
cooperation_mode: "cooperative"  # Villager cooperation strategy
use_daily_tasks: True  # Enable daily guidance for villagers

# Model of the villager team, the werewolf team and the judge.
# Any OpenAI-compatible endpoint works.
villager_config:
  base_url: "https://api.openai.com/v1"
  api_key_env: "OPENAI_API_KEY"     # the key is read from this environment variable
  model_name: "gpt-4o"

werewolf_config:
  base_url: "https://openrouter.ai/api/v1"
  api_key_env: "OPENROUTER_API_KEY"
  model_name: "google/gemini-2.5-flash"

eval_config:
  base_url: "https://api.openai.com/v1"
  api_key_env: "OPENAI_API_KEY"
  model_name: "gpt-4o"
```

Important notes:

- API keys are read from the environment variable named by `api_key_env`
  (default `OPENAI_API_KEY`). You can still put a key directly in the file with `api_key: "..."`.
- Currently supports 9-player games (3 wolves, 3 villagers, 3 unique special roles). You can change
  roles in the config.
- Do not duplicate special roles (seer/witch/guard).

## Running Simulations

Start new simulations from any directory:

```bash
bash scripts/werewolf/run_simulation.sh

# several games with a custom config
ROUNDS=10 NAME=my_run CONFIG=path/to/werewolf_config.yaml bash scripts/werewolf/run_simulation.sh
```

or call the entry point directly:

```bash
python marble/environments/werewolf_env.py --rounds 1 --name demo \
    --config_path marble/configs/test_config/werewolf_config/werewolf_config.yaml
```

Output: game logs, per-player thoughts and checkpoints after each day/night phase are stored in
`./werewolf_log/game_<timestamp>/`.

## Running Evaluations

Evaluate existing checkpoints with:

```bash
bash scripts/werewolf/run_evaluation.sh

# custom locations
TOP_LEVEL_DIR=werewolf_log BASE_LOG_DIR=werewolf_eval bash scripts/werewolf/run_evaluation.sh
```

Evaluation modes:

- Single-day simulation: loads nightly checkpoints and simulates one full day-night cycle
- Full-game simulation: loads the first night checkpoint and simulates through game conclusion

## Key Parameters

| Parameter               | Description                                |
|-------------------------|--------------------------------------------|
| `roles`                 | List of roles in the game                  |
| `randomize_roles`       | Shuffle role assignments                   |
| `use_random_names`      | Generate random agent names                |
| `cooperation_mode`      | Villager collaboration strategy            |
| `use_daily_tasks`       | Provide daily guidance to villagers        |
| `villager_config/werewolf_config` | Team-specific model configurations     |


## Output Structure
base_log_dir/
├── simulation/
│   └── [game_name]_[timestamp]/
│       ├── shared_memory.json
│       ├── checkpoints/
│       ├── players' thought.txt
│       └── final_results.json
└── evaluation/
    └── [evaluation_name]/
        ├── daily_evaluation1/
        ├── daily_evaluations2/
        ├── ...
        └── global_evaluations/

For questions or issues, please open an issue in the repository.
