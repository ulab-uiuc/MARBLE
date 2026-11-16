#!/usr/bin/env python

"""
Script to run minecraft experiments.

It can be started from any directory and expects a Minecraft 1.19.2 server
(see the README). The unified runner does the same with more options::

    python scripts/run_benchmark.py --scenario minecraft --model gpt-4o-mini
"""

import os
import subprocess
import sys
import time

MARBLE_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    for model in ["gpt-4o-mini"]:
        for task_id in range(0, 10):
            config = os.path.join(
                MARBLE_DIR,
                "configs",
                "test_config_minecraft",
                f"test_config_{model}_{task_id}.yaml",
            )
            subprocess.run(
                [sys.executable, os.path.join(MARBLE_DIR, "main.py"), "--config_path", config]
            )
            time.sleep(10)
