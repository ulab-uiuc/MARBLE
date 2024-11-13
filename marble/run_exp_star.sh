#!/bin/bash

# Define the path to the configuration file
CONFIG_FILE="./configs/generated_yaml_files_star_research_Llama3.1_70B"

# Execute the simulation engine with the specified configuration
python main.py --config "$CONFIG_FILE"
