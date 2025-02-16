import os
import pandas as pd
import json

def process_folder_scores(input_dir, output_jsonl="output.jsonl"):
    """
    在 input_dir 下读取所有 .csv / .xlsx 文件，
    并根据每行的 folder_path、communication_score、planning_score 
    组装成 {folder_path: {communication_score_1, planning_score_1, communication_score_2, planning_score_2}},
    然后输出到 output_jsonl (jsonl) 文件。
    """

    # 存放最终结果: {folder_path: {"communication_score_1":..., "planning_score_1":..., "communication_score_2":..., "planning_score_2":...}}
    folder_dict = {}

    # 扫描文件夹
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        if not os.path.isfile(file_path):
            continue

        # 判断后缀
        ext = os.path.splitext(filename)[1].lower()
        if ext not in [".csv", ".xlsx"]:
            continue

        print(f"正在读取文件: {file_path}")
        # 尝试读取
        try:
            if ext == ".csv":
                df = pd.read_csv(file_path, encoding="utf-8")
            else:  # xlsx
                df = pd.read_excel(file_path)
        except Exception as e:
            print(f"读取文件失败: {file_path}, 错误: {e}")
            continue

        # 假设DataFrame里至少包含以下列: folder_path, communication_score, planning_score
        # 也可以用 df.columns 检查实际列名
        required_cols = ["folder_path", "communication_score", "planning_score"]
        for col in required_cols:
            if col not in df.columns:
                print(f"[WARNING] 文件 {filename} 中缺少列: {col}, 跳过")
                continue

        # 遍历行
        for idx, row in df.iterrows():
            folder_path = row["folder_path"]
            comm_score  = row["communication_score"]
            plan_score  = row["planning_score"]

            # 如果comm_score 或 plan_score不是数字，需要跳过或处理
            # 若为空值NaN等情况，可判定
            if pd.isna(comm_score):
                comm_score = -1
            if pd.isna(plan_score):
                plan_score = -1

            # 只处理不是 -1 的项
            if (comm_score == -1 and plan_score == -1):
                # 表示这行数据无效(都为 -1), 可跳过
                continue

            # 如果 folder_path 不在字典里，先初始化
            if folder_path not in folder_dict:
                folder_dict[folder_path] = {
                    "communication_score_1": -1,
                    "planning_score_1": -1,
                    "communication_score_2": -1,
                    "planning_score_2": -1,
                }

            slot_data = folder_dict[folder_path]

            # 检查第1槽，若为 -1, 则填入
            # 否则填第2槽
            # 如果第1槽已经不是 -1, 并且第2槽也不是 -1, 则说明已经有2组分数了，不再处理
            if slot_data["communication_score_1"] == -1 and slot_data["planning_score_1"] == -1:
                # 填第1组
                slot_data["communication_score_1"] = comm_score
                slot_data["planning_score_1"]      = plan_score
            elif slot_data["communication_score_2"] == -1 and slot_data["planning_score_2"] == -1:
                # 填第2组
                slot_data["communication_score_2"] = comm_score
                slot_data["planning_score_2"]      = plan_score
            else:
                # 两个槽都占满, 什么都不做(或可以看情况覆盖?)
                pass

    # 生成 jsonl 文件
    with open(output_jsonl, "w", encoding="utf-8") as f_out:
        for folder_path, score_data in folder_dict.items():
            # 输出时可以追加 folder_path 字段便于识别
            # 也可只输出分数
            output_line = {
                "folder_path": folder_path,
                "communication_score_1": score_data["communication_score_1"],
                "planning_score_1": score_data["planning_score_1"],
                "communication_score_2": score_data["communication_score_2"],
                "planning_score_2": score_data["planning_score_2"]
            }
            # 每行一个 JSON
            f_out.write(json.dumps(output_line, ensure_ascii=False))
            f_out.write("\n")

    print(f"[INFO] 已处理完毕, 结果输出到 {output_jsonl}")


if __name__ == "__main__":
    input_dir = "human_eval\werewolf"  # TODO: 替换成实际存放 CSV/XLSX 的文件夹路径
    process_folder_scores(input_dir, output_jsonl="human_eval\werewolf_human_output.jsonl")