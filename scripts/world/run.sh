#!/bin/bash
# Run the bargaining (world simulation) scenario of MultiAgentBench.
#
#   bash scripts/world/run.sh                               # all 100 tasks, gpt-4o-mini
#   MODEL=openrouter/google/gemini-2.5-flash bash scripts/world/run.sh --task_ids 1-10
#
# Extra arguments are forwarded to scripts/run_benchmark.py (see --help).
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MODEL="${MODEL:-gpt-4o-mini}"

python "$REPO_ROOT/scripts/run_benchmark.py" --scenario bargaining --model "$MODEL" "$@"
