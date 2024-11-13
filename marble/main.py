"""
Main entry point for running the Marble simulation engine.
"""

import argparse
import logging
import os
import sys

from marble.configs.config import Config
from marble.engine.engine import Engine
from tqdm import tqdm


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Run the Marble simulation engine for all YAML config files in a directory.")
    parser.add_argument(
        '--config_path',
        type=str,
        required=True,
        help='Path to the directory containing configuration YAML files.'
    )
    return parser.parse_args()


def main() -> None:
    """
    Main function to run the simulation for each YAML config file in the specified directory.
    """
    args = parse_args()

    # Check if the config path is a valid directory
    if not os.path.isdir(args.config_path):
        logging.error(f"Configuration path is not a directory: {args.config_path}")
        sys.exit(1)

    # Iterate over all YAML files in the directory
    counter = 0
    for filename in tqdm(os.listdir(args.config_path)):
        if filename.endswith(".yaml"):
            config_file_path = os.path.join(args.config_path, filename)
            # Load configuration
            # try:
            config = Config.load(config_file_path)
            counter += 1
            # Check the existence and line count of config.output['file_path']
            output_file_path = config.output['file_path']
            if not os.path.exists(output_file_path):
                # Create the file if it doesn't exist
                with open(output_file_path, 'w') as f:
                    pass
            # Count lines in the file
            with open(output_file_path, 'r') as f:
                line_count = sum(1 for _ in f)
            # Continue the loop if counter is not equal to line count + 1
            if counter != line_count + 1:
                continue
            # except FileNotFoundError:
            #     logging.error(f"Configuration file not found at path: {config_file_path}")
            #     continue
            # except Exception as e:
            #     logging.error(f"Error loading configuration from {config_file_path}: {e}")
            #     continue

            # Initialize and start the engine
            try:
                logging.info(f"Starting engine with configuration: {config_file_path}")
                engine = Engine(config)
                engine.start()
            except Exception:
                logging.exception(f"An error occurred while running the engine with configuration: {config_file_path}")
                continue


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
