import os
import json
import sys
import csv
from statistics import mean

def process_jsonl_file(file_path):
    planning_scores = []
    communication_scores = []
    kpi_scores = []
    total_milestones_list = []
    innovation_scores = []
    safety_scores = []
    feasibility_scores = []
    task_scores = []
    token_usage = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue  # Skip invalid JSON lines

            # Process token_usage
            if 'token_usage' in data and isinstance(data['token_usage'], int):
                token_usage.append(data['token_usage'])

            # Process planning_scores
            if 'planning_scores' in data and isinstance(data['planning_scores'], list) and data['planning_scores']:
                avg_planning = mean(data['planning_scores'])
                planning_scores.append(avg_planning)

            # Process communication_scores
            if 'communication_scores' in data and isinstance(data['communication_scores'], list):
                filtered_comm = [score for score in data['communication_scores'] if score != -1]
                if filtered_comm:
                    avg_comm = mean(filtered_comm)
                    communication_scores.append(avg_comm)

            # Process agent_kpis and total_milestones
            if 'agent_kpis' in data and isinstance(data['agent_kpis'], dict) and 'total_milestones' in data:
                total_milestones = data['total_milestones']
                if isinstance(total_milestones, (int, float)) and total_milestones != 0:
                    kpi_sum = sum(
                        value / total_milestones
                        for value in data['agent_kpis'].values()
                        if isinstance(value, (int, float))
                    )
                    kpi_scores.append(kpi_sum / len(data['agent_kpis']))
                    total_milestones_list.append(total_milestones)

            # Process task_evaluation
            if 'task_evaluation' in data and isinstance(data['task_evaluation'], dict):
                task_eval = data['task_evaluation']
                innovation = task_eval.get('innovation')
                safety = task_eval.get('safety')
                feasibility = task_eval.get('feasibility')

                current_task_scores = []
                if isinstance(innovation, (int, float)):
                    innovation_scores.append(innovation)
                    current_task_scores.append(innovation)
                if isinstance(safety, (int, float)):
                    safety_scores.append(safety)
                    current_task_scores.append(safety)
                if isinstance(feasibility, (int, float)):
                    feasibility_scores.append(feasibility)
                    current_task_scores.append(feasibility)
                if current_task_scores:
                    task_score = mean(current_task_scores)
                    task_scores.append(task_score)

    # Calculate all average values
    result = {}
    result['average_planning_score'] = mean(planning_scores) if planning_scores else None
    result['average_communication_score'] = mean(communication_scores) if communication_scores else None
    result['average_kpi_score'] = mean(kpi_scores) if kpi_scores else None
    result['average_total_milestones'] = mean(total_milestones_list) if total_milestones_list else None
    result['average_innovation'] = mean(innovation_scores) if innovation_scores else None
    result['average_safety'] = mean(safety_scores) if safety_scores else None
    result['average_feasibility'] = mean(feasibility_scores) if feasibility_scores else None
    result['average_task_score'] = mean(task_scores) if task_scores else None
    result['average_token_usage'] = mean(token_usage) if token_usage else None

    return result

def main(folder_path, output_csv='output.csv'):
    # Check if the folder exists
    if not os.path.isdir(folder_path):
        print(f"Folder path '{folder_path}' does not exist.")
        return

    # Get all jsonl files
    jsonl_files = [f for f in os.listdir(folder_path) if f.endswith('.jsonl')]

    if not jsonl_files:
        print(f"No jsonl files found in the folder '{folder_path}'.")
        return

    # Prepare CSV headers
    headers = [
        'filename',
        'average_planning_score',
        'average_communication_score',
        'average_kpi_score',
        'average_total_milestones',
        'average_innovation',
        'average_safety',
        'average_feasibility',
        'average_task_score',
        'average_token_usage'
    ]

    # Write to CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()

        for file in jsonl_files:
            file_path = os.path.join(folder_path, file)
            metrics = process_jsonl_file(file_path)
            row = {'filename': file}
            row.update(metrics)
            writer.writerow(row)

    print(f"Processing complete. Results have been saved to '{output_csv}'.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the folder path as an argument. For example:")
        print("python script.py /path/to/folder")
    else:
        folder_path = sys.argv[1]
        main(folder_path)