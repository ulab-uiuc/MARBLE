"""
Web search tool module.
"""

from typing import Any

import requests


class WebSearchTool:
    """
    Tool to perform web searches.
    """

    def __init__(self, api_key: str):
        """
        Initialize the web search tool with an API key.

        Args:
            api_key (str): API key for the web search service.
        """
        self.api_key = api_key
        self.endpoint = "https://api.example.com/search"

    def search(self, query: str) -> Any:
        """
        Perform a web search.

        Args:
            query (str): The search query.

        Returns:
            Any: Parsed search results.

        Raises:
            requests.exceptions.RequestException: If the HTTP request fails.
        """
        params = {"q": query, "key": self.api_key}
        response = requests.get(self.endpoint, params=params)
        response.raise_for_status()
        return response.json()
