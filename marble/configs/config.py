"""
Configuration management module.
"""

from typing import Any, Dict

import yaml


class Config:
    """
    Configuration class to load and store system configurations.
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize the Config with data.

        Args:
            data (Dict[str, Any]): Configuration data.
        """
        data = data or {}

        def section(key: str, default: Any) -> Any:
            # A key that is present but empty in the YAML (``metrics:``) is
            # loaded as ``None``; treat it like a missing key.
            value = data.get(key)
            return default if value is None else value

        self.environment = section("environment", {})
        self.relationships = section("relationships", [])
        self.agents = section("agents", [])
        self.metrics = section("metrics", {})
        self.llm = section("llm", "")
        self.tools = section("tools", {})
        self.logger = section("logger", {})
        self.parallel = section("parallel", {})
        self.graph = section("graph", {})
        self.memory = section("memory", {})
        self.engine_planner = section("engine_planner", {})
        self.task: Dict[str, Any] = section("task", {})
        self.coordination_mode = section("coordinate_mode", "centralized")
        self.output = section("output", {})
        # Optional bookkeeping fields from the MultiAgentBench JSONL files;
        # they are copied into the result record when present.
        self.task_id = data.get("task_id")
        self.scenario = data.get("scenario")

    @staticmethod
    def load(file_path: str) -> "Config":
        """
        Load configuration from a YAML file.

        Args:
            file_path (str): Path to the configuration file.

        Returns:
            Config: An instance of the Config class.

        Raises:
            FileNotFoundError: If the configuration file is not found.
            yaml.YAMLError: If there is an error parsing the YAML file.
        """
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
        return Config(data)
