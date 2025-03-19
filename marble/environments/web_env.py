import time
from typing import Any, Dict

import requests
from bs4 import BeautifulSoup
from litellm.utils import trim_messages

from marble.environments.base_env import BaseEnvironment


class WebEnvironment(BaseEnvironment):
    def __init__(self, config: Dict[str, Any], name: str = "WebEnv"):
        """
        Initialize the WebEnvironment.
        Args:
            name (str): The name of the environment.
        """
        super().__init__(name, config)
        self.last_visited_timestamp: float = 0
        self.last_visited_url: str = ""
        self.web_cache: Dict[str, str] = {}  # Cache for storing webpage content

        # Register the fetch_webpage action
        fetch_webpage_description = {
            "type": "function",
            "function": {
                "name": "fetch_webpage",
                "description": "Fetches the content of a webpage from a given URL. The function includes rate limiting and caching to avoid excessive requests.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "The URL of the webpage to fetch. Must be a valid HTTP/HTTPS URL.",
                        }
                    },
                    "required": ["url"],
                    "additionalProperties": False,
                },
            },
        }
        self.register_action(
            "fetch_webpage",
            handler=self._fetch_webpage_handler,
            description=fetch_webpage_description,
        )

    def extract_text_from_html(self, html_content: str) -> str:
        """
        Extract meaningful text content from HTML.

        Args:
            html_content (str): Raw HTML content

        Returns:
            str: Extracted text content
        """
        soup = BeautifulSoup(html_content, "html.parser")

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Get text content
        text = soup.get_text(separator=" ", strip=True)

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text_ret = " ".join(chunk for chunk in chunks if chunk)

        return text_ret

    def _fetch_webpage_handler(self, url: str = "") -> Dict[str, Any]:
        """
        Action handler to fetch a webpage.
        Args:
            url (str): url to fetch
        Returns:
            Dict[str, Any]: The result of the action, including the webpage content.
        """
        if not url:
            return {
                "success": False,
                "error-msg": "URL is required to fetch a webpage.",
            }

        # Check if the URL is already cached
        if url in self.web_cache:
            content = self.web_cache[url]
        else:
            # Set up a browser-like User-Agent
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.0.0"
            }

            while time.time() - self.last_visited_timestamp < 1:
                time.sleep(0.5)

            try:
                response = requests.get(
                    url, headers=headers, timeout=5.0
                )  # 5 second timeout
                response.raise_for_status()  # Raise an error for bad responses
                content = response.text
                self.web_cache[url] = content
                self.last_visited_url = url
                self.last_visited_timestamp = time.time()
            except requests.RequestException as e:
                return {
                    "success": False,
                    "error-msg": str(e),
                }

        # Extract text content and trim it
        extracted_text = self.extract_text_from_html(content)
        trimmed_content = trim_messages(
            [{"role": "assistant", "content": extracted_text}],
            "gpt-3.5-turbo",
            max_tokens=2048,
        )[0]["content"]

        return {
            "success": True,
            "error-msg": "",
            "url": self.last_visited_url,
            "content": trimmed_content,
        }

    def get_state(self) -> Dict[str, Any]:
        """
        Get the current environment state.
        Returns:
            Dict[str, Any]: The current environment state.
        """
        return {
            "url": self.last_visited_url,
            "content": self.web_cache[self.last_visited_url]
            if self.last_visited_url
            else "",
        }
