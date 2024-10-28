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
AgentGraphType = TypeVar('AgentGraphType', bound='AgentGraph')

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
        self.agent_graph: Union[None, Dict[str, str]] = None
        self.profile = config.get("profile", '')
        self.memory = BaseMemory()
        self.shared_memory = SharedMemory()
        self.relationships: Dict[str, str] = {}  # key: target_agent_id, value: relationship type
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info(f"Agent '{self.agent_id}' initialized.")
        self.token_usage = 0  # Initialize token usage
        self.msg_box: Dict[str, Dict[str, List[Tuple[int, str]]]] = defaultdict(lambda: defaultdict(list))
        self.FORWARD_TO = 0
        self.RECV_FROM = 1

    def set_agent_graph(self, agent_graph: AgentGraphType) -> None:
        self.agent_graph = agent_graph

    def perceive(self, state: Any) -> Any:
        """
        Agent perceives the environment state.

        Args:
            state (Any): The current state of the environment.

        Returns:
            Any: Processed perception data.
        """
        # For simplicity, return the task description from the state
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
        communicate_to_description = {
            "type": "function",
            "function": {
                "name": "communicate_to",
                "description": "Send a message to a specific target agent based on existing relationships",
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
                            "description": "The message to send to the target agent"
                        },
                        "session_id": {
                            "type": "string",
                            "description": "The session ID for the communication. You should use its default valye.",
                            "default": "default_session"
                        }
                    },
                    "required": ["target_agent_id", "message"],
                    "additionalProperties": False
                }
            }
        }

        tools.append(communicate_to_description)
        system_message = f"These are your memory: {self.memory}\n" \
                          "These are your chat history: {self.seralize_message()}\n" \
                          "Answering questions from other agents has higher priority than assigned task."
        result = model_prompting(
            llm_model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_message}, {"role":"user", "content": task + "Answer messages has higher priority than any task!!"}],
            return_num=1,
            max_token_num=512,
            temperature=0.0,
            top_p=None,
            stream=None,
            tools=tools,
            tool_choice="auto"
        )[0]
        import pdb; pdb.set_trace()
        if result.tool_calls:
            function_call = result.tool_calls[0]
            function_name = function_call.function.name
            assert function_name is not None
            function_args = json.loads(function_call.function.arguments)
            if function_name != "communicate_to":
                result_from_function = self.env.apply_action(agent_id=self.agent_id, action_name=function_name, arguments=function_args)
            else:
                target_agent_id = function_args["target_agent_id"]
                message = function_args["message"]
                session_id = function_args.get("session_id", "default_session")
                result_from_function = self._handle_communicate_to(target_agent_id=target_agent_id, message=message, session_id=session_id)
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
        # Simplified token count: 1 token per 4 characters (approximation)
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
        # Store the outgoing message in the message box for the target agent.
        self.msg_box[session_id][target_agent.agent_id].append((self.FORWARD_TO, message))

        # Log the action of sending the message to the target agent.
        self.logger.info(f"Agent {self.agent_id} sent message to {target_agent.agent_id}: {message}")

        # Notify the target agent that a message has been sent.
        target_agent.receive_message(session_id, self, message)

    def receive_message(self, session_id: str, from_agent: AgentType, message: str) -> None:
        """Receive a message from another agent within the specified session.

        Args:
            session_id (str): The identifier for the current session.
            from_agent (BaseAgent): The agent sending the message.
            message (str): The content of the received message.
        """
        # Store the received message in the message box for the sending agent.
        self.msg_box[session_id][from_agent.agent_id].append((self.RECV_FROM, message))

        # Log the action of receiving the message from the sender agent.
        self.logger.info(f"Agent {self.agent_id} received message from {from_agent.agent_id}: {message}")

    def seralize_message(self) -> str:
        seralized_msg = ""
        for session_id in self.msg_box:
            seralized_msg += f"In Session {session_id} \n"
            session_msg = self.msg_box[session_id]
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


    def _handle_communicate_to(self, target_agent_id: str, message: str, session_id: str = "default_session") -> Dict[str, Any]:
        """
        Handler for the communicate_to function.

        Args:
            target_agent_id (str): The ID of the target agent
            message (str): The message to send
            session_id (str): The session ID for the communication

        Returns:
            Dict[str, Any]: Result of the communication attempt
        """
        try:
            if not self.agent_graph or target_agent_id not in self.relationships:
                import pdb; pdb.set_trace()
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
            self.send_message(session_id, target_agent, message)

            return {
                "success": True,
                "message": f"Successfully sent message to agent {target_agent_id}",
                "session_id": session_id
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Error sending message: {str(e)}"
            }
