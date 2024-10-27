"""
Main entry point for running the Marble simulation engine.
"""

import argparse
import logging
import sys

from marble.configs.config import Config
from marble.engine.engine import Engine


def parse_args()->argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Run the Marble simulation engine.")
    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='Path to the configuration YAML file.'
    )
    return parser.parse_args()

def main()->None:
    """
    Main function to run the simulation.
    """
    args = parse_args()

    # Load configuration
    try:
        config = Config.load(args.config)
    except FileNotFoundError:
        logging.error(f"Configuration file not found at path: {args.config}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        sys.exit(1)

    # Initialize and start the engine
    try:
        engine = Engine(config)
        engine.start()
    except Exception:
        logging.exception("An error occurred while running the engine.")
        sys.exit(1)

if __name__ == '__main__':
    main()
