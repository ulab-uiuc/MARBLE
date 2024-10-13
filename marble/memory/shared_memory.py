"""
Shared memory module allowing agents to communicate.
"""

from typing import Any, Dict
from threading import Lock

class SharedMemory:
    """
    Shared memory accessible by multiple agents.
    """

    def __init__(self):
        """
        Initialize the shared memory with thread-safe access.
        """
        self.storage: Dict[str, Any] = {}
        self.lock = Lock()

    def update(self, key: str, information: Any):
        """
        Update shared memory with new information.

        Args:
            key (str): Key under which to store the information.
            information (Any): Information to store.
        """
        with self.lock:
            self.storage[key] = information

    def retrieve(self, key: str) -> Any:
        """
        Retrieve information from shared memory.

        Args:
            key (str): Key of the information to retrieve.

        Returns:
            Any: The retrieved information, or None if key does not exist.
        """
        with self.lock:
            return self.storage.get(key)

    def retrieve_all(self) -> Dict[str, Any]:
        """
        Retrieve all information from shared memory.

        Returns:
            Dict[str, Any]: A copy of all stored information.
        """
        with self.lock:
            return self.storage.copy()
