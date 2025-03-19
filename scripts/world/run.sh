#!/bin/bash

# Define the directory containing the YAML configuration files
CONFIG_DIR="/Users/guoshuyi/Desktop/marble2/MARBLE/data/bargaining-data/yaml-seller-Llama-3.1-70B-Instruct-Turbo"

# Check if the directory exists
if [ ! -d "$CONFIG_DIR" ]; then
    echo "Error: Directory $CONFIG_DIR does not exist."
    exit 1
fi

# Iterate over all YAML files in the directory
for CONFIG_FILE in "$CONFIG_DIR"/*.yaml; do
    if [ -f "$CONFIG_FILE" ]; then
        echo "Running configuration: $CONFIG_FILE"
        python main.py --config_path "$CONFIG_FILE"

        # Check if the execution was successful
        if [ $? -ne 0 ]; then
            echo "Error: Failed to run $CONFIG_FILE"
        else
            echo "Successfully ran $CONFIG_FILE"
        fi
    fi
done
