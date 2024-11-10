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
        self.environment = data.get('environment', {})
        self.relationships = data.get('relationships', [])
        self.agents = data.get('agents', [])
        self.metrics = data.get('metrics', {})
        self.llm = data.get('llm', {})
        self.tools = data.get('tools', {})
        self.logger = data.get('logger', {})
        self.parallel = data.get('parallel', {})
        self.graph = data.get('graph', {})
        self.memory = data.get('memory', {})
        self.engine_planner = data.get('engine_planner', {})
        self.task:Dict[str, Any] = data.get('task', {})
        self.coordination_mode = data.get('coordinate_mode', 'centralized')
        self.relationships = data.get('relationships', [])
        self.output = data.get('output', {})

    @staticmethod
    def load(file_path: str) -> 'Config':
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
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return Config(data)
