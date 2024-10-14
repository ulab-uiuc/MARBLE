"""
CombineAnswer operation node.
"""

from typing import Any, List

from marble.swarm.node import Node
from marble.swarm.operation_registry import OperationRegistry
from marble.llms.model_prompting import model_prompting
from marble.utils.logger import get_logger


@OperationRegistry.register("CombineAnswer", Node)
class CombineAnswerNode(Node):
    def __init__(self, agent_id: str, agent: BaseAgent):
        super().__init__(agent_id, agent)
        self.logger = get_logger(f"CombineAnswerNode-{self.id}")

    async def execute(self) -> None:
        # Collect inputs from predecessors
        for pred in self.predecessors:
            self.inputs.extend(pred.outputs)

        # Combine inputs
        combined_input = "\n".join(self.inputs)
        # Use the agent to process the combined input
        perception = self.agent.perceive({'combined_input': combined_input})
        action = self.agent.act(perception)
        self.outputs.append(action)
        self.logger.info(f"CombineAnswerNode '{self.id}' executed with outputs: {self.outputs}")
