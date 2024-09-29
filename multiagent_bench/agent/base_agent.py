"""
Base agent module.
"""

from typing import Any
from memory.base_memory import BaseMemory
from utils.logger import get_logger

class BaseAgent:
    """
    Base class for all agents.
    """

    def __init__(self, config: dict, shared_memory: BaseMemory = None):
        """
        Initialize the agent.

        Args:
            config (dict): Configuration for the agent.
            shared_memory (BaseMemory, optional): Shared memory instance.
        """
        self.agent_id = config.get("agent_id")
        self.memory = BaseMemory()
        self.shared_memory = shared_memory
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info(f"Agent '{self.agent_id}' initialized.")

    def perceive(self, state: Any) -> Any:
        """
        Agent perceives the environment state.

        Args:
            state (Any): The current state of the environment.

        Returns:
            Any: Processed perception data.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    def act(self, perception: Any) -> Any:
        """
        Agent decides on an action to take.

        Args:
            perception (Any): Perception data processed by the agent.

        Returns:
            Any: The action decided by the agent.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    def communicate(self, message: Any):
        """
        Communicate with other agents via shared memory.

        Args:
            message (Any): The message or data to share.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        if self.shared_memory is not None:
            self.shared_memory.update(self.agent_id, message)
        else:
            raise NotImplementedError("Shared memory is not initialized for this agent.")

    def receive_communication(self) -> Any:
        """
        Receive communication from other agents via shared memory.

        Returns:
            Any: Messages or data from other agents.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        if self.shared_memory is not None:
            messages = self.shared_memory.retrieve_all()
            # Exclude self messages
            messages.pop(self.agent_id, None)
            return messages
        else:
            raise NotImplementedError("Shared memory is not initialized for this agent.")