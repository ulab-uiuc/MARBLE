import os
import re
import sys
import time
import json
from typing import List, Dict, Any, Optional
import openai
from openai import OpenAI
import yaml
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from marble.environments.werewolf_env import WerewolfEnv


class WerewolfEvaluator:
    """
    A class to evaluate a single game snapshot directory.
    1) It loads every night checkpoint (e.g., checkpoint_Night1.json) 
       and simulates exactly one cycle per checkpoint (simulate_one_cycle=True).
    2) After finishing all 'per-night' simulations, it performs a full-run 
       from the earliest night checkpoint to the end (simulate_one_cycle=False).
    3) Stores logs in subfolders under 'werewolf_log' as needed.
    """

    def __init__(self, snapshot_folder: str, config_dir: str, base_log_dir: str = "werewolf_log"):
        """
        Args:
            snapshot_folder (str): The folder that contains multiple checkpoint_NightX.json 
                                   (or DayX) files from the same game snapshot.
            config_dir (str): The YAML config file path that contains 'eval_config' etc.
            base_log_dir (str): The top-level directory under which new logs will be created.
        """
        self.snapshot_folder = snapshot_folder
        self.base_log_dir = base_log_dir
        self.config_dir = config_dir

        # 用来保存每一夜模拟后的结果
        self.night_cycle_results: List[Dict[str, Any]] = []

        # 用来保存整局模拟的结果
        self.full_run_result: Dict[str, Any] = {}

        if not os.path.exists(config_dir):
            raise FileNotFoundError(f"Config file not found at: {config_dir}")

        with open(config_dir, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)  # 假设使用 YAML 存放配置

        eval_config = config.get("eval_config", {})

        # 获取 API 的基本配置
        self.base_url = eval_config.get("base_url", "https://api.openai.com/v1")
        self.api_key = eval_config.get("api_key", "")
        self.model_name = eval_config.get("model_name", "gpt-4o")

        # 设置 openai 客户端的参数
        openai.api_base = self.base_url
        openai.api_key = self.api_key

        # 为本次评估专门创建一个子文件夹
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        self.evaluator_dir = os.path.join(self.base_log_dir, f"eval_{timestamp}")
        os.makedirs(self.evaluator_dir, exist_ok=True)

        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )

    def find_checkpoint_files(self, pattern="night") -> List[str]:
        """
        在 self.snapshot_folder 中查找并返回所有符合 'checkpoint_Night(\d+).json' 
        或 'checkpoint_Day(\d+).json' 的文件路径列表，按数字顺序排列。
        """
        if not os.path.isdir(self.snapshot_folder):
            raise NotADirectoryError(f"Snapshot folder not found: {self.snapshot_folder}")

        pattern_night = re.compile(r'^checkpoint_Night(\d+)\.json$', re.IGNORECASE)
        pattern_day = re.compile(r'^checkpoint_Day(\d+)\.json$', re.IGNORECASE)

        all_files = os.listdir(self.snapshot_folder)
        matched = []

        for f in all_files:
            night_match = pattern_night.match(f)
            # 判断 pattern == "night" 或 "all" 时才加入
            if night_match and (pattern in ["night", "all"]):
                matched.append((int(night_match.group(1)), "night", f))
                continue

            day_match = pattern_day.match(f)
            # 判断 pattern == "day" 或 "all" 时才加入
            if day_match and (pattern in ["day", "all"]):
                matched.append((int(day_match.group(1)), "day", f))
                continue

        # 排序：先按数字升序，再按 day/night 顺序
        matched.sort(key=lambda x: (x[0], x[1]))
        # 返回绝对路径
        return [os.path.join(self.snapshot_folder, x[2]) for x in matched]

    def evaluate_all_nights(self):
        """
        主调函数:
        1) 找到所有 checkpoint_*.json 文件, 逐个执行 'simulate_one_cycle=True'。
        2) 保存单日/单夜模拟结果到 self.night_cycle_results。
        3) 最后调用 simulate_full_game_run() 执行整局模拟。
        4) 在 self.evaluator_dir 下写入 final_result.json。
        """
        checkpoint_files = self.find_checkpoint_files()
        if not checkpoint_files:
            print(f"[SnapshotEvaluator] No checkpoint files found in {self.snapshot_folder}.")
            return

        print(f"[SnapshotEvaluator] Found {len(checkpoint_files)} checkpoint(s). Now evaluating per-night cycles...")

        # 逐个checkpoint文件做单次模拟
        for ckpt_file in checkpoint_files:
            single_result = self.evaluate_single_checkpoint(ckpt_file)
            if single_result:
                self.night_cycle_results.append(single_result)

        # 等所有夜晚模拟完成后，再来一次全局模拟
        first_night_path = None
        for ckpt_file in checkpoint_files:
            if "checkpoint_Night1.json" in ckpt_file:
                first_night_path = ckpt_file
                break

        if first_night_path:
            # 这里让 simulate_full_game_run 返回 (结果, env)
            full_run_info, final_env = self.simulate_full_game_run(first_night_path)
            self.full_run_result = full_run_info

            # 在整局模拟结束后，用 env 来做村民阵营整体的绩效打分
            if final_env is not None:
                performance_scores = self.evaluate_villager_merged_performance(final_env)
                self.full_run_result["villagers_performance"] = performance_scores
        else:
            print("[SnapshotEvaluator] No 'Night1' checkpoint found, skip full-run simulation.")

        # 组合最终结果并写入 final_result.json
        final_info = {
            "per_cycle_results": self.night_cycle_results,
            "full_run_result": self.full_run_result
        }
        final_json_path = os.path.join(self.evaluator_dir, "final_result.json")
        with open(final_json_path, "w", encoding="utf-8") as f:
            json.dump(final_info, f, indent=4, ensure_ascii=False)

        print(f"[SnapshotEvaluator] Evaluation done. final_result.json saved at {final_json_path}")

    def evaluate_single_checkpoint(self, ckpt_path: str) -> Optional[Dict[str, Any]]:
        """
        针对单个 checkpoint 文件执行一次"simulate_one_cycle=True"的夜晚或白天模拟
        """
        if not os.path.exists(ckpt_path):
            print(f"[evaluate_single_checkpoint] File not found: {ckpt_path}")
            return None

        base_name = os.path.splitext(os.path.basename(ckpt_path))[0]
        timestamp_str = time.strftime("%Y%m%d_%H%M%S")
        subfolder_name = f"{base_name}_run_{timestamp_str}"
        run_dir = os.path.join(self.evaluator_dir, subfolder_name)
        os.makedirs(run_dir, exist_ok=True)

        try:
            env = WerewolfEnv.load_from_file(
                file_path=ckpt_path,
                log_dir=run_dir,
                override_config_path=self.config_dir  # <-- 新增这个
            )
            print(f"[evaluate_single_checkpoint] Loaded env from {ckpt_path}, logs in {run_dir}")
        except Exception as e:
            print(f"[evaluate_single_checkpoint] Error loading env: {e}")
            return None

        try:
            game_result = env.continue_game(simulate_one_cycle=True)
            return {
                "ckpt_path": ckpt_path,
                "logs_folder": run_dir,
                "simulate_one_cycle": True,
                "result": game_result
            }
        except Exception as e:
            print(f"[evaluate_single_checkpoint] Error in continue_game: {e}")
            return None

    def simulate_full_game_run(self, ckpt_path: str):
        """
        从指定的(通常是 Night1) checkpoint 载入并执行 "simulate_one_cycle=False"，即整局模拟到结束。
        返回 (game_result, env) 方便外部继续使用 env。
        """
        base_name = os.path.splitext(os.path.basename(ckpt_path))[0]
        timestamp_str = time.strftime("%Y%m%d_%H%M%S")
        subfolder_name = f"fullrun_from_{base_name}_{timestamp_str}"
        run_dir = os.path.join(self.evaluator_dir, subfolder_name)
        os.makedirs(run_dir, exist_ok=True)

        try:
            env = WerewolfEnv.load_from_file(
                file_path=ckpt_path,
                log_dir=run_dir,
                override_config_path=self.config_dir  # <-- 新增这个
            )
            print(f"[simulate_full_game_run] Loaded env from {ckpt_path}, logs in {run_dir}")
        except Exception as e:
            print(f"[simulate_full_game_run] Error loading env: {e}")
            return ({"error": str(e)}, None)

        try:
            game_result = env.continue_game(simulate_one_cycle=False)
            print("[simulate_full_game_run] The game ended with result:", game_result)
            return (
                {
                    "start_ckpt": ckpt_path,
                    "logs_folder": run_dir,
                    "simulate_one_cycle": False,
                    "result": game_result
                },
                env
            )
        except Exception as e:
            print(f"[simulate_full_game_run] Error in continue_game: {e}")
            return ({"error": str(e)}, env)

    def gpt_tool_call(self, messages, tools):
        """
        调用 GPT 模型和指定的工具
        """
        rounds = 0
        while True:
            rounds += 1
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    tools=tools,
                    tool_choice="required",
                    temperature=1.0,
                    n=1,
                )
                tool_calls = response.choices[0].message.tool_calls
                return tool_calls
            except Exception as e:
                print(f"Chat Generation Error: {e}")
                time.sleep(5)
                if rounds > 3:
                    raise Exception("Chat Completion failed too many times")

    def evaluate_villager_merged_performance(self, env: WerewolfEnv) -> Dict[str, Any]:
        """
        使用“七维度合并”模型对村民方的表现进行综合评估。
        包含以下维度：
        1) info_effectiveness_score (10%)
        2) collaboration_limiting_score (20%)
        3) logic_and_reasoning_score (10%)
        4) leadership_and_sheriff_score (20%)
        5) voting_eliminations_score (10%)
        6) protect_key_players_score (10%)
        7) result_orientation_score (20%)

        调用 GPT 工具 'villager_combined_evaluation' 并解析输出，然后计算加权总分。
        """

        shared_memory = env.shared_memory
        # 1) 获取日志
        full_log_text = shared_memory.get("private_event_log", "")
        if not isinstance(full_log_text, str):
            full_log_text = json.dumps(full_log_text, ensure_ascii=False, indent=2)

        # 2) 加载包含七维度Prompt/Tools的 YAML
        #    你需要提前准备好 'villager_combined_evaluation.yaml' (或其他文件名)
        #    其中包含 "system"、"user"、"tools"，以及 function: "villager_combined_evaluation"
        combined_yaml_file = "prompts/villager_combined_evaluation.yaml"
        if not os.path.exists(combined_yaml_file):
            print(f"[evaluate_villager_merged_performance] YAML not found: {combined_yaml_file}")
            return {}

        with open(combined_yaml_file, "r", encoding="utf-8") as f:
            tool_data = yaml.safe_load(f)

        system_prompt = tool_data.get("system", "")
        user_prompt = tool_data.get("user", "")
        tools = tool_data.get("tools", [])

        # 将日志替换到 user_prompt 的占位符
        user_prompt_filled = user_prompt.replace("<<game_log>>", full_log_text)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt_filled},
        ]

        # 3) 调用 gpt_tool_call()
        try:
            tool_calls = self.gpt_tool_call(messages, tools)
        except Exception as e:
            print(f"[evaluate_villager_merged_performance] GPT call error: {e}")
            return {}

        if not tool_calls:
            print("[evaluate_villager_merged_performance] No tool calls from GPT.")
            return {}

        first_call = tool_calls[0]
        arguments_json = first_call.function.arguments

        # 4) 解析 GPT 返回的 JSON
        try:
            eval_result = json.loads(arguments_json)
        except json.JSONDecodeError as e:
            print(f"[evaluate_villager_merged_performance] JSON decode error: {e}")
            return {}

        # 5) 依次获取七个维度的 score
        info_score = eval_result.get("info_effectiveness_score", 0)
        collab_limiting_score = eval_result.get("collaboration_limiting_score", 0)
        logic_score = eval_result.get("logic_and_reasoning_score", 0)
        leader_sheriff_score = eval_result.get("leadership_and_sheriff_score", 0)
        voting_score = eval_result.get("voting_eliminations_score", 0)
        protect_score = eval_result.get("protect_key_players_score", 0)
        result_score = eval_result.get("result_orientation_score", 0)

        # 6) 根据要求计算加权总分
        #    collaboration_limiting_score, leadership_and_sheriff_score, result_orientation_score 各20%
        #    其余 info_score, logic_score, voting_score, protect_score 各10%
        weighted_overall = (
            info_score * 0.10 +
            collab_limiting_score * 0.20 +
            logic_score * 0.10 +
            leader_sheriff_score * 0.20 +
            voting_score * 0.10 +
            protect_score * 0.10 +
            result_score * 0.20
        )

        # 7) 组装返回结构（含详细文本）
        merged_performance = {
            # 各维度分
            "info_effectiveness_score": info_score,
            "collaboration_limiting_score": collab_limiting_score,
            "logic_and_reasoning_score": logic_score,
            "leadership_and_sheriff_score": leader_sheriff_score,
            "voting_eliminations_score": voting_score,
            "protect_key_players_score": protect_score,
            "result_orientation_score": result_score,
            
            # 各维度的详细说明（GPT 可能会返回长文本）
            "info_effectiveness_detail": eval_result.get("info_effectiveness", ""),
            "collaboration_limiting_detail": eval_result.get("collaboration_limiting", ""),
            "logic_and_reasoning_detail": eval_result.get("logic_and_reasoning", ""),
            "leadership_and_sheriff_detail": eval_result.get("leadership_and_sheriff", ""),
            "voting_eliminations_detail": eval_result.get("voting_eliminations", ""),
            "protect_key_players_detail": eval_result.get("protect_key_players", ""),
            "result_orientation_detail": eval_result.get("result_orientation", ""),

            # 加权总分
            "weighted_overall_score": weighted_overall
        }

        return merged_performance
    

    
    def evaluate_multiple_snapshots(self, top_level_dir: str):
        """
        遍历 top_level_dir 中的所有子文件夹（每个子文件夹对应一局游戏的快照），
        并对每个子文件夹调用 evaluate_all_nights() 进行评估。
        
        每完成一个子文件夹的评估，就将该局的七个细分评分和总分追加到 self.batch_evaluation_results，
        并将进度保存到 "batch_evaluation_progress.json" 防止中途崩溃数据丢失。

        在全部子文件夹都评估完后，输出每个维度的分数分布和平均分，总分分布和平均分，
        写入 "batch_evaluation_summary.json"。
        """

        if not os.path.isdir(top_level_dir):
            print(f"[evaluate_multiple_snapshots] {top_level_dir} is not a directory.")
            return

        # 存储所有子文件夹的评分结果，结构示例：
        # [
        #   {
        #       "folder": "game_20250108_083807_Villagers_win",
        #       "info_effectiveness_score": 4,
        #       "collaboration_limiting_score": 5,
        #       ...
        #       "weighted_overall_score": 4.3
        #   },
        #   { ... },
        #   ...
        # ]
        self.batch_evaluation_results: List[Dict[str, Any]] = []

        # 先找出 top_level_dir 下的所有子文件夹，假设其中每个子文件夹就对应一个“快照存档”
        subfolders = [
            d for d in os.listdir(top_level_dir)
            if os.path.isdir(os.path.join(top_level_dir, d))
        ]
        if not subfolders:
            print(f"[evaluate_multiple_snapshots] No subfolders found in {top_level_dir}.")
            return

        # 逐个子文件夹进行评估
        for idx, folder_name in enumerate(subfolders, start=1):
            snapshot_path = os.path.join(top_level_dir, folder_name)
            print(f"\n=== Evaluating folder {idx}/{len(subfolders)}: {snapshot_path} ===")

            # 每个子文件夹都可以用一个新的 WerewolfEvaluator 实例去跑
            # 或者你也可重用同一个对象并切换 snapshot_folder，但需注意路径等。
            sub_evaluator = WerewolfEvaluator(
                snapshot_folder=snapshot_path,
                config_dir=os.path.join(os.path.dirname(self.snapshot_folder), self.config_dir),
                base_log_dir=self.base_log_dir
            )

            # 调用 evaluate_all_nights()，它会生成 final_result.json 并在 sub_evaluator.full_run_result 中留存结果
            sub_evaluator.evaluate_all_nights()

            # 提取合并后的评分
            # 注意：在 evaluate_all_nights() 完成后，最终结果会存储在 sub_evaluator.full_run_result["villagers_performance"]
            merged_perf = sub_evaluator.full_run_result.get("villagers_performance", {})

            # 把这局的评分记录下来
            # 这里可以把七个明细 + overall_score 全部放进一个dict
            record = {
                "folder": folder_name,  # 方便追溯
                "info_effectiveness_score": merged_perf.get("info_effectiveness_score", 0),
                "collaboration_limiting_score": merged_perf.get("collaboration_limiting_score", 0),
                "logic_and_reasoning_score": merged_perf.get("logic_and_reasoning_score", 0),
                "leadership_and_sheriff_score": merged_perf.get("leadership_and_sheriff_score", 0),
                "voting_eliminations_score": merged_perf.get("voting_eliminations_score", 0),
                "protect_key_players_score": merged_perf.get("protect_key_players_score", 0),
                "result_orientation_score": merged_perf.get("result_orientation_score", 0),
                "weighted_overall_score": merged_perf.get("weighted_overall_score", 0),
            }
            self.batch_evaluation_results.append(record)

            # 为防止中途崩溃丢失结果，这里立即写一个进度文件
            progress_path = os.path.join(self.evaluator_dir, "batch_evaluation_progress.json")
            with open(progress_path, "w", encoding="utf-8") as f:
                json.dump(self.batch_evaluation_results, f, indent=4, ensure_ascii=False)

        # 全部子文件夹评估完成后，统计各维度的分布和平均值
        dimension_keys = [
            "info_effectiveness_score",
            "collaboration_limiting_score",
            "logic_and_reasoning_score",
            "leadership_and_sheriff_score",
            "voting_eliminations_score",
            "protect_key_players_score",
            "result_orientation_score",
            "weighted_overall_score",
        ]

        # 收集分布
        dimension_distributions = {k: [] for k in dimension_keys}
        for item in self.batch_evaluation_results:
            for k in dimension_keys:
                dimension_distributions[k].append(item.get(k, 0))

        # 计算平均分
        dimension_averages = {}
        for k in dimension_keys:
            values = dimension_distributions[k]
            if values:
                avg = sum(values) / len(values)
            else:
                avg = 0
            dimension_averages[k] = avg

        # 组装一个 summary
        summary = {
            "count_of_snapshots": len(self.batch_evaluation_results),
            "dimension_distributions": dimension_distributions,
            "dimension_averages": dimension_averages
        }

        # 写入最终汇总文件
        summary_path = os.path.join(self.evaluator_dir, "batch_evaluation_summary.json")
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=4, ensure_ascii=False)

        print("\n[evaluate_multiple_snapshots] All subfolders evaluated.")
        print(f"Batch summary saved to: {summary_path}")
        print(f"Progress details saved to: {progress_path}")

if __name__ == "__main__":
    top_level_dir = "werewolf_log"
    config_path = r"marble\configs\test_config\werewolf_config_llama31_70b.yaml"

    # 这时 snapshot_folder 给一个占位值即可，不会真正使用到，因为 evaluate_multiple_snapshots() 会替换
    evaluator = WerewolfEvaluator(snapshot_folder="placeholder", config_dir=config_path, base_log_dir="werewolf_eval/llama31_70b")
    evaluator.evaluate_multiple_snapshots(top_level_dir)
