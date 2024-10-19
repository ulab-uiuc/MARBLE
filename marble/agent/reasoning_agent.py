"""
Reasoning agent module.
"""

from typing import Any, Dict, Union

from marble.agent import BaseAgent
from marble.llms import OpenAILLM
from marble.memory import BaseMemory, SharedMemory
from marble.environments import BaseEnvironment, WebEnvironment

EnvType = Union[BaseEnvironment, WebEnvironment]

class ReasoningAgent(BaseAgent):
    """
    Agent that uses reasoning strategies (Chain-of-Thought, ReAct, etc.).
    """

    def __init__(self, config: Dict[str, Union[Any, Dict[str, Any]]], env: EnvType, shared_memory: Union[SharedMemory, None] = None):
        """
        Initialize the ReasoningAgent.

        Args:
            config (dict): Configuration for the reasoning agent.
        """
        super().__init__(config, env, shared_memory)
        llm_config = config.get("llm")
        assert llm_config is not None
        llm_type = llm_config.get("type")
        if llm_type == "OpenAI":
            self.llm = OpenAILLM(llm_config)
        else:
            raise ValueError(f"Unsupported LLM type: {llm_type}")
        self.memory = BaseMemory()

    def perceive(self, state: Any) -> Any:
        """
        Process perception with cognitive abilities.

        Args:
            state (Any): The current state of the environment.

        Returns:
            Any: Processed perception data.
        """
        self.memory.update(self.agent_id, state)
        perception = self.memory.retrieve_latest()
        return perception

    def act(self, perception: Any) -> Any:
        """
        Decide on an action using the LLM.

        Args:
            perception (Any): Processed perception data.

        Returns:
            Any: The action decided by the agent.
        """
        prompt = self._generate_prompt(perception)
        action = self.llm.generate_text(prompt)
        return action

    def _generate_prompt(self, perception: Any) -> str:
        """
        Generate a prompt for the LLM based on perception.

        Args:
            perception (Any): Perception data.

        Returns:
            str: Generated prompt.
        """
        return f"Based on the perception: {perception}, what action should be taken?"
