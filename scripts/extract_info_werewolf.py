#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json

def find_subfolder_by_prefix(parent_dir, prefix="fullrun"):
    """
    在 parent_dir 目录下查找名称以 prefix 开头的文件夹（不递归）。
    如果找到多个，则返回第一个；若找不到则返回 None。
    """
    if not os.path.isdir(parent_dir):
        return None
    
    for item in os.listdir(parent_dir):
        full_path = os.path.join(parent_dir, item)
        if os.path.isdir(full_path) and item.startswith(prefix):
            return full_path
    return None

def get_single_subfolder(folder_path):
    """
    在 folder_path 下找“唯一的子文件夹”，返回它的完整路径。
    如果不存在或找到多个，则返回 None。
    """
    if not os.path.isdir(folder_path):
        return None
    
    subfolders = [
        os.path.join(folder_path, d)
        for d in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, d))
    ]
    if len(subfolders) == 1:
        return subfolders[0]
    else:
        return None

def load_shared_memory(json_path):
    """
    加载 shared_memory.json 并返回解析结果(字典)。
    若失败则返回 None。
    """
    if not os.path.isfile(json_path):
        print(f"[警告] 未找到文件: {json_path}")
        return None
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"[警告] 解析 JSON 文件出错: {json_path}, 错误: {e}")
        return None

def load_txt_file_keep_braces_only(txt_path):
    """
    读取 txt 文件内容，逐行处理，只保留“去掉前后空格后以 '{' 开头”的行。
    将这些行拼成一个字符串（用换行分隔）。
    若文件不存在或出错则返回 None；若无满足行则返回空字符串("")。
    """
    if not os.path.isfile(txt_path):
        return None
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        brace_lines = []
        for ln in lines:
            stripped = ln.strip()
            if stripped.startswith("{"):
                brace_lines.append(stripped)
        return "\n".join(brace_lines)
    except Exception as e:
        print(f"[警告] 读取TXT文件出错: {txt_path}, 错误: {e}")
        return None

def load_thought_txt_files(folder_path):
    """
    在给定文件夹下查找并处理 'witch', 'guard', 'seer' txt文件。
    对每个文件仅保留以 '{' 开头的行，拼成字符串。
    若文件不存在，则值为 None；文件存在但无匹配行则为 ""。
    """
    result = {
        "witch_thought": None,
        "guard_thought": None,
        "seer_thought": None
    }
    
    if not os.path.isdir(folder_path):
        return result

    for file_name in os.listdir(folder_path):
        lower_name = file_name.lower()
        if file_name.endswith(".txt"):
            full_path = os.path.join(folder_path, file_name)
            if "witch" in lower_name:
                result["witch_thought"] = load_txt_file_keep_braces_only(full_path)
            elif "guard" in lower_name:
                result["guard_thought"] = load_txt_file_keep_braces_only(full_path)
            elif "seer" in lower_name:
                result["seer_thought"] = load_txt_file_keep_braces_only(full_path)
    
    return result

def build_roles_summary(shared_data):
    """
    从 shared_data["private_state"]["players"] 提取玩家名称与角色，
    将 'wolf' 视为狼人阵营，其它全部视为村民阵营，
    最后返回字符串，例如：
    
    狼人阵营: Robert: wolf, Irma: wolf, Marlene: wolf
    村民阵营: Arthur: witch, Angela: guard, ...
    """
    if not isinstance(shared_data, dict):
        return ""

    players = shared_data.get("private_state", {}).get("players", {})
    if not players:
        return ""

    wolf_list = []
    villager_list = []
    for player_name, info in players.items():
        role = info.get("role", "unknown")
        if role == "wolf":
            wolf_list.append(f"{player_name}: {role}")
        else:
            villager_list.append(f"{player_name}: {role}")

    # 拼成两行或一行均可，下面演示两行
    wolf_part = ", ".join(wolf_list) if wolf_list else "（无狼）"
    villager_part = ", ".join(villager_list) if villager_list else "（无村民）"

    summary_str = f"狼人阵营: {wolf_part}\n村民阵营: {villager_part}"
    return summary_str

def process_single_archive(archive_dir):
    """
    处理单个“存档模拟”目录：
      1. 找到 fullrun* 文件夹
      2. 进入它唯一的子文件夹
      3. 读取 shared_memory.json -> private_event_log(完整)
      4. 根据玩家角色分组生成 roles_summary
      5. 读取 witch/guard/seer 三个txt，只保留以 '{' 开头的行
      6. 返回一个结果字典
    """
    # 1. fullrun文件夹
    fullrun_folder = find_subfolder_by_prefix(archive_dir, prefix="fullrun")
    if not fullrun_folder:
        print(f"[提示] 在 {archive_dir} 未找到以 'fullrun' 开头的文件夹，跳过。")
        return None
    
    # 2. 唯一子文件夹
    subfolder = get_single_subfolder(fullrun_folder)
    if not subfolder:
        print(f"[提示] 在 {fullrun_folder} 下无法确定唯一子文件夹，跳过。")
        return None

    # 3. load shared_memory
    shared_memory_path = os.path.join(subfolder, "shared_memory.json")
    shared_data = load_shared_memory(shared_memory_path)

    private_event_log = None
    roles_summary = ""
    if shared_data:
        private_event_log = shared_data.get("private_event_log", "")
        roles_summary = build_roles_summary(shared_data)

    # 4. 读3个txt
    thought_txts = load_thought_txt_files(subfolder)

    # 此处把 archive_dir, fullrun_folder, subfolder 三个字段合并为一个字符串
    # 你也可改成其它拼接方式
    combined_archive_path = f"{archive_dir} | {fullrun_folder} | {subfolder}"

    # 汇总结果
    result = {
        "archive_dir": combined_archive_path,    # 合并路径信息
        "private_event_log": private_event_log,  # 原封不动存储
        "roles_summary": roles_summary,          # 狼人阵营 + 村民阵营
        "witch_thought": thought_txts["witch_thought"],
        "guard_thought": thought_txts["guard_thought"],
        "seer_thought": thought_txts["seer_thought"]
    }
    return result

def process_all_archives(root_dir):
    """
    在 root_dir 下，假设有多个存档模拟文件夹（视为所有直接子目录）。
    逐个处理后返回列表(每个元素是上面 process_single_archive 的返回)。
    """
    if not os.path.isdir(root_dir):
        print(f"[错误] 提供的根目录不存在: {root_dir}")
        return []
    
    result_list = []
    for entry in os.listdir(root_dir):
        archive_path = os.path.join(root_dir, entry)
        if os.path.isdir(archive_path):
            data = process_single_archive(archive_path)
            if data:
                result_list.append(data)
    return result_list

def main(root_dir, output_path):
    

    all_results = process_all_archives(root_dir)

    # 将结果写入 JSONL 文件，每个dict一行
    with open(output_path, "w", encoding="utf-8") as outf:
        for item in all_results:
            line = json.dumps(item, ensure_ascii=False)
            outf.write(line + "\n")
    
    print(f"[完成] 已处理 {len(all_results)} 个存档，并写入 {output_path}")

if __name__ == "__main__":
    root_dir = "werewolf_eval\\llama33"
    output_path = "output_llama33.jsonl"
    main(root_dir, output_path)
