"""
Swarm graph module for representing agent structures and interactions.
"""

import asyncio
import shortuuid
from typing import Any, Dict, List, Optional, Union
from copy import deepcopy

from marble.swarm.node import Node
from marble.agent.base_agent import BaseAgent
from marble.utils.logger import get_logger


class SwarmGraph:
    """
    A framework for managing and executing a network of interconnected nodes using agents.

    This class enables the creation of a graph structure for processing and analyzing data.
    Each node in the graph can perform specific operations, allowing for complex data processing workflows.
    The graph supports integration with agents, making it suitable for tasks that require
    multi-agent collaboration.

    Attributes:
        agents (Dict[str, BaseAgent]): A dictionary of agent_id to agent instances.
        nodes (Dict[str, Node]): A collection of nodes, each identified by a unique UUID.
        logger: Logger instance for logging information.
        input_nodes (List[Node]): List of nodes designated as input points to the graph.
        output_nodes (List[Node]): List of nodes designated as output points of the graph.
    """

    def __init__(self, agents: List[BaseAgent], structure_config: Dict[str, Any]):
        """
        Initialize the SwarmGraph with agents and structure configuration.

        Args:
            agents (List[BaseAgent]): List of agent instances.
            structure_config (Dict[str, Any]): Configuration defining the graph structure.
        """
        self.id = shortuuid.ShortUUID().random(length=4)
        self.logger = get_logger(self.__class__.__name__)
        self.agents = {agent.agent_id: agent for agent in agents}
        self.nodes: Dict[str, Node] = {}
        self.input_nodes: List[Node] = []
        self.output_nodes: List[Node] = []
        self._build_graph(structure_config.get('structure', {}))

    def _build_graph(self, structure: Dict[str, Any]) -> None:
        """
        Build the graph based on the structure configuration.

        Args:
            structure (Dict[str, Any]): Configuration defining the graph structure.
        """
        # Create nodes for each agent
        for agent_id, agent in self.agents.items():
            node = Node(agent_id=agent_id, agent=agent)
            self.nodes[agent_id] = node

        # Build connections between nodes
        for parent_id, child_ids in structure.items():
            parent_node = self.nodes.get(parent_id)
            if not parent_node:
                raise ValueError(f"Parent node '{parent_id}' not found.")
            for child_id in child_ids:
                child_node = self.nodes.get(child_id)
                if not child_node:
                    raise ValueError(f"Child node '{child_id}' not found.")
                parent_node.add_successor(child_node)
                child_node.add_predecessor(parent_node)
                self.logger.debug(f"Node '{parent_id}' connected to '{child_id}'.")

        # Identify input and output nodes
        self.input_nodes = [node for node in self.nodes.values() if not node.predecessors]
        self.output_nodes = [node for node in self.nodes.values() if not node.successors]
        self.logger.info(f"Input nodes: {[node.id for node in self.input_nodes]}")
        self.logger.info(f"Output nodes: {[node.id for node in self.output_nodes]}")

    async def run(self, inputs: Dict[str, Any], max_tries: int = 3, max_time: int = 600) -> List[Any]:
        """
        Execute the graph for a specified number of steps, processing provided inputs.

        Args:
            inputs (Dict[str, Any]): Input data for the graph.
            max_tries (int): Maximum number of retries for node execution.
            max_time (int): Maximum time allowed for node execution.

        Returns:
            List[Any]: Outputs from the output nodes.
        """
        # Initialize input nodes with inputs
        for node in self.input_nodes:
            node.inputs = [deepcopy(inputs)]

        # Topological sort
        in_degree = {node.id: len(node.predecessors) for node in self.nodes.values()}
        zero_in_degree_queue = [node for node in self.nodes.values() if in_degree[node.id] == 0]

        while zero_in_degree_queue:
            current_node = zero_in_degree_queue.pop(0)
            tries = 0
            while tries < max_tries:
                try:
                    await asyncio.wait_for(current_node.execute(), timeout=max_time)
                    break
                except asyncio.TimeoutError:
                    self.logger.warning(f"Node {current_node.id} execution timed out, retrying {tries + 1}/{max_tries}...")
                except Exception as e:
                    self.logger.error(f"Error during execution of node {current_node.id}: {e}")
                    break
                tries += 1

            for successor in current_node.successors:
                in_degree[successor.id] -= 1
                if in_degree[successor.id] == 0:
                    zero_in_degree_queue.append(successor)

        # Collect outputs
        final_outputs = []
        for node in self.output_nodes:
            final_outputs.extend(node.outputs)

        return final_outputs
