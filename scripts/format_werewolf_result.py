import os
import sys
import json
import tqdm
#########################
#   工具函数
#########################

def load_json(path):
    """带调试信息的加载 JSON 函数。"""
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def get_role_of_player(ckpt_data, player_name):
    players = ckpt_data.get("shared_memory", {}) \
                       .get("private_state", {}) \
                       .get("players", {})
    pinfo = players.get(player_name, {})
    return pinfo.get("role")

def is_player_alive(ckpt_data, player_name):
    players = ckpt_data.get("shared_memory", {}) \
                       .get("private_state", {}) \
                       .get("players", {})
    pinfo = players.get(player_name, {})
    status = pinfo.get("status", {})
    return status.get("health", 0) > 0

def get_current_scores(ckpt_data):
    scores = ckpt_data.get("scores", {})
    villager = scores.get("villager", {}).get("total", 0.0)
    werewolf = scores.get("werewolf", {}).get("total", 0.0)
    return (villager, werewolf)

def find_player_by_role(ckpt_data, role_name):
    players = ckpt_data.get("shared_memory", {}) \
                       .get("private_state", {}) \
                       .get("players", {})
    for name, info in players.items():
        if info.get("role") == role_name:
            return name
    return None

def check_witch_action(end_ckpt_data):
    night_cache = end_ckpt_data.get("shared_memory", {}) \
                               .get("private_state", {}) \
                               .get("night_cache", [])
    if not night_cache:
        return ("none", None)
    last_night = night_cache[-1]
    witch_action = last_night.get("witch_action", {})
    result = (witch_action.get("action", "none"), witch_action.get("target", None))

    return result

def get_banishment_result(end_ckpt_data):
    day_cache = end_ckpt_data.get("shared_memory", {}) \
                             .get("public_state", {}) \
                             .get("day_cache", [])
    if not day_cache:
        return None
    last_day = day_cache[-1]
    return last_day.get("banishment_result")

#############################
#   额外工具: 进入子目录查找
#############################

def find_end_ckpt_for_single_day(logs_folder):
    """
    单日模拟需要深入子目录:
      1) 若 logs_folder 下只有一个子目录 => 进入
      2) 在该(或当前)目录里找 'checkpoint_Night*.json'
    """
    if not os.path.isdir(logs_folder):
        print(f"[DEBUG] logs_folder不是文件夹 => {logs_folder}")
        return []

    items = os.listdir(logs_folder)
    items = [x for x in items if not x.startswith(".")]  # 过滤隐藏文件
    subfolders = [x for x in items if os.path.isdir(os.path.join(logs_folder, x))]

    # 如果只有一个子文件夹, 则进入
    if len(subfolders) == 1:
        only_sub = subfolders[0]
        new_path = os.path.join(logs_folder, only_sub)
        logs_folder = new_path

    cands = [
        f for f in os.listdir(logs_folder)
        if f.startswith("checkpoint_Night") and f.endswith(".json")
    ]
    cands.sort()
    fullpaths = [os.path.join(logs_folder, x) for x in cands]
    return fullpaths
def get_subfolder_path(folder_path):
    """ 获取 logs_folder 里面的唯一子文件夹路径 """
    if not os.path.exists(folder_path):
        return None
    
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    
    if len(subfolders) != 1:
        return None
    return os.path.join(folder_path, subfolders[0])
#############################
#   单日任务分析函数
#############################
def analyze_one_day(start_ckpt_data, end_ckpt_data):

    tasks_available = []
    task_completion = {
        "poison_werewolf": False,
        "rescue_villager": False,
        "exile_werewolf": False,
        "protect_seer": False
    }

    # 找巫女
    witch_player = find_player_by_role(start_ckpt_data, "witch")
    has_poison = False
    has_antidote = False
    if witch_player and is_player_alive(start_ckpt_data, witch_player):
        w_info = (start_ckpt_data.get("shared_memory", {})
                                  .get("private_state", {})
                                  .get("players", {})
                                  .get(witch_player, {}))
        poison_count   = w_info.get("status", {}).get("poison_count", 0)
        antidote_count = w_info.get("status", {}).get("antidote_count", 0)
        has_poison     = (poison_count > 0)
        has_antidote   = (antidote_count > 0)

    # 找预言家
    seer_player = find_player_by_role(start_ckpt_data, "seer")
    seer_alive_start = (seer_player and is_player_alive(start_ckpt_data, seer_player))

    # 常驻任务：放逐狼人
    tasks_available.append("exile_werewolf")

    if witch_player and is_player_alive(start_ckpt_data, witch_player) and has_poison:
        tasks_available.append("poison_werewolf")

    if witch_player and is_player_alive(start_ckpt_data, witch_player) and has_antidote:
        tasks_available.append("rescue_villager")

    if seer_alive_start:
        tasks_available.append("protect_seer")

    sc_exile   = 2 if "exile_werewolf" in tasks_available else 0
    sc_poison  = 2 if "poison_werewolf" in tasks_available else 0
    sc_rescue  = 2 if "rescue_villager" in tasks_available else 0
    sc_protect = 1 if "protect_seer" in tasks_available else 0

    best_of_poison_rescue = max(sc_poison, sc_rescue)
    theoretical_max = sc_exile + best_of_poison_rescue + sc_protect

    banished_player = get_banishment_result(end_ckpt_data)
    if banished_player:
        if get_role_of_player(end_ckpt_data, banished_player) == "wolf":
            task_completion["exile_werewolf"] = True

    witch_action, witch_target = check_witch_action(end_ckpt_data)
    if witch_action == "poison" and witch_target:
        if get_role_of_player(end_ckpt_data, witch_target) == "wolf":
            task_completion["poison_werewolf"] = True
    elif witch_action == "antidote" and witch_target:
        role_target = get_role_of_player(end_ckpt_data, witch_target)
        if role_target != "wolf":
            task_completion["rescue_villager"] = True

    if seer_alive_start and seer_player:
        if is_player_alive(end_ckpt_data, seer_player):
            task_completion["protect_seer"] = True

    # 计算当日任务分值
    daily_actual_major_score = 0.0
    if task_completion["exile_werewolf"]:
        daily_actual_major_score += 2
    if task_completion["poison_werewolf"]:
        daily_actual_major_score += 2
    if task_completion["rescue_villager"]:
        daily_actual_major_score += 2
        # 如果救下seer或guard额外+1
        if witch_target:
            r_role = get_role_of_player(end_ckpt_data, witch_target)
            if r_role in ["seer", "guard"]:
                daily_actual_major_score += 1

    if task_completion["protect_seer"]:
        daily_actual_major_score += 1

    # 村民、狼人当日分增量
    v_start, w_start = get_current_scores(start_ckpt_data)
    v_end, w_end     = get_current_scores(end_ckpt_data)
    daily_score_villager = v_end - v_start
    daily_score_werewolf = w_end - w_start

    # 任务完成度
    completion_ratio = 0.0
    if theoretical_max > 0:
        completion_ratio = round(daily_actual_major_score / theoretical_max, 2)

    return {
        "tasks_available": tasks_available,
        "task_completion": task_completion,
        "theoretical_max": theoretical_max,
        "daily_actual_major_score": round(daily_actual_major_score, 2),
        "completion_ratio": completion_ratio,
        "daily_score_villager": round(daily_score_villager, 2),
        "daily_score_werewolf": round(daily_score_werewolf, 2),
    }

#############################
#   处理整局模拟(Full-run)
#############################
def analyze_full_run(full_run_item):
    """
    分析完整模拟结果，包括:
    1. 从 `start_ckpt` 对应的原始游戏文件夹 (`origin_folder`) 读取 `result.json` 到 out["origin_result"]
    2. 从 `logs_folder` 内的唯一子文件夹读取 `result.json` 和 `shared_memory.json` 到 out["simulation_result"] & out["simulation_log"]
    """

    out = {
        "origin_result": {},
        "simulation_result": {},
        "simulation_log": ""
    }
    if not full_run_item:
        return out

    start_ckpt = full_run_item.get("start_ckpt", "")
    logs_folder = full_run_item.get("logs_folder", "")

    if not start_ckpt or not logs_folder:
        return out

    # 1) **获取原始游戏存档文件夹**
    origin_folder = os.path.dirname(start_ckpt)
    origin_result_path = os.path.join(origin_folder, "result.json")

    # 读取原始游戏的 result.json (origin_result)
    if os.path.exists(origin_result_path):
        origin_data = load_json(origin_result_path)
        # 将关键信息存入 out["origin_result"]
        out["origin_result"]["process_scores"] = origin_data.get("process_scores", {})
        out["origin_result"]["result_score"] = origin_data.get("result_score")
        out["origin_result"]["surviving_players"] = origin_data.get("surviving_players", [])
        out["origin_result"]["game_result"] = origin_data.get("game_result", "")

    # 2) **进入 logs_folder 里的唯一子文件夹**
    logs_subfolder = get_subfolder_path(logs_folder)
    if not logs_subfolder:
        print(f"[ERROR] {logs_folder} 里没有可用的子文件夹，无法继续。")
        return out

    # 3) **读取 `logs_subfolder` 里的 result.json (simulation_result)**
    sim_result_path = os.path.join(logs_subfolder, "result.json")
    if os.path.exists(sim_result_path):
        sim_data = load_json(sim_result_path)
        # 将关键信息同样存入 out["simulation_result"]
        out["simulation_result"]["process_scores"] = sim_data.get("process_scores", {})
        out["simulation_result"]["result_score"] = sim_data.get("result_score")
        out["simulation_result"]["surviving_players"] = sim_data.get("surviving_players", [])
        out["simulation_result"]["game_result"] = sim_data.get("game_result", "")

    # 4) **读取 `logs_subfolder` 里的 shared_memory.json**
    sim_shared_path = os.path.join(logs_subfolder, "shared_memory.json")
    try:
        with open(sim_shared_path, "r", encoding="utf-8") as f:
            shared_data = json.load(f)
            game_log = shared_data.get("private_event_log", "")
            out["simulation_log"] = game_log  # 确保获取 private_event_log
    except Exception as e:
        print(f"[ERROR] 读取 {sim_shared_path} 失败: {e}")

    return out
#############################
#   模型名称映射 (如有需要)
#############################
MODEL_MAP = {
    "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo":  "llama31-8B",
    "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo": "llama31-70B",
    "meta-llama/Llama-3.3-70B-Instruct-Turbo":      "llama33-70B",
    "gpt-4o":                                       "gpt-4o",
    "gpt-3.5-turbo":                                "gpt-35",
    "gpt-4o-mini":                                  "gpt-4o-mini",
}

def simplify_model_name(orig_name: str) -> str:
    return MODEL_MAP.get(orig_name, orig_name)

#############################
#   主流程
#############################
def run_analysis(eval_folder_path, output_dir):
    """
    读取 eval_folder_path/final_result.json, 处理单日 & 整局模拟。
    单日模拟 => 会深入子目录找到 checkpoint_Night*.json
    整局模拟 => 不深入子目录 => 直接找 result.json / shared_memory.json
    最终写出 JSON 到 output_dir/<gameName>_<modelShort>.json
    """
    final_result_path = os.path.join(eval_folder_path, "final_result.json")
    if not os.path.exists(final_result_path):
        print(f"[ERROR] 未找到 final_result.json => {final_result_path}")
        return

    final_data = load_json(final_result_path)
    per_cycle_results = final_data.get("per_cycle_results", [])
    full_run_item     = final_data.get("full_run_result", {})


    # 收集单日模拟结果
    single_day_results = []
    for idx, cycle_item in enumerate(per_cycle_results):
        is_cycle = cycle_item.get("simulate_one_cycle", False)
        if not is_cycle:
            continue

        ckpt_path   = cycle_item.get("ckpt_path", "")
        logs_folder = cycle_item.get("logs_folder", "")
        if not (ckpt_path and logs_folder):
            continue

        if not (os.path.exists(ckpt_path) and os.path.exists(logs_folder)):
            continue

        # 在 logs_folder 下进入子目录找 checkpoint_Night*.json
        end_ckpt_list = find_end_ckpt_for_single_day(logs_folder)
        if not end_ckpt_list:
            continue

        # 假设只取第一个
        end_ckpt_path = end_ckpt_list[0]
        start_data = load_json(ckpt_path)
        end_data   = load_json(end_ckpt_path)
        day_res = analyze_one_day(start_data, end_data)

        # 可加更多字段
        day_res["ckpt_path"]      = ckpt_path
        day_res["logs_folder"]    = logs_folder
        day_res["end_ckpt_file"]  = os.path.basename(end_ckpt_path)

        single_day_results.append(day_res)

    # 整局模拟
    full_run_data = {}
    if full_run_item and (full_run_item.get("simulate_one_cycle", True) == False):
        # analyze
        full_run_data = analyze_full_run(full_run_item)
    

    # 合并结果
    output_data = {
        "single_day_results": single_day_results,
        "full_run_result": full_run_data
    }

    # 提取 game_name + model_short
    game_name = "unknown_game"
    model_short = "unknown_model"

    # 先在 per_cycle 里找
    for citem in per_cycle_results:
        cp = citem.get("ckpt_path", "")
        if cp:
            norm = cp.replace("\\", "/")
            parts = norm.split("/")
            if len(parts) >= 3 and parts[0] == "werewolf_log":
                game_name = parts[1]
                break

    # 如果没找到, 看 full_run_item
    if game_name == "unknown_game" and full_run_item:
        sc = full_run_item.get("start_ckpt", "")
        if sc:
            norm = sc.replace("\\", "/")
            parts = norm.split("/")
            if len(parts) >= 3 and parts[0] == "werewolf_log":
                game_name = parts[1]

    # 找 model_name
    for citem in per_cycle_results:
        stage_res = citem.get("result", {}).get("stage_result", {})
        cfg = stage_res.get("config", {})
        villager_cfg = cfg.get("villager_config", {})
        if "model_name" in villager_cfg:
            raw_model = villager_cfg["model_name"]
            model_short = simplify_model_name(raw_model)
            break

    if model_short == "unknown_model" and full_run_item:
        fu_stage = full_run_item.get("result", {}).get("stage_result", {})
        fu_cfg   = fu_stage.get("config", {})
        villager_cfg2 = fu_cfg.get("villager_config", {})
        if "model_name" in villager_cfg2:
            raw_model = villager_cfg2["model_name"]
            model_short = simplify_model_name(raw_model)

    file_name = f"{game_name}_{model_short}.json"
    out_path  = os.path.join(output_dir, file_name)

    with open(out_path, 'w', encoding='utf-8') as f_out:
        json.dump(output_data, f_out, ensure_ascii=False, indent=2)


def collect_folders_with_final_result(root_folder):
    """
    从 root_folder 的直接子文件夹里查找是否存在 final_result.json，收集并返回这些文件夹列表。

    如果需要递归多层目录，可以改成用 os.walk 或 glob：
      - os.walk(root_folder)
      - glob.glob(os.path.join(root_folder, '**', 'final_result.json'), recursive=True)
      ...
    """
    folders = []
    for entry in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, entry)
        if os.path.isdir(folder_path):
            # 在该子目录内查找 final_result.json
            final_result_path = os.path.join(folder_path, "final_result.json")
            if os.path.exists(final_result_path):
                folders.append(folder_path)
    return folders


def collect_eval_folders(root_folder):
    """
    遍历 root_folder 下所有「一级子目录 -> 二级子目录」，
    如果存在 final_result.json，则把该二级子目录记录下来。
    返回值: eval_folders (List[str])
    """
    eval_folders = []
    for first_level in os.listdir(root_folder):
        path1 = os.path.join(root_folder, first_level)
        if not os.path.isdir(path1):
            continue

        for second_level in os.listdir(path1):
            path2 = os.path.join(path1, second_level)
            if not os.path.isdir(path2):
                continue

            final_path = os.path.join(path2, "final_result.json")
            if os.path.exists(final_path):
                eval_folders.append(path2)

    return eval_folders

def analyze_all_storages(root_folder, out_dir):
    """
    1. 收集二级子目录下所有含有 final_result.json 的目录路径
    2. 使用 tqdm 显示进度条依次调用 run_analysis(...)
    3. 捕获异常并输出错误
    """
    if not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    
    eval_folders = collect_eval_folders(root_folder)
    total_found = len(eval_folders)
    success_count = 0

    if total_found == 0:
        print(f"[INFO] 在 {root_folder} 未找到任何二级子目录包含 final_result.json")
        return

    print(f"[INFO] 在 {root_folder} 下共找到 {total_found} 个存档目录，开始分析...")

    from tqdm import tqdm
    with tqdm(total=total_found, desc="Analyzing storages") as pbar:
        for folder in eval_folders:
            try:
                run_analysis(folder, out_dir)
                success_count += 1
            except Exception as e:
                print(f"[ERROR] 分析 {folder} 时出错: {e}")
            finally:
                pbar.update(1)

    print(f"[SUMMARY] 全部处理完成 => 共找到 {total_found} 个需要分析的存档，成功处理 {success_count} 个.")


#############################
#   脚本入口 (示例)
#############################
if __name__ == "__main__":
    # 根据需要修改 root_dir 或通过命令行传入
    root_dir = "werewolf_eval"  # 两级子目录根路径
    out_dir  = "werewolf_result"       # 分析结果输出目录

    #analyze_all_storages(root_dir, out_dir)
    analyze_all_storages(root_dir, out_dir)
    print("[INFO] 全部存档分析结束。")