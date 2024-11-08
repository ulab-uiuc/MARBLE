"""
Base memory module for agents.
"""

import json
from typing import Any, List

class BaseMemory:
    """Base class for agent memory modules."""

    def __init__(self) -> None:
        """Initialize the memory module."""
        self.storage: List[Any] = []

    def update(self, key: str, information: Any) -> None:
        """
        Update memory with new information.

        Args:
            key (str): Only here to keep the signature consistent with SharedMemory.
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

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the memory.

        Returns:
            str: Formatted string showing memory contents.
        """
        if not self.storage:
            return "Memory: Empty"

        items = [f"    {i}: {str(item)}" for i, item in enumerate(self.storage)]
        return "Memory Contents:\n" + "\n".join(items)

    def __repr__(self) -> str:
        """
        Returns a detailed string representation of the memory object.

        Returns:
            str: Technical string representation.
        """
        return f"BaseMemory(storage={self.storage})"
      
    def get_memory_str(self) -> str:
        """
        Get a string representation of the memory.

        Returns:
            str: String representation of the memory.
        """
        memory_str = " ".join([json.dumps(info) for info in self.storage])
        return memory_str