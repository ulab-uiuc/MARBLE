#!/bin/bash
# Run the coding scenario of MultiAgentBench.
#
#   bash scripts/coding/run_demo.sh                         # all 100 tasks, gpt-4o-mini
#   MODEL=openrouter/google/gemini-2.5-flash bash scripts/coding/run_demo.sh --limit 5
#
# Every task gets its own workspace; the generated programs are kept in
#   results/coding/<model>/workspace/task_<id>/solution.py
# Extra arguments are forwarded to scripts/run_benchmark.py (see --help).
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MODEL="${MODEL:-gpt-4o-mini}"

python "$REPO_ROOT/scripts/run_benchmark.py" --scenario coding --model "$MODEL" "$@"
