import os
import re
import json
from collections import defaultdict

##########################
# 1) 模型 -> 机器评文件名映射（示例）
##########################
MODEL_FILE_MAP = {
    "llama31_70b": "test_output_llama31_70b.jsonl",
    "llama31_8b":  "test_output_llama31_8b.jsonl",
    "llama33":     "test_output_llama33.jsonl",
    "gpt-4o-mini": "test_output_4omini.jsonl",
    "gpt3.5-turbo":"test_output_gpt35.jsonl",
}

##########################
# 2) 加载机器评到 machine_data
##########################
# 结构: {model_name: { eval_key: (comm_score, plan_score), ...}}

def load_machine_eval(machine_eval_dir):
    """
    从 machine_eval_dir 下各模型对应的 JSONL 文件读取，
    按 (model_name, eval_key) 保存 communication_score, planning_score
    """
    machine_data = defaultdict(dict)

    for model_name, filename in MODEL_FILE_MAP.items():
        file_path = os.path.join(machine_eval_dir, filename)
        if not os.path.isfile(file_path):
            print(f"[WARNING] 机器评文件不存在: {file_path}, 跳过.")
            continue

        with open(file_path, "r", encoding="utf-8") as fin:
            for line in fin:
                line=line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except:
                    continue

                archive_dir = obj.get("archive_dir", "")
                comm = obj.get("communication_score", -1)
                plan = obj.get("planning_score", -1)

                # 正则匹配 eval_20250126_143016 或 eval_YYYYmmdd_HHMMSS
                eval_key = None
                match = re.search(r"eval_\d{8}_\d{6}", archive_dir)
                if match:
                    eval_key = match.group(0)
                else:
                    # 再试一个较宽松的 pattern
                    match2 = re.search(r"eval_\d{8}_\d+", archive_dir)
                    if match2:
                        eval_key = match2.group(0)

                if eval_key:
                    machine_data[model_name][eval_key] = (comm, plan)

    return machine_data


##########################
# 3) 辅助函数：从人评 folder_path 提取模型名/eval_key
##########################

def parse_model_from_path(folder_path: str) -> str:
    """
    根据 folder_path 决定模型名, 
    例如包含 '\\llama31_70b\\' 就返回 'llama31_70b'; 
    或者 '\\4o\\' 就是 '4o', 依需求可改
    """
    if "\\4o\\" in folder_path:
        return "4o"
    elif "\\llama31_70b\\" in folder_path:
        return "llama31_70b"
    elif "\\llama31_8b\\" in folder_path:
        return "llama31_8b"
    elif "\\llama33\\" in folder_path:
        return "llama33"
    elif "\\4omini\\" in folder_path:
        return "gpt-4o-mini"
    elif "\\gpt35\\" in folder_path:
        return "gpt3.5-turbo"
    return ""

def parse_eval_key(folder_path: str) -> str:
    """
    匹配 folder_path 中的 eval_xxxx 标识符
    """
    match = re.search(r"eval_\d{8}_\d{6}", folder_path)
    if match:
        return match.group(0)
    match2 = re.search(r"eval_\d{8}_\d+", folder_path)
    if match2:
        return match2.group(0)
    return ""


##########################
# 4) 主处理函数：对齐 & 合并 & 输出
##########################

def process_human_eval_and_merge(
    human_eval_path: str,
    machine_eval_dir: str,
    output_jsonl_path: str
):
    """
    1) 加载机器评 => machine_data
    2) 遍历人评 JSONL:
        - 跳过模型=4o
        - 判断是否三项以上 -1/两个comm=-1/两个plan=-1 => 跳过
        - 否则取非-1 comm/planning平均 => final_human_comm/plan
        - 从folder_path提取eval_key & model
        - 到 machine_data中找对应机器评 comm/plan => merged输出
    3) 统计并打印每个模型的人评(communication,planning) & 机器评(communication,planning)平均
    """

    # 先加载机器评 => machine_data[(model_name)][eval_key] = (comm, plan)
    machine_data = load_machine_eval(machine_eval_dir)

    # 用于统计
    stats = defaultdict(list)

    with open(human_eval_path, "r", encoding="utf-8") as fin, \
         open(output_jsonl_path, "w", encoding="utf-8") as fout:

        for line in fin:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except:
                continue

            folder_path = obj.get("folder_path", "")
            # 取四个槽:
            c1 = obj.get("communication_score_1", -1)
            p1 = obj.get("planning_score_1", -1)
            c2 = obj.get("communication_score_2", -1)
            p2 = obj.get("planning_score_2", -1)

            # step1: parse 模型
            model_name = parse_model_from_path(folder_path)
            if model_name == "4o":
                # 跳过
                continue

            # 判断是否三项以上= -1 或 comm都-1 或 plan都-1
            scores = [c1, p1, c2, p2]
            negative_count = sum(1 for s in scores if s == -1)

            if negative_count >= 3:
                continue
            if (c1 == -1 and c2 == -1):
                continue
            if (p1 == -1 and p2 == -1):
                continue

            # 算人评平均
            valid_comm = []
            if c1 != -1: valid_comm.append(c1)
            if c2 != -1: valid_comm.append(c2)
            final_human_comm = sum(valid_comm)/len(valid_comm) if valid_comm else -1

            valid_plan = []
            if p1 != -1: valid_plan.append(p1)
            if p2 != -1: valid_plan.append(p2)
            final_human_plan = sum(valid_plan)/len(valid_plan) if valid_plan else -1

            # 获取eval_key
            eval_key = parse_eval_key(folder_path)
            if not eval_key:
                # 找不到唯一标识 => skip
                continue

            # 去 machine_data 找
            if model_name not in machine_data:
                # 无此模型的机评
                continue

            model_dict = machine_data[model_name]
            if eval_key not in model_dict:
                # 无此 archive
                continue

            llm_comm, llm_plan = model_dict[eval_key]

            # 组装
            merged = {
                "folder_path": folder_path,
                "final_human_comm": final_human_comm,
                "final_human_plan": final_human_plan,
                "llm_communication_score": llm_comm,
                "llm_planning_score": llm_plan,
                "model": model_name,
                "eval_key": eval_key
            }
            # 写出
            fout.write(json.dumps(merged, ensure_ascii=False) + "\n")

            stats[model_name].append((final_human_comm, final_human_plan, llm_comm, llm_plan))

    # 最后统计
    print("=== 模型统计 ===")
    for m, arr in stats.items():
        if not arr:
            continue
        hum_comm_list = [x[0] for x in arr]
        hum_plan_list = [x[1] for x in arr]
        llm_comm_list = [x[2] for x in arr]
        llm_plan_list = [x[3] for x in arr]

        avg_hum_comm = sum(hum_comm_list)/len(hum_comm_list)
        avg_hum_plan = sum(hum_plan_list)/len(hum_plan_list)
        avg_llm_comm = sum(llm_comm_list)/len(llm_comm_list)
        avg_llm_plan = sum(llm_plan_list)/len(llm_plan_list)

        print(f"模型: {m}")
        print(f"  人评 comm 平均: {avg_hum_comm:.2f}, plan 平均: {avg_hum_plan:.2f}")
        print(f"  机评 comm 平均: {avg_llm_comm:.2f}, plan 平均: {avg_llm_plan:.2f}")
        print("-"*60)


######################
# 主函数
######################
def main():
    # 你可以自己写 argparse 或手动
    # 例如:
    human_eval_path = "human_eval\werewolf_human_output.jsonl"  # 你的输入人评文件
    machine_eval_dir = "llm_eval_result\werewolf\output"     # 机器评文件夹
    output_jsonl_path = "human_eval\werewolf_merged_output.jsonl"

    process_human_eval_and_merge(human_eval_path, machine_eval_dir, output_jsonl_path)


if __name__ == "__main__":
    main()
