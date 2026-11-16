#!/bin/bash
# Run the database diagnosis scenario of MultiAgentBench (needs Docker).
#
#   bash scripts/database/run_simulation.sh                 # all 100 tasks, gpt-4o-mini
#   MODEL=openrouter/google/gemini-2.5-flash bash scripts/database/run_simulation.sh --limit 5
#
# Extra arguments are forwarded to scripts/run_benchmark.py (see --help).
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MODEL="${MODEL:-gpt-4o-mini}"

python "$REPO_ROOT/scripts/run_benchmark.py" --scenario database --model "$MODEL" "$@"
