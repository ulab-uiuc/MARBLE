import os
import json
from collections import defaultdict

# 机器评文件映射：每个模型名 -> 对应文件名
MODEL_FILE_MAP = {
    "gpt3.5-turbo": "result_gpt-3.5-turbo.jsonl",
    "gpt-4o-mini":  "result_gpt-4o-mini.jsonl",
    "llama31-8b":   "result_llama-3.1-8b.jsonl",
    "llama31-70b":  "result_llama-3.1-70b.jsonl",
    "llama33-70b":  "result_llama-3.3-70b.jsonl",
}

def load_machine_evals(machine_eval_dir):
    """
    从 machine_eval_dir 下每个模型对应 JSONL 文件读取所有行
    => machine_data[model][task_str] = (comm, plan)
    不检查行内 "model"，整份文件都归属于该 model_name。
    """
    machine_data = defaultdict(dict)

    for model_name, filename in MODEL_FILE_MAP.items():
        fpath = os.path.join(machine_eval_dir, filename)
        if not os.path.isfile(fpath):
            print(f"[WARNING] File not found for model={model_name}: {fpath}. Skip.")
            continue

        count_lines = 0
        with open(fpath, "r", encoding="utf-8") as fin:
            for line in fin:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception as e:
                    print(f"  [WARN] JSON decode error in {filename}: {e}")
                    continue

                # 只要当前行有 "task"、communication_score、planning_score
                task_str = obj.get("task", "")
                comm = obj.get("communication_score", -1)
                plan = obj.get("planning_score", -1)
                if not task_str:
                    # 缺少 "task" 就跳过
                    print(f"  [DEBUG] skip line - missing 'task' field.")
                    continue

                # 存入
                machine_data[model_name][task_str] = (comm, plan)
                count_lines += 1

        print(f"  [INFO] Loaded {count_lines} lines for model={model_name}")
    return machine_data

def process_eval_and_merge(human_eval_path, machine_eval_dir, output_jsonl):
    """
    1) 加载机器评 => machine_data[model][task_str] = (comm, plan)
    2) 遍历人评 JSONL, 做低质量过滤, 再与machine_data对齐 => 合并输出
    3) 统计 & 打印各模型平均值
    """
    # 加载所有机器评
    machine_data = load_machine_evals(machine_eval_dir)

    # 用于统计: stats[model] = list of (human_comm, human_plan, machine_comm, machine_plan)
    stats = defaultdict(list)

    with open(human_eval_path, "r", encoding="utf-8") as fin, \
         open(output_jsonl, "w", encoding="utf-8") as fout:

        line_num = 0
        matched_count = 0

        for line in fin:
            line = line.strip()
            if not line:
                continue
            line_num += 1
            try:
                obj = json.loads(line)
            except Exception as e:
                print(f"[WARN] JSON decode error in human_eval line #{line_num}: {e}")
                continue

            task_content = obj.get("task_content","")
            model_name   = obj.get("model","")
            if not task_content or not model_name:
                print(f"[DEBUG] line #{line_num}: skip missing task_content or model.")
                continue

            def convert_to_float(val):
                try:
                    return float(val)
                except:
                    return -1

            c1 = convert_to_float(obj.get("communication_score_1", -1))
            p1 = convert_to_float(obj.get("planning_score_1", -1))
            c2 = convert_to_float(obj.get("communication_score_2", -1))
            p2 = convert_to_float(obj.get("planning_score_2", -1))

            

            # 判断低质量
            scores = [c1, p1, c2, p2]
            negative_count = sum(1 for s in scores if s == -1)
            if negative_count >= 3:
                print(f"  [FILTER] skip line #{line_num}: >=3 negative scores.")
                continue
            if (c1 == -1 and c2 == -1):
                print(f"  [FILTER] skip line #{line_num}: comm all -1.")
                continue
            if (p1 == -1 and p2 == -1):
                print(f"  [FILTER] skip line #{line_num}: plan all -1.")
                continue

            # 人评均值
            valid_comm = []
            if c1 != -1: valid_comm.append(c1)
            if c2 != -1: valid_comm.append(c2)
            human_comm = sum(valid_comm)/len(valid_comm) if valid_comm else -1

            valid_plan = []
            if p1 != -1: valid_plan.append(p1)
            if p2 != -1: valid_plan.append(p2)
            human_plan = sum(valid_plan)/len(valid_plan) if valid_plan else -1


            # 去 machine_data[model_name] 里找
            if model_name not in machine_data:
                print(f"  [DEBUG] line #{line_num}: model={model_name} not in machine_data => skip.")
                continue

            model_dict = machine_data[model_name]
            if task_content not in model_dict:
                print(f"  [DEBUG] line #{line_num}: not found {task_content[:50]} in machine_data[{model_name}] => skip.")
                continue

            llm_comm, llm_plan = model_dict[task_content]

            # 输出
            merged = {
                "task_content": task_content,
                "model": model_name,
                "final_human_communication_score": human_comm,
                "final_human_planning_score": human_plan,
                "llm_communication_score": llm_comm,
                "llm_planning_score": llm_plan
            }
            fout.write(json.dumps(merged, ensure_ascii=False)+"\n")
            stats[model_name].append((human_comm, human_plan, llm_comm, llm_plan))
            matched_count += 1

        print(f"\n[INFO] Finished reading {line_num} lines from {human_eval_path}, matched = {matched_count}.\n")

    # 统计
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
        print(f"  人评 Comm 平均: {avg_hum_comm:.2f}, Plan 平均: {avg_hum_plan:.2f}")
        print(f"  机评 Comm 平均: {avg_llm_comm:.2f}, Plan 平均: {avg_llm_plan:.2f}")
        print("-"*60)


def main():
    # 你的人评 JSONL
    human_eval_path = "human_eval\\database_human_output.jsonl"
    # 你的机器评文件夹
    machine_eval_dir= "llm_eval_result\\db\\output"
    # 输出文件名
    output_jsonl = "human_eval\\database_merged_output.jsonl"

    process_eval_and_merge(human_eval_path, machine_eval_dir, output_jsonl)

if __name__=="__main__":
    main()
