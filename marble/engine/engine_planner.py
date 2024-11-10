# marble/engine/engine_planner.py

"""
Engine Planner module responsible for task assignment and scheduling.
"""

import json
from typing import Any, Dict, List

from litellm.types.utils import Message

from marble.graph.agent_graph import AgentGraph
from marble.llms.model_prompting import model_prompting
from marble.utils.logger import get_logger


class EnginePlanner:
    """
    The EnginePlanner class handles task assignment and scheduling for agents.
    """

    def __init__(self, agent_graph: AgentGraph, memory: Any, config: Dict[str, Any], task:str):
        """
        Initialize the EnginePlanner.

        Args:
            agent_graph (AgentGraph): The graph of agents.
            memory (Any): Shared memory instance.
            config (Dict[str, Any]): Configuration parameters.
        """
        self.agent_graph = agent_graph
        self.memory = memory
        self.logger = get_logger(self.__class__.__name__)
        self.config = config
        self.current_progress = config.get('initial_progress', '')
        self.task = task
        self.logger.info("EnginePlanner initialized.")

    def create_prompt(self) -> str:
        """
        Create a prompt for the LLM to assign tasks to agents.

        Returns:
            str: The prompt string.
        """
        agent_profiles = self.agent_graph.get_agent_profiles()
        prompt = (
            "You are an orchestrator assigning tasks to a group of agents based on their profiles and current progress and task description.\n\n"
            f"Task Description:\n{self.task}\n\n"
            f"Current Progress: {self.current_progress}\n\n"
            "Agent Profiles:\n"
        )
        for agent_id, profile in agent_profiles.items():
            prompt += f"- Agent ID: {agent_id}\n"
            prompt += f"  Relationships: {profile['relationships']}\n"
            prompt += f"  Profile: {profile['profile']}\n"

        prompt += (
            "Based on the current progress and agent profiles, assign the next task to each agent that needs to perform an action.\n"
            "Provide the assignments in the following JSON format:\n\n"
            "{\n"
            '  "tasks": {\n'
            '    "agent1": "...", \n'
            '    "agent2": "...", \n'
            '    // Add more agents as needed\n'
            '  },\n'
            '  "continue": true // Set to false if the task is completed\n'
            "}\n\n"
            "If an agent does not need to be assigned a task, you can omit it from the 'tasks' section.\n"
        )
        self.logger.debug(f"Created prompt for task assignment:\n{prompt}")
        return prompt

    def assign_tasks(self) -> Dict[str, Any]:
        """
        Assign tasks to agents by interacting with the LLM.

        Returns:
            Dict[str, Any]: The task assignments and continuation flag.
        """
        prompt = self.create_prompt()
        system_message = (
            "You are a task assignment system for multiple AI agents based on their profiles and current progress.\n"
            "Your task is to analyze the current state and assign the next task to each agent that requires an action.\n"
            "Don't ask agents to assign tasks to other agents.\n"
        )
        messages = [{"role": "system", "content": system_message}, {"role": "user", "content": prompt}]
        response = model_prompting(
            llm_model="gpt-3.5-turbo",
            messages=messages,
            return_num=1,
            max_token_num=1024,
            temperature=0.7,
            top_p=1.0
        )

        try:
            assignment:Dict[str, Any] = json.loads(response[0].content if response[0].content else "")
            self.logger.debug(f"Received task assignment: {assignment}")
            return assignment
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON response: {e}")
            return {"tasks": {}, "continue": False}

    def update_progress(self, summary: str) -> None:
        """
        Update the current progress based on the agents' outputs.

        Args:
            summary (str): Summary of the latest iteration.
        """
        self.current_progress += f"\n{summary}"
        self.logger.debug(f"Updated progress: {self.current_progress}")

    def summarize_output(self, summary:str, task:str) -> Message:
        """
        Summarize the output of the agents.

        Args:
            summary (str): Summary of the latest iteration.

        Returns:
            str: The summarized output.
        """
        response = model_prompting(
            llm_model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Summarize the output of the agents for the task: {task}\n\nNow here is some result of thr agent: {summary}, please summarize it."}],
            return_num=1,
            max_token_num=1024,
            temperature=0.0,
            top_p=None,
            stream=None
        )[0]
        return response

    def decide_next_step(self, agents_results: List[Dict[str, Any]]) -> bool:
        """
        Decide whether to continue or terminate the simulation based on agents' results.

        Args:
            agents_results (Dict[str, Any]): The results from all agents.

        Returns:
            bool: True to continue, False to terminate.
        """
        prompt = (
            "Based on the following agents' results, determine whether the overall task is completed.\n\n"
            "Agents' Results:\n"
        )
        for result in agents_results:
            prompt += f"- {result}\n"

        prompt += (
            "\nRespond with a JSON object containing a single key 'continue' set to true or false.\n"
            "Example:\n"
            "{\n"
            '  "continue": true\n'
            "}"
        )

        messages = [{"role": "system", "content": prompt}]
        response = model_prompting(
            llm_model="gpt-3.5-turbo",
            messages=messages,
            return_num=1,
            max_token_num=256,
            temperature=0.3,
            top_p=1.0
        )

        try:
            decision = json.loads(response[0].content if response[0].content else "")
            self.logger.debug(f"Received continuation decision: {decision}")
            bool_decision:bool = decision.get("continue", False)
            return bool_decision
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON decision response: {e}")
            return False
