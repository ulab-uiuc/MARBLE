import json
import argparse
import os
from ruamel.yaml import YAML

def load_benchmark(benchmark_path, target_id):
    with open(benchmark_path, 'r', encoding='utf-8') as f:
        for line in f:
            entry = json.loads(line)
            if entry.get('id') == target_id:
                return entry
    raise ValueError(f"No benchmark entry found with id={target_id}")

def update_config(config_path, benchmark_entry):
    yaml = YAML()
    yaml.preserve_quotes = True  # 保留引号
    yaml.indent(mapping=2, sequence=4, offset=2)  # 设置缩进风格

    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.load(f)

    # 固定部分
    original_content = config['task']['content']
    fixed_project_structure = "\n\n2. Project structure:\n   - solution.py (main implementation)\n"
    fixed_development_process = "\n3. Development process:\n   - Developer: Create the code.\n   - Developer: Update the code.\n   - Reviewer: Code review\n\nPlease work together to complete this task following software engineering best practices."

    # 新内容
    new_content = "Software Development Task:\n\n" + benchmark_entry['content']

    # 将 requirements 列表格式化为字符串
    requirements = benchmark_entry.get('requirements', [])
    formatted_requirements = ""
    for req in requirements:
        formatted_requirements += f"   - {req}\n"

    new_task_content = f"{new_content}\n1. Implementation requirements:\n{formatted_requirements}"
    # 合并新内容和固定部分
    merged_content = new_task_content + fixed_project_structure + fixed_development_process

    # 更新配置
    config['task']['content'] = merged_content

    # 保存更新后的配置
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f)

def main():
    parser = argparse.ArgumentParser(description="Update configuration file based on benchmark ID.")
    parser.add_argument('--id', type=int, required=True, help='Benchmark entry ID to use for updating the config.')
    args = parser.parse_args()

    config_path = "/home/zhe36/MARBLE/marble/configs/coding_config/coding_config.yaml"
    benchmark_path = "/home/zhe36/MARBLE/marble/environments/coding_utils/benchmark.jsonl"

    if not os.path.exists(config_path):
        print(f"配置文件不存在: {config_path}")
        return

    if not os.path.exists(benchmark_path):
        print(f"Benchmark文件不存在: {benchmark_path}")
        return

    try:
        benchmark_entry = load_benchmark(benchmark_path, args.id)
    except ValueError as e:
        print(e)
        return

    update_config(config_path, benchmark_entry)
    print(f"配置文件已更新为使用benchmark ID={args.id}")

if __name__ == "__main__":
    main()
