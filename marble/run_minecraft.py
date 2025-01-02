#!/usr/bin/env python

import time

"""
Script to run minecraft experiments.
"""

import os

if __name__ == "__main__":
    os.chdir("marble")
    for model in ["gpt-35-turbo"]:
        for task_id in range(10):
            config = f"configs/test_config_minecraft/test_config_{model}_{task_id}.yaml"
            os.system(f"python main.py --config_path {config}")
            time.sleep(10)