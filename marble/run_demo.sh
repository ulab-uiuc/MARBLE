#!/bin/bash
# Run a single demo configuration (coding scenario by default).
#
#   bash marble/run_demo.sh
#   bash marble/run_demo.sh --llm openrouter/google/gemini-2.5-flash
#   CONFIG_FILE=marble/configs/test_config.yaml bash marble/run_demo.sh
#
# Extra arguments are forwarded to marble/main.py (see --help).
set -euo pipefail
MARBLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${CONFIG_FILE:-$MARBLE_DIR/configs/coding_config/coding_config.yaml}"

# Execute the simulation engine with the specified configuration
python "$MARBLE_DIR/main.py" --config_path "$CONFIG_FILE" "$@"
