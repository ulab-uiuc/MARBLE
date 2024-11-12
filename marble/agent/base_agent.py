"""
Base agent module.
"""

import json
import uuid
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple, TypeVar, Union

from marble.environments import BaseEnvironment, WebEnvironment
from marble.llms.model_prompting import model_prompting
from marble.memory import BaseMemory, SharedMemory
from marble.utils.logger import get_logger

EnvType = Union[BaseEnvironment, WebEnvironment]
AgentType = TypeVar('AgentType', bound='BaseAgent')

def convert_to_str(result):
    if isinstance(result, bool):
        return str(result)  # 转为 'True' 或 'False'
    elif isinstance(result, dict):
        return json.dumps(result)  # 将字典转为JSON格式的字符串
    else:
        return str(result)  # 处理字符串和数字等其他类型

class BaseAgent:
    """
    Base class for all agents.
    """

    def __init__(self, config: Dict[str, Union[Any, Dict[str, Any]]], env: EnvType, shared_memory: Union[SharedMemory, None] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize the agent.

        Args:
            config (dict): Configuration for the agent.
            env (EnvType): Environment for the agent.
            shared_memory (BaseMemory, optional): Shared memory instance.
        """
        agent_id = config.get("agent_id")
        self.llm = model
        assert isinstance(agent_id, str), "agent_id must be a string."
        assert env is not None, "agent must has an environment."
        self.env: EnvType = env
        self.actions: List[str] = []
        self.agent_id: str = agent_id
        self.agent_graph = None
        self.profile = config.get("profile", '')
        self.system_message = (
            f"You are \"{self.agent_id}\": \"{self.profile}\"\n"
            f"As a role-playing agent, you embody a dynamic character with unique traits, motivations, and skills. "
            f"Your goal is to engage not only with users but also with other agents in the environment. "
            f"Collaborate, compete, or form alliances as you navigate through immersive storytelling and challenges. "
            f"Interact meaningfully with fellow agents, contributing to the evolving narrative and responding creatively "
            f"to their actions. Maintain consistency with your character's background and personality, and be prepared to adapt "
            f"to the evolving dynamics of the scenario. Remember, your responses should enhance the experience and encourage "
            f"user engagement while enriching interactions with other agents."
        )
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
        self.session_id: str = ''

    def set_agent_graph(self, agent_graph: Any) -> None:
        self.agent_graph = agent_graph

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
        available_agents = {}
        for agent_id_1, agent_id_2, relationship in self.agent_graph.relationships:
            if agent_id_1 != self.agent_id and agent_id_2 != self.agent_id:
                continue
            else:
                if agent_id_1 == self.agent_id:
                    profile = self.agent_graph.agents[agent_id_2].get_profile()
                    agent_id = agent_id_2
                elif agent_id_2 == self.agent_id:
                    profile = self.agent_graph.agents[agent_id_1].get_profile()
                    agent_id = agent_id_1
                available_agents[agent_id] = {
                    "profile": profile,
                    "role": f"{agent_id_1} {relationship} {agent_id_2}"
                }
        self.available_agents = available_agents
        # Create the enum description with detailed information about each agent
        agent_descriptions = [
            f"{agent_id} ({info['role']} - {info['profile']})"
            for agent_id, info in available_agents.items()
        ]
        # Add communicate_to function description
        new_communication_session_description = {
            "type": "function",
            "function": {
                "name": "new_communication_session",
                "description": "Send a message to a specific target agent based on existing relationships, and begin communication",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "target_agent_id": {
                            "type": "string",
                            "description": "The ID of the target agent to communicate with. Available agents:\n" + "\n".join([f"- {desc}" for desc in agent_descriptions]),
                            "enum": list(self.relationships.keys())  # Dynamically list available target agents
                        },
                        "message": {
                            "type": "string",
                            "description": "The initial message to send to the target agent"
                        },
                    },
                    "required": ["target_agent_id", "message"],
                    "additionalProperties": False
                }
            }
        }
        tools.append(new_communication_session_description)
        act_task = (
            f"You are {self.agent_id}: {self.profile}\n"
            f"This is your task: {task}\n"
            f"These are the ids and profiles of other agents you can interact with:\n"
            f"{agent_descriptions}"
            f"But you do not have to communcate with other agents.\n"
            f"You can also solve the task by calling other functions to solve it by yourself.\n"
            f"These are your memory: {self.memory.get_memory_str()}\n"
        )
        if len(tools) == 0:
            result = model_prompting(
                llm_model=self.llm,
                messages=[{"role":"user", "content": act_task}],
                return_num=1,
                max_token_num=512,
                temperature=0.0,
                top_p=None,
                stream=None,
            )[0]
        else:
            result = model_prompting(
                llm_model=self.llm,
                messages=[{"role":"user", "content": act_task}],
                return_num=1,
                max_token_num=512,
                temperature=0.0,
                top_p=None,
                stream=None,
                tools=tools,
                tool_choice="auto"
            )[0]
        communication = None
        result_from_function_str = None
        if result.tool_calls:
            function_call = result.tool_calls[0]
            function_name = function_call.function.name
            assert function_name is not None
            function_args = json.loads(function_call.function.arguments)
            if function_name != "new_communication_session":
                result_from_function = self.env.apply_action(agent_id=self.agent_id, action_name=function_name, arguments=function_args)
                result_from_function_str = convert_to_str(result_from_function)
            else: # function_name == "new_communication_session"
                self.session_id = uuid.uuid4() # new session id
                target_agent_id = function_args["target_agent_id"]
                message = function_args["message"]
                result_from_function = self._handle_new_communication_session(target_agent_id=target_agent_id, message=message, session_id=self.session_id, task=task, turns=5)
                result_from_function_str = convert_to_str(result_from_function)
                communication = result_from_function.get("full_chat_history", None)
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
                    "result": result.content
                }
            )
            self.logger.info(f"Agent '{self.agent_id}' acted with result '{result}'.")
        result_content = result.content if result.content else ""
        self.token_usage += self._calculate_token_usage(task, result_content)
        output = "Result from the model:" + result_content + "\n"
        if result_from_function_str:
            output += "Result from the function:" + result_from_function_str
        return output, communication


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
        self.session_id = session_id

        # Store the received message in the message box for the sending agent.
        self.msg_box[session_id][from_agent.agent_id].append((self.RECV_FROM, message))
        self.logger.info(f"Agent {self.agent_id} received message from {from_agent.agent_id}: {message[:10]}...")

    def seralize_message(self, session_id: str = "") -> str:
        seralized_msg = ""

        # Check if session_id is provided
        if session_id:
            # Serialize messages for a specific session
            session_ids = [session_id] if session_id in self.msg_box else []
        else:
            # Serialize messages for all sessions
            session_ids = self.msg_box.keys()

        for sid in session_ids:
            seralized_msg += f"In Session {sid} \n"
            session_msg = self.msg_box[sid]

            for target_agent_id in session_msg:
                msg_list = session_msg[target_agent_id]
                for direction, msg_content in msg_list:
                    if direction == self.FORWARD_TO:
                        seralized_msg += f"From {self.agent_id} to {target_agent_id}: "
                    else:
                        seralized_msg += f"From {target_agent_id} to {self.agent_id}: "
                    seralized_msg += msg_content + "\n"

        return seralized_msg


    def get_profile(self) -> Union[str, Any]:
        """
        Get the agent's profile.

        Returns:
            str: The agent's profile.
        """
        return self.profile

    def _handle_new_communication_session(self, target_agent_id: str, message: str, session_id: str, task: str, turns: int = 5) -> Dict[str, Any]:
        """
        Handler for the new communication function. This will start a session using a random uuid
        and arrage communication between two agents until matter is resolved.

        Args:
            target_agent_id (str): The ID of the target agent
            message (str): The message to send
            session_id (str): Session ID of chat between two agents
            task (str): Task of source agent
            turns (int): Maximum number of allowed turns of communication

        Returns:
            Dict[str, Any]: Result of the communication attempt
        """
        initial_communication = self._handle_communicate_to(target_agent_id, message, session_id)
        if not initial_communication["success"]:
            return initial_communication
        agents = [self.agent_graph.agents.get(target_agent_id), self]
        for t in range(turns):
            session_current_agent = agents[t % 2]
            session_current_agent_id = session_current_agent.agent_id
            session_other_agent = agents[(t + 1) % 2]
            session_other_agent_id = session_other_agent.agent_id

            agent_descriptions = [
                f"{session_other_agent_id} (session_other_agent.profile)"
            ]
            communicate_to_description = {
                "type": "function",
                "function": {
                    "name": "communicate_to",
                    "description": "Send a message to a specific target agent:" + "\n".join([f"- {desc}" for desc in agent_descriptions]),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "The initial message to send to the target agent"
                            },
                        },
                        "required": ["target_agent_id", "message"],
                        "additionalProperties": False
                    }
                }
            }

            communicate_task = (
                f"These are your memory: {session_current_agent.memory}\n"
                f"The task is: {task}. \n"
                f"Please respond to {session_other_agent_id}({session_other_agent.profile}). \n"
                f"Your previous chat history: {session_current_agent.seralize_message(session_id=self.session_id)}.\n"
                f"You should answer to this question {session_current_agent.msg_box[self.session_id][session_other_agent_id][-1][1]} using your memory, and other relevant context. \n"
                f"Return <end-of-session> if you cannot answer using information you have right now. \n"
                f"You are talking to {session_other_agent_id}. You cannot talk with anyone else.\n"
                f"From {session_current_agent_id} to {session_other_agent_id}:"
            )
            result = model_prompting(
                llm_model=self.llm,
                messages=[{"role": "system", "content": session_current_agent.system_message}, {"role":"user", "content": communicate_task}],
                return_num=1,
                max_token_num=512,
                temperature=0.0,
                top_p=None,
                stream=None,
                tools=[communicate_to_description],
                tool_choice="required"
            )[0]
            if result.tool_calls:
                function_call = result.tool_calls[0]
                function_name = function_call.function.name
                assert function_name is not None
                function_args = json.loads(function_call.function.arguments)
                if function_name == "communicate_to":
                    message = function_args["message"]
                    print(message)
                    session_current_agent._handle_communicate_to(target_agent_id=session_other_agent_id, message=message, session_id=session_current_agent.session_id)
                    if "<end-of-session>" in message:
                        break

        # summarize chat history
        system_message_summary = (
            "You are an advanced summarizer agent designed to condense and clarify the history of conversations between multiple agents. "
            "Your task is to analyze dialogues from various participants and generate a cohesive summary that captures the key points, themes, and decisions made throughout the interactions.\n\n"
            "Your primary objectives are:\n\n"
            "1. Contextual Analysis: Carefully review the entire conversation history to understand the context, including the roles of different agents and the progression of discussions.\n\n"
            "2. Identify Key Themes: Extract the main themes, topics, and significant moments in the dialogue, noting any recurring issues or points of contention.\n\n"
            "3. Summarize Conversations: Create a clear and concise summary that outlines the conversation's flow, important exchanges, decisions made, and any action items that emerged. Ensure that the summary reflects the contributions of each agent without losing the overall narrative.\n\n"
            "4. Highlight Outcomes: Emphasize any conclusions reached or actions agreed upon by the agents, providing a sense of closure to the summarized conversation.\n\n"
            "5. Engage with User Input: If the user has specific interests or focuses within the conversation, inquire to tailor the summary accordingly, ensuring it meets their needs.\n\n"
            "When composing the summary, maintain clarity, coherence, and logical organization. Your goal is to provide a comprehensive yet succinct overview that enables users to understand the essence of the multi-agent dialogue at a glance."
        )
        summary_task = (
            f"These are an chat history: {session_current_agent.seralize_message(session_id=self.session_id)}\n"
            f"Please summarize information in the chat history relevant to the task: {task}."
        )
        result = model_prompting(
            llm_model=self.llm,
            messages=[{"role": "system", "content": system_message_summary}, {"role":"user", "content": summary_task}],
            return_num=1,
            max_token_num=512,
            temperature=0.0,
            top_p=None,
            stream=None,
        )[0]
        self.memory.update(self.agent_id, {
                "type": "action_communicate",
                "action_name": "communicate_to",
                # "args": function_args,
                "result": result.content if result.content else ""
            }
        )
        return {
            "success": True,
            "message": f"Successfully completed session {session_id}",
            "full_chat_history": session_current_agent.seralize_message(session_id=self.session_id),
            "session_id": result.content if result.content else ""
        }

    def _handle_communicate_to(self, target_agent_id: str, message: str, session_id: str) -> Dict[str, Any]:
        """
        Handler for the communicate_to function.

        Args:
            target_agent_id (str): The ID of the target agent
            message (str): The message to send
            session_id (str): Session ID of chat between two agents

        Returns:
            Dict[str, Any]: Result of the communication attempt
        """
        old_session_id = self.session_id
        try:
            self.session_id = session_id
            linked_by_graph = False
            for a1_id, a2_id, rel in self.agent_graph.relationships:
                if a1_id == self.agent_id or a2_id == self.agent_id:
                    linked_by_graph = True
                    break

            if not self.agent_graph or not linked_by_graph:
                return {
                    "success": False,
                    "error": f"No relationship found with agent {target_agent_id}"
                }

            target_agent = self.agent_graph.agents.get(target_agent_id)
            if not target_agent:
                return {
                    "success": False,
                    "error": f"Target agent {target_agent_id} not found in agent graph"
                }

            # Send the message using the existing send_message method
            self.send_message(self.session_id, target_agent, message)

            return {
                "success": True,
                "message": f"Successfully sent message to agent {target_agent_id}",
                "session_id": session_id
            }

        except Exception as e:
            self.session_id = old_session_id
            return {
                "success": False,
                "error": f"Error sending message: {str(e)}"
            }
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
            llm_model=self.llm,
            messages=[{"role": "user", "content": f"Agent '{self.agent_id}' should prioritize tasks that align with their role: {persona}. Based on the task history: {task_history_str}, and memory: {memory_str}, what should be the next task?"}],
            return_num=1,
            max_token_num=512,
            temperature=0.0,
            top_p=None,
            stream=None,
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
            llm_model=self.llm,
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

    def process_children_results(self, children_results: Dict[str, Any]) -> str:
        """
        Process the results from children agents using model prompting.
        """
        prompt = "Summarize the results from children agents:\n"
        for agent_id, result in children_results.items():
            prompt += f"- Agent '{agent_id}': {result}\n"
        response = model_prompting(
            llm_model=self.llm,
            messages=[{"role": "system", "content": prompt}],
            return_num=1,
            max_token_num=512,
            temperature=0.7,
            top_p=1.0
        )[0]
        summary = response.content if response.content else ""
        return summary


    def plan_next_agent(self, result: Any, agent_profiles: Dict[str, Dict[str, Any]]) -> Tuple[Optional[str], Optional[str]]:
        """
        Choose the next agent to pass the task to and provide a planning task, based on the result and profiles of other agents.

        Args:
            result (Any): The result from the agent's action.
            agent_profiles (Dict[str, Dict[str, Any]]): Profiles of all other agents.

        Returns:
            Tuple[Optional[str], Optional[str]]: The agent_id of the next agent and the planning task, or (None, None) if no suitable agent is found.
        """
        self.logger.info(f"Agent '{self.agent_id}' is planning the next step.")

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
            "\nBased on the result and the agent profiles provided, select the most suitable agent to continue the task and provide a brief plan for the next agent to execute. "
            "Respond in the following format:\n"
            "{\"agent_id\": \"<next_agent_id>\", \"planning_task\": \"<description of the next planning task>\"}"
        )

        # Use the LLM to select the next agent and create a planning task
        response = model_prompting(
            llm_model=self.llm,
            messages=[{"role": "system", "content": prompt}],
            return_num=1,
            max_token_num=256,
            temperature=0.7,
            top_p=1.0
        )[0].content

        # Parse the response to extract the agent ID and planning task
        next_agent_id: Optional[str] = None
        planning_task: Optional[str] = None

        try:
            response_data: Dict[str, Any] = json.loads(response)
            next_agent_id = response_data.get("agent_id")
            planning_task = response_data.get("planning_task")
        except (json.JSONDecodeError, KeyError):
            self.logger.warning(f"Agent '{self.agent_id}' received an invalid response format from the LLM.")

        if next_agent_id in agent_profiles and next_agent_id != self.agent_id:
            self.logger.info(f"Agent '{self.agent_id}' selected '{next_agent_id}' as the next agent with plan: '{planning_task}'.")
            return next_agent_id, planning_task
        else:
            self.logger.warning(f"Agent '{self.agent_id}' did not select a valid next agent.")
            return None, None
