WORKSPACE_DIR="marble/workspace"
UPDATE_SCRIPT="scripts/coding/utils/update_reasoning_config.py"
RUN_DEMO_SCRIPT="marble/run_demo.sh"
BASE_CONFIG_DIR="marble/configs"

CONFIG_PATHS=(
    "${BASE_CONFIG_DIR}/reflexion_config/coding_config.yaml"
    "${BASE_CONFIG_DIR}/react_config/coding_config.yaml"
    "${BASE_CONFIG_DIR}/cot_config/coding_config.yaml"
)

model_name="gpt-3.5-turbo"
safe_model_name=$(echo ${model_name} | tr '/' '_')
BASE_LOG_DIR="marble/logs/${safe_model_name}"

for config_path in "${CONFIG_PATHS[@]}"; do
    method_name=$(echo ${config_path} | grep -o '[^/]*/coding_config.yaml' | cut -d'/' -f1)
    LOG_DIR="${BASE_LOG_DIR}/${method_name}"
    CONFIG_OUTPUT_DIR="${BASE_CONFIG_DIR}/${method_name}_configs"
    mkdir -p ${LOG_DIR}
    mkdir -p ${CONFIG_OUTPUT_DIR}

    echo "Starting experiments with ${method_name}..."

    for id in {1..10}; do
        echo "Processing ${method_name} task with ID=$id..."
        rm -rf ${WORKSPACE_DIR}/*
        python ${UPDATE_SCRIPT} --id ${id} --config ${config_path}
        echo "Running the demo script..."
        config_dir=$(dirname ${config_path})

        echo "Saving solution file..."
        cp ${WORKSPACE_DIR}/solution.py ${LOG_DIR}/solution_${id}.py
        cp ${config_path} ${CONFIG_OUTPUT_DIR}/config_${id}.yaml
        echo "Task with ID=$id completed."
        echo "==============================="
    done

    echo "Copying result file for ${method_name}..."
    cp marble/result/development_output.jsonl marble/result/${method_name}_output.jsonl
    rm marble/result/development_output.jsonl

    echo "${method_name} experiments completed!"
    echo "==============================="
done

echo "All experiments have been completed!"
