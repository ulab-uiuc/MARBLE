"""
Node module for representing nodes in the swarm graph.
"""

from typing import Any, List

from marble.agent.base_agent import BaseAgent
from marble.utils.logger import get_logger


class Node:
    """
    Represents a node in the swarm graph.

    Attributes:
        id (str): Unique identifier for the node.
        agent (BaseAgent): The agent associated with this node.
        predecessors (List[Node]): Nodes that precede this node.
        successors (List[Node]): Nodes that succeed this node.
        inputs (List[Any]): Inputs to the node.
        outputs (List[Any]): Outputs from the node.
    """

    def __init__(self, agent_id: str, agent: BaseAgent):
        """
        Initialize the node.

        Args:
            agent_id (str): Identifier for the agent.
            agent (BaseAgent): The agent instance.
        """
        self.id = agent_id
        self.agent = agent
        self.predecessors: List['Node'] = []
        self.successors: List['Node'] = []
        self.inputs: List[Any] = []
        self.outputs: List[Any] = []
        self.logger = get_logger(f"Node-{self.id}")

    def add_predecessor(self, node: 'Node') -> None:
        """
        Add a predecessor node.

        Args:
            node (Node): The predecessor node.
        """
        self.predecessors.append(node)

    def add_successor(self, node: 'Node') -> None:
        """
        Add a successor node.

        Args:
            node (Node): The successor node.
        """
        self.successors.append(node)

    async def execute(self) -> None:
        """
        Execute the node's operation.
        """
        # Collect inputs from predecessors
        for pred in self.predecessors:
            self.inputs.extend(pred.outputs)

        # Process inputs
        perception = self.agent.perceive(self.inputs)
        action = self.agent.act(perception)
        self.outputs.append(action)
        self.logger.info(f"Node '{self.id}' executed with outputs: {self.outputs}")
