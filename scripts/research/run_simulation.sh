#!/bin/bash

# Define the path to the configuration file
CONFIG_FILE="./configs/test_config" #config path for the research scenario

# Execute the simulation engine with the specified configuration
python marble/main.py --config "$CONFIG_FILE"
