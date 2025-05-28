#!/bin/bash

# Define the path to the configuration file
CONFIG_FILE="/opt/dlami/nvme/zhe/MARBLE/marble/configs/coding_config/coding_config.yaml"

# Execute the simulation engine with the specified configuration
python main.py --config_path "$CONFIG_FILE"
