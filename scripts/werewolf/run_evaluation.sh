#!/bin/bash
# Evaluate Werewolf checkpoints produced by run_simulation.sh.
#
#   bash scripts/werewolf/run_evaluation.sh
#   TOP_LEVEL_DIR=werewolf_log BASE_LOG_DIR=werewolf_eval bash scripts/werewolf/run_evaluation.sh
#
# The judge model is the `eval_config` block of the config file (see readme.md).
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CONFIG="${CONFIG:-$REPO_ROOT/marble/configs/test_config/werewolf_config/werewolf_config.yaml}"
TOP_LEVEL_DIR="${TOP_LEVEL_DIR:-werewolf_log}"
BASE_LOG_DIR="${BASE_LOG_DIR:-werewolf_eval}"

python "$REPO_ROOT/marble/evaluator/werewolf_evaluator.py" \
  --top_level_dir "$TOP_LEVEL_DIR" \
  --config_path "$CONFIG" \
  --snapshot_folder "placeholder" \
  --base_log_dir "$BASE_LOG_DIR" "$@"
