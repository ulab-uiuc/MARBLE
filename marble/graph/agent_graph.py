"""
Agent graph module for representing agent structures and interactions.
"""

from typing import Any, Dict, List

from marble.agents.base_agent import BaseAgent
from marble.utils.logger import get_logger


class AgentGraph:
    """
    Represents the network structure of agents, supporting different execution methods
    such as hierarchical execution and cooperative communication.

    Attributes:
        agents (Dict[str, BaseAgent]): A dictionary of agent_id to agent instances.
        adjacency_list (Dict[str, List[str]]): The graph represented as an adjacency list.
    """

    def __init__(self, agents: List[BaseAgent], structure_config: Dict[str, Any]):
        """
        Initialize the AgentGraph with agents and structure configuration.

        Args:
            agents (List[BaseAgent]): List of agent instances.
            structure_config (Dict[str, Any]): Configuration defining the graph structure.
        """
        self.logger = get_logger(self.__class__.__name__)
        self.agents = {agent.agent_id: agent for agent in agents}
        self.adjacency_list: Dict[str, List[str]] = {}
        self.execution_mode = structure_config.get('execution_mode', 'parallel')
        self.logger.info(f"AgentGraph initialized with execution mode '{self.execution_mode}'.")
        self._build_graph(structure_config.get('structure', {}))

    def _build_graph(self, structure: Dict[str, List[str]]) -> None:
        """
        Build the adjacency list based on the structure configuration.

        Args:
            structure (Dict[str, List[str]]): Dictionary defining parent to child relationships.

        Raises:
            ValueError: If the structure references unknown agents.
        """
        for parent_id, child_ids in structure.items():
            if parent_id not in self.agents:
                raise ValueError(f"Parent agent '{parent_id}' not found among agents.")
            for child_id in child_ids:
                if child_id not in self.agents:
                    raise ValueError(f"Child agent '{child_id}' not found among agents.")
            self.adjacency_list[parent_id] = child_ids
            self.logger.debug(f"Agent '{parent_id}' connected to children {child_ids}.")

    def get_children(self, agent_id: str) -> List[BaseAgent]:
        """
        Get the child agents of a given agent.

        Args:
            agent_id (str): The ID of the agent.

        Returns:
            List[BaseAgent]: List of child agents.
        """
        child_ids = self.adjacency_list.get(agent_id, [])
        return [self.agents[child_id] for child_id in child_ids]

    def get_roots(self) -> List[BaseAgent]:
        """
        Get the root agents (agents with no parents).

        Returns:
            List[BaseAgent]: List of root agent instances.
        """
        all_children = {child_id for children in self.adjacency_list.values() for child_id in children}
        root_ids = [agent_id for agent_id in self.agents.keys() if agent_id not in all_children]
        self.logger.debug(f"Root agents: {root_ids}")
        return [self.agents[agent_id] for agent_id in root_ids]

    def traverse(self) -> List[BaseAgent]:
        """
        Traverse the graph based on the execution_mode and return agents in execution order.

        Returns:
            List[BaseAgent]: Ordered list of agents to execute.
        """
        if self.execution_mode == 'hierarchical':
            return self._hierarchical_traversal()
        elif self.execution_mode == 'cooperative':
            return self._cooperative_traversal()
        else:  # Default to parallel execution
            return list(self.agents.values())

    def _hierarchical_traversal(self) -> List[BaseAgent]:
        """
        Perform a hierarchical traversal (e.g., BFS) of the agent graph.

        Returns:
            List[BaseAgent]: Ordered list of agents for hierarchical execution.
        """
        visited = set()
        queue = self.get_roots()
        execution_order = []

        while queue:
            current_agent = queue.pop(0)
            agent_id = current_agent.agent_id
            if agent_id not in visited:
                visited.add(agent_id)
                execution_order.append(current_agent)
                children = self.get_children(agent_id)
                queue.extend(children)
                self.logger.debug(f"Agent '{agent_id}' added to execution order.")
        return execution_order

    def _cooperative_traversal(self) -> List[BaseAgent]:
        """
        Prepare agents for cooperative execution.

        Returns:
            List[BaseAgent]: List of agents (order may not be significant).
        """
        # In cooperative mode, agents may need to communicate; return all agents.
        self.logger.debug("Preparing agents for cooperative execution.")
        return list(self.agents.values())
