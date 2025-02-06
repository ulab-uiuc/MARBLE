import os

def replace_model_name(file_paths):
    old_model = "meta-llama/Llama-3.1-8B-Instruct"
    new_model = "meta-llama/Llama-3.1-70B-Instruct"
    
    for file_path in file_paths:
        try:
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                continue
                
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
           
            if old_model in content:
                new_content = content.replace(old_model, new_model)
                
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                print(f"Replaced model name in: {file_path}")
            else:
                print(f"Model name not found in: {file_path}")
                
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

if __name__ == "__main__":
    files_to_process = [
        "/opt/dlami/nvme/zhe/MARBLE/marble/engine/engine_planner.py",
        "/opt/dlami/nvme/zhe/MARBLE/marble/configs/coding_config/coding_config.yaml",
        "/opt/dlami/nvme/zhe/MARBLE/marble/evaluator/evaluator.py",
        "/opt/dlami/nvme/zhe/MARBLE/marble/agent/coding_agent.py",
        "/opt/dlami/nvme/zhe/MARBLE/marble/agent/base_agent.py",
        "/opt/dlami/nvme/zhe/MARBLE/marble/memory/long_term_memory.py",
        "/opt/dlami/nvme/zhe/MARBLE/marble/memory/short_term_memory.py",
        "/opt/dlami/nvme/zhe/MARBLE/marble/environments/coding_utils/coder.py",
        "/opt/dlami/nvme/zhe/MARBLE/marble/environments/coding_utils/reviewer.py",
    ]
    
    print("Starting model name replacement...")
    replace_model_name(files_to_process)
    print("Replacement process completed.")