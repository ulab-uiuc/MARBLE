WORKSPACE_DIR="/opt/dlami/nvme/zhe/MARBLE/marble/workspace"
UPDATE_SCRIPT="/opt/dlami/nvme/zhe/MARBLE/marble/environments/coding_utils/tools/update_config.py"
RUN_DEMO_SCRIPT="/opt/dlami/nvme/zhe/MARBLE/marble/run_demo.sh"

model_name="meta-llama/Llama-3.1-70B-Instruct"
safe_model_name=$(echo ${model_name} | tr '/' '_')
LOG_DIR="/opt/dlami/nvme/zhe/MARBLE/marble/logs/${safe_model_name}"

mkdir -p ${LOG_DIR}

for id in {1..2}; do
    echo "Processing task with ID=$id..."
    rm -rf ${WORKSPACE_DIR}/*
    python ${UPDATE_SCRIPT} --id ${id}
    echo "Running the demo script..."
    bash ${RUN_DEMO_SCRIPT}
    echo "Saving solution file..."
    cp ${WORKSPACE_DIR}/solution.py ${LOG_DIR}/solution_${id}.py
    echo "Task with ID=$id completed."
    echo "==============================="
done

echo "All tasks have been processed!"
