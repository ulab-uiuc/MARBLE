#!/bin/bash

# Define the path to the configuration file
CONFIG_FILE="./configs/test_config_tree.yaml"

# Execute the simulation engine with the specified configuration
python main.py --config "$CONFIG_FILE"
