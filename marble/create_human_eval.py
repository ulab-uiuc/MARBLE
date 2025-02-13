import csv
import json
import os

import yaml


def load_yaml_files(yaml_folder):
    """
    Load and parse the first 10 YAML files from the given folder.
    Returns a list of parsed YAML data dictionaries.
    """
    # List YAML files (files ending with .yaml or .yml)
    files = [f for f in os.listdir(yaml_folder) if f.endswith('.yaml') or f.endswith('.yml')]
    files = sorted(files)
    yaml_data_list = []
    # Process only the first 12 files
    for filename in files[:12]:
        full_path = os.path.join(yaml_folder, filename)
        with open(full_path, 'r', encoding='utf-8') as f:
            try:
                data = yaml.safe_load(f)
                yaml_data_list.append(data)
            except Exception as e:
                print(f"Error parsing YAML file {full_path}: {e}")
    return yaml_data_list

def load_jsonl_file(jsonl_path):
    """
    Load a JSONL file and return a dictionary mapping the task string (after stripping)
    to the corresponding JSON object.
    Assumes that each JSON object has a "task" field.
    """
    data_dict = {}
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    obj = json.loads(line)
                    # Use the task text (stripped) as key for fast lookup.
                    task_str = obj.get('task', '').strip()
                    data_dict[task_str] = obj
                except Exception as e:
                    print(f"Error parsing JSON line in {jsonl_path}: {line}\nError: {e}")
    return data_dict

def merge_iterations(iterations):
    """
    Given a list of iteration dictionaries (each containing 'iteration',
    'task_assignments', and 'communications'), merge the task assignments and communications
    into two strings. Each merged string includes the iteration number.
    """
    merged_assignments = []
    merged_communications = []
    for iteration in iterations:
        iter_num = iteration.get('iteration')
        # Convert task_assignments dict to a string using JSON formatting
        task_assignments = iteration.get('task_assignments', {})
        assignment_str = json.dumps(task_assignments, ensure_ascii=False)
        merged_assignments.append(f"Iteration {iter_num}: {assignment_str}")

        # Merge communications list into one string (separated by a space)
        communications = iteration.get('communications', [])
        communications_str = " ".join(communications)
        merged_communications.append(f"Iteration {iter_num}: {communications_str}")

    # Join different iterations with a separator (e.g., " | ")
    merged_assignments_str = " | ".join(merged_assignments)
    merged_communications_str = " | ".join(merged_communications)
    return merged_assignments_str, merged_communications_str

def main():
    # Modify the file paths for your inputs and output here.

    # Folder containing YAML files.
    yaml_folder = "/Users/zhukunlun/Documents/GitHub/MARBLE/marble/configs/generated_yaml_files_graph_gpt_35_100"  # <-- Change this path

    # File paths for each model's JSONL outputs.
    # Model labels: A: GPT3.5, B: GPT4o-mini, C: Llama3.1-8b, D: Llama3.1-70b, E: Llama3.3-70b.
    gpt35_file = "/Users/zhukunlun/Documents/GitHub/MARBLE/marble/result_main/discussion_output_35_0202.jsonl"         # Model A
    gpt4omini_file = "/Users/zhukunlun/Documents/GitHub/MARBLE/marble/result_main/discussion_output_4o_mini.jsonl"   # Model B
    llama31_8b_file = "/Users/zhukunlun/Documents/GitHub/MARBLE/marble/result_main/discussion_output_llama3.1_8b.jsonl"   # Model C
    llama31_70b_file = "/Users/zhukunlun/Documents/GitHub/MARBLE/marble/result_main/discussion_output_llama3.1_70b.jsonl" # Model D
    llama33_70b_file = "/Users/zhukunlun/Documents/GitHub/MARBLE/marble/result_main/discussion_output_llama3.3_70b.jsonl" # Model E

    # Output CSV file path.
    output_csv = "./human_eval_research.csv"  # <-- Change this path

    # Load YAML files (first 10 only)
    yaml_data_list = load_yaml_files(yaml_folder)

    # Load JSONL data for each model and create a mapping from model label to its data.
    model_files = {
        'A': load_jsonl_file(gpt35_file),
        'B': load_jsonl_file(gpt4omini_file),
        'C': load_jsonl_file(llama31_8b_file),
        'D': load_jsonl_file(llama31_70b_file),
        'E': load_jsonl_file(llama33_70b_file)
    }

    # Prepare list to collect CSV rows.
    csv_rows = []
    task_id = 1

    # Process each YAML file (each representing one task).
    for yaml_data in yaml_data_list:
        # Extract the agents list and convert to a JSON-formatted string.
        agents = yaml_data.get('agents', [])
        agents_str = json.dumps(agents, ensure_ascii=False)

        # Extract the task content from the YAML (assuming it is under key 'task' -> 'content').
        task_field = yaml_data.get('task', {})
        task_content = task_field.get('content', '').strip()

        # For each model, find the corresponding JSON object by matching the task content.
        for model_label, model_data in model_files.items():
            # Look up the JSON object for the current task (exact string match).
            json_obj = model_data.get(task_content)
            if not json_obj:
                print(f"Task not found in model {model_label} JSONL file for task starting with: {task_content[:30]}...")
                merged_assignments_str = ""
                merged_communications_str = ""
            else:
                iterations = json_obj.get('iterations', [])
                merged_assignments_str, merged_communications_str = merge_iterations(iterations)

            # Append a CSV row with the required columns:
            # task_id, agent_profiles, model (model letter), merged task assignments, merged communications.
            csv_rows.append({
                'task_id': task_id,
                'task_content': json_obj.get('task', ''),
                'agent_profiles': agents_str,
                'model': model_label,
                'merged_task_assignments': merged_assignments_str,
                'merged_communications': merged_communications_str,
                'summary': json_obj.get('iterations', [])[-1].get('summary', ''),
                'communication_score': -1,
                'planning_score': -1,
                'task_score': -1,
            })
        # Increase task_id for the next YAML file.
        task_id += 1

    # Write the collected data to a CSV file.
    fieldnames = ['task_id', 'task_content','agent_profiles', 'model', 'merged_task_assignments', 'merged_communications', 'summary', 'communication_score', 'planning_score', 'task_score']
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in csv_rows:
            writer.writerow(row)
    print(f"CSV file generated at: {output_csv}")

if __name__ == "__main__":
    main()
