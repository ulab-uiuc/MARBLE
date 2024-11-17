#!/bin/bash

# Define the path to the configuration file
CONFIG_FILE="./configs/coding_config"

# Execute the simulation engine with the specified configuration
python main.py --config "$CONFIG_FILE"
