#!/bin/bash

# Define paths
WORKSPACE_DIR="/home/zhe36/MARBLE/marble/workspace"
UPDATE_SCRIPT="/home/zhe36/MARBLE/marble/environments/coding_utils/update_config.py"
RUN_DEMO_SCRIPT="/home/zhe36/MARBLE/marble/run_demo.sh"

# Loop from id=1 to id=10
for id in {17..100}; do
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

echo "All tasks have been processed!"
