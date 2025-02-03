import json
import os

import yaml

# 定义输入 JSON 文件所在目录和输出 YAML 文件目录
json_files_dir = "./researchtown_json"  # 存放三个 JSON 文件的文件夹
output_dir = "./generated_yaml_files_graph_gpt_35"

# 如果输出目录不存在则创建之
os.makedirs(output_dir, exist_ok=True)

# 获取目录下所有 .json 文件
json_filenames = [f for f in os.listdir(json_files_dir) if f.endswith('.json')]

# 遍历每个 JSON 文件
paper_num = 1
for json_filename in json_filenames:
    json_path = os.path.join(json_files_dir, json_filename)
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 每个 JSON 文件内容格式为 { arxiv_id: { ... } }
    for paper_id, paper_info in data.items():
        # 获取 paper_data 与 author_data
        paper_data = paper_info.get("paper_data", {})
        author_data = paper_info.get("author_data", {})
        introduction = paper_data.get("introduction", "No introduction provided.")
        paper_authors = paper_data.get("authors", [])

        # 如果作者数量超过5个则取前5个
        limited_authors = paper_authors[:5]

        # 构造 agents 列表，根据 limited_authors 顺序，匹配 author_data 中对应的 bio
        agents = []
        for idx, author_name in enumerate(limited_authors):
            profile = ""
            # 遍历 author_data，按 name 字段匹配
            for auth_info in author_data.values():
                if auth_info.get("name") == author_name:
                    profile = auth_info.get("bio", "")
                    break
            agents.append({
                "type": "BaseAgent",
                "agent_id": f"agent{idx + 1}",
                "profile": profile
            })

        # 构造 fully connected relationships
        relationships = []
        for j in range(len(agents)):
            for k in range(j + 1, len(agents)):
                relationships.append([f"agent{j + 1}", f"agent{k + 1}", "collaborate with"])

        # 构造任务内容，使用 paper_data 中的 introduction
        task_content = f"""
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
            """
        yaml_data = {
            "coordinate_mode": "graph",
            "relationships": relationships,
            "llm": "gpt-3.5-turbo",
            "environment": {
                "type": "Research",
                "name": "Research Collaboration Environment",
                "max_iterations": 5  # 修改为 5
            },
            "task": {
                "content": task_content,
                "output_format": """You should answer the task in the following format:
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
                "file_path": "result/discussion_output_35.jsonl"
            }
        }

        # 构造输出 YAML 文件名，文件名中加入 paper_id 以便区分
        output_filename = f"profile_{paper_num}.yaml"
        paper_num += 1
        output_path = os.path.join(output_dir, output_filename)
        with open(output_path, "w", encoding="utf-8") as yaml_file:
            yaml.dump(yaml_data, yaml_file, allow_unicode=True)

        print(f"Generated YAML file for paper {paper_id}: {output_filename}")
