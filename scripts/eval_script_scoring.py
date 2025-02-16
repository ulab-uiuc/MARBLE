#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI
from tqdm import tqdm

# Regular expression to extract rating in the format: "Rating: [[[rating]]]"
def json_parse(input_str: str) -> dict:
    """
    Extracts the JSON part from a string that contains a JSON block and parses it into a dictionary.
    
    Args:
        input_str (str): A string that includes a JSON block.
        
    Returns:
        dict: The parsed JSON data.
        
    Raises:
        ValueError: If JSON parsing fails due to invalid format.
    """
    pattern = r"```json\s*(\{.*?\})\s*```"
    match = re.search(pattern, input_str, re.DOTALL)
    
    if match:
        json_str = match.group(1)
    else:
        # Fallback: extract substring from the first '{' to the last '}'
        start = input_str.find('{')
        end = input_str.rfind('}')
        if start != -1 and end != -1 and end > start:
            json_str = input_str[start:end+1]
        else:
            json_str = input_str
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError("JSON parsing failed. Please check the input format.") from e
    return data

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def call_openai(prompt, model="gpt-4o", max_retries=3, delay=5):
    """
    Call OpenAI's ChatCompletion API with the provided prompt and return the response text.
    Implements a simple retry mechanism.
    """
    for attempt in range(max_retries):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=model,
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI API: {e}. Retry {attempt+1}/{max_retries}")
            time.sleep(delay)
    return None

def truncate_text(text, max_length=3000):
    """
    Truncate the text to max_length characters, appending "..." if truncated.
    """
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text

def aggregate_communications(iterations):
    """
    Aggregate communications and task_results from all iterations.
    For each iteration, include the iteration id and concatenate communications and task_results.
    """
    comm_parts = []
    task_result_parts = []
    for idx, iteration in enumerate(iterations, start=1):
        iteration_id = iteration.get("iteration", f"Iteration {idx}")
        # Process communications
        comms = iteration.get("communications", [])
        if comms:
            comm_text = "\n".join(comms)
        else:
            comm_text = "None"
        comm_parts.append(f"Iteration {iteration_id} Communications:\n{comm_text}")
        
        # Process task_results
        results = iteration.get("task_results", [])
        result_texts = []
        for result in results:
            agent_id = result.get("agent_id", "Unknown Agent")
            res = result.get("result", "")
            res_truncated = truncate_text(res)
            result_texts.append(f"Agent {agent_id}: {res_truncated}")
        if result_texts:
            results_combined = "\n".join(result_texts)
        else:
            results_combined = "None"
        task_result_parts.append(f"Iteration {iteration_id} Task Results:\n{results_combined}")
    
    communications_all = "\n\n".join(comm_parts)
    task_results_all = "\n\n".join(task_result_parts)
    return communications_all, task_results_all

def aggregate_planning(iterations):
    """
    Aggregate planning-related data from all iterations.
    For each iteration, include summary, task assignments, and task results.
    """
    planning_parts = []
    for idx, iteration in enumerate(iterations, start=1):
        iteration_id = iteration.get("iteration", f"Iteration {idx}")
        summary = iteration.get("summary", "None")
        task_assignments = iteration.get("task_assignments", {})
        task_assignments_str = json.dumps(task_assignments, ensure_ascii=False, indent=2) if task_assignments else "None"
        results = iteration.get("task_results", [])
        result_texts = []
        for result in results:
            agent_id = result.get("agent_id", "Unknown Agent")
            res = result.get("result", "")
            res_truncated = truncate_text(res)
            result_texts.append(f"Agent {agent_id}: {res_truncated}")
        if result_texts:
            results_combined = "\n".join(result_texts)
        else:
            results_combined = "None"
        planning_parts.append(
            f"Iteration {iteration_id}:\nSummary: {summary}\nTask Assignments: {task_assignments_str}\nTask Results: {results_combined}"
        )
    planning_all = "\n\n".join(planning_parts)
    return planning_all

def build_communication_prompt(item, iterations):
    """
    Build the prompt for the communication evaluation based on the input item and its iterations.
    Aggregates communications and task_results from all iterations.
    """
    task = item.get("task", "")
    agent_profiles = item.get("agent_profiles", "")
    relationship = item.get("relationship", "")
    
    communications_all, task_results_all = aggregate_communications(iterations)
    
    prompt = f"""Task: {truncate_text(task)}
Agent Profiles: {truncate_text(agent_profiles)}
Social Relationship: {truncate_text(relationship)}

Aggregated Task Results:
{truncate_text(task_results_all)}

Aggregated Communication Data:
{truncate_text(communications_all, 6000)}

[System] You are tasked with evaluating the quality of communication among agents operating within a multiagent system. Evaluate whether agents made effective decisions based on the provided task results and whether their communication aligns with their agent profiles and social relationships. Consider the following:
1. Effective Decision-Making: Did agents use task results to guide their decisions effectively?
2. Clarity and Precision: Were communications clear and unambiguous?
3. Adherence to Social Relationships: Did communications reflect the expected interactions based on the agents' social relationships?
4. Alignment with Agent Profiles: Were the messages consistent with the defined agent profiles?
5. Overall Effectiveness: Did the communication facilitate task progress, considering both cooperative and competitive aspects?

Scoring Criteria (Communication):
- 5 (Exceptional): Outstanding communication with clear, precise messages fully aligned with agent profiles and social relationships.
  Example: Every agent provided concise, accurate, and strategic information that directly advanced the task.
- 4 (Very Good): Mostly effective communication with only minor lapses and slight ambiguities.
  Example: Occasional minor unclear messages, but overall effective.
- 3 (Adequate): Acceptable communication with moderate ambiguities or inconsistencies.
  Example: Some messages were vague and did not fully meet required standards.
- 2 (Poor): Frequent unclear or misaligned communications causing significant miscommunication.
  Example: Repeated incoherence negatively impacted task progress.
- 1 (Very Poor): Largely ineffective communication with confusing messages and complete misalignment.
  Example: Chaotic communication with severely flawed decisions.

Please provide your answer in a JSON code block in the following format:
```json
{{
  "score": 5
}}```
"""
    #print(prompt)
    return prompt

def build_planning_prompt(item, iterations):
    """
    Build the prompt for the planning evaluation based on the input item and its iterations.
    Aggregates planning data from all iterations.
    """
    agent_profiles = item.get("agent_profiles", "")
    
    planning_all = aggregate_planning(iterations)
    
    prompt = f"""Agent Profiles: {truncate_text(agent_profiles)}

Aggregated Planning Data from All Iterations:
{truncate_text(planning_all, 6000)}

[System] You are tasked with evaluating the effectiveness of the planning process in a multiagent system. Evaluate whether the planning across all iterations demonstrates clear role definitions, effective task assignments, and a rational workload distribution that aligns with each agent's profile. Consider the following:
1. Clarity of Task Assignment: Were tasks assigned in a clear and unambiguous manner?
2. Definition of Roles: Were roles and responsibilities clearly defined in each iteration?
3. Workload Distribution: Was the distribution of tasks reasonable and aligned with each agent's profile?
4. Effectiveness of Outcomes: Did the planning lead to successful progress in task advancement across iterations?
5. Overall Strategic Coordination: Did the planning incorporate effective cooperation and competition strategies?

Scoring Criteria (Planning):
- 5 (Exceptional Planning): Planning is exemplary; every iteration shows clear, well-structured task assignments with roles perfectly defined and workloads optimally distributed, consistently advancing the objectives.
  Example: All plans were strategic, with perfect alignment to agent profiles and minimal ambiguity.
- 4 (Very Good Planning): Planning is mostly effective with only minor ambiguities; roles are clear and task assignments are appropriate, though there were slight inefficiencies.
  Example: Only occasional parts were a bit vague, but overall the planning was reasonable.
- 3 (Adequate Planning): Planning is acceptable but shows moderate ambiguities or inefficiencies. In some iterations, role definitions or task assignments were not entirely clear or well-matched to agent capabilities.
  Example: Some plans were vague or did not fully match the agents' capabilities.
- 2 (Poor Planning): There were frequent ambiguities in task assignments and role definitions; planning was inconsistent and did not align well with agent profiles, resulting in noticeable inefficiencies.
  Example: Multiple instances of unclear roles and unreasonable task distributions were observed.
- 1 (Very Poor Planning): Planning was severely flawed; task assignments were unclear, roles were undefined, and workload distributions were unreasonable, hindering progress.
  Example: The planning was chaotic, lacking clear strategy and alignment with agent profiles.

Please provide your answer in a JSON code block in the following format:
```json
{{
  "score": 5
}}```
"""
    #print(prompt)
    return prompt

def process_item(item):
    """
    Process a single item: build prompts, call the API for both evaluations, parse the results,
    """
    iterations = item.get("iterations", [])
    if not iterations:
        print("No iterations found for this item. Skipping.")
        print(item)
        return item

    # Communication evaluation
    comm_prompt = build_communication_prompt(item, iterations)
    comm_response = call_openai(comm_prompt, model=MODEL)
    try:
        parsed_comm = json_parse(comm_response)
        comm_score = parsed_comm.get("score")
    except Exception as e:
        print(f"Error parsing communication response: {e}")
        comm_score = None

    # Planning evaluation
    planning_prompt = build_planning_prompt(item, iterations)
    planning_response = call_openai(planning_prompt, model=MODEL)
    try:
        parsed_planning = json_parse(planning_response)
        planning_score = parsed_planning.get("score")
    except Exception as e:
        print(f"Error parsing planning response: {e}")
        planning_score = None

    item["communication_score"] = comm_score
    item["planning_score"] = planning_score
    item["communication_response"] = comm_response
    item["planning_response"] = planning_response

    return item

def load_processed_yaml_files(output_file):
    """
    Load the output file (if exists) and return a set of yaml_file values that have been processed.
    """
    processed = set()
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    yaml_id = data.get("yaml_file")
                    if yaml_id:
                        processed.add(yaml_id)
                except json.JSONDecodeError:
                    continue
    return processed

def main(model, openai_key, input, output, parallel):
    global MODEL, client
    MODEL = model
    client = OpenAI(api_key=openai_key)

    with open(input, "r", encoding="utf-8") as infile:
        items = [json.loads(line) for line in infile if line.strip()]

    processed_yaml = load_processed_yaml_files(output)
    to_process = []
    for item in items:
        yaml_id = item.get("yaml_file")
        if yaml_id not in processed_yaml:
            to_process.append(item)

    total = len(to_process)
    if total == 0:
        print("No new items to process.")
        sys.exit(0)

    with open(output, "a", encoding="utf-8") as outfile:
        with ThreadPoolExecutor(max_workers=parallel) as executor:
            futures = {executor.submit(process_item, item): item for item in to_process}
            for future in tqdm(as_completed(futures), total=total, desc="Processing items"):
                result = future.result()
                outfile.write(json.dumps(result, ensure_ascii=False) + "\n")
                outfile.flush()

if __name__ == "__main__":
    OPENAI_KEY="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"
    INPUT_FILE="llm_eval_result\\ablation\input\discussion_output_gpt-4o-mini_20.jsonl"
    OUTPUT_FILE="llm_eval_result\\ablation\output\discussion_output_gpt-4o-mini_20.jsonl"
    PARALLEL_COUNT=8
    EVAL_MODEL="gpt-4o"
    main(EVAL_MODEL, OPENAI_KEY, INPUT_FILE, OUTPUT_FILE, PARALLEL_COUNT)