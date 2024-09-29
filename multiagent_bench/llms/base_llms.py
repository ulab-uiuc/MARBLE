"""
Base interface for Language Model (LLM) integrations.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseLLM(ABC):
    """
    Abstract base class for interacting with language models.

    Attributes:
        config (Dict[str, Any]): Configuration parameters for the LLM.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the LLM with the provided configuration.

        Args:
            config (Dict[str, Any]): Configuration parameters.
        """
        self.config = config
        self.model_name = config.get('model_name')
        self.temperature = config.get('temperature', 0.7)
        self.max_tokens = config.get('max_tokens', 150)
        self.api_key = config.get('api_key')
        self.api_base = config.get('api_base')
        self.timeout = config.get('timeout', 30)

    @abstractmethod
    def generate_text(self, prompt: str, **kwargs) -> str:
        """
        Generate text based on the input prompt.

        Args:
            prompt (str): The prompt to send to the language model.
            **kwargs: Additional parameters specific to the LLM.

        Returns:
            str: The generated text response.

        Raises:
            Exception: If an error occurs during text generation.
        """
        pass

    @abstractmethod
    def generate_stream(self, prompt: str, **kwargs) -> Any:
        """
        Generate text as a stream based on the input prompt.

        Args:
            prompt (str): The prompt to send to the language model.
            **kwargs: Additional parameters specific to the LLM.

        Yields:
            Any: Streamed content from the language model.

        Raises:
            Exception: If an error occurs during text generation.
        """
        pass