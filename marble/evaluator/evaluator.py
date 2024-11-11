"""
Evaluator module for tracking metrics and evaluating agent performance.
"""

from typing import Any, Dict, List

from marble.agent import BaseAgent
from marble.environments import BaseEnvironment
from marble.utils.logger import get_logger


class Evaluator:
    """
    Evaluator class for tracking metrics like task completion success rate and token consumption.
    """
    def __init__(self, metrics_config: Dict[str, Any]):
        """
        Initialize the Evaluator with the specified metrics.

        Args:
            metrics_config (Dict[str, Any]): Configuration for the metrics to track.
        """
        self.logger = get_logger(self.__class__.__name__)
        self.metrics_config = metrics_config
        self.metrics:Dict[str, Any] = {
            "task_completion": [],
            "token_consumption": [],
            "planning_score": [],
            "communication_score": []
        }

    def intermediate_evaluation(self, summary_data: Dict[str, Any]) -> None:
       """
       save intermediate evaluation results
       """
       pass

    def update(self, environment: BaseEnvironment, agents: List[BaseAgent]) -> None:
        """
        Update the metrics based on the current state of the environment and agents.

        Args:
            environment (BaseEnvironment): The environment instance.
            agents (List[BaseAgent]): List of agent instances.
        """
        # For task completion, check if the environment indicates the task is done
        if environment.is_task_completed():
            self.metrics["task_completion"].append(1)
        else:
            self.metrics["task_completion"].append(0)

        # For token consumption, sum up the tokens used by agents in this iteration
        total_tokens = sum(agent.get_token_usage() for agent in agents)
        self.metrics["token_consumption"].append(total_tokens)

    def finalize(self) -> None:
        """
        Finalize the evaluation, compute final metrics, and log or save the results.
        """
        total_tasks = len(self.metrics["task_completion"])
        tasks_completed = sum(self.metrics["task_completion"])
        success_rate = tasks_completed / total_tasks if total_tasks > 0 else 0

        total_tokens = sum(self.metrics["token_consumption"])
        avg_tokens_per_iteration = total_tokens / total_tasks if total_tasks > 0 else 0

        self.logger.info(f"Task Completion Success Rate: {success_rate * 100:.2f}%")
        self.logger.info(f"Total Token Consumption: {total_tokens}")
        self.logger.info(f"Average Tokens per Iteration: {avg_tokens_per_iteration}")

        # Additional metrics can be computed and logged here

    def get_metrics(self) -> Dict[str, Any]:
        """
        Get the computed metrics.

        Returns:
            Dict[str, Any]: The computed metrics.
        """
        return {
            "success_rate": sum(self.metrics["task_completion"]) / len(self.metrics["task_completion"]) if self.metrics["task_completion"] else 0,
            "total_tokens": sum(self.metrics["token_consumption"]),
            "avg_tokens_per_iteration": sum(self.metrics["token_consumption"]) / len(self.metrics["token_consumption"]) if self.metrics["token_consumption"] else 0
        }
