WORKSPACE_DIR="workspace"
UPDATE_SCRIPT="../scripts/coding/utils/update_coding_config.py"
RUN_DEMO_SCRIPT="run_demo.sh"
CONFIG_FILE="configs/coding_config/coding_config.yaml"

model_name="gpt-3.5-turbo"
safe_model_name=$(echo ${model_name} | tr '/' '_')
LOG_DIR="logs/${safe_model_name}"

mkdir -p ${LOG_DIR}

for id in $(seq 1 1); do
    echo "Processing task with ID=$id..."
    rm -rf ${WORKSPACE_DIR}/*
    python ${UPDATE_SCRIPT} --benchmark_id ${id}
    echo "Running the demo script..."
    python main.py --config_path "$CONFIG_FILE"
    echo "Saving solution file..."
    cp ${WORKSPACE_DIR}/solution.py ${LOG_DIR}/solution_${id}.py
    echo "Task with ID=$id completed."
    echo "==============================="
done

echo "All tasks have been processed!"