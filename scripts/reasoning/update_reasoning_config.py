import argparse
import json
import os

from ruamel.yaml import YAML


def load_benchmark(benchmark_path, target_id):
    with open(benchmark_path, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            if entry.get("id") == target_id:
                return entry
    raise ValueError(f"No benchmark entry found with id={target_id}")


def update_config(config_path, benchmark_entry):
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


def main():
    parser = argparse.ArgumentParser(
        description="Update configuration file based on benchmark ID."
    )
    parser.add_argument(
        "--id",
        type=int,
        required=True,
        help="Benchmark entry ID to use for updating the config.",
    )
    parser.add_argument(
        "--config", type=str, required=True, help="Path to the configuration file"
    )
    args = parser.parse_args()

    config_path = args.config
    benchmark_path = "environments/coding_utils/assets/benchmark.jsonl"

    if not os.path.exists(config_path):
        print(f"Config file not found: {config_path}")
        return

    if not os.path.exists(benchmark_path):
        print(f"Benchmark file not found: {benchmark_path}")
        return

    try:
        benchmark_entry = load_benchmark(benchmark_path, args.id)
    except ValueError as e:
        print(e)
        return

    update_config(config_path, benchmark_entry)
    print(f"Config file updated to use benchmark ID={args.id}")


if __name__ == "__main__":
    main()
