# marble/engine/engine_planner.py

"""
Engine Planner module responsible for task assignment and scheduling.
"""

import json
import re
from typing import Any, Dict, List

from litellm import token_counter
from litellm.types.utils import Message

from marble.graph.agent_graph import AgentGraph
from marble.llms.model_prompting import model_prompting
from marble.utils.logger import get_logger


def json_parse(input_str: str) -> Dict[str, Any]:
    """
    Extracts the JSON part from a string that contains a JSON block and parses it into a dictionary.

    Args:
        input_str (str): A string that includes a JSON block, for example:
            Final Output:
            ```json
            {
              "tasks": {
                "agent1": "Lead the literature review.",
                "agent2": "Contribute to brainstorming potential research ideas.",
                "agent3": "Lead the summarization of collective ideas.",
                "agent4": "Formulate a new research idea in the '5q' format.",
                "agent5": "Contribute to brainstorming potential research ideas."
              },
              "chain_of_thought": "Assign tasks based on agents' expertise and backgrounds to ensure effective collaboration and utilization of diverse skill sets.",
              "continue": true
            }
            ```

    Returns:
        Dict[str, Any]: The parsed JSON data as a dictionary.

    Raises:
        ValueError: If JSON parsing fails due to invalid format.
    """
    # Regular expression to match the content between ```json and ```
    pattern = r"```json\s*(\{.*?\})\s*```"
    match = re.search(pattern, input_str, re.DOTALL)

    if match:
        json_str = match.group(1)
    else:
        # If no code block is found, try to extract a JSON substring by looking for the first '{' and the last '}'
        start = input_str.find('{')
        end = input_str.rfind('}')
        if start != -1 and end != -1 and end > start:
            json_str = input_str[start:end+1]
        else:
            # Fallback: use the entire string as JSON
            json_str = input_str

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError("JSON parsing failed. Please check the input format.") from e

    return data


class EnginePlanner:
    """
    The EnginePlanner class handles task assignment and scheduling for agents.
    """

    def __init__(self, agent_graph: AgentGraph, memory: Any, config: Dict[str, Any], task: str, model: str = "gpt-3.5-turbo"):
        """
        Initialize the EnginePlanner.

        Args:
            agent_graph (AgentGraph): The graph of agents.
            memory (Any): Shared memory instance (an instance of SharedMemory).
            config (Dict[str, Any]): Configuration parameters.
            task (str): The overall task description.
            model (str, optional): The LLM model to use. Defaults to "gpt-3.5-turbo".
        """
        self.agent_graph = agent_graph
        self.memory = memory  # Expected to be an instance of SharedMemory.
        self.logger = get_logger(self.__class__.__name__)
        self.config = config
        self.current_progress = config.get('initial_progress', '')
        self.task = task
        self.model = model
        self.token_usage = 0
        self.logger.info("EnginePlanner initialized.")

    def create_prompt(self) -> str:
        """
        Create a base prompt for the LLM to assign tasks to agents.

        Returns:
            str: The base prompt string.
        """
        agent_profiles = self.agent_graph.get_agent_profiles()
        prompt = (
            "You are an orchestrator assigning tasks to a group of agents based on their profiles, current progress, and task description.\n\n"
            f"Task Description:\n{self.task}\n\n"
            f"Current Progress:\n{self.current_progress}\n\n"
            "Agent Profiles:\n"
        )
        for agent_id, profile in agent_profiles.items():
            prompt += f"- Agent ID: {agent_id}\n"
            prompt += f"  Relationships: {profile['relationships']}\n"
            prompt += f"  Profile: {profile['profile']}\n"

        # (The final JSON output instructions will be appended in each planning method.)
        return prompt

    def assign_tasks(self, planning_method: str = "naive") -> Dict[str, Any]:
        """
        Assign tasks to agents by interacting with the LLM using one of four planning strategies.

        Args:
            planning_method (str, optional): The planning strategy to use.
                Options are:
                  - "naive": Basic planning (default).
                  - "cot": Chain-of-Thought planning with step-by-step reasoning.
                  - "group_discuss": Each agent first proposes a subtask, then the planner synthesizes these into a final plan.
                  - "cognitive_evolve": Uses memory from previous rounds to compare expected vs. actual progress and evolve planning.
                Defaults to "naive".

        Returns:
            Dict[str, Any]: The task assignments and a continuation flag.
        """
        # ----- GROUP DISCUSSION MODE -----
        if planning_method == "group_discuss":
            agent_profiles = self.agent_graph.get_agent_profiles()
            agent_proposals = {}
            # For each agent, prompt a proposal round.
            for agent_id, profile in agent_profiles.items():
                agent_prompt = (
                    f"You are agent {agent_id} with the following profile:\n"
                    f"Profile: {profile['profile']}\n"
                    f"Relationships: {profile['relationships']}\n"
                    f"Task Description: {self.task}\n"
                    f"Current Progress: {self.current_progress}\n\n"
                    "Based on the above, please propose your next subtask. "
                    "Keep your answer concise and in plain text."
                )
                system_message_agent = f"You are agent {agent_id} providing your subtask proposal."
                messages_agent = [
                    {"role": "system", "content": system_message_agent},
                    {"role": "user", "content": agent_prompt}
                ]
                response_agent = model_prompting(
                    llm_model=self.model,
                    messages=messages_agent,
                    return_num=1,
                    max_token_num=512,
                    temperature=0.7,
                    top_p=1.0
                )
                proposal = response_agent[0].content.strip() if response_agent[0].content else ""
                agent_proposals[agent_id] = proposal
                messages_for_token = messages_agent + [{"role": "assistant", "content": proposal}]
                self.token_usage += token_counter(model=self.model, messages=messages_for_token)

            # Synthesize proposals into a final plan.
            proposals_text = ""
            for agent_id, proposal in agent_proposals.items():
                proposals_text += f"- Agent {agent_id}: {proposal}\n"

            final_prompt = (
                self.create_prompt() +
                "\nGroup Discussion Synthesis:\n" +
                "The following are the proposals from each agent:\n" +
                proposals_text +
                "\nBased on the above proposals, please synthesize a final task assignment plan for all agents. "
                "Ensure that your final output is a valid JSON object with the following format:\n\n"
                "{\n"
                '  "tasks": {\n'
                '    "agent1": "...", \n'
                '    "agent2": "..." \n'
                "  },\n"
                '  "continue": true\n'
                "}\n"
            )
            system_message_final = (
                "You are an agent planner synthesizing group discussion proposals into a final task assignment plan."
            )
            messages_final = [
                {"role": "system", "content": system_message_final},
                {"role": "user", "content": final_prompt}
            ]
            response_final = model_prompting(
                llm_model=self.model,
                messages=messages_final,
                return_num=1,
                max_token_num=1024,
                temperature=0.7,
                top_p=1.0
            )
            messages_for_token = messages_final + [{"role": "assistant", "content": response_final[0].content}]
            self.token_usage += token_counter(model=self.model, messages=messages_for_token)
            try:
                assignment: Dict[str, Any] = json_parse(response_final[0].content)
                self.logger.debug(f"Received task assignment using group discussion: {assignment}")
                return assignment
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse JSON response in group discussion: {e}")
                return {"tasks": {}, "continue": False}

        # ----- COGNITIVE EVOLVE MODE -----
        elif planning_method == "cognitive_evolve":
            # Retrieve memory information using SharedMemory methods.
            memory_info = ""
            if self.memory:
                evolving_experiences = self.memory.retrieve("evolving_experiences") or "None"
                expected_result = self.memory.retrieve("expected_result") or "None"
                expected_progress = self.memory.retrieve("expected_progress") or "None"
                memory_info += "Memory Information:\n"
                memory_info += f"- Previous evolving experiences: {evolving_experiences}\n"
                memory_info += f"- Previous expected result: {expected_result}\n"
                memory_info += f"- Previous expected progress: {expected_progress}\n"

            cognitive_prompt = (
                self.create_prompt() +
                ("\n" + memory_info if memory_info else "\n") +
                "\nCognitive Evolution Instructions:\n"
                "Reflect on the current progress and, if available, compare it with the previous expected result and expected progress. "
                "Based on this reflection, propose improved task assignments for each agent. Additionally, generate an 'expected_result' "
                "and 'expected_progress' for this round, and provide any 'evolving_experiences' that may help refine future planning. "
                "Ensure that your final output is a valid JSON object with the following format:\n\n"
                "{\n"
                '  "tasks": {\n'
                '    "agent1": "...", \n'
                '    "agent2": "..." \n'
                "  },\n"
                '  "expected_result": "...",\n'
                '  "expected_progress": "...",\n'
                '  "evolving_experiences": "...",\n'
                '  "continue": true\n'
                "}\n"
            )
            system_message = (
                "You are a cognitively evolving task planner. Use previous experiences and current progress to refine your planning strategy."
            )
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": cognitive_prompt}
            ]
            response = model_prompting(
                llm_model=self.model,
                messages=messages,
                return_num=1,
                max_token_num=1024,
                temperature=0.7,
                top_p=1.0
            )
            messages_for_token = messages + [{"role": "assistant", "content": response[0].content}]
            self.token_usage += token_counter(model=self.model, messages=messages_for_token)
            try:
                assignment: Dict[str, Any] = json_parse(response[0].content)
                self.logger.debug(f"Received task assignment using cognitive evolve: {assignment}")
                # Update memory with new expected values and evolving experiences using SharedMemory methods.
                if self.memory:
                    self.memory.update("expected_result", assignment.get("expected_result", ""))
                    self.memory.update("expected_progress", assignment.get("expected_progress", ""))
                    self.memory.update("evolving_experiences", assignment.get("evolving_experiences", ""))
                return assignment
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse JSON response in cognitive evolve: {e}")
                return {"tasks": {}, "continue": False}

        # ----- CHAIN-OF-THOUGHT (cot) MODE -----
        elif planning_method == "cot":
            base_prompt = self.create_prompt()
            prompt = base_prompt + (
                "\nChain-of-Thought Instructions:\n"
                "Before providing the final task assignments, think through the process step by step. "
                "Explain your reasoning process, taking into account each agent's capabilities and relationships. "
                "For example, if the task were to organize an event, you might reason: "
                "'Step 1: Choose a venue based on agent expertise; Step 2: Delegate invitations; Step 3: Plan the schedule.'\n"
                "After your reasoning, please provide your final output in a valid JSON format that includes the following keys:\n"
                '  "tasks": { "agent1": "...", "agent2": "..." },\n'
                '  "chain_of_thought": "Your reasoning process here",\n'
                '  "continue": true\n'
            )
            system_message = (
                "You are a chain-of-thought task assignment system. Please detail your reasoning step by step and include your thought process in the final JSON output."
            )
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]
            response = model_prompting(
                llm_model=self.model,
                messages=messages,
                return_num=1,
                max_token_num=1024,
                temperature=0.7,
                top_p=1.0
            )
            messages_for_token = messages + [{"role": "assistant", "content": response[0].content}]
            self.token_usage += token_counter(model=self.model, messages=messages_for_token)
            response_json = json_parse(response[0].content)
            self.logger.debug(f"Received task assignment using chain-of-thought planning: {response}")
            return response_json

        # ----- NAIVE MODE (DEFAULT) -----
        else:
            base_prompt = self.create_prompt()
            prompt = base_prompt + (
                "\nBased on the above, assign the next task to each agent that needs to perform an action.\n"
                "Provide the assignments in the following JSON format:\n\n"
                "{\n"
                '  "tasks": {\n'
                '    "agent1": "...", \n'
                '    "agent2": "..." \n'
                "  },\n"
                '  "continue": true\n // Set to false if the task is completed\n'
                "}\n"
            )
            system_message = (
            "You are a task assignment system for multiple AI agents based on their profiles and current progress.\n"
            "Your task is to analyze the current state and assign the next task to each agent that requires an action.\n"
            "Don't ask agents to assign tasks to other agents.\n"
        )
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]
            response = model_prompting(
                llm_model=self.model,
                messages=messages,
                return_num=1,
                max_token_num=1024,
                temperature=0.7,
                top_p=1.0
            )
            messages_for_token = messages + [{"role": "assistant", "content": response[0].content}]
            self.token_usage += token_counter(model=self.model, messages=messages_for_token)
            try:
                assignment: Dict[str, Any] = json_parse(response[0].content)
                #assignment: Dict[str, Any] = json.loads(response[0].content if response[0].content else "")
                self.logger.debug(f"Received task assignment using naive planning: {assignment}")
                return assignment
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse JSON response in naive mode: {e}")
                return {"tasks": {}, "continue": False}

    def update_progress(self, summary: str) -> None:
        """
        Update the current progress based on the agents' outputs.

        Args:
            summary (str): Summary of the latest iteration.
        """
        self.current_progress += f"\n{summary}"
        self.logger.debug(f"Updated progress: {self.current_progress}")

    def summarize_output(self, summary:str, task:str, output_format:str) -> Message:
        """
        Summarize the output of the agents.

        Args:
            summary (str): Summary of the latest iteration.

        Returns:
            str: The summarized output.
        """
        response = model_prompting(
            llm_model=self.model,
            messages=[{"role": "user", "content": f"Summarize the output of the agents for the task: {task}\n\nNow here is some result of thr agent: {summary}, please analyze it. Return the final output into a json following the format: {output_format}"}],
            return_num=1,
            max_token_num=1024,
            temperature=0.0,
            top_p=None,
            stream=None
        )[0]
        self.token_usage += token_counter(model=self.model, messages=[{"role": "user", "content": f"Summarize the output of the agents for the task: {task}\n\nNow here is some result of thr agent: {summary}, please analyze it. Return the final output into a json following the format: {output_format}"}, {"role": "assistant", "content": response.content}])
        return response

    def decide_next_step(self, agents_results: List[Dict[str, Any]]) -> bool:
        """
        Decide whether to continue or terminate the simulation based on agents' results.

        Args:
            agents_results (List[Dict[str, Any]]): The results from all agents.

        Returns:
            bool: True to continue, False to terminate.
        """
        prompt = (
            "Based on the following agents' results, determine whether the overall task is completed.\n\n"
            f"Task Description:\n{self.task}\n\n"
            "Agents' Results:\n"
        )
        for result in agents_results:
            prompt += f"- {result}\n"[:500]

        prompt += (
            "\nRespond with a JSON object containing a single key 'continue' set to true or false.\n"
            "Sometimes the results may include a key 'success' with a value of true, but that only indicates the tool executed successfully, "
            "not that the task is complete.\n"
            "If there meets an error of the results and unfinished, please respond with a JSON object containing a single key 'continue' set to True.\n"
            "Analyze the results and decide whether the task should continue or be terminated.\n"
            "Example:\n"
            "{\n"
            '  "continue": true\n'
            "}"
        )

        messages = [{"role": "system", "content": prompt}]
        response = model_prompting(
            llm_model=self.model,
            messages=messages,
            return_num=1,
            max_token_num=256,
            temperature=0.3,
            top_p=1.0
        )
        messages_for_token = messages + [{"role": "assistant", "content": response[0].content}]
        self.token_usage += token_counter(model=self.model, messages=messages_for_token)
        try:
            # decision = json.loads(response[0].content if response[0].content else "")
            decision = json_parse(response[0].content)
            self.logger.debug(f"Received continuation decision: {decision}")
            return decision.get("continue", False)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON decision response: {e}")
            return False
