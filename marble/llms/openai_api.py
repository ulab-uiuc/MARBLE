"""
OpenAI LLM integration module.
"""

import time
from typing import Any, Dict, Generator

import openai
from llms.base_llm import BaseLLM
from openai.error import (
    APIConnectionError,
    APIError,
    OpenAIError,
    RateLimitError,
    Timeout,
)
from utils.logger import get_logger


class OpenAILLM(BaseLLM):
    """
    Concrete implementation of BaseLLM for OpenAI's language models.

    Attributes:
        logger (logging.Logger): Logger instance for logging information.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize OpenAILLM with the given configuration.

        Args:
            config (Dict[str, Any]): Configuration parameters specific to OpenAI LLM.
        """
        super().__init__(config)
        self.logger = get_logger(self.__class__.__name__)
        self._validate_config()
        self._initialize_api()

    def _validate_config(self):
        """
        Validate that all required configuration parameters are present.

        Raises:
            ValueError: If a required configuration parameter is missing.
        """
        if not self.api_key:
            raise ValueError("API key is required for OpenAI LLM.")
        if not self.model_name:
            raise ValueError("Model name is required for OpenAI LLM.")

    def _initialize_api(self):
        """
        Initialize the OpenAI API with the provided credentials.
        """
        openai.api_key = self.api_key
        if self.api_base:
            openai.api_base = self.api_base
        self.logger.debug("OpenAI API initialized.")

    def generate_text(self, prompt: str, **kwargs) -> str:
        """
        Generate text based on the input prompt.

        Args:
            prompt (str): The prompt to send to the language model.
            **kwargs: Additional parameters for the OpenAI API.

        Returns:
            str: The generated text response.

        Raises:
            OpenAIError: If an error occurs with the OpenAI API.
        """
        payload = self._build_payload(prompt, **kwargs)
        response = self._call_api(payload)
        text = response['choices'][0]['text'].strip()
        self.logger.debug(f"Generated text: {text}")
        return text

    def generate_stream(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        """
        Generate text as a stream based on the input prompt.

        Args:
            prompt (str): The prompt to send to the language model.
            **kwargs: Additional parameters for the OpenAI API.

        Yields:
            str: Streamed content from the language model.

        Raises:
            OpenAIError: If an error occurs with the OpenAI API.
        """
        payload = self._build_payload(prompt, stream=True, **kwargs)
        try:
            response = openai.Completion.create(**payload)
            for chunk in response:
                text = chunk['choices'][0].get('text', '')
                if text:
                    self.logger.debug(f"Streaming text: {text}")
                    yield text
        except OpenAIError as e:
            self.logger.error(f"Error during streaming generation: {e}")
            raise

    def _build_payload(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Build the payload for the OpenAI API request.

        Args:
            prompt (str): The input prompt.
            **kwargs: Additional parameters.

        Returns:
            Dict[str, Any]: The payload dictionary.
        """
        payload = {
            'engine': self.model_name,
            'prompt': prompt,
            'max_tokens': kwargs.get('max_tokens', self.max_tokens),
            'temperature': kwargs.get('temperature', self.temperature),
            'n': kwargs.get('n', 1),
            'stop': kwargs.get('stop', None),
            'timeout': kwargs.get('timeout', self.timeout),
        }
        payload.update(kwargs)
        self.logger.debug(f"API payload: {payload}")
        return payload

    def _call_api(self, payload: Dict[str, Any]) -> Any:
        """
        Make the API call to OpenAI with exponential backoff.

        Args:
            payload (Dict[str, Any]): The payload for the API call.

        Returns:
            Any: The response from the OpenAI API.

        Raises:
            OpenAIError: If the API call fails after retries.
        """
        max_retries = 5
        backoff_factor = 2
        for attempt in range(max_retries):
            try:
                response = openai.Completion.create(**payload)
                self.logger.debug("API call successful.")
                return response
            except (RateLimitError, APIConnectionError, APIError, Timeout):
                wait_time = backoff_factor ** attempt
                self.logger.warning(f"API call failed (attempt {attempt + 1}/{max_retries}). Retrying in {wait_time} seconds.")
                time.sleep(wait_time)
            except OpenAIError as e:
                self.logger.error(f"OpenAI API error: {e}")
                raise e
        raise OpenAIError("Max retries exceeded for OpenAI API call.")
