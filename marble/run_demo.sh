#!/bin/bash

# Define the directory containing the configuration files
CONFIG_DIR="./configs/test_config_db_base"

scenarios=(
    'BASE'
    'EDUCATION'
    'FILE_SHARING'
    'FINANCIAL'
    'HEALTH_CARE'
    'INTERNET_OF_THINGS'
    'SOCIAL_MEDIA'
    'TELECOMMUNICATION'
)

# List scenarios and ask user to select one or more
echo "1) E_COMMERCE"
echo "2) EDUCATION"
echo "3) FILE_SHARING"
echo "4) FINANCIAL"
echo "5) HEALTH_CARE"
echo "6) INTERNET_OF_THINGS"
echo "7) SOCIAL_MEDIA"
echo "8) TELECOMMUNICATION"

read -p "Your selection: " selection

# Process user input
if [ "$selection" == "all" ]; then
    selected_scenarios=("${scenarios[@]}")
else
    IFS=',' read -r -a indices <<< "$selection"
    selected_scenarios=()
    for index in "${indices[@]}"; do
        selected_scenarios+=("${scenarios[$((index-1))]}")
    done
fi

echo "Selected scenarios: ${selected_scenarios[@]}"

# Iterate over each YAML file in the configuration directory
for CONFIG_FILE in "$CONFIG_DIR"/*.yaml; do
    # Check if the YAML file contains any of the selected scenario names
    for scenario in "${selected_scenarios[@]}"; do
        if grep -q "$scenario" "$CONFIG_FILE"; then
            # Execute the simulation engine with the specified configuration
            python main.py --config "$CONFIG_FILE" | tee "logs/$(basename "$CONFIG_FILE" .yaml)_$(date +'%Y%m%d_%H%M%S').log"
            break
        fi
    done
done
