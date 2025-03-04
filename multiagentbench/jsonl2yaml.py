#!/usr/bin/env python3
"""
Script: jsonl_to_yaml.py
Description: Convert a JSONL file to individual YAML files.
             For each JSON record, if the cleared keys/sub-keys have empty values,
             fill them with the provided default values.
             For dictionary keys ('environment', 'memory', 'output'),
             only update sub-keys that are in the provided defaults.
             For 'metrics', only update the sub-key 'evaluate_llm' if its value is empty.
             The output YAML files are named task_<task_id>.yaml.
"""

import argparse
import json
import os

import yaml


def parse_default(value):
    """
    Parse a JSON string into a Python object.
    """
    try:
        return json.loads(value)
    except Exception:
        return value

def fill_defaults(data, defaults):
    # For string keys.
    if "coordinate_mode" in data and data["coordinate_mode"] == "":
        data["coordinate_mode"] = defaults["coordinate_mode"]
    if "llm" in data and data["llm"] == "":
        data["llm"] = defaults["llm"]

    # For dictionary keys: environment, memory, output.
    for key in ["environment", "memory", "output"]:
        if key in data and isinstance(data[key], dict):
            for sub_key, default_val in defaults[key].items():
                if sub_key in data[key] and data[key][sub_key] == "":
                    data[key][sub_key] = default_val

    # For metrics: only update evaluate_llm.
    if "metrics" in data and isinstance(data["metrics"], dict):
        if "evaluate_llm" in data["metrics"] and data["metrics"]["evaluate_llm"] == "":
            data["metrics"]["evaluate_llm"] = defaults["metrics"]["evaluate_llm"]

    return data

def main():
    parser = argparse.ArgumentParser(
        description="Convert a JSONL file to YAML files with default values filled in."
    )
    parser.add_argument("--input_file", type=str, required=True,
                        help="Path to the input JSONL file.")
    parser.add_argument("--output_folder", type=str, default=".",
                        help="Folder where the YAML files will be saved.")
    parser.add_argument("--default_coordinate_mode", type=str, default="graph",
                        help="Default value for coordinate_mode.")
    parser.add_argument("--default_environment", type=str,
                        default='{"max_iterations": 3, "name": "Research Collaboration Environment", "type": "Research"}',
                        help="Default JSON string for environment.")
    parser.add_argument("--default_llm", type=str, default="gpt-3.5-turbo",
                        help="Default value for llm.")
    parser.add_argument("--default_memory", type=str,
                        default='{"type": "BaseMemory"}',
                        help="Default JSON string for memory.")
    parser.add_argument("--default_metrics_evaluate_llm", type=str, default="gpt-4o",
                        help="Default value for metrics.evaluate_llm.")
    parser.add_argument("--default_output", type=str,
                        default='{"file_path": "result/discussion_output.jsonl"}',
                        help="Default JSON string for output.")
    args = parser.parse_args()

    defaults = {
        "coordinate_mode": args.default_coordinate_mode,
        "environment": parse_default(args.default_environment),
        "llm": args.default_llm,
        "memory": parse_default(args.default_memory),
        "metrics": {"evaluate_llm": args.default_metrics_evaluate_llm},
        "output": parse_default(args.default_output)
    }

    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

    with open(args.input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data = json.loads(line)
                data = fill_defaults(data, defaults)
                task_id = data.get("task_id", 1)
                output_filename = f"task_{task_id}.yaml"
                output_path = os.path.join(args.output_folder, output_filename)
                with open(output_path, 'w', encoding='utf-8') as out_f:
                    yaml.dump(data, out_f, allow_unicode=True, sort_keys=False)

if __name__ == "__main__":
    main()
