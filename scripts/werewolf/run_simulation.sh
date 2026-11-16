#!/bin/bash
# Simulate Werewolf games.
#
#   bash scripts/werewolf/run_simulation.sh                       # 1 game, default config
#   ROUNDS=10 CONFIG=path/to/werewolf_config.yaml bash scripts/werewolf/run_simulation.sh
#
# Models, endpoints and API keys are set in the config file (see readme.md).
# Game logs and checkpoints are written to ./werewolf_log/.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CONFIG="${CONFIG:-$REPO_ROOT/marble/configs/test_config/werewolf_config/werewolf_config.yaml}"
ROUNDS="${ROUNDS:-1}"
NAME="${NAME:-werewolf_engine_demo}"

python "$REPO_ROOT/marble/environments/werewolf_env.py" \
  --rounds "$ROUNDS" \
  --name "$NAME" \
  --config_path "$CONFIG" "$@"
