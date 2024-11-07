"""
Base agent module.
"""

import json
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple, TypeVar, Union

from marble.environments import BaseEnvironment, WebEnvironment
from marble.llms.model_prompting import model_prompting
from marble.memory import BaseMemory, SharedMemory
from marble.utils.logger import get_logger

EnvType = Union[BaseEnvironment, WebEnvironment]
AgentType = TypeVar('AgentType', bound='BaseAgent')

class BaseAgent:
    """
    Base class for all agents.
    """

    def __init__(self, config: Dict[str, Union[Any, Dict[str, Any]]], env: EnvType, shared_memory: Union[SharedMemory, None] = None):
        """
        Initialize the agent.

        Args:
            config (dict): Configuration for the agent.
            env (EnvType): Environment for the agent.
            shared_memory (BaseMemory, optional): Shared memory instance.
        """
        agent_id = config.get("agent_id")
        assert isinstance(agent_id, str), "agent_id must be a string."
        assert env is not None, "agent must has an environment."
        self.env: EnvType = env
        self.actions: List[str] = []
        self.agent_id: str = agent_id
        self.profile = config.get("profile", '')
        self.memory = BaseMemory()
        self.shared_memory = SharedMemory()
        self.relationships: Dict[str, str] = {}
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info(f"Agent '{self.agent_id}' initialized.")
        self.token_usage = 0
        self.task_history: List[str] = []
        self.msg_box: Dict[str, Dict[str, List[Tuple[int, str]]]] = defaultdict(lambda: defaultdict(list))
        self.children: List[BaseAgent] = []
        self.parent: Optional[BaseAgent] = None
        self.FORWARD_TO = 0
        self.RECV_FROM = 1

    def perceive(self, state: Any) -> Any:
        """
        Agent perceives the environment state.

        Args:
            state (Any): The current state of the environment.

        Returns:
            Any: Processed perception data.
        """
        return state.get('task_description', '')

    def act(self, task: str) -> Any:
        """
        Agent decides on an action to take.

        Args:
            task (str): The task to perform.

        Returns:
            Any: The action decided by the agent.
        """
        self.task_history.append(task)
        self.logger.info(f"Agent '{self.agent_id}' acting on task '{task}'.")
        tools = [self.env.action_handler_descriptions[name] for name in self.env.action_handler_descriptions]
        if len(tools) == 0:
            result = model_prompting(
                llm_model="gpt-3.5-turbo",
                messages=[{"role":"user", "content": task}],
                return_num=1,
                max_token_num=512,
                temperature=0.0,
                top_p=None,
                stream=None,
            )[0]
        else:
            result = model_prompting(
                llm_model="gpt-3.5-turbo",
                messages=[{"role":"user", "content": task}],
                return_num=1,
                max_token_num=512,
                temperature=0.0,
                top_p=None,
                stream=None,
                tools=tools,
                tool_choice="auto"
            )[0]

        if result.tool_calls:
            function_call = result.tool_calls[0]
            function_name = function_call.function.name
            assert function_name is not None
            function_args = json.loads(function_call.function.arguments)
            result_from_function = self.env.apply_action(agent_id=self.agent_id, action_name=function_name, arguments=function_args)
            self.memory.update(self.agent_id, {
                    "type": "action_function_call",
                    "action_name": function_name,
                    "args": function_args,
                    "result": result_from_function
                }
            )
            self.logger.info(f"Agent '{self.agent_id}' called '{function_name}' with args '{function_args}'.")
            self.logger.info(f"Agent '{self.agent_id}' obtained result '{result_from_function}'.")

        else:
            self.memory.update(self.agent_id, {
                    "type": "action_response",
                    "result": result
                }
            )
            self.logger.info(f"Agent '{self.agent_id}' acted with result '{result}'.")
        result_content = result.content if result.content else ""
        self.token_usage += self._calculate_token_usage(task, result_content)

        return result

    def _calculate_token_usage(self, task: str, result: str) -> int:
        """
        Calculate token usage based on input and output lengths.

        Args:
            task (str): The input task.
            result (str): The output result.

        Returns:
            int: The number of tokens used.
        """
        token_count = (len(task) + len(result)) // 4
        return token_count

    def get_token_usage(self) -> int:
        """
        Get the total token usage by the agent.

        Returns:
            int: The total tokens used by the agent.
        """
        return self.token_usage

    def send_message(self, session_id: str, target_agent: AgentType, message: str) -> None:
        """Send a message to the target agent within the specified session.

        Args:
            session_id (str): The identifier for the current session.
            target_agent (BaseAgent): The agent to whom the message is being sent.
            message (str): The message content to be sent.
        """
        self.msg_box[session_id][target_agent.agent_id].append((self.FORWARD_TO, message))

        self.logger.info(f"Agent {self.agent_id} sent message to {target_agent.agent_id}: {message}")

        target_agent.receive_message(session_id, self, message)

    def receive_message(self, session_id: str, from_agent: AgentType, message: str) -> None:
        """Receive a message from another agent within the specified session.

        Args:
            session_id (str): The identifier for the current session.
            from_agent (BaseAgent): The agent sending the message.
            message (str): The content of the received message.
        """
        self.msg_box[session_id][from_agent.agent_id].append((self.RECV_FROM, message))
        self.logger.info(f"Agent {self.agent_id} received message from {from_agent.agent_id}: {message}")

    def get_profile(self) -> Union[str, Any]:
        """
        Get the agent's profile.

        Returns:
            str: The agent's profile.
        """
        return self.profile

    def plan_task(self) -> Optional[str]:
        """
        Plan the next task based on the original tasks input, the agent's memory, task history, and its profile/persona.

        Returns:
            str: The next task description.
        """
        self.logger.info(f"Agent '{self.agent_id}' is planning the next task.")

        # Retrieve all memory entries for this agent
        memory_str = self.memory.get_memory_str()
        task_history_str = ", ".join(self.task_history)

        # Incorporate agent's profile/persona in decision making
        persona = self.get_profile()

        # Use memory entries, persona, and task history to determine the next task
        next_task = model_prompting(
            llm_model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Agent '{self.agent_id}' should prioritize tasks that align with their role: {persona}. Based on the task history: {task_history_str}, and memory: {memory_str}, what should be the next task?"}],
            return_num=1,
            max_token_num=512,
            temperature=0.0,
            top_p=None,
            stream=None,
            tools=[],
            tool_choice="auto"
        )[0].content
        self.logger.info(f"Agent '{self.agent_id}' plans next task based on persona: {next_task}")

        return next_task


    def _is_task_completed(self, result: Any) -> bool:
        """
        Determine if the task is completed based on the result of the last action.

        Args:
            result (Any): The result from the last action.

        Returns:
            bool: True if task is completed, False otherwise.
        """
        # Placeholder logic; implement actual completion criteria
        if isinstance(result, str):
            return "completed" in result.lower()
        return False

    def _define_next_task_based_on_result(self, result: Any) -> str:
        """
        Define the next task based on the result of the last action.

        Args:
            result (Any): The result from the last action.

        Returns:
            str: The next task description.
        """
        # Placeholder logic; implement actual task definition
        if isinstance(result, str):
            if "error" in result.lower():
                return "Retry the previous action."
            else:
                return "Proceed to the next step based on the result."
        return "Analyze the result and determine the next task."

    def _is_response_satisfactory(self, response: Any) -> bool:
        """
        Determine if the response is satisfactory.

        Args:
            response (Any): The response from the last action.

        Returns:
            bool: True if satisfactory, False otherwise.
        """
        # Placeholder logic; implement actual response evaluation
        if isinstance(response, str):
            return "success" in response.lower()
        return False

    def _define_next_task_based_on_response(self, response: Any) -> str:
        """
        Define the next task based on the response of the last action.

        Args:
            response (Any): The response from the last action.

        Returns:
            str: The next task description.
        """
        # Placeholder logic; implement actual task definition
        if isinstance(response, str):
            if "need more information" in response.lower():
                return "Gather additional information required to proceed."
            else:
                return "Address the issues identified in the response."
        return "Review the response and determine the next steps."

    def plan_tasks_for_children(self, task: str) -> Dict[str, Any]:
        """
        Plan tasks for children agents based on the given task and children's profiles.
        """
        self.logger.info(f"Agent '{self.agent_id}' is planning tasks for children.")
        children_profiles = {child.agent_id: child.get_profile() for child in self.children}
        prompt = (
            f"You are agent '{self.agent_id}'. Based on the overall task:\n{task}\n\n"
            f"And your children's profiles:\n"
        )
        for child_id, profile in children_profiles.items():
            prompt += f"- {child_id}: {profile}\n"
        prompt += "\nAssign specific tasks to your children agents to help accomplish the overall task. Provide the assignments in JSON format:\n\n"
        prompt += "{\n"
        '  "child_agent_id": "Task description",\n'
        '  "another_child_agent_id": "Task description"\n'
        "}\n"
        response = model_prompting(
            llm_model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            return_num=1,
            max_token_num=512,
            temperature=0.7,
            top_p=1.0
        )[0]
        try:
            tasks_for_children:Dict[str, Any] = json.loads(response.content if response.content else "{}")
            self.logger.info(f"Agent '{self.agent_id}' assigned tasks to children: {tasks_for_children}")
            return tasks_for_children
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse tasks for children: {e}")
            return {}

    def summarize_results(self, children_results: Dict[str, Any], own_result: Any) -> Any:
        """
        Summarize the results from children agents and own result.
        """
        self.logger.info(f"Agent '{self.agent_id}' is summarizing results.")
        summary = self.process_children_results(children_results)
        summary += f"\nOwn result: {own_result}"
        return summary

    def choose_next_agent(self, result: Any, agent_profiles: Dict[str, Dict[str, Any]]) -> Optional[str]:
        """
        Choose the next agent to pass the task to, based on the result and profiles of other agents.

        Args:
            result (Any): The result from the agent's action.
            agent_profiles (Dict[str, Dict[str, Any]]): Profiles of all other agents.

        Returns:
            Optional[str]: The agent_id of the next agent, or None if no suitable agent is found.
        """
        self.logger.info(f"Agent '{self.agent_id}' is choosing the next agent.")

        # Prepare the prompt for the LLM
        prompt = (
            f"As Agent '{self.agent_id}' with profile: {self.profile}, "
            f"you have completed your part of the task with the result:\n{result}\n\n"
            "Here are the profiles of other available agents:\n"
        )
        for agent_id, profile_info in agent_profiles.items():
            if agent_id != self.agent_id:  # Exclude self
                prompt += f"- Agent ID: {agent_id}\n"
                prompt += f"  Profile: {profile_info['profile']}\n"
        prompt += (
            "\nBased on your result and the agents' profiles, select the most suitable agent to continue the task. "
            "Provide only the Agent ID in your response."
        )

        # Use the LLM to select the next agent
        response = model_prompting(
            llm_model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            return_num=1,
            max_token_num=256,
            temperature=0.7,
            top_p=1.0
        )[0].content.strip()

        # Extract the agent ID from the response
        next_agent_id = response

        if next_agent_id in agent_profiles and next_agent_id != self.agent_id:
            self.logger.info(f"Agent '{self.agent_id}' selected '{next_agent_id}' as the next agent.")
            return next_agent_id
        else:
            self.logger.warning(f"Agent '{self.agent_id}' did not select a valid next agent.")
            return None
