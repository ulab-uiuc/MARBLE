#!/bin/bash

# Define paths
WORKSPACE_DIR="/home/zhe36/MARBLE/marble/workspace"
UPDATE_SCRIPT="/home/zhe36/MARBLE/marble/environments/coding_utils/update_config.py"
RUN_DEMO_SCRIPT="/home/zhe36/MARBLE/marble/run_demo.sh"
REPLACE_MODEL_SCRIPT="/home/zhe36/MARBLE/marble/environments/coding_utils/replace_model.py"
RESULT_OUTPUT_FILE="/home/zhe36/MARBLE/marble/result/development_output.jsonl"

# Function to replace model keyword and handle results
replace_model_and_process_result() {
    local old_model=$1
    local new_model=$2
    local result_file=$3

    # Replace model keyword
    echo "Replacing model from '${old_model}' to '${new_model}'..."
    python ${REPLACE_MODEL_SCRIPT} "${old_model}" "${new_model}"

    # Run tasks
    for id in 1; do
        echo "Processing task with ID=$id..."

        # Clean the workspace directory
        echo "Cleaning ${WORKSPACE_DIR}..."
        rm -rf ${WORKSPACE_DIR}/*
        
        # Update the configuration file
        echo "Updating configuration file with ID=${id}..."
        python ${UPDATE_SCRIPT} --id ${id}
        
        # Run the demo script
        echo "Running the demo script..."
        bash ${RUN_DEMO_SCRIPT}

        echo "Task with ID=$id completed."
        echo "==============================="
    done

    # Process the result file
    echo "Copying results to ${result_file} and clearing ${RESULT_OUTPUT_FILE}..."
    cp ${RESULT_OUTPUT_FILE} ${result_file}
    > ${RESULT_OUTPUT_FILE}
}

echo "Starting tasks..."

# Step 1: Replace to Llama-3.1-70B
replace_model_and_process_result \
    "together_ai/meta-llama/Llama-3.3-70B-Instruct-Turbo" \
    "together_ai/meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo" \
    "/home/zhe36/MARBLE/marble/result/development_3.1-70B.jsonl"

# Step 2: Replace to Llama-3.1-8B
replace_model_and_process_result \
    "together_ai/meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo" \
    "together_ai/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo" \
    "/home/zhe36/MARBLE/marble/result/development_3.1-8B.jsonl"

# Step 3: Replace to GPT-3.5-Turbo
replace_model_and_process_result \
    "together_ai/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo" \
    "gpt-3.5-turbo" \
    "/home/zhe36/MARBLE/marble/result/development_3.5-turbo.jsonl"

echo "All tasks completed!"
