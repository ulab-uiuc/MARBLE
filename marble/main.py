"""
Main entry point for running the Marble simulation engine.
"""

import argparse
import logging
import os
import sys

from marble.configs.config import Config
from marble.engine.engine import Engine


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Run the Marble simulation engine.")
    parser.add_argument(
        "--config_path",
        type=str,
        required=True,
        help="Path to the configuration YAML file.",
    )
    return parser.parse_args()


def main() -> None:
    """
    Main function to run the simulation with the specified config file.
    """
    args = parse_args()

    # Check if the config file exists
    if not os.path.isfile(args.config_path):
        logging.error(f"Configuration file not found: {args.config_path}")
        sys.exit(1)

    # Load configuration
    try:
        config = Config.load(args.config_path)
    except Exception as e:
        logging.error(f"Error loading configuration from {args.config_path}: {e}")
        sys.exit(1)

    # Initialize and start the engine
    try:
        logging.info(f"Starting engine with configuration: {args.config_path}")
        engine = Engine(config)
        engine.start()
    except Exception:
        logging.exception(
            f"An error occurred while running the engine with configuration: {args.config_path}"
        )
        sys.exit(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
