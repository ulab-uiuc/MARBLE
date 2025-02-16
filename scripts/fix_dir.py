import os
import glob
import json
from tqdm import tqdm

# 模型名称映射表
MODEL_MAP = {
    "gpt-4o": "4o",
    "gpt-4o-mini": "4omini",
    "gpt-3.5-turbo": "gpt35",
    "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo": "llama31_8b",
    "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo": "llama31_70b",
    "meta-llama/Llama-3.3-70B-Instruct-Turbo": "llama33"
}

def get_correct_log_folder(logs_folder, model_name):
    """
    修正 logs_folder 目录路径，确保其位于 werewolf_eval/<model_dir>/eval_xxx/ 目录下，
    而不是 werewolf_eval/eval_xxx/<model_dir>/。
    """

    path_parts = logs_folder.split(os.sep)

    # 确保路径以 werewolf_eval 开头
    if len(path_parts) < 2 or path_parts[0] != "werewolf_eval":
        # 格式异常，直接返回原路径，或你也可根据需求报错
        # print(f"[WARNING] 非标准路径，不处理: {logs_folder}")
        return logs_folder

    # 取 werewolf_eval 后的那一段，假设是 eval_xxx_...
    eval_name = path_parts[1]  # 例如 'eval_20250126_135325'
    
    model_dir = MODEL_MAP.get(model_name)
    if model_dir is None:
        # 如果找不到模型名称对应的映射，就不修正
        # print(f"[WARNING] 未找到模型 `{model_name}` 对应文件夹，跳过修正。")
        return logs_folder

    # 重构正确路径: werewolf_eval/<model_dir>/eval_xxx/...余下部分
    correct_folder = os.path.join("werewolf_eval", model_dir, eval_name, *path_parts[2:])
    return correct_folder

def fix_final_result(final_result_path):
    """
    读取 `final_result.json`，检查并修复 logs_folder 地址错误，然后覆盖原文件。
    返回值: 是否有修改（True/False）。
    """
    if not os.path.exists(final_result_path):
        # 不存在文件，跳过
        return False

    with open(final_result_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    modified = False

    # 1) 修复单日模拟 per_cycle_results
    for cycle_item in data.get("per_cycle_results", []):
        logs_folder = cycle_item.get("logs_folder", "")
        config = cycle_item.get("result", {}).get("stage_result", {}).get("config", {})
        model_name = config.get("villager_config", {}).get("model_name", "")

        if logs_folder and model_name:
            corrected_folder = get_correct_log_folder(logs_folder, model_name)
            if corrected_folder != logs_folder:
                # 打印修正信息
                print(f"[FIXED] logs_folder 修正: {logs_folder} -> {corrected_folder}")
                cycle_item["logs_folder"] = corrected_folder
                modified = True

    # 2) 修复整局模拟 full_run_result
    full_run = data.get("full_run_result", {})
    logs_folder = full_run.get("logs_folder", "")
    config = full_run.get("result", {}).get("stage_result", {}).get("config", {})
    model_name = config.get("villager_config", {}).get("model_name", "")

    if logs_folder and model_name:
        corrected_folder = get_correct_log_folder(logs_folder, model_name)
        if corrected_folder != logs_folder:
            print(f"[FIXED] full_run logs_folder 修正: {logs_folder} -> {corrected_folder}")
            full_run["logs_folder"] = corrected_folder
            modified = True

    # 如有变动则覆盖文件
    if modified:
        with open(final_result_path, "w", encoding="utf-8") as f_out:
            json.dump(data, f_out, ensure_ascii=False, indent=2)
        print(f"[INFO] 修正完成，已覆盖 `{final_result_path}`")

    return modified

def fix_all_final_results(root_folder):
    """
    1. 使用 glob 递归搜索 root_folder 下的所有 final_result.json
    2. 依次修正 logs_folder
    3. 显示进度条
    """
    # 找到所有 final_result.json
    pattern = os.path.join(root_folder, "**", "final_result.json")
    all_paths = glob.glob(pattern, recursive=True)

    if not all_paths:
        print(f"[INFO] 在 {root_folder} 下未发现任何 final_result.json 文件。")
        return

    print(f"[INFO] 在 {root_folder} 下共发现 {len(all_paths)} 个 final_result.json 文件。")
    
    count_fixed = 0
    with tqdm(total=len(all_paths), desc="Processing final_result.json") as pbar:
        for final_path in all_paths:
            # 修复
            if fix_final_result(final_path):
                count_fixed += 1
            pbar.update(1)

    print(f"[SUMMARY] 处理完毕，共修正 {count_fixed}/{len(all_paths)} 个文件。")

if __name__ == "__main__":
    # 让用户在终端输入 root_folder
    folder = "werewolf_eval"
    fix_all_final_results(folder)
