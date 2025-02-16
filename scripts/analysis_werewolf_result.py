import os
import sys
import json
import re
import matplotlib.pyplot as plt
from collections import defaultdict

# 模型名称映射 (可根据需求自行扩展/修改)
MODEL_MAP = {
    "gpt-4o": "4o",
    "gpt-4o-mini": "4o-mini",
    "gpt-3.5-turbo": "gpt-35",
    "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo": "llama31-8B",
    "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo": "llama31-70B",
    "meta-llama/Llama-3.3-70B-Instruct-Turbo": "llama33-70B"
}

def analyze_model_files(model_short_name, input_dir, output_dir):
    """
    从 input_dir 下读取所有以 <model_short_name>.json 结尾的文件，
    解析并统计:
      - 单日模拟指标: completion_ratio, villager_score, werewolf_score, net_score
      - 整局模拟指标: villager process score, net process score, result_score
      - 单日任务出现/完成率
      - 原本胜负 → 模拟胜负的翻盘率(含狼人赢→村民赢 & 村民赢→狼人赢)
      - 新增“原始胜率” (original_villager_win_ratio / original_werewolf_win_ratio)，与模拟村民胜率对比

    并生成:
      1) 原有每场数据的柱状图(7 张)
      2) 数据分布图(直方图)(7 张)
    最终结果写入 JSON (analysis_{model_short_name}.json)，图表保存到 output_dir/charts。
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    charts_dir = os.path.join(output_dir, "charts")
    if not os.path.exists(charts_dir):
        os.makedirs(charts_dir)

    # -- 单日模拟统计容器
    day_completion_ratios = []
    day_villager_scores   = []
    day_werewolf_scores   = []
    day_net_scores        = []

    # -- 整局模拟统计容器
    full_villager_scores  = []
    full_net_scores       = []
    full_result_scores    = []

    # 单日任务出现与完成 => { "exile_werewolf": [appear_count, complete_count], ... }
    task_stats = defaultdict(lambda: [0, 0])

    # 全局模拟胜利统计
    full_count            = 0               # 记录完整模拟场次 (有 full_run_result 就算 1 场)
    villager_win_count    = 0               # 模拟时 "Villagers win" 的场数

    # 原始狼人赢 → 模拟村民赢
    original_wolf_count   = 0
    wolf_to_villager_win  = 0

    # 原始村民赢 → 模拟狼人赢
    original_vill_count   = 0
    vill_to_werewolf_win  = 0

    # 遍历输入目录下所有文件
    files = os.listdir(input_dir)

    # endswith + 正则 "_xxx.json$" 匹配
    pattern = re.compile(rf"_{re.escape(model_short_name)}\.json$")
    target_files = [
        f for f in files
        if f.endswith(f"{model_short_name}.json") or pattern.search(f)
    ]


    for filename in target_files:
        filepath = os.path.join(input_dir, filename)
        if not os.path.isfile(filepath):
            continue

        # 1) 根据文件名检查"原始胜利"是谁
        # 例如 fileName = "game_20250101_180159_Werewolves_win_4o.json"
        original_win = None
        if "_Werewolves_win_" in filename:
            original_win = "Werewolves win"
        elif "_Villagers_win_" in filename:
            original_win = "Villagers win"

        # 2) 读取 JSON
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[WARNING] 读取失败 {filepath}: {e}")
            continue

        # 3) 单日模拟
        single_days = data.get("single_day_results", [])
        for day_res in single_days:
            ratio = day_res.get("completion_ratio", 0.0)
            dv    = day_res.get("daily_score_villager", 0.0)
            dw    = day_res.get("daily_score_werewolf", 0.0)

            day_completion_ratios.append(ratio)
            day_villager_scores.append(dv)
            day_werewolf_scores.append(dw)
            day_net_scores.append(dv - dw)

            tasks_avail = day_res.get("tasks_available", [])
            tasks_comp  = day_res.get("task_completion", {})
            for tsk in tasks_avail:
                task_stats[tsk][0] += 1
                if tasks_comp.get(tsk, False):
                    task_stats[tsk][1] += 1

        # 4) 整局模拟
        full_res   = data.get("full_run_result", {})
        origin_res = full_res.get("origin_result", {})
        sim_res    = full_res.get("simulation_result", {})

        # 如果 full_res 或 sim_res 存在 => 表示有一次完整模拟
        if full_res or sim_res:
            full_count += 1

            # origin_result 中的 process_scores
            proc_scores = sim_res.get("process_scores", {})
            vill_score  = proc_scores.get("villager", {}).get("total", 0.0)
            wolf_score  = proc_scores.get("werewolf", {}).get("total", 0.0)

            full_villager_scores.append(vill_score)
            full_net_scores.append(vill_score - wolf_score)

            result_score = sim_res.get("result_score", 0.0)
            full_result_scores.append(result_score)

            # 模拟结果
            final_game_result = sim_res.get("game_result", "")

            if final_game_result == "Villagers win":
                villager_win_count += 1

            # 4.1) 原始 & 模拟翻盘情况
            if original_win == "Werewolves win":
                original_wolf_count += 1
                if final_game_result == "Villagers win":
                    wolf_to_villager_win += 1

            if original_win == "Villagers win":
                original_vill_count += 1
                if final_game_result == "Werewolves win":
                    vill_to_werewolf_win += 1

    # ========== 计算统计指标 ==========

    def safe_mean(arr):
        return round(sum(arr)/len(arr), 4) if arr else 0.0

    # 单日
    avg_day_completion_ratio = safe_mean(day_completion_ratios)
    avg_day_villager_score   = safe_mean(day_villager_scores)
    avg_day_werewolf_score   = safe_mean(day_werewolf_scores)
    avg_day_net_score        = safe_mean(day_net_scores)

    # 整局
    avg_full_villager_score = safe_mean(full_villager_scores)
    avg_full_net_score      = safe_mean(full_net_scores)
    avg_full_result_score   = safe_mean(full_result_scores)

    # 任务出现 / 完成率
    task_completion_summary = {}
    for tsk_name, (appear, comp) in task_stats.items():
        ratio = comp / appear if appear > 0 else 0.0
        task_completion_summary[tsk_name] = {
            "appear_count": appear,
            "complete_count": comp,
            "completion_ratio": round(ratio, 4)
        }

    # 模拟村民胜率
    villager_win_ratio = 0.0
    if full_count > 0:
        villager_win_ratio = round(villager_win_count / full_count, 4)

    # 原始狼赢→村民赢
    wolf_to_villager_ratio = 0.0
    if original_wolf_count > 0:
        wolf_to_villager_ratio = round(wolf_to_villager_win / original_wolf_count, 4)

    # 原始村赢→狼人赢
    vill_to_werewolf_ratio = 0.0
    if original_vill_count > 0:
        vill_to_werewolf_ratio = round(vill_to_werewolf_win / original_vill_count, 4)

    # ========== 新增原始胜率(村民/狼人) ==========

    # 既然 full_count 代表有效整局数，则
    # original_villager_win_ratio = original_vill_count / full_count
    # original_werewolf_win_ratio= original_wolf_count / full_count
    # 若 full_count==0 就保持 0
    original_villager_win_ratio = 0.0
    original_werewolf_win_ratio = 0.0
    if full_count > 0:
        original_villager_win_ratio = round(original_vill_count / full_count, 4)
        original_werewolf_win_ratio = round(original_wolf_count / full_count, 4)

    # ========== 画原有每场数据的柱状图 (7 张) ==========

    # 1) 单日任务完成率
    plt.figure()
    plt.bar(range(len(day_completion_ratios)), day_completion_ratios, color='blue', alpha=0.7)
    plt.title(f"Single-day Task Completion Ratio ({model_short_name})")
    plt.xlabel("Single-day simulation index")
    plt.ylabel("Completion Ratio")
    plt.ylim(0,1.1)
    plt.savefig(os.path.join(charts_dir, f"{model_short_name}_day_completion_ratio.png"))
    plt.close()

    # 2) 单日村民得分
    plt.figure()
    plt.bar(range(len(day_villager_scores)), day_villager_scores, color='green', alpha=0.7)
    plt.title(f"Single-day Villager Scores ({model_short_name})")
    plt.xlabel("Single-day simulation index")
    plt.ylabel("Villager Score")
    plt.savefig(os.path.join(charts_dir, f"{model_short_name}_day_villager_score.png"))
    plt.close()

    # 3) 单日狼人得分
    plt.figure()
    plt.bar(range(len(day_werewolf_scores)), day_werewolf_scores, color='red', alpha=0.7)
    plt.title(f"Single-day Werewolf Scores ({model_short_name})")
    plt.xlabel("Single-day simulation index")
    plt.ylabel("Werewolf Score")
    plt.savefig(os.path.join(charts_dir, f"{model_short_name}_day_werewolf_score.png"))
    plt.close()

    # 4) 单日村民净得分
    plt.figure()
    plt.bar(range(len(day_net_scores)), day_net_scores, color='purple', alpha=0.7)
    plt.title(f"Single-day Villager Net Scores ({model_short_name})")
    plt.xlabel("Single-day simulation index")
    plt.ylabel("Net Score (V - W)")
    plt.savefig(os.path.join(charts_dir, f"{model_short_name}_day_net_score.png"))
    plt.close()

    # 5) 整局: Villager process score
    plt.figure()
    plt.bar(range(len(full_villager_scores)), full_villager_scores, color='green', alpha=0.7)
    plt.title(f"Full-run Villager Process Scores ({model_short_name})")
    plt.xlabel("Full-run index")
    plt.ylabel("Villager Process Score")
    plt.savefig(os.path.join(charts_dir, f"{model_short_name}_full_villager_score.png"))
    plt.close()

    # 6) 整局: Net process score
    plt.figure()
    plt.bar(range(len(full_net_scores)), full_net_scores, color='purple', alpha=0.7)
    plt.title(f"Full-run Villager Net Process Scores ({model_short_name})")
    plt.xlabel("Full-run index")
    plt.ylabel("Villager Net Score (V - W)")
    plt.savefig(os.path.join(charts_dir, f"{model_short_name}_full_net_score.png"))
    plt.close()

    # 7) 整局: result_score
    plt.figure()
    plt.bar(range(len(full_result_scores)), full_result_scores, color='blue', alpha=0.7)
    plt.title(f"Full-run Result Scores ({model_short_name})")
    plt.xlabel("Full-run index")
    plt.ylabel("Result Score")
    plt.savefig(os.path.join(charts_dir, f"{model_short_name}_full_result_score.png"))
    plt.close()

    # ========== 再额外生成分布图（Histogram），以展示数据分布 (7 张) ==========

    def plot_hist(data_list, title, color, outfile, bins=10):
        plt.figure()
        plt.hist(data_list, bins=bins, color=color, alpha=0.7)
        plt.title(title)
        plt.xlabel("Value")
        plt.ylabel("Frequency")
        plt.savefig(outfile)
        plt.close()

    # 1) 单日任务完成率分布
    if day_completion_ratios:
        plot_hist(day_completion_ratios,
                  f"Distribution of Single-day Task Completion Ratio ({model_short_name})",
                  'blue',
                  os.path.join(charts_dir, f"{model_short_name}_hist_day_completion_ratio.png"))

    # 2) 单日村民得分分布
    if day_villager_scores:
        plot_hist(day_villager_scores,
                  f"Distribution of Single-day Villager Scores ({model_short_name})",
                  'green',
                  os.path.join(charts_dir, f"{model_short_name}_hist_day_villager_score.png"))

    # 3) 单日狼人得分分布
    if day_werewolf_scores:
        plot_hist(day_werewolf_scores,
                  f"Distribution of Single-day Werewolf Scores ({model_short_name})",
                  'red',
                  os.path.join(charts_dir, f"{model_short_name}_hist_day_werewolf_score.png"))

    # 4) 单日村民净得分分布
    if day_net_scores:
        plot_hist(day_net_scores,
                  f"Distribution of Single-day Villager Net Scores ({model_short_name})",
                  'purple',
                  os.path.join(charts_dir, f"{model_short_name}_hist_day_net_score.png"))

    # 5) 整局: Villager Process Score 分布
    if full_villager_scores:
        plot_hist(full_villager_scores,
                  f"Distribution of Full-run Villager Process Scores ({model_short_name})",
                  'green',
                  os.path.join(charts_dir, f"{model_short_name}_hist_full_villager_score.png"))

    # 6) 整局: Net Process Score 分布
    if full_net_scores:
        plot_hist(full_net_scores,
                  f"Distribution of Full-run Villager Net Scores ({model_short_name})",
                  'purple',
                  os.path.join(charts_dir, f"{model_short_name}_hist_full_net_score.png"))

    # 7) 整局: result_score 分布
    if full_result_scores:
        plot_hist(full_result_scores,
                  f"Distribution of Full-run result_score ({model_short_name})",
                  'blue',
                  os.path.join(charts_dir, f"{model_short_name}_hist_full_result_score.png"))

    # ========== 汇总 JSON ==========

    summary_data = {
        "model": model_short_name,
        "counts": {
            "num_single_day_records": len(day_completion_ratios),
            "num_full_run_records": full_count
        },
        "single_day_stats": {
            "completion_ratio": {
                "values": day_completion_ratios,
                "mean": avg_day_completion_ratio
            },
            "villager_score": {
                "values": day_villager_scores,
                "mean": avg_day_villager_score
            },
            "werewolf_score": {
                "values": day_werewolf_scores,
                "mean": avg_day_werewolf_score
            },
            "villager_net_score": {
                "values": day_net_scores,
                "mean": avg_day_net_score
            }
        },
        "full_run_stats": {
            "villager_score": {
                "values": full_villager_scores,
                "mean": avg_full_villager_score
            },
            "net_score": {
                "values": full_net_scores,
                "mean": avg_full_net_score
            },
            "result_score": {
                "values": full_result_scores,
                "mean": avg_full_result_score
            }
        },
        "task_completion_stats": task_completion_summary,
        "full_run_ratios": {
            "villager_win_ratio": villager_win_ratio,
            "werewolvesWin_to_villagersWin_ratio": wolf_to_villager_ratio,
            "villagersWin_to_werewolvesWin_ratio": vill_to_werewolf_ratio,
            # 新增 "原始村民/狼人胜率"
            "original_villager_win_ratio": original_villager_win_ratio,
            "original_werewolf_win_ratio": original_werewolf_win_ratio
        }
    }

    out_json_path = os.path.join(output_dir, f"analysis_{model_short_name}.json")
    with open(out_json_path, "w", encoding="utf-8") as jf:
        json.dump(summary_data, jf, ensure_ascii=False, indent=2)

    print(f"[INFO] 统计完成, 结果写入 => {out_json_path}")
    print(f"[INFO] 图表保存于 => {charts_dir}")


if __name__ == "__main__":
    MODEL_MAP = {
        "gpt-4o": "4o",
        "gpt-4o-mini": "4o-mini",
        "gpt-3.5-turbo": "gpt-35",
        "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo": "llama31-8B",
        "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo": "llama31-70B",
        "meta-llama/Llama-3.3-70B-Instruct-Turbo": "llama33-70B"
    }
    # 示例：手动指定模型名、输入文件夹、输出文件夹
    '''
    
    
    model_short = "gpt-35"
    input_dir   = "werewolf_result"    # JSON 结果文件所在目录
    output_dir  = "werewolf_data/gpt35"   # 统计与图表输出目录
    model_short = "llama33-70B"
    input_dir   = "werewolf_result"    # JSON 结果文件所在目录
    output_dir  = "werewolf_data/llama33"   # 统计与图表输出目录
    model_short = "llama31-8B"
    input_dir   = "werewolf_result"    # JSON 结果文件所在目录
    output_dir  = "werewolf_data/llama31_8b"   # 统计与图表输出目录
    model_short = "llama31-70B"
    input_dir   = "werewolf_result"    # JSON 结果文件所在目录
    output_dir  = "werewolf_data/llama31_70b"   # 统计与图表输出目录
    
    model_short = "4o-mini"
    input_dir   = "werewolf_result"    # JSON 结果文件所在目录
    output_dir  = "werewolf_data/4omini"   # 统计与图表输出目录
    '''
    
    
    model_short = "4o"
    input_dir   = "werewolf_result"    # JSON 结果文件所在目录
    output_dir  = "werewolf_data/4o"   # 统计与图表输出目录
    analyze_model_files(model_short, input_dir, output_dir)
