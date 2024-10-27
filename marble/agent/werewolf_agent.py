import json
import os
import time
import yaml
import logging
from typing import Any, Dict, Union
from marble.utils.logger import get_logger
from ..environments.werewolf_env import EventBus, WerewolfEnv
from base_agent import BaseAgent  # 假设 BaseAgent 在 base_agent_module 中
from openai import OpenAI
class WerewolfAgent:
    """
    WerewolfAgent class without calling BaseAgent's __init__.
    """

    def __init__(self, config: Dict[str, Any], role: str, log_path: str, event_bus: EventBus, shared_memory_path: str):
        """
        Custom initialization for WerewolfAgent without calling BaseAgent's __init__.
        
        Args:
            config (dict): Configuration for the agent.
            role (str): Role of the agent (e.g., "wolf", "villager", "prophet", "witch", "guard").
            log_path (str): Path where the game log will be stored.
            event_bus (EventBus): The event bus for subscribing and publishing events.
            shared_memory_path (str): Path to the shared memory JSON file.
        """
        # 自定义初始化逻辑
        self.client = OpenAI(
            api_key=config["openai_api_key"]
        )
        self.agent_id = config.get("agent_id")
        assert isinstance(self.agent_id, str), "agent_id must be a string"
        
        self.role = role  # 设置角色
        self.status = {
            "health": 1,  # 默认血量为 1
            "protection_count": 0,  # 默认守护数量为 0
            "poison_count": 1 if role == "witch" else 0,  # 女巫有1个毒药
            "antidote_count": 1 if role == "witch" else 0,  # 女巫有1个解药
            "badge_count": 0  # 默认警徽数量为 0
        }

        # 共享内存文件路径
        self.shared_memory = shared_memory_path
        
        # 创建一个独立的 logger
        self.logger = self._create_logger(self.agent_id)
        
        # 设置日志文件的路径
        self.log_file_path = os.path.join(log_path, f"{self.agent_id}_log.txt")
        self._initialize_log_file()

        # 在终端输出并写入日志文件
        init_message = f"{self.role} agent '{self.agent_id}' initialized with role '{self.role}'"
        self._log_and_save(init_message)

        # 订阅事件
        event_bus.subscribe(self.receive_communication)

        # 保存 event_bus 引用，方便发布事件
        self.event_bus = event_bus

    def _create_logger(self, agent_id: str):
        """
        创建并返回每个实例独立的 logger。

        Args:
            agent_id (str): 当前 Agent 的 ID。
        
        Returns:
            logging.Logger: 与 agent_id 绑定的日志记录器。
        """
        logger = logging.getLogger(agent_id)
        logger.setLevel(logging.INFO)

        # 设置处理器和格式
        handler = logging.StreamHandler()  # 输出到终端
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # 添加处理器
        if not logger.handlers:  # 避免重复添加处理器
            logger.addHandler(handler)
        
        return logger

    def _initialize_log_file(self) -> None:
        """
        初始化日志文件。如果文件不存在则创建，不记录任何内容。
        """
        if not os.path.exists(self.log_file_path):
            with open(self.log_file_path, 'w') as log_file:
                pass  # 创建空的日志文件，不写入内容

    def _log_and_save(self, log_entry: str) -> None:
        """
        将日志信息输出到终端并保存到日志文件中。

        Args:
            log_entry (str): 要记录和保存的日志信息。
        """
        # 输出到终端
        self.logger.info(log_entry)

        # 将日志信息写入日志文件
        with open(self.log_file_path, 'a') as log_file:
            log_file.write(log_entry + "\n")

    def _write_log_entry(self, log_entry: str) -> None:
        """
        只将日志信息保存到日志文件，不输出到终端。

        Args:
            log_entry (str): 要保存的日志信息。
        """
        # 只将日志信息写入日志文件，不输出到终端
        with open(self.log_file_path, 'a') as log_file:
            log_file.write(log_entry + "\n")
    
    def act(self, event: Dict[str, Any]) -> str:
        """
        Agent takes an action based on the received event.
        
        Args:
            event (Dict[str, Any]): The event that triggers an action.

        Returns:
            Dict: The action decided by the agent.
        """
        self.logger.info(f"Agent {self.agent_id} received event: {event}")

        event_type = event.get("event_type", "")

        # Initialize result as no_action
        result = {"action": "no_action", "status": self.status, "role": self.role}

        try:
            # Call the generalized _perform_action method
            result = self._perform_action(event, event_type)
        except Exception as e:
            self.logger.error(f"Error while performing action {event_type}: {e}")
            result = {"action": "no_action", "error": str(e)}

        # Log and return the action taken
        self.logger.info(f"Agent {self.agent_id} decided on action: {result['action']}")
        self._write_log_entry(result)
        
        return result["action"]
    
    def receive_communication(self, event: Dict[str, Any]) -> None:
        """
        Receive communication (from EventBus) and process the event.
        
        Args:
            event (Dict[str, Any]): The event data received (e.g., other players' actions, state updates).
        """
        self.logger.info(f"Agent {self.agent_id} received event: {event}")

        # 检查自己是否是事件的接受者之一
        recipients = event.get("recipients", [])
        if self.agent_id not in recipients:
            self.logger.info(f"Agent {self.agent_id} is not a recipient of this event, ignoring.")
            return  # 事件不针对该 agent，不做处理

        # 检查 agent 是否已经死亡（通过 health 判断）
        if self.status.get("health", 1) == 0:
            self.logger.info(f"Agent {self.agent_id} is dead, ignoring the event.")
            return  # 如果 agent 已死亡，不进行处理

        event_type = event.get("event_type")

        # 针对警长的特殊事件，确保 agent 持有警徽才能执行
        if event_type == "decide_speech_order" or event_type == "decide_badge_flow":
            if self.status.get("badge_count", 0) != 1:
                return  # 如果角色不是警长或没有警徽，忽略事件

        # 执行动作并返回 action
        action = self.act(event)
        
        # 发布动作
        self._publish_action(action)

    def _publish_action(self, action: str) -> None:
        """
        Publish the action decided by the agent.
        
        Args:
            action (str): The action to publish.
        """
        self.event_bus.publish(action)

    def gpt_tool_call(self, messages, tools):
        rounds = 0
        while True:
            rounds += 1
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o",  # 使用 gpt-4o-mini 模型
                    messages=messages,
                    tools=tools,
                    tool_choice="required",
                    temperature=0.0,  # 设置温度为1以增加生成的多样性
                    n=1,
                )
                tool_calls = response.choices[0].message.tool_calls
                return tool_calls
            except Exception as e:
                print(f"Chat Generation Error: {e}")
                time.sleep(5)
                if rounds > 3:
                    raise Exception("Chat Completion failed too many times")
                

    # 示例中的角色行为方法
    def _wolf_action(self, game_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Wolf's action: choose a target to kill.
        
        Args:
            game_state (Dict[str, Any]): The current state of the game.
            
        Returns:
            Dict[str, Any]: A dictionary containing the action and the selected target.
        """
        # 逻辑可以通过其他狼人商议来选择目标
        target = game_state.get("suggested_target", "unknown_player")
        self.logger.info(f"Wolf {self.agent_id} decided to kill {target}")
        return {"action": "kill", "target": target}

    def _perform_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generalized action based on the action type.

        Args:
            action (Dict[str, Any]): The action dict, which includes "event_type" (e.g., "witch_action", "guard_action", "seer_action") 
                                    and other relevant details like "night_info", "content", etc.

        Returns:
            Dict[str, Any]: The action decided by the LLM tool.
        """
        # Step 1: Get the event type from the action dictionary
        event_type = action.get("event_type", "")
        
        # Step 2: Define YAML path based on the action type
        yaml_paths = {
            "witch_action": "werewolf_prompts/witch_prompt.yaml",
            "guard_action": "werewolf_prompts/guard_prompt.yaml",
            "run_for_sheriff": "werewolf_prompts/run_for_sheriff.yaml",
            "sheriff_speech": "werewolf_prompts/sheriff_speech.yaml",
            "vote_for_sheriff": "werewolf_prompts/vote_for_sheriff.yaml",
            "decide_speech_sequence": "werewolf_prompts/decide_speech_sequence.yaml",
            "seer_action": "werewolf_prompts/seer_prompt.yaml",
            "speech_action": "werewolf_prompts/speech_prompt.yaml",
            "vote_action": "werewolf_prompts/vote_prompt.yaml",
            "last_words_action": "werewolf_prompts/last_words_prompt.yaml",
            "badge_flow": "werewolf_prompts/badge_flow.yaml"
        }
        yaml_path = yaml_paths.get(event_type, None)

        if not yaml_path:
            self.logger.error(f"Invalid event type: {event_type}")
            return {"action": "no_action", "target": None}

        # Step 3: Load the prompt template and tools for the given action from YAML
        try:
            with open(yaml_path, 'r') as f:
                action_template = yaml.safe_load(f)
            prompt_template = action_template.get('user', '')
            tools = action_template.get('tools', [])
        except Exception as e:
            self.logger.error(f"Failed to load prompt template for event {event_type}: {e}")
            return {"action": "no_action", "target": None}

        # Step 4: Read from shared memory (public and private)
        try:
            with open(self.shared_memory, 'r') as f:
                shared_memory = json.load(f)
                    
            public_state = shared_memory.get("public_state", {})
            private_state = shared_memory.get("private_state", {}).get("players", {}).get(self.agent_id, {})
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
            status = private_state.get("status", {})
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
            election_info = "\n".join([f"{n}: {info['player']} said - {info['speech']}"
                                    for n, info in enumerate(action['content'].get('election_info', []), 1)])

            # Get speech position
            speech_position = action['content'].get('speech_position', 'unknown')

            # Fill in specific placeholders for sheriff_speech
            filled_prompt = prompt_template.replace("<<public_chat>>", public_chat)
            filled_prompt = filled_prompt.replace("<<game_state>>", json.dumps(game_state, indent=2))
            filled_prompt = filled_prompt.replace("<<election_info>>", election_info)
            filled_prompt = filled_prompt.replace("<<speech_position>>", speech_position)

        # For Vote for Sheriff Action
        elif event_type == "vote_for_sheriff":
            # Fetch election log and candidate list
            election_log = "\n".join([f"{info['player']}: {info['speech']}" 
                                    for info in action['content'].get('election_log', [])])
            candidate_list = ", ".join(action['content'].get('candidate_list', []))

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

                # Fill in specific placeholders for decide_speech_sequence
            filled_prompt = prompt_template.replace("<<public_chat>>", public_chat)
            filled_prompt = filled_prompt.replace("<<game_state>>", json.dumps(game_state, indent=2))
            filled_prompt = filled_prompt.replace("<<dead player_list>>", dead_players_str)

        elif event_type == "speech_action":
            # Fetch previous speech info (who spoke before and what they said)
            speech_info = "\n".join([f"{n}: {info['player']} said - {info['speech']}"
                                    for n, info in enumerate(action['content'].get('speech_info', []), 1)])

            # Get speech position
            speech_position = action['content'].get('speech_position', 'unknown')

            # Fill in specific placeholders for speech_action
            filled_prompt = prompt_template.replace("<<public_chat>>", public_chat)
            filled_prompt = filled_prompt.replace("<<game_state>>", json.dumps(game_state, indent=2))
            filled_prompt = filled_prompt.replace("<<speech_info>>", speech_info)
            filled_prompt = filled_prompt.replace("<<speech_position>>", speech_position)

        elif event_type == "vote_action":

            filled_prompt = prompt_template.replace("<<public_chat>>", public_chat)
            filled_prompt = filled_prompt.replace("<<game_state>>", json.dumps(game_state, indent=2))       
        else:

            filled_prompt = prompt_template.replace("<<public_chat>>", public_chat)
            filled_prompt = filled_prompt.replace("<<game_state>>", json.dumps(game_state, indent=2))
        
        # Step 6: Create messages to pass to the tool
        messages = [
            {'role': 'system', 'content': action_template.get('system', '')},
            {'role': 'user', 'content': filled_prompt}
        ]

        # Step 7: Call the GPT tool to decide the action
        try:
            tool_calls = self.gpt_tool_call(messages, tools)
            return tool_calls
        except Exception as e:
            self.logger.error(f"Error during {event_type}'s tool call: {e}")
            return {"action": "no_action", "target": None}
