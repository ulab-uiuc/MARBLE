#!/bin/bash

# Define the path to the configuration file
CONFIG_FILE="./configs/test_config_db_single/test_config_db.yaml"

# Execute the simulation engine with the specified configuration
python main.py --config "$CONFIG_FILE"
