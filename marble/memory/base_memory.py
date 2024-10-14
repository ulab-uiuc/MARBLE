"""
Base memory module for agents.
"""

from typing import Any, List


class BaseMemory:
    """
    Base class for agent memory modules.
    """

    def __init__(self) -> None:
        """
        Initialize the memory module.
        """
        self.storage: List[Any] = []

    def update(self, key: str, information: Any) -> None:
        """
        Update memory with new information.

        Args:
            key (str): Only here to keep the signature consistent with SharedMemory
            information (Any): Information to store.
        """
        self.storage.append(information)

    def retrieve_latest(self) -> Any:
        """
        Retrieve the most recent information from memory.

        Returns:
            Any: The most recently stored information, or None if empty.
        """
        return self.storage[-1] if self.storage else None

    def retrieve_all(self) -> List[Any]:
        """
        Retrieve all stored information.

        Returns:
            List[Any]: All stored information.
        """
        return self.storage.copy()
