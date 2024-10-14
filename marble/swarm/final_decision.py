"""
FinalDecision operation node.
"""

import random
from typing import Any, List

from marble.agent.base_agent import BaseAgent
from marble.swarm.node import Node
from marble.swarm.operation_registry import OperationRegistry
from marble.utils.logger import get_logger


@OperationRegistry.register("FinalDecision", Node)
class FinalDecisionNode(Node):
    def __init__(self, agent_id: str, agent: BaseAgent, strategy: str = "majority_vote"):
        super().__init__(agent_id, agent)
        self.strategy = strategy
        self.logger = get_logger(f"FinalDecisionNode-{self.id}")

    async def execute(self) -> None:
        # Collect inputs from predecessors
        for pred in self.predecessors:
            self.inputs.extend(pred.outputs)

        # Make a final decision based on the strategy
        if self.strategy == "majority_vote":
            decision = self.majority_vote(self.inputs)
        elif self.strategy == "random_choice":
            decision = random.choice(self.inputs)
        else:
            # Default to majority vote
            decision = self.majority_vote(self.inputs)

        # Use the agent to process the decision
        perception = self.agent.perceive({'decision': decision})
        action = self.agent.act(perception)
        self.outputs.append(action)
        self.logger.info(f"FinalDecisionNode '{self.id}' executed with outputs: {self.outputs}")

    @staticmethod
    def majority_vote(inputs: List[Any]) -> Any:
        from collections import Counter
        counter = Counter(inputs)
        most_common = counter.most_common(1)
        return most_common[0][0] if most_common else None
