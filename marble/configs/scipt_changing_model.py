import os

import yaml


def update_yaml_llm(directory):
    """
    遍历指定目录下的所有 YAML 文件，并将 llm 键的值更新为
    'together_ai/meta-llama/Llama-3.3-70B-Instruct-Turbo'
    """
    for filename in os.listdir(directory):
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            file_path = os.path.join(directory, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)

            # 修改 llm 键的值
            if 'llm' in data:
                data['llm'] = 'together_ai/meta-llama/Llama-3.3-70B-Instruct-Turbo'

            # 保存回原文件
            with open(file_path, 'w', encoding='utf-8') as file:
                yaml.dump(data, file, allow_unicode=True, default_flow_style=False)

            print(f"Updated: {file_path}")

if __name__ == "__main__":
    folder_path = '/Users/zhukunlun/Documents/GitHub/MARBLE/marble/configs/generated_yaml_files_graph_llama3.3_70b_100'
    update_yaml_llm(folder_path)
    print("所有 YAML 文件已更新！")
