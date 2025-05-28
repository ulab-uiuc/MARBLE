import json
import os

import fire
from ruamel.yaml import YAML


def update_coding_config(
    benchmark_id,
    config_path="/opt/dlami/nvme/zhe/MARBLE/marble/configs/coding_config/coding_config.yaml",
    benchmark_path="/opt/dlami/nvme/zhe/MARBLE/marble/environments/coding_utils/assets/benchmark.jsonl",
):
    if not os.path.exists(config_path):
        print(f"Config file not found: {config_path}")
        return

    if not os.path.exists(benchmark_path):
        print(f"Benchmark file not found: {benchmark_path}")
        return

    benchmark_entry = None
    with open(benchmark_path, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            if entry.get("id") == benchmark_id:
                benchmark_entry = entry
                break

    if not benchmark_entry:
        print(f"No benchmark entry found with id={benchmark_id}")
        return

    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.load(f)

    current_content = config["task"]["content"]
    start_marker = "Software Development Task:\n\n"
    end_marker = "\n1. Implementation requirements:"

    new_task = benchmark_entry["content"]
    requirements = benchmark_entry.get("requirements", [])
    formatted_requirements = ""
    for req in requirements:
        formatted_requirements += f"   - {req}\n"

    updated_content = current_content.replace(
        current_content[
            current_content.find(start_marker)
            + len(start_marker) : current_content.find(end_marker)
        ],
        new_task,
    )

    requirements_start = "1. Implementation requirements:\n"
    requirements_end = "\n\n2. Project structure:"
    updated_content = updated_content.replace(
        updated_content[
            updated_content.find(requirements_start)
            + len(requirements_start) : updated_content.find(requirements_end)
        ],
        formatted_requirements,
    )

    config["task"]["content"] = updated_content

    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f)

    print(f"Config file updated to use benchmark ID={benchmark_id}")


if __name__ == "__main__":
    fire.Fire(update_coding_config)
