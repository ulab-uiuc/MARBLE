"""
Agent graph module for representing agent structures and interactions.
"""

from typing import Any, Dict, List, Sequence, Tuple

from marble.agent.base_agent import BaseAgent
from marble.utils.logger import get_logger


class AgentGraph:
    """
    Represents the network structure of agents, supporting different execution methods
    such as hierarchical execution and cooperative communication.

    Attributes:
        agents (Dict[str, BaseAgent]): A dictionary of agent_id to agent instances.
        adjacency_list (Dict[str, List[str]]): The graph represented as an adjacency list.
        relationships (List[Tuple[str, str, str]]): List of relationships as triples.
    """

    # def __init__(self, agents: Sequence[BaseAgent], structure_config: Dict[str, Any]):
    #     """
    #     Initialize the AgentGraph with agents and structure configuration.

    #     Args:
    #         agents (List[BaseAgent]): List of agent instances.
    #         structure_config (Dict[str, Any]): Configuration defining the graph structure.
    #     """
    #     self.logger = get_logger(self.__class__.__name__)
    #     self.agents = {agent.agent_id: agent for agent in agents}
    #     self.adjacency_list: Dict[str, List[str]] = {}
    #     self.relationships: List[Tuple[str, str, str]] = []
    #     self.execution_mode = structure_config.get('execution_mode', 'parallel')
    #     self.logger.info(f"AgentGraph initialized with execution mode '{self.execution_mode}'.")
    #     self._build_graph(structure_config.get('structure', {}))
    #     self._initialize_relationships(structure_config.get('relationships', []))
    def __init__(self, agents: Sequence[BaseAgent], structure_config: Dict[str, Any]):
        """
        Initialize the AgentGraph with agents and structure configuration.

        Args:
            agents (List[BaseAgent]): List of agent instances.
            structure_config (Dict[str, Any]): Configuration defining the graph structure.
                Expected keys:
                    - execution_mode: 'parallel', 'hierarchical', or 'cooperative'
                    - relationships: List of triples [node1, node2, relationship]
        """
        self.logger = get_logger(self.__class__.__name__)
        self.agents = {agent.agent_id: agent for agent in agents}
        self.relationships: List[Tuple[str, str, str]] = []
        self.execution_mode = structure_config.get('execution_mode', 'parallel')
        self.logger.info(f"AgentGraph initialized with execution mode '{self.execution_mode}'.")
        relationships = structure_config.get('relationships', [])
        for rel in relationships:
            if len(rel) != 3:
                raise ValueError(f"Invalid relationship format: {rel}. Expected 3 elements.")
            node1, node2, relationship = rel
            self.add_relationship(node1, node2, relationship)

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

    def _initialize_relationships(self, relationships: List[Dict[str, str]]) -> None:
        """
        Initialize relationships between agents.

        Args:
            relationships (List[Dict[str, str]]): List of relationship dictionaries with 'source', 'target', and 'type'.

        Raises:
            ValueError: If any referenced agent is unknown.
        """
        for rel in relationships:
            source = rel.get('source')
            target = rel.get('target')
            rel_type = rel.get('type', 'related_to')
            if source not in self.agents:
                raise ValueError(f"Source agent '{source}' not found among agents.")
            if target not in self.agents:
                raise ValueError(f"Target agent '{target}' not found among agents.")
            self.relationships.append((source, target, rel_type))
            # Assign relationship to agents
            self.agents[source].relationships[target] = rel_type
            self.logger.debug(f"Relationship added: {source} --[{rel_type}]--> {target}")

    # CRUD Operations

    def add_agent(self, agent: BaseAgent) -> None:
        """
        Add a new agent to the graph.

        Args:
            agent (BaseAgent): The agent instance to add.

        Raises:
            ValueError: If agent_id already exists.
        """
        if agent.agent_id in self.agents:
            raise ValueError(f"Agent '{agent.agent_id}' already exists.")
        self.agents[agent.agent_id] = agent
        self.adjacency_list[agent.agent_id] = []
        self.logger.info(f"Agent '{agent.agent_id}' added to the graph.")

    def remove_agent(self, agent_id: str) -> None:
        """
        Remove an agent from the graph.

        Args:
            agent_id (str): The ID of the agent to remove.

        Raises:
            ValueError: If agent_id does not exist.
        """
        if agent_id not in self.agents:
            raise ValueError(f"Agent '{agent_id}' does not exist.")
        # Remove from adjacency list
        self.adjacency_list.pop(agent_id, None)
        # Remove from other agents' adjacency lists
        for children in self.adjacency_list.values():
            if agent_id in children:
                children.remove(agent_id)
        # Remove relationships
        self.relationships = [rel for rel in self.relationships if rel[0] != agent_id and rel[1] != agent_id]
        # Remove from agents
        del self.agents[agent_id]
        self.logger.info(f"Agent '{agent_id}' removed from the graph.")

    def update_agent(self, agent_id: str, **kwargs: Any) -> None:
        """
        Update an agent's configuration.

        Args:
            agent_id (str): The ID of the agent to update.
            **kwargs: Attributes to update on the agent.

        Raises:
            ValueError: If agent_id does not exist.
        """
        if agent_id not in self.agents:
            raise ValueError(f"Agent '{agent_id}' does not exist.")
        agent = self.agents[agent_id]
        for key, value in kwargs.items():
            if hasattr(agent, key):
                setattr(agent, key, value)
                self.logger.debug(f"Agent '{agent_id}' attribute '{key}' updated to '{value}'.")
            else:
                self.logger.warning(f"Agent '{agent_id}' has no attribute '{key}'.")

    def get_agent(self, agent_id: str) -> BaseAgent:
        """
        Retrieve an agent by its ID.

        Args:
            agent_id (str): The ID of the agent to retrieve.

        Raises:
            ValueError: If agent_id does not exist.

        Returns:
            BaseAgent: The requested agent instance.
        """
        if agent_id not in self.agents:
            raise ValueError(f"Agent '{agent_id}' does not exist.")
        return self.agents[agent_id]

    def add_relationship(self, source: str, target: str, rel_type: str = 'related_to') -> None:
        """
        Add a relationship between two agents.

        Args:
            source (str): Source agent ID.
            target (str): Target agent ID.
            rel_type (str): Type of relationship.

        Raises:
            ValueError: If either agent does not exist.
        """
        if source not in self.agents:
            raise ValueError(f"Source agent '{source}' does not exist.")
        if target not in self.agents:
            raise ValueError(f"Target agent '{target}' does not exist.")
        self.relationships.append((source, target, rel_type))
        self.agents[source].relationships[target] = rel_type
        self.logger.info(f"Relationship added: {source} --[{rel_type}]--> {target}")

    def remove_relationship(self, source: str, target: str) -> None:
        """
        Remove a relationship between two agents.

        Args:
            source (str): Source agent ID.
            target (str): Target agent ID.

        Raises:
            ValueError: If the relationship does not exist.
        """
        rel_to_remove = None
        for rel in self.relationships:
            if rel[0] == source and rel[1] == target:
                rel_to_remove = rel
                break
        if not rel_to_remove:
            raise ValueError(f"Relationship from '{source}' to '{target}' does not exist.")
        self.relationships.remove(rel_to_remove)
        del self.agents[source].relationships[target]
        self.logger.info(f"Relationship removed: {source} --> {target}")

    def update_relationship(self, source: str, target: str, new_type: str) -> None:
        """
        Update the type of a relationship between two agents.

        Args:
            source (str): Source agent ID.
            target (str): Target agent ID.
            new_type (str): New relationship type.

        Raises:
            ValueError: If the relationship does not exist.
        """
        for idx, rel in enumerate(self.relationships):
            if rel[0] == source and rel[1] == target:
                self.relationships[idx] = (source, target, new_type)
                self.agents[source].relationships[target] = new_type
                self.logger.info(f"Relationship updated: {source} --[{new_type}]--> {target}")
                return
        raise ValueError(f"Relationship from '{source}' to '{target}' does not exist.")

    # Existing methods remain unchanged...

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

    def get_agent_profiles(self) -> Dict[str, Dict[str, Any]]:
        """
        Get profiles of all agents in the graph.

        Returns:
            Dict[str, Dict[str, Any]]: A dictionary mapping agent IDs to their profiles.
        """
        profiles = {}
        for agent_id, agent in self.agents.items():
            profiles[agent_id] = {
                "agent_id": agent.agent_id,
                "relationships": agent.get_relationships(),
                "token_usage": agent.get_token_usage(),
                # Add other relevant profile information if needed
            }
        return profiles
