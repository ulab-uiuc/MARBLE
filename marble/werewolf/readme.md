# Werewolf Game Simulation Environment

This repository provides a configurable environment for simulating Werewolf (Mafia) games with AI agents. Key features include full-game simulation, checkpoint loading, and evaluation modes.

## Installation

```bash
pip install -r requirements.txt

## Configuration

Modify game settings in marble/configs/test_config/werewolf_config/werewolf_config.yaml:

roles: # List of roles in the game
  - werewolf
  - villager
  - seer
  - witch
  - guardian
  ...
randomize_roles: True  # Shuffle role order
use_random_names: True  # Assign random names to agents
cooperation_mode: "cooperative"  # Villager cooperation strategy
use_daily_tasks: True  # Enable daily guidance for villagers

### API configurations
villager_config:
  base_model: "gpt-3.5-turbo"
  api_key: "your_villager_api_key"

werewolf_config:
  base_model: "gpt-4"
  api_key: "your_werewolf_api_key"
Important Notes:

Currently supports 9-player games (3 wolves, 3 villagers, 3 unique special roles). You can change roles in config.yaml.

Do not duplicate special roles (seer/witch/guardian)

## Running Simulations
Start new simulations using:

./marble/werewolf/run_simulation.sh \
  --rounds 10 \
  --name "werewolf_engine_demo" \
  --config_path "marble/configs/test_config/werewolf_config/werewolf_config.yaml"
Output:

Game checkpoints stored in base_log_dir/simulation

Includes complete game states after each day/night phase

## Running Evaluations
Evaluate existing checkpoints with:

./marble/werewolf/run_evaluation.sh \
  --top_level_dir "path/to/checkpoints" \
  --config_path "marble/configs/test_config/werewolf_config/werewolf_config.yaml" \
  --snapshot_folder "any_name_here" \
  --base_log_dir "path/to/evaluation/results"
Evaluation Modes:

Single-day Simulation: Loads nightly checkpoints and simulates one full day-night cycle

Full-game Simulation: Loads first night checkpoint and simulates through game conclusion

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