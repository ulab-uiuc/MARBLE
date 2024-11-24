import json
import os

import yaml

# Define input directories and output directory
profile_dbs_dir = "./profile_dbs"
intro_logging_path = "intro_logging.jsonl"
output_dir = "generated_yaml_files"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Load introductions from intro_logging.jsonl
with open(intro_logging_path, "r") as intro_file:
    print("Loading introductions from intro_logging.jsonl...")
    introductions = []
    #introductions = [json.loads(line)["referenced_intros"][0] for line in intro_file]
    for line in intro_file:
        intro_data = json.loads(line)
        try:
            introductions.append(intro_data["referenced_intros"][0])
        except IndexError:
            print(f"Error: No introductions found in line: {line}")
            continue

# Iterate over each profile directory
for i in range(1, 101):
    profile_dir = os.path.join(profile_dbs_dir, f"profile_{i}")
    profile_db_path = os.path.join(profile_dir, "ProfileDB.json")

    # Load profile data from ProfileDB.json
    with open(profile_db_path, "r") as profile_file:
        profiles = json.load(profile_file)

    # Prepare agents and relationships
    agents = []
    relationships = []
    agent_ids = list(profiles.keys())

    for idx, (agent_id, profile_data) in enumerate(profiles.items()):
        agent_name = f"agent{idx + 1}"
        agent_profile = profile_data["bio"]
        agents.append({
            "type": "BaseAgent",
            "agent_id": agent_name,
            "profile": agent_profile
        })

    # Create fully connected relationships
    for j in range(len(agent_ids)):
        for k in range(j + 1, len(agent_ids)):
            relationships.append([f"agent{j + 1}", f"agent{k + 1}", "collaborate with"])

    # Select an introduction for the task
    introduction = introductions[(i - 1) % len(introductions)]

    # Create YAML structure
    yaml_data = {
        "coordinate_mode": "graph",
        "relationships": relationships,
        "llm": "gpt-3.5-turbo",
        "environment": {
            "type": "Research",
            "name": "Research Collaboration Environment",
            "max_iterations": 3
        },
        "task": {
            "content": f"""
            Dear Research Team,

            You are collaborating to generate a new research idea based on the following Introduction:

            **Introduction**

            {introduction}

            **Your Task**

            1. **Literature Review**: Analyze the Introduction provided and conduct a brief literature review to understand the current state of research in this area.

            2. **Brainstorming**: Collaboratively brainstorm potential research ideas that build upon or address gaps in the Introduction.

            3. **Summarization**: Summarize your collective ideas.

            4. **Formulate a New Research Idea**: Develop a new research proposal in the format of the '5q', defined below:

               **Here is a high-level summarized insight of a research field Machine Learning.**

               **Here are the five core questions:**

               **[Question 1] - What is the problem?**

               Formulate the specific research question you aim to address. Only output one question and do not include any more information.

               **[Question 2] - Why is it interesting and important?**

               Explain the broader implications of solving this problem for the research community.
               Discuss how such a paper will affect future research.
               Discuss how addressing this question could advance knowledge or lead to practical applications.

               **[Question 3] - Why is it hard?**

               Discuss the challenges and complexities involved in solving this problem.
               Explain why naive or straightforward approaches may fail.
               Identify any technical, theoretical, or practical obstacles that need to be overcome. MAKE IT CLEAR.

               **[Question 4] - Why hasn't it been solved before?**

               Identify gaps or limitations in previous research or existing solutions.
               Discuss any barriers that have prevented this problem from being solved until now.
               Explain how your approach differs from or improves upon prior work. MAKE IT CLEAR.

               **[Question 5] - What are the key components of my approach and results?**

               Outline your proposed methodology in detail, including the method, dataset, and metrics that you plan to use.
               Describe the expected outcomes. MAKE IT CLEAR.

            Please work together to produce the '5q' for your proposed research idea.

            Good luck!
            """,
            "output_format": """You should answer the task in the fllowing format:
                **[Question 1] - What is the problem?**

                Formulate the specific research question you aim to address. Only output one question and do not include any more information.

                **[Question 2] - Why is it interesting and important?**

                Explain the broader implications of solving this problem for the research community.
                Discuss how such a paper will affect future research.
                Discuss how addressing this question could advance knowledge or lead to practical applications.

                **[Question 3] - Why is it hard?**

                Discuss the challenges and complexities involved in solving this problem.
                Explain why naive or straightforward approaches may fail.
                Identify any technical, theoretical, or practical obstacles that need to be overcome. MAKE IT CLEAR.

                **[Question 4] - Why hasn't it been solved before?**

                Identify gaps or limitations in previous research or existing solutions.
                Discuss any barriers that have prevented this problem from being solved until now.
                Explain how your approach differs from or improves upon prior work. MAKE IT CLEAR.

                **[Question 5] - What are the key components of my approach and results?**

                Outline your proposed methodology in detail, including the method, dataset, and metrics that you plan to use.
                Describe the expected outcomes. MAKE IT CLEAR."""
        },
        "agents": agents,
        "memory": {
            "type": "SharedMemory"
        },
        "metrics": {
            "evaluate_llm": "gpt-4o-mini",
            "engagement_level": True,
            "relevance": True,
            "diversity_of_perspectives": True
        },
        "engine_planner": {
            "initial_progress": "Starting the collaborative research idea generation based on the provided Introduction."
        },
        "output": {
            "format": "jsonl",
            "file_path": "result/discussion_output.jsonl"
        }
    }

    # Write YAML data to a file
    yaml_filename = os.path.join(output_dir, f"profile_{i}.yaml")
    with open(yaml_filename, "w") as yaml_file:
        yaml.dump(yaml_data, yaml_file)

print(f"Generated YAML files are saved in '{output_dir}' directory.")
