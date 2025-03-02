WORKSPACE_DIR="/opt/dlami/nvme/zhe/MARBLE/marble/configs/coding_config"
UPDATE_SCRIPT="/opt/dlami/nvme/zhe/MARBLE/marble/environments/coding_utils/tools/update_config.py"
RUN_DEMO_SCRIPT="/opt/dlami/nvme/zhe/MARBLE/marble/run_demo.sh"
CONFIG_DIR="/opt/dlami/nvme/zhe/MARBLE/marble/configs/coding_configs"

model_name="together_ai/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
safe_model_name=$(echo ${model_name} | tr '/' '_')
LOG_DIR="/opt/dlami/nvme/zhe/MARBLE/marble/logs/${safe_model_name}"

mkdir -p ${LOG_DIR}

for id in {1..100}; do
    echo "Processing task with ID=$id..."
    python ${UPDATE_SCRIPT} --id ${id}
    echo "Running the demo script..."
    cp ${WORKSPACE_DIR}/coding_config.yaml ${CONFIG_DIR}/config_${id}.yaml
    echo "==============================="
done

echo "All tasks have been processed!"

