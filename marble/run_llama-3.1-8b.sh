#!/bin/bash

# Define the directory containing the configuration files
CONFIG_DIR="./configs/test_config_db_llama-3.1-8b"

count=0
# Iterate over each YAML file in the configuration directory
for CONFIG_FILE in "$CONFIG_DIR"/*.yaml; do
    # ((count++))
    # # Skip files until count >= 24
    # [ "$count" -lt 42 ] && continue
    # Execute the simulation engine with the specified configuration
    python main.py --config "$CONFIG_FILE" | tee "logs/llama-3.1-8b-$(basename "$CONFIG_FILE" .yaml)_$(date +'%Y%m%d_%H%M%S').log"
done
