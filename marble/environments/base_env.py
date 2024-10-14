"""
Base environment module.
"""

from typing import Any, Callable, Dict, List, Union

from marble.agent.reasoning_agent import ReasoningAgent

AgentType = Union[ReasoningAgent] # will expand to include other agent types

class BaseEnvironment:
    def __init__(self, name: str, config: Dict[str, Any]):
        """
        Initialize the environment.

        Args:
            name (str): The name of the environment.
        """
        self.name = name
        self.agents: List[AgentType] = []
        self.state: Dict[str, Any] = {}
        self.action_handlers: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {}
        self.done = False

    def is_done(self) -> bool:
        return self.done

    def add_agent(self, agent: AgentType) -> None:
        """
        Add an agent to the environment.

        Args:
            agent (AgentType): The agent to add.
        """
        self.agents.append(agent)

    def remove_agent(self, agent: AgentType) -> None:
        """
        Remove an agent from the environment.

        Args:
            agent (AgentType): The agent to remove.
        """
        self.agents.remove(agent)

    def register_action(self, action_name: str, handler: Callable[[Dict[str, Any]], Dict[str, Any]]) -> None:
        """
        Register an action handler for the environment.

        Args:
            action_name (str): The name of the action.
            handler (Callable): The handler function for the action.
        """
        self.action_handlers[action_name] = handler

    def apply_action(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an action in the environment.

        Args:
            action (str): The action to execute.
            params (Dict[str, Any]): Parameters for the action.
        """
        if action not in self.action_handlers:
            raise ValueError(f"Action '{action}' is not supported in this environment.")
        return self.action_handlers[action](params)

    def get_state(self) -> Dict[str, Any]:
        """
        Get the current environment state.

        Returns:
            Dict[str, Any]: The current environment state.
        """
        return self.state.copy()
