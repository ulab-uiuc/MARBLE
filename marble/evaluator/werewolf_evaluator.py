import os
import re
import sys
import time
import json
import argparse
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

        self.night_cycle_results: List[Dict[str, Any]] = []

        self.full_run_result: Dict[str, Any] = {}

        if not os.path.exists(config_dir):
            raise FileNotFoundError(f"Config file not found at: {config_dir}")

        with open(config_dir, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)  # Assuming YAML is used for configuration

        eval_config = config.get("eval_config", {})

        self.base_url = eval_config.get("base_url", "https://api.openai.com/v1")
        self.api_key = eval_config.get("api_key", "")
        self.model_name = eval_config.get("model_name", "gpt-4o")

        openai.api_base = self.base_url
        openai.api_key = self.api_key

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        self.evaluator_dir = os.path.join(self.base_log_dir, f"eval_{timestamp}")
        os.makedirs(self.evaluator_dir, exist_ok=True)

        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )

    def find_checkpoint_files(self, pattern="night") -> List[str]:
        """
        Search for and return all files matching 'checkpoint_Night(\d+).json' 
        or 'checkpoint_Day(\d+).json' in self.snapshot_folder, sorted numerically.
        """
        if not os.path.isdir(self.snapshot_folder):
            raise NotADirectoryError(f"Snapshot folder not found: {self.snapshot_folder}")

        pattern_night = re.compile(r'^checkpoint_Night(\d+)\.json$', re.IGNORECASE)
        pattern_day = re.compile(r'^checkpoint_Day(\d+)\.json$', re.IGNORECASE)

        all_files = os.listdir(self.snapshot_folder)
        matched = []

        for f in all_files:
            night_match = pattern_night.match(f)
            # Add only when pattern == "night" or "all"
            if night_match and (pattern in ["night", "all"]):
                matched.append((int(night_match.group(1)), "night", f))
                continue

            day_match = pattern_day.match(f)
            # Add only when pattern == "day" or "all"
            if day_match and (pattern in ["day", "all"]):
                matched.append((int(day_match.group(1)), "day", f))
                continue

        # Sort by number and then by day/night order
        matched.sort(key=lambda x: (x[0], x[1]))
        # Return absolute paths
        return [os.path.join(self.snapshot_folder, x[2]) for x in matched]

    def evaluate_all_nights(self):
        """
        Main function:
        1) Find all checkpoint_*.json files, and simulate each one with 'simulate_one_cycle=True'.
        2) Save per-night simulation results to self.night_cycle_results.
        3) After all night simulations are done, run the full simulation from the first night checkpoint.
        4) Write the final result to 'final_result.json' in self.evaluator_dir.
        """
        checkpoint_files = self.find_checkpoint_files()
        if not checkpoint_files:
            print(f"[SnapshotEvaluator] No checkpoint files found in {self.snapshot_folder}.")
            return

        print(f"[SnapshotEvaluator] Found {len(checkpoint_files)} checkpoint(s). Now evaluating per-night cycles...")

        # Simulate each checkpoint file one by one
        for ckpt_file in checkpoint_files:
            single_result = self.evaluate_single_checkpoint(ckpt_file)
            if single_result:
                self.night_cycle_results.append(single_result)

        # After all night simulations, perform a full-run simulation
        first_night_path = None
        for ckpt_file in checkpoint_files:
            if "checkpoint_Night1.json" in ckpt_file:
                first_night_path = ckpt_file
                break

        if first_night_path:
            # Return (result, env) from simulate_full_game_run
            full_run_info, final_env = self.simulate_full_game_run(first_night_path)
            self.full_run_result = full_run_info

            # After the full run ends, use env to evaluate the performance of the Villagers
            if final_env is not None:
                performance_scores = self.evaluate_villager_merged_performance(final_env)
                self.full_run_result["villagers_performance"] = performance_scores
        else:
            print("[SnapshotEvaluator] No 'Night1' checkpoint found, skip full-run simulation.")

        # Combine final results and write to final_result.json
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
        Simulate a single night or day cycle with 'simulate_one_cycle=True' for a given checkpoint file.
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
                override_config_path=self.config_dir  # <-- Added this
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
        Load the specified checkpoint (usually Night1) and perform a full simulation to the game end.
        Returns (game_result, env) for further use with env.
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
                override_config_path=self.config_dir  # <-- Added this
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
        Call the GPT model with specified tools.
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
        Use the "seven dimensions merged" model to evaluate the performance of the Villagers.
        It includes the following dimensions:
        1) info_effectiveness_score (10%)
        2) collaboration_limiting_score (20%)
        3) logic_and_reasoning_score (10%)
        4) leadership_and_sheriff_score (20%)
        5) voting_eliminations_score (10%)
        6) protect_key_players_score (10%)
        7) result_orientation_score (20%)

        Call GPT tool 'villager_combined_evaluation' and parse the output to calculate the weighted total score.
        """

        shared_memory = env.shared_memory
        # 1) Get logs
        full_log_text = shared_memory.get("private_event_log", "")
        if not isinstance(full_log_text, str):
            full_log_text = json.dumps(full_log_text, ensure_ascii=False, indent=2)

        # 2) Load the YAML with the seven dimensions prompts/tools
        #    You need to prepare 'villager_combined_evaluation.yaml' (or other file names)
        #    containing "system", "user", "tools", and function: "villager_combined_evaluation"
        combined_yaml_file = "prompts/villager_combined_evaluation.yaml"
        if not os.path.exists(combined_yaml_file):
            print(f"[evaluate_villager_merged_performance] YAML not found: {combined_yaml_file}")
            return {}

        with open(combined_yaml_file, "r", encoding="utf-8") as f:
            tool_data = yaml.safe_load(f)

        system_prompt = tool_data.get("system", "")
        user_prompt = tool_data.get("user", "")
        tools = tool_data.get("tools", [])

        # Replace logs in user_prompt placeholder
        user_prompt_filled = user_prompt.replace("<<game_log>>", full_log_text)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt_filled},
        ]

        # 3) Call gpt_tool_call()
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

        # 4) Parse the JSON returned by GPT
        try:
            eval_result = json.loads(arguments_json)
        except json.JSONDecodeError as e:
            print(f"[evaluate_villager_merged_performance] JSON decode error: {e}")
            return {}

        # 5) Retrieve the seven dimension scores
        info_score = eval_result.get("info_effectiveness_score", 0)
        collab_limiting_score = eval_result.get("collaboration_limiting_score", 0)
        logic_score = eval_result.get("logic_and_reasoning_score", 0)
        leader_sheriff_score = eval_result.get("leadership_and_sheriff_score", 0)
        voting_score = eval_result.get("voting_eliminations_score", 0)
        protect_score = eval_result.get("protect_key_players_score", 0)
        result_score = eval_result.get("result_orientation_score", 0)

        # 6) Calculate the weighted overall score
        weighted_overall = (
            info_score * 0.10 +
            collab_limiting_score * 0.20 +
            logic_score * 0.10 +
            leader_sheriff_score * 0.20 +
            voting_score * 0.10 +
            protect_score * 0.10 +
            result_score * 0.20
        )

        # 7) Return the merged performance with detailed explanation
        merged_performance = {
            # Scores for each dimension
            "info_effectiveness_score": info_score,
            "collaboration_limiting_score": collab_limiting_score,
            "logic_and_reasoning_score": logic_score,
            "leadership_and_sheriff_score": leader_sheriff_score,
            "voting_eliminations_score": voting_score,
            "protect_key_players_score": protect_score,
            "result_orientation_score": result_score,
            
            # Detailed explanation for each dimension (GPT might return long texts)
            "info_effectiveness_detail": eval_result.get("info_effectiveness", ""),
            "collaboration_limiting_detail": eval_result.get("collaboration_limiting", ""),
            "logic_and_reasoning_detail": eval_result.get("logic_and_reasoning", ""),
            "leadership_and_sheriff_detail": eval_result.get("leadership_and_sheriff", ""),
            "voting_eliminations_detail": eval_result.get("voting_eliminations", ""),
            "protect_key_players_detail": eval_result.get("protect_key_players", ""),
            "result_orientation_detail": eval_result.get("result_orientation", ""),

            # Weighted overall score
            "weighted_overall_score": weighted_overall
        }

        return merged_performance

    

    
    def evaluate_multiple_snapshots(self, top_level_dir: str):
        """
        Traverse all subfolders in top_level_dir (each subfolder corresponds to a game snapshot),
        and call evaluate_all_nights() for each subfolder to evaluate.
        
        After completing the evaluation for each subfolder, append the seven detailed scores and 
        total score for that game to self.batch_evaluation_results, and save progress to 
        "batch_evaluation_progress.json" to prevent data loss in case of crashes.

        After all subfolders have been evaluated, output the score distributions and average scores 
        for each dimension, as well as the total score distribution and average, 
        and write them to "batch_evaluation_summary.json".
        """

        if not os.path.isdir(top_level_dir):
            print(f"[evaluate_multiple_snapshots] {top_level_dir} is not a directory.")
            return

        # Store the evaluation results for all subfolders, example structure:
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

        # Find all subfolders under top_level_dir, assuming each subfolder corresponds to a "snapshot archive"
        subfolders = [
            d for d in os.listdir(top_level_dir)
            if os.path.isdir(os.path.join(top_level_dir, d))
        ]
        if not subfolders:
            print(f"[evaluate_multiple_snapshots] No subfolders found in {top_level_dir}.")
            return

        # Evaluate each subfolder
        for idx, folder_name in enumerate(subfolders, start=1):
            snapshot_path = os.path.join(top_level_dir, folder_name)
            print(f"\n=== Evaluating folder {idx}/{len(subfolders)}: {snapshot_path} ===")

            # You can either create a new WerewolfEvaluator instance for each subfolder,
            # or reuse the same object by switching snapshot_folder, but make sure to adjust paths and configurations.
            sub_evaluator = WerewolfEvaluator(
                snapshot_folder=snapshot_path,
                config_dir=os.path.join(os.path.dirname(self.snapshot_folder), self.config_dir),
                base_log_dir=self.base_log_dir
            )

            # Call evaluate_all_nights(), which generates final_result.json and stores results in sub_evaluator.full_run_result
            sub_evaluator.evaluate_all_nights()

            # Extract the merged performance scores
            # Note: After evaluate_all_nights() is completed, the final result is stored in sub_evaluator.full_run_result["villagers_performance"]
            merged_perf = sub_evaluator.full_run_result.get("villagers_performance", {})

            # Record the scores for this game
            # Here, you can place all seven dimensions and the overall_score into a dictionary
            record = {
                "folder": folder_name,  # For traceability
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

            # To prevent data loss due to crash, immediately save progress to a file
            progress_path = os.path.join(self.evaluator_dir, "batch_evaluation_progress.json")
            with open(progress_path, "w", encoding="utf-8") as f:
                json.dump(self.batch_evaluation_results, f, indent=4, ensure_ascii=False)

        # After all subfolders have been evaluated, calculate score distributions and averages for each dimension
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

        # Collect distributions
        dimension_distributions = {k: [] for k in dimension_keys}
        for item in self.batch_evaluation_results:
            for k in dimension_keys:
                dimension_distributions[k].append(item.get(k, 0))

        # Calculate averages
        dimension_averages = {}
        for k in dimension_keys:
            values = dimension_distributions[k]
            if values:
                avg = sum(values) / len(values)
            else:
                avg = 0
            dimension_averages[k] = avg

        # Create a summary
        summary = {
            "count_of_snapshots": len(self.batch_evaluation_results),
            "dimension_distributions": dimension_distributions,
            "dimension_averages": dimension_averages
        }

        summary_path = os.path.join(self.evaluator_dir, "batch_evaluation_summary.json")
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=4, ensure_ascii=False)

        print("\n[evaluate_multiple_snapshots] All subfolders evaluated.")
        print(f"Batch summary saved to: {summary_path}")
        print(f"Progress details saved to: {progress_path}")

def evaluate(top_level_dir, config_path, snapshot_folder, base_log_dir):
    evaluator = WerewolfEvaluator(snapshot_folder=snapshot_folder, config_dir=config_path, base_log_dir=base_log_dir)
    evaluator.evaluate_multiple_snapshots(top_level_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start the Werewolf evaluation environment")
    parser.add_argument('--top_level_dir', type=str, default="werewolf_log", help="Top-level log directory")
    parser.add_argument('--config_path', type=str, default=r"marble\configs\test_config\werewolf_config.yaml", help="Path to the configuration file")
    parser.add_argument('--snapshot_folder', type=str, default="placeholder", help="Snapshot folder placeholder, will be replaced by evaluate_multiple_snapshots")
    parser.add_argument('--base_log_dir', type=str, default="werewolf_eval/4omini", help="Base log directory")

    args = parser.parse_args()

    evaluate(args.top_level_dir, args.config_path, args.snapshot_folder, args.base_log_dir)