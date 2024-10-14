"""
Base agent module.
"""

from typing import Any, Dict, Union

from marble.llms.model_prompting import model_prompting
from marble.memory import BaseMemory, SharedMemory
from marble.utils.logger import get_logger


class BaseAgent:
    """
    Base class for all agents.
    """

    def __init__(self, config: Dict[str, Any], shared_memory: Union[SharedMemory, None] = None):
        """
        Initialize the agent.

        Args:
            config (dict): Configuration for the agent.
            shared_memory (BaseMemory, optional): Shared memory instance.
        """
        agent_id = config.get("agent_id")
        assert isinstance(agent_id, str)
        self.agent_id: str = agent_id
        self.memory = BaseMemory()
        self.shared_memory = shared_memory
        self.relationships = {}
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info(f"Agent '{self.agent_id}' initialized.")
        self.token_usage = 0  # Initialize token usage

    def perceive(self, state: Any) -> Any:
        """
        Agent perceives the environment state.

        Args:
            state (Any): The current state of the environment.

        Returns:
            Any: Processed perception data.
        """
        # For simplicity, return the task description from the state
        return state.get('task_description', '')

    def act(self, task: str) -> Any:
        """
        Agent decides on an action to take.

        Args:
            task (str): The task to perform.

        Returns:
            Any: The action decided by the agent.
        """
        self.logger.info(f"Agent '{self.agent_id}' acting on task '{task}'.")
        result = model_prompting(
            llm_model="gpt-3-turbo",
            messages=[{"content": task}],
            return_num=1,
            max_token_num=512,
            temperature=0.0,
            top_p=None,
            stream=None
        )
        self.memory.update(self.agent_id, result)
        self.token_usage += self._calculate_token_usage(task, result)
        self.logger.info(f"Agent '{self.agent_id}' acted with result '{result}'.")
        return result

    def _calculate_token_usage(self, task: str, result: str) -> int:
        """
        Calculate token usage based on input and output lengths.

        Args:
            task (str): The input task.
            result (str): The output result.

        Returns:
            int: The number of tokens used.
        """
        # Simplified token count: 1 token per 4 characters (approximation)
        token_count = (len(task) + len(result)) // 4
        return token_count

    def get_token_usage(self) -> int:
        """
        Get the total token usage by the agent.

        Returns:
            int: The total tokens used by the agent.
        """
        return self.token_usage

    def communicate(self, message: Any) -> None:
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
