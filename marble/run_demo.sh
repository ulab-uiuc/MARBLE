#!/bin/bash

# Define the directory containing the configuration files
CONFIG_DIR="./configs/test_config_db_100"

# Iterate over each YAML file in the configuration directory
for CONFIG_FILE in "$CONFIG_DIR"/*.yaml; do
    # Execute the simulation engine with the specified configuration
    python main.py --config "$CONFIG_FILE"
done
