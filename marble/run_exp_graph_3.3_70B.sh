#!/bin/bash

# Define the path to the configuration file
CONFIG_FILE="./configs/generated_yaml_files_graph_llama3.3_70b_100_test2"

# Execute the simulation engine with the specified configuration
python main.py --config "$CONFIG_FILE"
