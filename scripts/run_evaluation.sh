#!/bin/bash
# Example bash script to run the evaluation script.
# Make sure to give this script execute permission: chmod +x run_evaluation.sh

# Set your parameters here
OPENAI_KEY="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"
INPUT_FILE="output_4omini.jsonl"
OUTPUT_FILE="test_output_4omini.jsonl"
PARALLEL_COUNT=8
EVAL_MODEL="gpt-4o"

# Run the evaluation script with the specified parameters
python3 ./eval_script_scoring.py \
    --openai_key "$OPENAI_KEY" \
    --input "$INPUT_FILE" \
    --output "$OUTPUT_FILE" \
    --parallel "$PARALLEL_COUNT" \
    --model "$EVAL_MODEL"
