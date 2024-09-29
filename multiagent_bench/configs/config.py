"""
Configuration management module.
"""

import yaml
from typing import Any, Dict

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
        self.agents = data.get('agents', [])
        self.metrics = data.get('metrics', {})
        self.llm = data.get('llm', {})
        self.tools = data.get('tools', {})
        self.logger = data.get('logger', {})
        self.parallel = data.get('parallel', {})

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