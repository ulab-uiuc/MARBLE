#!/usr/bin/env python3
import glob
import json
import os
import shutil

import yaml


def extract_task_content(yaml_data):
    """
    Given the loaded YAML data, extract the task content.
    The task field may either be a string or a dictionary with a 'content' key.
    """
    if "task" in yaml_data:
        task_field = yaml_data["task"]
        if isinstance(task_field, dict) and "content" in task_field:
            return task_field["content"]
        elif isinstance(task_field, str):
            return task_field
    return None

def build_yaml_mapping(yaml_folder):
    """
    Scan the yaml_folder for YAML files and build a mapping from task content to
    the full path of the YAML file.

    If more than one file has the same task content, they are stored in a list.
    """
    mapping = {}
    # Support both .yaml and .yml file extensions
    yaml_files = glob.glob(os.path.join(yaml_folder, "*.yaml"))
    yaml_files.extend(glob.glob(os.path.join(yaml_folder, "*.yml")))

    for file_path in yaml_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            task_content = extract_task_content(data)
            if task_content is not None:
                if task_content in mapping:
                    mapping[task_content].append(file_path)
                else:
                    mapping[task_content] = [file_path]
            else:
                print(f"Warning: No valid task content in {file_path}")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    return mapping

def process_jsonl_and_copy(jsonl_file, yaml_folder, dest_folder):
    """
    Read the jsonl_file line by line. First, determine the number of JSON objects
    with an empty 'iterations' field. Then, for each of these objects, find the
    corresponding YAML file (by matching the 'task' content) in the yaml_folder and copy
    it to dest_folder.
    """
    # List to store JSON objects with empty iterations
    empty_iterations_items = []

    # Read the JSONL file and count items with empty iterations.
    with open(jsonl_file, 'r', encoding='utf-8') as jf:
        for line_num, line in enumerate(jf, start=1):
            try:
                record = json.loads(line)
                print(record['iterations'])
            except Exception as e:
                print(f"Error parsing JSON on line {line_num}: {e}")
                continue

            # Get the iterations field (defaulting to an empty list if not available)
            iterations = record.get("iterations", [])
            if not isinstance(iterations, list):
                iterations = []

            if len(iterations) == 0:
                empty_iterations_items.append(record)

    # Print the count of items with empty iterations
    print(f"Found {len(empty_iterations_items)} item(s) with empty iterations.")

    # Build a mapping from task content to YAML file paths from the YAML folder
    yaml_mapping = build_yaml_mapping(yaml_folder)

    # Ensure the destination folder exists
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # Process each item with empty iterations and copy the corresponding YAML file(s)
    for idx, record in enumerate(empty_iterations_items, start=1):
        task_text = record.get("task", "")
        if task_text in yaml_mapping:
            for yaml_file in yaml_mapping[task_text]:
                dest_path = os.path.join(dest_folder, os.path.basename(yaml_file))
                try:
                    shutil.copy(yaml_file, dest_path)
                    print(f"[Item {idx}] Copied {yaml_file} to {dest_path}")
                except Exception as e:
                    print(f"Error copying {yaml_file} to {dest_path}: {e}")
        else:
            print(f"[Item {idx}] Warning: No matching YAML file found for task.")

def main():
    # Define sample file paths and folder names directly.
    jsonl_file = "/Users/zhukunlun/Documents/GitHub/MARBLE/marble/result/discussion_output_llama3.3_70b.jsonl"
    yaml_folder = "/Users/zhukunlun/Documents/GitHub/MARBLE/marble/configs/generated_yaml_files_graph_llama3.3_70b_100"                       # Folder containing YAML files
    dest_folder = "/Users/zhukunlun/Documents/GitHub/MARBLE/marble/configs/generated_yaml_files_graph_llama3.3_70b_100_test2" # Destination folder for YAML files with empty iterations

    # Ensure the directory for the JSONL file exists (if needed)
    jsonl_dir = os.path.dirname(jsonl_file)
    if jsonl_dir and not os.path.exists(jsonl_dir):
        os.makedirs(jsonl_dir)

    process_jsonl_and_copy(jsonl_file, yaml_folder, dest_folder)

if __name__ == "__main__":
    main()
