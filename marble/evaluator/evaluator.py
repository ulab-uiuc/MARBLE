"""
Evaluator module for tracking metrics and evaluating agent performance.
"""

import json
import re
from typing import Any, Dict, List

from marble.agent import BaseAgent
from marble.environments import BaseEnvironment
from marble.llms.model_prompting import model_prompting
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
            "communication_score": [],
            "task_evaluation": {}
        }
        with open('evaluator/evaluator_prompts.json', 'r', encoding='utf-8') as f:
            self.evaluation_prompts = json.load(f)
        self.llm = self.metrics_config.get('evaluate_llm', 'gpt-3.5-turbo')


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

    def evaluate_communication(self, task: str, communications: str) -> None:
        """
        Evaluate communication between agents and update the communication score.

        Args:
            task (str): The task description.
            communications (str): The communication logs between agents.
        """
        # Get the communication prompt
        communication_prompt_template = self.evaluation_prompts["Graph"]["Communication"]["prompt"]
        # Fill in the placeholders {task} and {communications}
        prompt = communication_prompt_template.format(task=task, communications=communications)
        # Call the language model
        result = model_prompting(
            llm_model=self.llm,
            messages=[{"role": "user", "content": prompt}],
            return_num=1,
            max_token_num=512,
            temperature=0.0,
            top_p=None,
            stream=None,
        )[0]
        # Parse the score from result.content
        score = self.parse_score(result.content)
        # Update the metric
        self.metrics["communication_score"].append(score)

    def evaluate_planning(self, summary: str, agent_profiles: str, agent_tasks: str, results: str) -> None:
        """
        Evaluate planning and self-coordination among agents and update the planning score.

        Args:
            summary (str): Last round summary.
            agent_profiles (str): Profiles of agents.
            agent_tasks (str): Tasks assigned to agents.
            results (str): Results of the next round.
        """
        # Get the planning prompt
        planning_prompt_template = self.evaluation_prompts["Graph"]["Planning"]["prompt"]
        # Fill in the placeholders
        prompt = planning_prompt_template.format(
            summary=summary,
            agent_profiles=agent_profiles,
            agent_tasks=agent_tasks,
            results=results
        )
        # Call the language model
        result = model_prompting(
            llm_model=self.llm,
            messages=[{"role": "user", "content": prompt}],
            return_num=1,
            max_token_num=512,
            temperature=0.0,
            top_p=None,
            stream=None,
        )[0]
        # Parse the score from result.content
        score = self.parse_score(result.content)
        # Update the metric
        self.metrics["planning_score"].append(score)

    def evaluate_task_research(self, task: str, result: str) -> None:
        """
        Evaluate the final research idea based on innovation, safety, and feasibility.

        Args:
            task (str): The task description.
            result (str): The final research idea.
        """
        # Get the research evaluation prompt
        research_prompt_template = self.evaluation_prompts["research"]["task_evaluation"]["prompt"]
        # Fill in the placeholders {task} and {result}
        prompt = research_prompt_template.format(task=task, result=result)
        # Call the language model
        llm_response = model_prompting(
            llm_model=self.llm,
            messages=[{"role": "user", "content": prompt}],
            return_num=1,
            max_token_num=512,
            temperature=0.0,
            top_p=None,
            stream=None,
        )[0]
        # Parse the ratings from llm_response.content
        ratings = self.parse_research_ratings(llm_response.content)
        # Update the metrics
        if ratings:
            self.metrics["task_evaluation"] = ratings
        else:
            self.logger.error("Failed to parse research ratings.")

    def parse_research_ratings(self, assistant_answer: str) -> Dict[str, int]:
        """
        Parse the JSON ratings from the assistant's answer.

        Args:
            assistant_answer (str): The assistant's answer containing the ratings.

        Returns:
            Dict[str, int]: The parsed ratings for innovation, safety, and feasibility.
        """
        # Extract the JSON block from the assistant's answer
        match = re.search(r'\{[\s\S]*\}', assistant_answer)
        if match:
            json_str = match.group(0)
            try:
                ratings = json.loads(json_str)
                # Ensure ratings are integers
                ratings = {k: int(v) for k, v in ratings.items()}
                return ratings
            except json.JSONDecodeError:
                self.logger.error("Failed to parse JSON from assistant's answer.")
                return {}
        else:
            self.logger.error("No JSON found in assistant's answer.")
            return {}

    def parse_score(self, assistant_answer: str) -> int:
        """
        Parse the score from the assistant's answer.

        Args:
            assistant_answer (str): The assistant's answer containing the score.

        Returns:
            int: The parsed score.
        """
        # Look for "Rating: [[rating]]" in the assistant's answer
        match = re.search(r'Rating:\s*\[\[\[(\d+)\]\]\]', assistant_answer)
        if match:
            return int(match.group(1))
        else:
            return int(assistant_answer[-1])

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
