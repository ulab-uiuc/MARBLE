"""
Base agent module.
"""

import json
from collections import defaultdict
from typing import Any, Dict, List, Tuple, TypeVar, Union

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
        self.msg_box: Dict[str, Dict[str, List[Tuple[int, str]]]] = defaultdict(lambda: defaultdict(list))
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
        self.logger.info(f"Agent '{self.agent_id}' acting on task '{task}'.")
        tools = [self.env.action_handler_descriptions[name] for name in self.env.action_handler_descriptions]

        # messages = self._create_strategy_messages(task)

        # result = model_prompting(
        #     llm_model="gpt-3.5-turbo",
        #     messages=messages,
        #     return_num=1,
        #     max_token_num=512,
        #     temperature=0.0,
        #     top_p=None,
        #     stream=None,
        #     tools=tools,
        #     tool_choice="auto"
        # )[0]
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

    def plan_task(self) -> str:
        """
        Plan the next task based on the initial task input and the agent's memory.

        Returns:
            str: The next task description.
        """
        self.logger.info(f"Agent '{self.agent_id}' is planning the next task.")

        # Retrieve all memory entries for this agent
        memory_entries = self.memory.get_memory_str()

        if not memory_entries:
            self.logger.info(f"Agent '{self.agent_id}' has no prior memory. Returning initial task.")
            return self.env.get_initial_task()  # Assumes the environment can provide the initial task

        # Analyze the last memory entry to decide the next task
        last_entry = memory_entries[-1]
        self.logger.debug(f"Agent '{self.agent_id}' last memory entry: {last_entry}")

        if last_entry['type'] == 'action_function_call':
            # If the last action was a function call, decide next task based on the result
            result = last_entry['result']
            if self._is_task_completed(result):
                self.logger.info(f"Agent '{self.agent_id}' determined that the task is completed.")
                return "Task Completed"  # Or some signal to indicate completion
            else:
                # Define the next task based on the result
                next_task = self._define_next_task_based_on_result(result)
                self.logger.info(f"Agent '{self.agent_id}' plans next task: {next_task}")
                return next_task

        elif last_entry['type'] == 'action_response':
            # If the last action was a direct response, decide next task based on the response
            response = last_entry['result']
            if self._is_response_satisfactory(response):
                self.logger.info(f"Agent '{self.agent_id}' found the response satisfactory. Task might be completed.")
                return "Task Completed"  # Or some signal to indicate completion
            else:
                # Define the next task based on the unsatisfactory response
                next_task = self._define_next_task_based_on_response(response)
                self.logger.info(f"Agent '{self.agent_id}' plans next task: {next_task}")
                return next_task

        else:
            self.logger.warning(f"Agent '{self.agent_id}' encountered unknown memory entry type: {last_entry['type']}")
            return "Awaiting Instructions"

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
