import os
import json
import time
from tqdm import tqdm
import litellm
from litellm.utils import trim_messages

# Initialize error counter
error_count = 0

# List all folders in the current directory
folder_list = [folder for folder in os.listdir() if os.path.isdir(folder)]

for folder in folder_list:
    print(f"Processing folder: {folder}")
    folder_files = os.listdir(folder)
    collaboration_scores = []
    task_scores = []

    for file_name in tqdm(folder_files):
        if not file_name.endswith(".json"):
            continue

        file_path = os.path.join(folder, file_name)

        # Load JSON data
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {file_name}")
            error_count += 1
            continue

        # Validate required fields
        if "planning_scores" not in data or "communication_scores" not in data:
            print(f"Missing planning or communication scores in file: {file_name}")
            error_count += 1
            continue

        if "task_evaluation" not in data or not data["task_evaluation"]:
            print(f"Missing or empty task_evaluation in file: {file_name}")
            error_count += 1
            continue

        # Calculate collaboration score
        planning_scores = data["planning_scores"]
        communication_scores = data["communication_scores"]
        try:
            planning_avg = sum(planning_scores) / len(planning_scores)
            communication_avg = sum(communication_scores) / len(communication_scores)
            collaboration_score = (planning_avg + communication_avg) / 2
            collaboration_scores.append(collaboration_score)
        except ZeroDivisionError:
            print(f"Error calculating collaboration scores in file: {file_name}")
            error_count += 1
            continue

        # Process task evaluation
        task_eval = data["task_evaluation"]
        gold_labels = task_eval.get("root_cause", [])

        if len(gold_labels) != 1:
            print(f"Invalid gold labels in file: {file_name}")
            error_count += 1
            continue

        gold_label = gold_labels[0]
        predicted = task_eval.get("predicted", "")

        # Create prompt for the LLM
        prompt = (
            f"{predicted}\n\n"
            f"From the text above, please identify the two predicted root causes of the issue.\n\n"
            f"Please print each of them in the form they appear in two separate lines."
            f"I have a very rudimentary system, so if it is not in the exact form, it will crash."
        )

        messages = [{"role": "user", "content": prompt}]

        # Call the LLM for completion
        try:
            completion = litellm.completion(
                model='gpt-4o-mini',
                messages=trim_messages(messages, model='gpt-4o-mini', max_tokens=int(16384 * 0.6)),
                max_tokens=512,
                temperature=0.0
            )

            response = completion.choices[0].message.content.strip()
            predicted_labels = [label.strip() for label in response.split("\n")]
        except Exception as e:
            print(f"Error during LLM call: {e}")
            error_count += 1
            continue

        # Compare predictions with the gold label
        task_scores.append(1 if gold_label in predicted_labels else 0)

        # Add a delay to avoid API rate limits
        time.sleep(0.5)

    # Calculate averages
    if collaboration_scores:
        avg_collaboration_score = sum(collaboration_scores) / len(collaboration_scores)
        print(f"Average collaboration score for {folder}: {avg_collaboration_score:.6f}")
    else:
        print(f"No collaboration scores for {folder}.")

    if task_scores:
        avg_task_score = sum(task_scores) / len(task_scores)
        print(f"Scaled task score for {folder}: {avg_task_score * 5:6f}")
    else:
        print(f"No task scores for {folder}.")

    print(f"Errors so far: {error_count}\n")

print(f"Total errors: {error_count}")