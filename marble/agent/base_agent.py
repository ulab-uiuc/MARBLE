"""
Base agent module.
"""

import json
from typing import Any, Dict, List, Union

from marble.environments import BaseEnvironment, WebEnvironment
from marble.llms.model_prompting import model_prompting
from marble.memory import BaseMemory, SharedMemory
from marble.utils.logger import get_logger

EnvType = Union[BaseEnvironment, WebEnvironment]

class BaseAgent:
    """
    Base class for all agents.
    """

    def __init__(self, config: Dict[str, Union[Any, Dict[str, Any]]], env: EnvType, shared_memory: Union[SharedMemory, None] = None):
        """
        Initialize the agent.

        Args:
            config (dict): Configuration for the agent.
            env (EnvType): Environment for the agent.
            shared_memory (BaseMemory, optional): Shared memory instance.
        """
        agent_id = config.get("agent_id")
        assert isinstance(agent_id, str), "agent_id must be a string."
        assert env is not None, "agent must has an environment."
        self.env: EnvType = env
        self.actions: List[str] = []
        self.agent_id: str = agent_id
        self.profile = config.get("profile", '')
        self.memory = BaseMemory()
        self.shared_memory = SharedMemory()
        self.relationships: Dict[str, str] = {}  # key: target_agent_id, value: relationship type
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
        tools = [self.env.action_handler_descriptions[name] for name in self.env.action_handler_descriptions]
        result = model_prompting(
            llm_model="gpt-3.5-turbo",
            messages=[{"role":"user", "content": task}],
            return_num=1,
            max_token_num=512,
            temperature=0.0,
            top_p=None,
            stream=None,
            tools=tools,
            tool_choice="auto"
        )[0]
        if result.tool_calls:
            function_call = result.tool_calls[0]
            function_name = function_call.function.name
            assert function_name is not None
            function_args = json.loads(function_call.function.arguments)
            result_from_function = self.env.apply_action(agent_id=self.agent_id, action_name=function_name, arguments=function_args)
            self.memory.update(self.agent_id, {
                    "type": "action_function_call",
                    "action_name": function_name,
                    "args": function_args,
                    "result": result_from_function
                }
            )
            self.logger.info(f"Agent '{self.agent_id}' called '{function_name}' with args '{function_args}'.")
            self.logger.info(f"Agent '{self.agent_id}' obtained result '{result_from_function}'.")

        else:
            self.memory.update(self.agent_id, {
                    "type": "action_response",
                    "result": result
                }
            )
            self.logger.info(f"Agent '{self.agent_id}' acted with result '{result}'.")
        result_content = result.content if result.content else ""
        self.token_usage += self._calculate_token_usage(task, result_content)

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

    def get_profile(self) -> Union[str, Any]:
        """
        Get the agent's profile.

        Returns:
            str: The agent's profile.
        """
        return self.profile
