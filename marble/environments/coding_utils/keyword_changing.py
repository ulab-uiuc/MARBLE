import os

def replace_model_name(file_paths):
    # 要替换的模型名称
    old_model = "gpt-3.5-turbo"
    new_model = "together_ai/meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
    
    for file_path in file_paths:
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                continue
                
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # 检查是否包含要替换的文本
            if old_model in content:
                # 替换文本
                new_content = content.replace(old_model, new_model)
                
                # 写入新内容
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                print(f"Replaced model name in: {file_path}")
            else:
                print(f"Model name not found in: {file_path}")
                
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

if __name__ == "__main__":
    # 要处理的文件列表
    files_to_process = [
        "/home/zhe36/MARBLE/marble/engine/engine_planner.py",
        "/home/zhe36/MARBLE/marble/configs/coding_config/coding_config.yaml",
        "/home/zhe36/MARBLE/marble/evaluator/evaluator.py",
        "/home/zhe36/MARBLE/marble/agent/coding_agent.py",
        "/home/zhe36/MARBLE/marble/agent/base_agent.py",
        "/home/zhe36/MARBLE/marble/memory/long_term_memory.py",
        "/home/zhe36/MARBLE/marble/memory/short_term_memory.py",
        "/home/zhe36/MARBLE/marble/environments/coding_utils/coder.py",
        "/home/zhe36/MARBLE/marble/environments/coding_utils/reviewer.py",
    ]
    
    print("Starting model name replacement...")
    replace_model_name(files_to_process)
    print("Replacement process completed.")