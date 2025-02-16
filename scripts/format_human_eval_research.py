import os
import pandas as pd
import json

# 映射表: A/B/C/D/E => 实际模型名称
MODEL_MAP = {
    'A': 'gpt3.5-turbo',
    'B': 'gpt-4o-mini',
    'C': 'llama31-8b',
    'D': 'llama31-70b',
    'E': 'llama33-70b'
}

def try_read_dataframe(file_path, ext, required_cols, max_header_guess=5):
    """
    尝试用多种 header= 行去读取, 
    检查是否包含 required_cols 所需列.
    如果成功, 返回 df; 否则 None.
    """
    possible_headers = range(max_header_guess)  # [0,1,2,3,4,...]

    for h in possible_headers:
        try:
            if ext == ".csv":
                df_test = pd.read_csv(file_path, encoding="utf-8", header=h)
            else:
                df_test = pd.read_excel(file_path, header=h)

            # 检查是否包含所有所需列
            missing = [col for col in required_cols if col not in df_test.columns]
            if not missing:
                print(f"[INFO] 成功用 header={h} 读取文件, 找到全部列.")
                return df_test
        except Exception as e:
            # 可能会出现解析错误等, 继续下一个 h
            pass

    # 若都失败或列不全, 返回 None
    return None


def process_task_content_scores_with_model(input_dir, output_jsonl="task_content_output.jsonl"):
    """
    在 input_dir 下读取所有 .csv / .xlsx 文件,
    并基于 (task_content, model) 作为键,
    为每个键保存:
      communication_score_1, planning_score_1, task_score_1,
      communication_score_2, planning_score_2, task_score_2,
    以及 model (字符串名称).

    若文件的实际标题行不在默认第1行, 我们会自动尝试多种 header= 行数, 
    找到满足 required_cols 的才视为可用.

    只要有任意一个分数 != -1, 就往下一组槽填; 若 _1 槽已填, 则填到 _2 槽.
    超过 2 组不再处理.
    """

    combined_dict = {}

    # 我们需要的列
    required_cols = ["task_content", "model", "communication_score", "planning_score", "task_score"]

    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        if not os.path.isfile(file_path):
            continue

        ext = os.path.splitext(filename)[1].lower()
        if ext not in [".csv", ".xlsx"]:
            continue

        print(f"[INFO] 正在读取文件: {file_path}")

        # 尝试多行 header
        df = try_read_dataframe(file_path, ext, required_cols, max_header_guess=5)
        if df is None:
            print(f"[WARNING] 文件 {filename} 无法找到所需列 {required_cols}，跳过.\n")
            continue

        # 如果我们成功拿到 df，就迭代行
        for idx, row in df.iterrows():
            task_content = str(row["task_content"])  # 转成字符串
            model_label  = str(row["model"])
            comm_score   = row["communication_score"]
            plan_score   = row["planning_score"]
            tscore       = row["task_score"]

            # 若是空值或NaN就视为-1
            if pd.isna(comm_score):
                comm_score = -1
            if pd.isna(plan_score):
                plan_score = -1
            if pd.isna(tscore):
                tscore = -1

            # 只要有一个 != -1，就可视为一行可用数据
            if (comm_score == -1) and (plan_score == -1) and (tscore == -1):
                continue

            # 映射模型名称
            model_name = MODEL_MAP.get(model_label, model_label)

            # key = (task_content, model_name)
            key = (task_content, model_name)

            if key not in combined_dict:
                combined_dict[key] = {
                    "task_content": task_content,
                    "model": model_name,
                    "communication_score_1": -1,
                    "planning_score_1": -1,
                    "task_score_1": -1,
                    "communication_score_2": -1,
                    "planning_score_2": -1,
                    "task_score_2": -1
                }

            slot_data = combined_dict[key]

            # 填充逻辑
            # 第1槽:
            if (slot_data["communication_score_1"] == -1 and
                slot_data["planning_score_1"] == -1 and
                slot_data["task_score_1"] == -1):
                slot_data["communication_score_1"] = comm_score
                slot_data["planning_score_1"]      = plan_score
                slot_data["task_score_1"]          = tscore
            # 第2槽:
            elif (slot_data["communication_score_2"] == -1 and
                  slot_data["planning_score_2"] == -1 and
                  slot_data["task_score_2"] == -1):
                slot_data["communication_score_2"] = comm_score
                slot_data["planning_score_2"]      = plan_score
                slot_data["task_score_2"]          = tscore
            else:
                # 超过2组则跳过
                pass

    # 最后输出到 jsonl
    with open(output_jsonl, "w", encoding="utf-8") as f_out:
        for (task_content, model_name), data_obj in combined_dict.items():
            f_out.write(json.dumps(data_obj, ensure_ascii=False))
            f_out.write("\n")

    print(f"[INFO] 处理完成, 结果输出至: {output_jsonl}")


if __name__ == "__main__":
    input_dir = "human_eval\\bargain\\buy"
    process_task_content_scores_with_model(input_dir, output_jsonl="human_eval\\buy_human_output.jsonl")
