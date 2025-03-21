#!/usr/bin/env python

"""
Script to run reasoning strategy ablation experiments.
"""

import os
from typing import List

import yaml


def create_config_with_strategy(
    base_config_path: str, strategy: str, output_path: str
) -> None:
    """
    Create a new config file with the specified reasoning strategy.

    Args:
        base_config_path (str): Path to the base config file
        strategy (str): Reasoning strategy to use
        output_path (str): Path to save the new config file
    """
    with open(base_config_path, "r") as f:
        config = yaml.safe_load(f)

    # Update strategy for all agents
    for agent in config["agents"]:
        agent["strategy"] = strategy

    # Update output path to include strategy
    config["output"]["file_path"] = f"result/discussion_output_{strategy}.jsonl"

    with open(output_path, "w") as f:
        yaml.dump(config, f)


def run_experiment(strategies: List[str]) -> None:
    """
    Run experiments for different reasoning strategies.

    Args:
        strategies (List[str]): List of reasoning strategies to test
    """
    base_config = "configs/test_config_reasoning.yaml"

    # Create result directory if it doesn't exist
    os.makedirs("result", exist_ok=True)

    for strategy in strategies:
        # Create strategy-specific config
        strategy_config = f"configs/test_config_reasoning_{strategy}.yaml"
        create_config_with_strategy(base_config, strategy, strategy_config)

        # Run experiment
        os.system(f"python main.py --config_path {strategy_config}")


if __name__ == "__main__":
    strategies = ["react"]
    run_experiment(strategies)
