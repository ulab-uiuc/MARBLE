#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI
from tqdm import tqdm

###############################################################################
# 全局常量 -- 你可自行填写或留空
###############################################################################
GLOBAL_TASK = '''
  Welcome to the Werewolf Game! In this game, players take on various roles, each with specific abilities.
  The game alternates between day and night phases. During the night, special roles perform their actions.
  During the day, players discuss and vote to eliminate suspects. The goal is for the villagers to eliminate
  all the werewolves, while the werewolves aim to outnumber the villagers. Be careful who you trust!'''
GLOBAL_AGENT_PROFILES = '''werewolf_introduction: |
  You are a Werewolf. Your goal is to eliminate the villagers without being caught. Each night, you and your fellow
  werewolves secretly choose one villager to eliminate. You must work together to deceive the other players during the
  day, while subtly protecting your fellow werewolves.
  To better hide your identity, you may choose to pretend to be other roles to gain credibility. Since werewolves know each other's identities, pretending to be the Seer is a good way to gain villagers' trust.
  If you manage to outnumber the villagers, you win the game.

villager_introduction: |
  You are a Villager. Your goal is to identify and eliminate the werewolves. During the day, you participate in discussions
  and voting to root out the werewolves. You have no special powers at night, but your ability to observe and reason
  is crucial to the village's survival. Work with other villagers and be careful whom you trust!
  Although you have no special skills, sometimes pretending to be another role can change the course of the game. For example, shielding a key player from harm could be your moment of glory.

witch_introduction: |
  You are the Witch. Each night, you will be told who has been attacked, and you must decide whether to use your antidote
  to save them or use your poison to eliminate another player. You only have one poison and one antidote, so use them wisely.
  During the daytime discussions, if the night ends without a death, you can reveal that you used your antidote to save someone, which may earn others' trust.
  Typically, you should use the antidote to save key players like the Seer, the Guard, or yourself, while the poison is best used to eliminate werewolves at night.
  However, be cautious: sometimes the werewolves will deliberately attack one of their own (self-knife strategy) to trick you into wasting the antidote, thereby boosting their credibility.

seer_introduction: |
  You are the Seer. Each night, you can check the identity of one player to see whether they are a werewolf or not.
  Your knowledge is critical for the villagers' victory, so share it carefully. The werewolves will likely target you
  or pretend to be you to mislead others.
  As the core of the good faction, the Seer is often the top target for werewolves to impersonate or kill. During the night, you should inspect players whose identities are uncertain (there is no need to check players who are highly suspected of being werewolves).
  When speaking during the day, your goal is to convince others that you are the real Seer. You must gather trust and
  share your findings without exposing yourself too early. Even though revealing your identity might put you in danger,
  a Seer trusted by both the Witch and the Guard can survive for at least three rounds if everyone acts accordingly.
  A good Seer will coordinate with the Witch and the Guard to divide responsibilities. For example, on the first night, the Guard protects the Seer, and the Witch doesn't use the antidote. On the second night, the Witch saves the Seer, and the Guard protects someone else.

guard_introduction: |
  You are the Guard. Each night, you can choose one player to protect from being killed by the werewolves. You cannot protect
  the same player two nights in a row. Your role is critical in keeping important players like the Seer or the Witch alive.
  You are in a constant mental battle with the werewolves, trying to predict who they will target. It might not always be the Seer, as the werewolves might expect you to protect them and kill someone else. In general, you should avoid revealing your identity unless absolutely necessary.
'''
GLOBAL_RESULT = "Please refer to the provided event log. All eliminations are mentioned in the log."

###############################################################################
# 从返回文本中提取 ```json { ... } ``` 结构并转换为 dict
###############################################################################
def json_parse(input_str: str) -> dict:
    pattern = r"```json\s*(\{.*?\})\s*```"
    match = re.search(pattern, input_str, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
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

###############################################################################
# OpenAI 客户端
###############################################################################

def call_openai(prompt, model="gpt-4o", max_retries=5, delay=1):
    """
    Call OpenAI's ChatCompletion API with retry logic.
    """
    for attempt in range(max_retries):
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model,
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            json_parse(chat_completion.choices[0].message.content)
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"[Error] calling OpenAI API: {e}. Retry {attempt+1}/{max_retries}")
            time.sleep(delay)
    return None

###############################################################################
# 可选：截断文本以防过长
###############################################################################
def truncate_text(text, max_length=500):
    """
    如果文本超过max_length，就截断并在末尾加"..."；否则原样返回。
    """
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text

###############################################################################
# 构造沟通(communication)评价 Prompt
# 注意，这里不使用 input JSON 中的 task/agent_profiles/relationship，
# 而是使用全局常量 + private_event_log
###############################################################################
def build_communication_prompt(item):
    global GLOBAL_TASK, GLOBAL_AGENT_PROFILES, GLOBAL_RESULT

    # 从 JSON 输入中取：private_event_log(字符串)
    private_event_log = item.get("private_event_log", "No data provided.")

    # 保留原本大段沟通提示
    prompt = f"""Task: {GLOBAL_TASK}
Agent Profiles: {GLOBAL_AGENT_PROFILES}
Global Result: {GLOBAL_RESULT}

Aggregated Communication + Task Results (from private_event_log):
{private_event_log}

[System] You are tasked with evaluating the quality of communication among agents operating within a decentralized Graph structure. Evaluate whether agents made effective decisions based on the provided task results and whether their communication aligns with their agent profiles and social relationships. Consider the following:
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
    return prompt


###############################################################################
# 构造规划(planning)评价 Prompt
# 把 item 中的 private_event_log, witch_thought, seer_thought 全都拼进去
###############################################################################
def build_planning_prompt(item):
    global GLOBAL_TASK, GLOBAL_AGENT_PROFILES, GLOBAL_RESULT

    private_event_log = item.get("private_event_log", "")
    # 新需求：把 witch_thought / seer_thought 也加进“规划”评价
    # 如果没有则默认为空字符串
    witch_thought = truncate_text(item.get("witch_thought", ""), 5000)
    seer_thought = truncate_text(item.get("seer_thought", ""), 5000)

    # 保留原先大段“规划”提示文本
    # 并在中间插入 Witch/Seer 的想法
    prompt = f"""Agent Profiles: {GLOBAL_AGENT_PROFILES}
Global Result: {GLOBAL_RESULT}

Aggregated Planning Data:
{private_event_log}

Additional Thoughts from special roles:
Witch Thought:
{witch_thought}

Seer Thought:
{seer_thought}

[System] You are tasked with evaluating the effectiveness of the planning process in a decentralized Graph structure. Evaluate whether the planning across all iterations demonstrates clear role definitions, effective task assignments, and a rational workload distribution that aligns with each agent's profile. Consider the following:
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
    return prompt

###############################################################################
# 对单条数据进行处理：生成沟通/规划提示，调用API，解析，写回
###############################################################################
def process_item(item):
    # 确保至少有 private_event_log
    if "private_event_log" not in item:
        print("[Skip] No private_event_log found.")
        return item

    # 1) Communication
    comm_prompt = build_communication_prompt(item)
    comm_response = call_openai(comm_prompt, model=MODEL)
    try:
        parsed_comm = json_parse(comm_response)
        comm_score = parsed_comm.get("score")
        comm_reasoning = parsed_comm.get("reasoning")
    except Exception as e:
        print(f"[Error] parse communication response: {e}")
        comm_score = None
        comm_reasoning = None

    # 2) Planning
    plan_prompt = build_planning_prompt(item)
    plan_response = call_openai(plan_prompt, model=MODEL)
    try:
        parsed_plan = json_parse(plan_response)
        plan_score = parsed_plan.get("score")
        plan_reasoning = parsed_plan.get("reasoning")
    except Exception as e:
        print(f"[Error] parse planning response: {e}")
        plan_score = None
        plan_reasoning = None

    # 写回
    item["communication_score"] = comm_score
    item["communication_reasoning"] = comm_reasoning
    item["planning_score"] = plan_score
    item["planning_reasoning"] = plan_reasoning
    item["communication_response"] = comm_response
    item["planning_response"] = plan_response

    return item

###############################################################################
# 去重： 用 archive_dir 做唯一标识
###############################################################################
def load_processed_archive_dirs(output_file):
    processed = set()
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    arch = data.get("archive_dir")
                    if arch:
                        processed.add(arch)
                except:
                    pass
    return processed

###############################################################################
# 主函数
###############################################################################
def main(model, openai_key, input, output, parallel):
    global MODEL, client
    MODEL = model
    client = OpenAI(api_key=openai_key)

    with open(input, "r", encoding="utf-8") as infile:
        items = [json.loads(line) for line in infile if line.strip()]

    processed_archives = load_processed_archive_dirs(output)
    to_process = []
    for item in items:
        arch_dir = item.get("archive_dir")
        if arch_dir not in processed_archives:
            to_process.append(item)

    total = len(to_process)
    if total == 0:
        print("No new items to process.")
        sys.exit(0)

    with open(output, "a", encoding="utf-8") as outfile:
        with ThreadPoolExecutor(max_workers=parallel) as executor:
            futures = {executor.submit(process_item, it): it for it in to_process}
            for future in tqdm(as_completed(futures), total=total, desc="Processing items"):
                result = future.result()
                outfile.write(json.dumps(result, ensure_ascii=False) + "\n")
                outfile.flush()

if __name__ == "__main__":
    print("=== This is the updated script, no argparse left! ===")
    # 直接在这里写死
    OPENAI_KEY = "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"
    INPUT_FILE = "output_35.jsonl"
    OUTPUT_FILE = "test_output_35.jsonl"
    PARALLEL_COUNT = 1
    EVAL_MODEL = "gpt-4o"

    main(EVAL_MODEL, OPENAI_KEY, INPUT_FILE, OUTPUT_FILE, PARALLEL_COUNT)