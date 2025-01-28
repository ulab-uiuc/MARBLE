#!/bin/bash

# Define the directory containing the configuration files
CONFIG_DIR="./configs/test_config_db_gpt-4o-mini"

# Start the sudo keep-alive loop in the background
(while true; do sudo -v; sleep 240; done) &
KEEP_ALIVE_PID=$!

# Cleanup function to terminate the keep-alive process
cleanup() {
    echo "Cleaning up sudo keep-alive process..."
    kill "$KEEP_ALIVE_PID" 2>/dev/null || echo "Process already terminated."
}
trap cleanup SIGINT SIGTERM EXIT

# Iterate over each YAML file in the configuration directory
count=0
for CONFIG_FILE in "$CONFIG_DIR"/*.yaml; do
    ((count++))
    # Skip files until count >= 24
    [ "$count" -lt 28 ] && continue

    # Run the Python script and log the output
    python main.py --config "$CONFIG_FILE" | tee "logs/gpt-4o-mini-$(basename "$CONFIG_FILE" .yaml)_$(date +'%Y%m%d_%H%M%S').log"
done
