import json
import logging
import logging
import os
import time
from typing import Any, Dict

from typing import Any, Dict

import yaml
import logging
from typing import Any, Dict
from marble.utils.eventbus import EventBus # 假设 BaseAgent 在 base_agent_module 中
from openai import OpenAI


class WerewolfAgent:
    """
    WerewolfAgent class without calling BaseAgent's __init__.
    """

    def __init__(self, config: Dict[str, Any], role: str, log_path: str, event_bus: EventBus, 
                shared_memory: Dict[str, Any], env: any, number: int, is_villager: bool, strategy="independent",):
        """
        Custom initialization for WerewolfAgent without calling BaseAgent's __init__.

        Args:
            config (dict): Configuration for the agent.
            role (str): Role of the agent (e.g., "wolf", "villager", "prophet", "witch", "guard").
            log_path (str): Path where the game log will be stored.
            event_bus (EventBus): The event bus for subscribing and publishing events.
            shared_memory: Reference to the shared memory dict.
            env (WerewolfEnv): The environment instance associated with the agent.
            number (int): Agent's unique number in the game.
            is_villager (bool): Whether the agent is a villager or not. Determines which configuration to use.
        """
        # Load different configurations based on `is_villager`
        config_key = "villager_config" if is_villager else "werewolf_config"
        model_config = config.get(config_key, {})
        self.config = config
        # Get and save API configuration details as attributes
        self.base_url = model_config.get("base_url", "https://api.openai.com/v1")  # Default to OpenAI API
        self.api_key = model_config.get("api_key", config.get("openai_api_key"))  # Default to using general OpenAI API key
        self.model_name = model_config.get("model_name", "gpt-4o")  # Default to GPT-4
        self.strategy = strategy
        # Initialize the API client
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )
        
        self.agent_id = config.get("agent_id")
        self.id = self.agent_id
        assert isinstance(self.agent_id, str), "agent_id must be a string"

        self.role = role  # Set the role
        self.agent_number = number
        self.is_villager = is_villager  # Save whether the agent is a villager
        
        # Save the environment instance
        self.env = env
        # Shared memory file path
        self.shared_memory = shared_memory
        
        # Create an independent logger
        self.logger = self._create_logger(self.agent_id)

        # Set the log file path
        self.log_file_path = os.path.join(log_path, f"{self.agent_number}-{self.role}-{self.agent_id}_log.txt")
        self._initialize_log_file()

        # Print to terminal and write to log file
        init_message = (
            f"{self.role} agent '{self.agent_id}' initialized with role '{self.role}', "
            f"using model '{self.model_name}', base URL '{self.base_url}'"
        )
        self._log_and_save(init_message)

        # Subscribe to events
        event_bus.subscribe(self, self.receive_communication)

        # Save event_bus reference for easy event publishing
        self.event_bus = event_bus

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the agent's key information into a JSON-serializable dictionary.
        Excludes external references such as event_bus, shared_memory, env, etc.
        """
        return {
            "role": self.role,
            "is_villager": self.is_villager,
            "number": self.agent_number,
            "config": self.config,
        }
    
    @classmethod
    def from_dict(
        cls, 
        agent_data: Dict[str, Any],
        log_path: str,
        event_bus: EventBus,
        shared_memory: Dict[str, Any],
        env: Any,
        strategy="independent"
    ) -> "WerewolfAgent":
        """
        Given serialized data (agent_data), along with new event_bus / shared_memory / env,
        create an equivalent WerewolfAgent.
        """
        role = agent_data["role"]
        is_villager = agent_data["is_villager"]
        number = agent_data["number"]
        # Directly extract the original config
        config = agent_data["config"]
        
        new_agent = cls(
            config=config,
            role=role,
            log_path=log_path,
            event_bus=event_bus,
            shared_memory=shared_memory,
            env=env,
            number=number,
            is_villager=is_villager,
            strategy=strategy
        )
        return new_agent
    
    def _create_logger(self, agent_id: str):
        """
        Creates and returns an independent logger for each instance.

        Args:
            agent_id (str): The current Agent's ID.

        Returns:
            logging.Logger: A logger associated with the agent_id.
        """
        logger = logging.getLogger(agent_id)
        logger.setLevel(logging.INFO)

        # Set handlers and formatter
        handler = logging.StreamHandler()  # Output to terminal
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # Add handler if not already added
        if not logger.handlers:  # Avoid adding duplicate handlers
            logger.addHandler(handler)

        return logger

    def _initialize_log_file(self) -> None:
        """
        Initializes the log file. If the file does not exist, it creates one without writing any content.
        """
        if not os.path.exists(self.log_file_path):
            with open(self.log_file_path, 'w', encoding='utf-8') as log_file:
                pass  # Create an empty log file without writing anything

    def _log_and_save(self, log_entry: str) -> None:
        """
        Outputs log information to the terminal and saves it to the log file.

        Args:
            log_entry (str): The log message to be recorded and saved.
        """
        # Output to terminal
        self.logger.info(log_entry)

        # Write the log entry to the log file
        with open(self.log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(log_entry + "\n")

    def _write_log_entry(self, log_entry: str) -> None:
        """
        Only saves the log information to the log file, without outputting to the terminal.

        Args:
            log_entry (str): The log message to be saved.
        """
        # Write the log entry to the log file without outputting to the terminal
        with open(self.log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(log_entry + "\n")


    def act(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Agent takes an action based on the received event.

        Args:
            event (Dict[str, Any]): The event that triggers an action.

        Returns:
            Dict: The action event dictionary decided by the agent.
        """

        event_type = event.get("event_type", "")
        reply_event_type = f"reply_{event_type}"  # Format the event type as reply_<event_type>

        # Initialize result as no_action in expected event format
        result = {"event_type": "reply_no_action", "sender": self.agent_id, "recipients": [], "content": {}}
        result_content = {}
        
        # Special processing for werewolf-related events
        if event_type in ["werewolf_action", "werewolf_discussion"]:
            try:
                result_content = self._wolf_action(event)  # Get werewolf action content
                result = {
                    "event_type": "reply_werewolf_action",  # Formatted event type
                    "sender": self.agent_id,
                    "recipients": [self.env],  # The recipient is the system
                    "content": result_content.get("action", "no action")  # Event content is inside the content field
                }
            except Exception as e:
                self.logger.error(f"Error while performing action {event_type}: {e}")
                result["content"] = {"error": str(e)}
        else:
            try:
                # Call a general method for other events
                result_content = self._perform_action(event)
                result = {
                    "event_type": reply_event_type,  # Formatted event type
                    "sender": self.agent_id,
                    "recipients": [self.env],
                    "content": result_content.get("action", "no action")
                }
            except Exception as e:
                self.logger.error(f"Error while performing action {event_type}: {e}")
                result["content"] = {"error": str(e)}

        self._write_log_entry(str(result_content))

        return result

    def receive_communication(self, event: Dict[str, Any], debug: bool = False) -> None:
        """
        Receive communication (from EventBus) and process the event.

        Args:
            event (Dict[str, Any]): The event data received (e.g., other players' actions, state updates).
            debug (bool): If True, enables detailed debug logging.
        """
        if debug:
            self.logger.info(f"Agent {self.agent_id} received event: {event}")

        # Check if the agent is one of the recipients of the event
        recipients = event.get("recipients", [])
        if self not in recipients:
            if debug:
                self.logger.info(f"Agent {self.agent_id} ignored event '{event.get('event_type')}' as it is not a recipient.")
            return  # Event is not for this agent, no need to process

        # Log event processing
        if debug:
            self.logger.info(f"Agent {self.agent_id} processing event '{event.get('event_type')}'. Recipients: {recipients}")

        # Check if the agent is in the list of alive players
        alive_players = self.shared_memory["public_state"].get("alive_players", [])
        if self.agent_id not in alive_players:
            if debug:
                self.logger.info(f"Agent {self.agent_id} ignored event '{event.get('event_type')}' as it is not in the alive players list.")
            return  # If agent is not in the alive players list, do not process

        # Log alive status
        if debug:
            self.logger.info(f"Agent {self.agent_id} is in the alive players list: {alive_players}")

        # Check if the event type requires special conditions
        event_type = event.get("event_type")
        if event_type in ["decide_speech_order", "decide_badge_flow"]:
            badge_count = self.shared_memory["private_state"]["players"][self.agent_id]["status"].get("badge_count", 0)
            if badge_count != 1:
                if debug:
                    self.logger.info(f"Agent {self.agent_id} ignored event '{event_type}' as it does not have the badge (badge_count: {badge_count}).")
                return
            if debug:
                self.logger.info(f"Agent {self.agent_id} processing special event '{event_type}' with badge_count: {badge_count}.")

        # Perform the action and return the action
        if debug:
            self.logger.info(f"Agent {self.agent_id} preparing to act on event '{event_type}'.")
        action = self.act(event)
        if debug:
            self.logger.info(f"Agent {self.agent_id} generated action: {action}")

        # Publish the action
        self._publish_action(action)
        if debug:
            self.logger.info(f"Agent {self.agent_id} published action: {action}")

    def _publish_action(self, action: str) -> None:
        """
        Publish the action decided by the agent.

        Args:
            action (str): The action to publish.
        """
        self.event_bus.publish(action)

    def gpt_tool_call(self, messages, tools):
        """
        Calls the GPT model using the specified messages and tools.
        
        Args:
            messages (list): A list of message dictionaries to send to the model.
            tools (list): A list of tool definitions to provide to the model.
            
        Returns:
            list: Tool calls generated by the model.
        """
        rounds = 0
        while True:
            rounds += 1
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,  # Use self.model_name instead of hardcoded model name
                    messages=messages,
                    tools=tools,
                    tool_choice="required",
                    temperature=0.7,  # Set temperature to 0.7 for more diverse results
                    n=1,
                )
                tool_calls = response.choices[0].message.tool_calls
                return tool_calls
            except Exception as e:
                print(f"Chat Generation Error: {e}")
                time.sleep(5)
                if rounds > 3:
                    raise Exception("Chat Completion failed too many times")

    def _wolf_action(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process werewolf-specific actions based on the event type (werewolf_action or werewolf_discussion).

        Args:
            event (Dict[str, Any]): The event data received (with event_type "werewolf_action" or "werewolf_discussion").
        """
        # Step 1: Get the event type
        event_type = event.get("event_type", "")

        # Step 2: Define YAML template path
        yaml_paths = {
            "werewolf_action": r"marble\agent\werewolf_prompts\werewolf_action.yaml",
            "werewolf_discussion": r"marble\agent\werewolf_prompts\werewolf_discussion.yaml"
        }
        yaml_path = yaml_paths.get(event_type, None)
        if not yaml_path:
            self.logger.error(f"Invalid event type for werewolf action: {event_type}")
            return {"action": "no_action", "target": None}

        # Step 3: Load YAML template
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                action_template = yaml.safe_load(f)
            prompt_template = action_template.get('user', '')
            tools = action_template.get('tools', [])
        except Exception as e:
            self.logger.error(f"Failed to load prompt template for {event_type}: {e}")
            return {"action": "no_action", "target": None}

        # Step 4: Retrieve game state from shared memory
        try:
            public_state = self.shared_memory.get("public_state", {})
            private_state = self.shared_memory.get("private_state", {}).get("players", {}).get(self.agent_id, {})
            personal_event_log = private_state.get("personal_event_log", "")

            # Build game state (from public_state)
            game_state = {
                "days": public_state.get("days", 0),
                "day/night": public_state.get("day/night", "night"),
                "alive_players": public_state.get("alive_players", []),
                "sheriff": public_state.get("sheriff", None)
            }

            # Use personal event log as the base for werewolf discussion
            public_chat = personal_event_log
        except Exception as e:
            self.logger.error(f"Error retrieving game state or personal event log from shared memory: {e}")
            return {"action": "no_action", "target": None}

        # Step 5: Fill in the prompt for werewolf_action and werewolf_discussion
        filled_prompt = ""

        # Werewolf Action: First time choosing a target
        if event_type == "werewolf_action":
            # Get current night's alive player information
            player_info = event["content"]["player_info"]
            alive_players_str = player_info["alive_players"]
            alive_werewolves_str = player_info["alive_werewolves"]

            # Fill in the specific information for werewolf action
            filled_prompt = prompt_template.replace("<<public_chat>>", public_chat)
            filled_prompt = filled_prompt.replace("<<game_state>>", json.dumps(game_state, indent=2))
            filled_prompt = prompt_template.replace("<<player info>>", f"Alive players: {alive_players_str}\nAlive werewolves: {alive_werewolves_str}")

        # Werewolf Discussion: Unified target
        elif event_type == "werewolf_discussion":
            # Get alive players, alive werewolves, and last round's target information
            player_info = event.get("content", {}).get("allies_info", {})
            alive_players_str = player_info.get("alive_players", "")
            alive_werewolves_str = player_info.get("alive_werewolves", "")
            last_round_targets = player_info.get("last_round_targets", {})
            rounds_remaining = event.get("content", {}).get("rounds_remaining")
            # Format the last_round_targets string
            last_round_targets_str = "\n".join(f"{wolf_id}: {target}" for wolf_id, target in last_round_targets.items())

            # Fill in the specific information for werewolf discussion
            filled_prompt = prompt_template.replace("<<public_chat>>", public_chat)
            filled_prompt = filled_prompt.replace("<<game_state>>", json.dumps(game_state, indent=2))
            filled_prompt = filled_prompt.replace("<<player info>>", f"Alive players: {alive_players_str}\nAlive werewolves: {alive_werewolves_str}\nLast round targets:\n{last_round_targets_str}")
            filled_prompt = filled_prompt.replace("<<rounds_remaining>>", str(rounds_remaining))

        # Step 6: Prepare the message content to pass to the tool
        messages = [
            {'role': 'system', 'content': action_template.get('system', '')},
            {'role': 'user', 'content': filled_prompt}
        ]

        # Step 7: Call GPT tool to decide the action
        try:
            tool_calls = json.loads(self.gpt_tool_call(messages, tools)[0].function.arguments)
            return tool_calls
        except Exception as e:
            self.logger.error(f"Error during {event_type}'s tool call: {e}")
            return {"action": "no_action", "target": None}

    def _perform_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generalized action based on the action type.

        Args:
            action (Dict[str, Any]): The action dict, which includes "event_type" (e.g., "witch_action", "guard_action", "seer_action")
            action (Dict[str, Any]): The action dict, which includes "event_type" (e.g., "witch_action", "guard_action", "seer_action")
                                    and other relevant details like "night_info", "content", etc.

        Returns:
            Dict[str, Any]: The action decided by the LLM tool.
        """
        # Step 1: Get the event type from the action dictionary
        event_type = action.get("event_type", "")


        # Step 2: Define YAML path based on the action type
        yaml_paths = {
            "witch_action": r"marble\agent\werewolf_prompts\witch_prompt.yaml",
            "guard_action": r"marble\agent\werewolf_prompts\guard_prompt.yaml",
            "run_for_sheriff": r"marble\agent\werewolf_prompts\run_for_sheriff.yaml",
            "sheriff_speech": r"marble\agent\werewolf_prompts\sheriff_speech.yaml",
            "vote_for_sheriff": r"marble\agent\werewolf_prompts\vote_for_sheriff.yaml",
            "decide_speech_sequence": r"marble\agent\werewolf_prompts\decide_speech_sequence.yaml",
            "seer_action": r"marble\agent\werewolf_prompts\seer_prompt.yaml",
            "player_speech": r"marble\agent\werewolf_prompts\speech_prompt.yaml",
            "vote_action": r"marble\agent\werewolf_prompts\vote_prompt.yaml",
            "last_words": r"marble\agent\werewolf_prompts\last_word_prompt.yaml",
            "badge_flow": r"marble\agent\werewolf_prompts\badge_flow.yaml"
        }
        yaml_path = yaml_paths.get(event_type, None)

        if not yaml_path:
            self.logger.error(f"Invalid event type: {event_type}")
            return {"action": "no_action", "target": None}

        # Step 3: Load the prompt template and tools for the given action from YAML
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                action_template = yaml.safe_load(f)
            prompt_template = action_template.get('user', '')
            tools = action_template.get('tools', [])
        except Exception as e:
            self.logger.error(f"Failed to load prompt template for event {event_type}: {e}")
            return {"action": "no_action", "target": None}

        # Step 4: Read from shared memory (public and private)
        try:
                    
            public_state = self.shared_memory.get("public_state", {})
            private_state = self.shared_memory.get("private_state", {}).get("players", {}).get(self.agent_id, {})
            personal_event_log = private_state.get("personal_event_log", "")

            # Build game state (from public_state)
            game_state = {
                "days": public_state.get("days", 0),
                "day/night": public_state.get("day/night", "night"),
                "alive_players": public_state.get("alive_players", []),
                "sheriff": public_state.get("sheriff", None)
            }

            # Use personal event log for private chat
            public_chat = personal_event_log
        except Exception as e:
            self.logger.error(f"Error retrieving game state or personal event log from shared memory: {e}")
            return {"action": "no_action", "target": None}

        # Step 5: Handle specific event types

        # For Witch Action
        if event_type == "witch_action":
            # Fetch night info (who was killed) from the action content
            night_info = f"Tonight, {action['content'].get('night_info', 'nobody')} was killed."

            # Get alive players
            alive_players = public_state.get("alive_players", [])
            alive_players_str = ", ".join(alive_players)

            # Get witch status for poison and antidote info
            status = self.shared_memory["private_state"]["players"][self.agent_id]["status"]
            poison_count = status.get("poison_count", 0)
            antidote_count = status.get("antidote_count", 0)

            # Generate poison and antidote info strings
            poison_info = f"You have {poison_count} poison potion(s) left."
            antidote_info = f"You have {antidote_count} antidote potion(s) left."

            # Fill in specific placeholders for witch_action
            filled_prompt = prompt_template.replace("<<public_chat>>", public_chat)
            filled_prompt = filled_prompt.replace("<<game_state>>", json.dumps(game_state, indent=2))
            filled_prompt = filled_prompt.replace("<<night info>>", night_info)
            filled_prompt = filled_prompt.replace("<<poison info>>", poison_info)
            filled_prompt = filled_prompt.replace("<<antidote info>>", antidote_info)
            filled_prompt = filled_prompt.replace("<<Player alive info>>", alive_players_str)

        # For Guard Action
        elif event_type == "guard_action":
            # Get alive players
            alive_players = public_state.get("alive_players", [])
            alive_players_str = ", ".join(alive_players)

            # Get previous protected target (if any) from status or shared memory
            last_protected = private_state.get("last_protected", None)

            # Generate night info for guard
            night_info = f"Tonight, you can protect one player from the werewolves. You cannot protect {last_protected} if you protected them last night."

            # Fill in specific placeholders for guard_action
            filled_prompt = prompt_template.replace("<<public_chat>>", public_chat)
            filled_prompt = filled_prompt.replace("<<game_state>>", json.dumps(game_state, indent=2))
            filled_prompt = filled_prompt.replace("<<night info>>", night_info)
            filled_prompt = filled_prompt.replace("<<player_alive_info>>", alive_players_str)

        # For Seer Action
        elif event_type == "seer_action":
            # Fetch previous night info (who was checked and the result)
            night_info = "\n".join([f"Night {n}: Checked {info['player']} - {info['result']}"
                                    for n, info in enumerate(action['content'].get('night_info', []), 1)])

            # Get alive players
            alive_players = public_state.get("alive_players", [])
            alive_players_str = ", ".join(alive_players)

            # Fill in specific placeholders for seer_action
            filled_prompt = prompt_template.replace("<<public_chat>>", public_chat)
            filled_prompt = filled_prompt.replace("<<game_state>>", json.dumps(game_state, indent=2))
            filled_prompt = filled_prompt.replace("<<night info>>", night_info)
            filled_prompt = filled_prompt.replace("<<player_alive_info>>", alive_players_str)

        # For Run for Sheriff Action
        elif event_type == "run_for_sheriff":
            # Fill in specific placeholders for run_for_sheriff
            filled_prompt = prompt_template.replace("<<public_chat>>", public_chat)
            filled_prompt = filled_prompt.replace("<<game_state>>", json.dumps(game_state, indent=2))

        # For Sheriff Speech Action
        elif event_type == "sheriff_speech":
            # Fetch election info (who spoke before and their content)
            election_info = action['content'].get('election_info', "No speeches available yet. You are the first one.")

            # Get speech position
            speech_position = action['content'].get('speech_position', 'unknown')
            speech_sequence = action['content'].get('speech_sequence', 'unknown')
            # Fill in specific placeholders for sheriff_speech
            filled_prompt = prompt_template.replace("<<public_chat>>", public_chat)
            filled_prompt = filled_prompt.replace("<<game_state>>", json.dumps(game_state, indent=2))
            filled_prompt = filled_prompt.replace("<<election_info>>", election_info)
            filled_prompt = filled_prompt.replace("<<speech_sequence>>", speech_sequence)
            filled_prompt = filled_prompt.replace("<<speech_position>>", speech_position)

        # For Vote for Sheriff Action
        elif event_type == "vote_for_sheriff":
            # Fetch election log and candidate list
            election_log = action['content'].get('election_log', "None")
            candidate_list = action['content'].get('candidate_list', "None")

            # Fill in specific placeholders for vote_for_sheriff
            filled_prompt = prompt_template.replace("<<public_chat>>", public_chat)
            filled_prompt = filled_prompt.replace("<<game_state>>", json.dumps(game_state, indent=2))
            filled_prompt = filled_prompt.replace("<<election_log>>", election_log)
            filled_prompt = filled_prompt.replace("<<candidate_list>>", candidate_list)

        # For Decide Speech Sequence Action
        if event_type == "decide_speech_sequence":
            # Fetch dead player and alive player info
            dead_players = action['content'].get('dead_player_list', [])
            dead_players_str = ", ".join(dead_players)

            # Include the sheriff's own ID (self.agent_id) in the candidates list
            beginning_candidates = dead_players + [self.agent_id]
            beginning_candidates_str = ", ".join(beginning_candidates)

            # Fill in specific placeholders for decide_speech_sequence
            filled_prompt = prompt_template.replace("<<public_chat>>", public_chat)
            filled_prompt = filled_prompt.replace("<<game_state>>", json.dumps(game_state, indent=2))
            filled_prompt = filled_prompt.replace("<<dead player_list>>", dead_players_str)
            filled_prompt = filled_prompt.replace("<<beginning candidates list>>", beginning_candidates_str)

            # Continue with further processing of the filled prompt

        elif event_type == "player_speech":
            # Fetch previous speech info (who spoke before and what they said)
            speech_info = action['content'].get("speech_history", 'unknown')

            # Get speech position
            speech_position = str(action['content'].get('speech_position', 'unknown'))

            # Fill in specific placeholders for speech_action
            filled_prompt = prompt_template.replace("<<public_chat>>", public_chat)
            filled_prompt = filled_prompt.replace("<<game_state>>", json.dumps(game_state, indent=2))
            filled_prompt = filled_prompt.replace("<<speech_info>>", speech_info)
            filled_prompt = filled_prompt.replace("<<speech_position>>", speech_position)

        elif event_type == "vote_action":

            filled_prompt = prompt_template.replace("<<public_chat>>", public_chat)
            filled_prompt = filled_prompt.replace("<<game_state>>", json.dumps(game_state, indent=2))       
 
        elif event_type == "last_words":

            filled_prompt = prompt_template.replace("<<public_chat>>", public_chat)
            filled_prompt = filled_prompt.replace("<<game_state>>", json.dumps(game_state, indent=2))
        
        elif event_type == "badge_flow":

            filled_prompt = prompt_template.replace("<<public_chat>>", public_chat)
            filled_prompt = filled_prompt.replace("<<game_state>>", json.dumps(game_state, indent=2))
        
        else:

            filled_prompt = prompt_template.replace("<<public_chat>>", public_chat)
            filled_prompt = filled_prompt.replace("<<game_state>>", json.dumps(game_state, indent=2))

        if self.env.config.get("use_daily_tasks", False):
            if self.env.daily_tasks:
                tasks_from_env = self.env.daily_tasks.get("public", [])
                if self.role == "witch":
                    # use all tasks that appear in tasks_from_env
                    tasks_considered = [t for t in ["protect_seer", "rescue_villager", "run_for_sheriff", "exile_werewolf", "poison_werewolf"]
                                        if t in tasks_from_env]
                else:
                    # not witch => only 3 tasks
                    tasks_considered = [t for t in ["protect_seer", "run_for_sheriff", "exile_werewolf"]
                                        if t in tasks_from_env]
                if tasks_considered:
                    # A dictionary mapping task name -> brief description
                    task_descriptions = {
                        "protect_seer": "Keep the seer alive by focusing on their safety.",
                        "rescue_villager": "Use antidote or supportive actions to save a villager.",
                        "run_for_sheriff": "Attempt to become the elected sheriff for additional influence.",
                        "exile_werewolf": "Coordinate with others to vote out a suspected werewolf.",
                        "poison_werewolf": "Use poison to eliminate a werewolf during the night phase."
                    }

                    # Build a multi-line string, one line per task
                    tasks_info_lines = []
                    for t in tasks_considered:
                        desc = task_descriptions.get(t, "No description available.")
                        # For example: "protect_seer: Keep the seer alive by focusing on their safety."
                        tasks_info_lines.append(f"{t}: {desc}")

                    # Join them with newline
                    tasks_info_str = "\n".join(tasks_info_lines)

                    # Insert into a new block at the end of the prompt
                    new_block = (
                        "\n\n=============================[Optional Daily Tasks]=============================\n"
                        "Here are the tasks relevant to you:\n"
                        f"{tasks_info_str}\n"
                        "You may incorporate them if appropriate."
                    )
                    filled_prompt += new_block
        # Step 6: Create messages to pass to the tool
        if self.is_villager:
            if self.strategy == "cooperative":
                # Append text or instructions that emphasize cooperation
                filled_prompt += "\n\nRemember, you are using a cooperative strategy. " \
                                "In your decisions, prioritize teamwork and collaboration " \
                                "with other villagers to increase your chances of success."
            else:
                # The default or "independent" approach
                filled_prompt += "\n\nRemember, you are using an independent strategy. " \
                                "Make decisions based on your own judgment, with less reliance " \
                                "on others' input."
        messages = [
            {'role': 'system', 'content': action_template.get('system', '')},
            {'role': 'user', 'content': filled_prompt}
        ]

        # Step 7: Call the GPT tool to decide the action
        try:
            tool_calls = json.loads(self.gpt_tool_call(messages, tools)[0].function.arguments)
            return tool_calls
        except Exception as e:
            self.logger.error(f"Error during {event_type}'s tool call: {e}")
            return {"action": "no_action", "target": None}
