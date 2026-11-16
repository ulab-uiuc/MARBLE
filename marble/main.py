"""
Main entry point for running the Marble simulation engine.

Usage (from any directory)::

    python marble/main.py --config_path path/to/config.yaml
    python -m marble.main --config_path path/to/config.yaml --llm gpt-4o-mini
"""

import argparse
import logging
import os
import sys

# Allow ``python marble/main.py`` to work without installing the package.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)


def load_env_files() -> None:
    """Load API keys from ``.env`` in the working directory or the repo root."""
    try:
        from dotenv import load_dotenv
    except ImportError:  # python-dotenv is optional
        return
    for candidate in (os.path.join(os.getcwd(), ".env"), os.path.join(_REPO_ROOT, ".env")):
        if os.path.isfile(candidate):
            load_dotenv(candidate, override=False)


load_env_files()

from marble.configs.config import Config  # noqa: E402
from marble.engine.engine import Engine  # noqa: E402


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
    parser.add_argument(
        "--llm",
        type=str,
        default=None,
        help="Override the agents' model (any LiteLLM model name), "
        "e.g. 'gpt-4o-mini' or 'openrouter/google/gemini-2.5-flash'.",
    )
    parser.add_argument(
        "--evaluate_llm",
        type=str,
        default=None,
        help="Override the judge model used by the evaluator.",
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default=None,
        help="Override the JSONL file the results are appended to.",
    )
    return parser.parse_args()


def apply_overrides(config: Config, args: argparse.Namespace) -> Config:
    """Apply command-line overrides on top of the YAML configuration."""
    if args.llm:
        config.llm = args.llm
        # Per-agent models would silently win over the override otherwise.
        for agent_config in config.agents:
            agent_config.pop("llm", None)
    if args.evaluate_llm:
        config.metrics["evaluate_llm"] = args.evaluate_llm
    if args.output_path:
        config.output["file_path"] = args.output_path
    return config


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
        config = apply_overrides(Config.load(args.config_path), args)
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
