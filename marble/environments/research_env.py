import time
from typing import Any, Dict, List, Optional

import requests

from marble.environments.base_env import BaseEnvironment
from marble.environments.research_utils.paper_collector import (
    get_paper_by_arxiv_id,
    get_paper_by_keyword,
    get_paper_by_title,
    get_recent_papers,
    get_related_papers,
)
from marble.environments.research_utils.profile_collector import (
    collect_publications_and_coauthors,
)


class ResearchEnvironment(BaseEnvironment):
    def __init__(self, config: Dict[str, Any], name: str = "ResearchEnv"):
        """
        Initialize the ResearchEnvironment.

        Args:
            name (str): The name of the environment.
        """
        super().__init__(name, config)

        # Register the actions available in this environment
        self.register_action(
            "get_related_papers",
            handler=self._get_related_papers_handler,
            description={
                "type": "function",
                "function": {
                    "name": "get_related_papers",
                    "description": "Fetches related research papers based on given query parameters.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "num_results": {"type": "integer", "description": "Number of results to fetch."},
                            "query": {"type": "string", "description": "Keyword or phrase to search for."},
                            "domain": {"type": "string", "description": "Specific research domain to search in."},
                            "author": {"type": "string", "description": "Author to search for."},
                        },
                        "required": ["num_results"],
                        "additionalProperties": False
                    }
                }
            }
        )

        self.register_action(
            "get_recent_papers",
            handler=self._get_recent_papers_handler,
            description={
                "type": "function",
                "function": {
                    "name": "get_recent_papers",
                    "description": "Fetches recent papers in a given domain.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "domain": {"type": "string", "description": "Domain to fetch recent papers from."},
                            "max_results": {"type": "integer", "description": "Maximum number of results to fetch."},
                        },
                        "required": ["max_results"],
                        "additionalProperties": False
                    }
                }
            }
        )

        self.register_action(
            "collect_publications_and_coauthors",
            handler=self._collect_publications_and_coauthors_handler,
            description={
                "type": "function",
                "function": {
                    "name": "collect_publications_and_coauthors",
                    "description": "Collects an author's publications and co-author information.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "author": {"type": "string", "description": "Author's name."},
                            "known_paper_titles": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of known paper titles for author disambiguation."
                            },
                            "paper_max_num": {"type": "integer", "description": "Maximum number of papers to fetch."},
                            "exclude_known": {"type": "boolean", "description": "Whether to exclude known papers."},
                        },
                        "required": ["author"],
                        "additionalProperties": False
                    }
                }
            }
        )

        self.register_action(
            "get_paper_by_keyword",
            handler=self._get_paper_by_keyword_handler,
            description={
                "type": "function",
                "function": {
                    "name": "get_paper_by_keyword",
                    "description": "Fetches papers based on a given keyword.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "keyword": {"type": "string", "description": "Keyword to search for."},
                            "max_papers": {"type": "integer", "description": "Maximum number of papers to fetch."},
                        },
                        "required": ["keyword", "max_papers"],
                        "additionalProperties": False
                    }
                }
            }
        )

        self.register_action(
            "get_paper_by_arxiv_id",
            handler=self._get_paper_by_arxiv_id_handler,
            description={
                "type": "function",
                "function": {
                    "name": "get_paper_by_arxiv_id",
                    "description": "Fetches a paper based on a given arXiv ID.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "arxiv_id": {"type": "string", "description": "arXiv ID of the paper."},
                        },
                        "required": ["arxiv_id"],
                        "additionalProperties": False
                    }
                }
            }
        )

        self.register_action(
            "get_paper_by_title",
            handler=self._get_paper_by_title_handler,
            description={
                "type": "function",
                "function": {
                    "name": "get_paper_by_title",
                    "description": "Fetches a paper based on a given title.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Title of the paper."},
                        },
                        "required": ["title"],
                        "additionalProperties": False
                    }
                }
            }
        )

        self.register_action(
            "fetch_webpage",
            handler=self._fetch_webpage_handler,
            description={
                "type": "function",
                "function": {
                    "name": "fetch_webpage",
                    "description": "Fetches the content of a webpage from a given URL. The function includes rate limiting and caching to avoid excessive requests.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "The URL of the webpage to fetch. Must be a valid HTTP/HTTPS URL."
                            }
                        },
                        "required": ["url"],
                        "additionalProperties": False
                    }
                }
            }
        )

    def _get_related_papers_handler(
        self,
        num_results: int,
        query: Optional[str] = None,
        domain: Optional[str] = None,
        author: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Action handler to get related papers.

        Args:
            num_results (int): Number of results to fetch.
            query (Optional[str]): Keyword or phrase to search for.
            domain (Optional[str]): Specific research domain to search in.
            author (Optional[str]): Author to search for.

        Returns:
            Dict[str, Any]: The result of the action, including related paper details.
        """
        try:
            papers = get_related_papers(num_results=num_results, query=query, domain=domain, author=author)
            return {"success": True, "papers": [paper.to_dict() for paper in papers]}
        except ValueError as e:
            return {"success": False, "error-msg": str(e)}

    def _get_recent_papers_handler(self, domain: Optional[str], max_results: int) -> Dict[str, Any]:
        """
        Action handler to get recent papers.

        Args:
            domain (Optional[str]): Domain to fetch recent papers from.
            max_results (int): Maximum number of results to fetch.

        Returns:
            Dict[str, Any]: The result of the action, including recent paper details.
        """
        try:
            papers = get_recent_papers(domain=domain, max_results=max_results)
            return {"success": True, "papers": [paper.to_dict() for paper in papers]}
        except ValueError as e:
            return {"success": False, "error-msg": str(e)}

    def _collect_publications_and_coauthors_handler(
        self,
        author: str,
        known_paper_titles: Optional[List[str]] = None,
        paper_max_num: int = 20,
        exclude_known: bool = True,
    ) -> Dict[str, Any]:
        """
        Action handler to collect publications and co-authors for a given author.

        Args:
            author (str): Author's name.
            known_paper_titles (Optional[List[str]]): List of known paper titles.
            paper_max_num (int): Maximum number of papers to fetch.
            exclude_known (bool): Whether to exclude known papers.

        Returns:
            Dict[str, Any]: The result of the action, including publication and co-author details.
        """
        try:
            paper_abstracts, paper_titles, co_authors = collect_publications_and_coauthors(
                author,
                known_paper_titles=known_paper_titles,
                paper_max_num=paper_max_num,
                exclude_known=exclude_known,
            )
            return {
                "success": True,
                "paper_abstracts": paper_abstracts,
                "paper_titles": paper_titles,
                "co_authors": co_authors,
            }
        except ValueError as e:
            return {"success": False, "error-msg": str(e)}

    def _get_paper_by_keyword_handler(self, keyword: str, max_papers: int) -> Dict[str, Any]:
        """
        Action handler to get papers by keyword.

        Args:
            keyword (str): Keyword to search for.
            max_papers (int): Maximum number of papers to fetch.

        Returns:
            Dict[str, Any]: The result of the action, including paper details.
        """
        try:
            papers = get_paper_by_keyword(keyword=keyword, existing_arxiv_ids=set(), max_papers=max_papers)
            return {"success": True, "papers": [paper.to_dict() for paper in papers]}
        except ValueError as e:
            return {"success": False, "error-msg": str(e)}

    def _get_paper_by_arxiv_id_handler(self, arxiv_id: str) -> Dict[str, Any]:
        """
        Action handler to get a paper by arXiv ID.

        Args:
            arxiv_id (str): arXiv ID of the paper.

        Returns:
            Dict[str, Any]: The result of the action, including paper details.
        """
        try:
            paper = get_paper_by_arxiv_id(arxiv_id=arxiv_id)
            if paper:
                return {"success": True, "paper": paper.to_dict()}
            else:
                return {"success": False, "error-msg": "Paper not found."}
        except ValueError as e:
            return {"success": False, "error-msg": str(e)}

    def _get_paper_by_title_handler(self, title: str) -> Dict[str, Any]:
        """
        Action handler to get a paper by title.

        Args:
            title (str): Title of the paper.

        Returns:
            Dict[str, Any]: The result of the action, including paper details.
        """
        try:
            paper = get_paper_by_title(title=title)
            if paper:
                return {"success": True, "paper": paper.to_dict()}
            else:
                return {"success": False, "error-msg": "Paper not found."}
        except ValueError as e:
            return {"success": False, "error-msg": str(e)}

    def _fetch_webpage_handler(self, url: str) -> Dict[str, Any]:
        """
        Action handler to fetch a webpage.

        Args:
            url (str): The URL of the webpage to fetch.

        Returns:
            Dict[str, Any]: The result of the action, including the webpage content.
        """
        try:
            # Set up a browser-like User-Agent
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.0.0'
            }

            # Rate limiting to avoid excessive requests
            while time.time() - getattr(self, "last_visited_timestamp", 0) < 1:
                time.sleep(0.5)

            response = requests.get(url, headers=headers, timeout=5.0)  # 5 second timeout
            response.raise_for_status()  # Raise an error for bad responses
            content = response.text
            self.last_visited_timestamp = time.time()

            return {
                "success": True,
                "content": content
            }
        except requests.RequestException as e:
            return {
                "success": False,
                "error-msg": str(e)
            }
