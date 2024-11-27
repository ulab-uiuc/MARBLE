import json
import logging
import os
import time
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

    def __init__(self, config: Dict[str, Any], role: str, log_path: str, event_bus: EventBus, shared_memory: Dict[str, Any], env: any, number: int):
        """
        Custom initialization for WerewolfAgent without calling BaseAgent's __init__.

        Args:
            config (dict): Configuration for the agent.
            role (str): Role of the agent (e.g., "wolf", "villager", "prophet", "witch", "guard").
            log_path (str): Path where the game log will be stored.
            event_bus (EventBus): The event bus for subscribing and publishing events.
            shared_memory: Reference to the shared memory dict.
            env (WerewolfEnv): The environment instance associated with the agent.
        """
        # 自定义初始化逻辑
        self.client = OpenAI(
            api_key=config["openai_api_key"]
        )
        self.agent_id = config.get("agent_id")
        self.id = self.agent_id
        assert isinstance(self.agent_id, str), "agent_id must be a string"

        self.role = role  # 设置角色
        self.agent_number = number
        # 保存环境实例
        self.env = env
        # 共享内存文件路径
        self.shared_memory = shared_memory
        
        # 创建一个独立的 logger
        self.logger = self._create_logger(self.agent_id)

        # 设置日志文件的路径
        self.log_file_path = os.path.join(log_path, f"{self.agent_number}-{self.role}-{self.agent_id}_log.txt")
        self._initialize_log_file()

        # 在终端输出并写入日志文件
        init_message = f"{self.role} agent '{self.agent_id}' initialized with role '{self.role}'"
        self._log_and_save(init_message)

        # 订阅事件
        event_bus.subscribe(self, self.receive_communication)

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
            with open(self.log_file_path, 'w', encoding='utf-8') as log_file:
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
        with open(self.log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(log_entry + "\n")

    def _write_log_entry(self, log_entry: str) -> None:
        """
        只将日志信息保存到日志文件，不输出到终端。

        Args:
            log_entry (str): 要保存的日志信息。
        """
        # 只将日志信息写入日志文件，不输出到终端
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
        reply_event_type = f"reply_{event_type}"  # 将事件类型格式化为 reply_<event_type>

        # Initialize result as no_action in expected event format
        result = {"event_type": "reply_no_action", "sender": self.agent_id, "recipients": [], "content": {}}
        result_content =  {}
        # 特定处理狼人事件的格式
        if event_type in ["werewolf_action", "werewolf_discussion"]:
            try:
                result_content = self._wolf_action(event)  # 获取狼人行动的内容
                result = {
                    "event_type": "reply_werewolf_action",  # 格式化后的事件类型
                    "sender": self.agent_id,
                    "recipients": [self.env],  # 接收者为系统
                    "content": result_content.get("action", "no action")  # 事件内容包含在内容字段中
                }
            except Exception as e:
                self.logger.error(f"Error while performing action {event_type}: {e}")
                result["content"] = {"error": str(e)}
        else:
            try:
                # 针对其他事件调用通用的 _perform_action 方法
                result_content = self._perform_action(event)
                result = {
                    "event_type": reply_event_type,  # 格式化后的事件类型
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

        # 检查自己是否是事件的接受者之一
        recipients = event.get("recipients", [])
        if self not in recipients:
            if debug:
                self.logger.info(f"Agent {self.agent_id} ignored event '{event.get('event_type')}' as it is not a recipient.")
            return  # 事件不针对该 agent，不做处理

        # 打印事件接收者及事件类型
        if debug:
            self.logger.info(f"Agent {self.agent_id} processing event '{event.get('event_type')}'. Recipients: {recipients}")

        # 检查 agent 是否在存活列表中
        alive_players = self.shared_memory["public_state"].get("alive_players", [])
        if self.agent_id not in alive_players:
            if debug:
                self.logger.info(f"Agent {self.agent_id} ignored event '{event.get('event_type')}' as it is not in the alive players list.")
            return  # 如果 agent 不在存活列表中，不进行处理

        # 打印存活状态
        if debug:
            self.logger.info(f"Agent {self.agent_id} is in the alive players list: {alive_players}")

        # 检查事件类型是否需要特殊条件
        event_type = event.get("event_type")
        if event_type in ["decide_speech_order", "decide_badge_flow"]:
            badge_count = self.shared_memory["private_state"]["players"][self.agent_id]["status"].get("badge_count", 0)
            if badge_count != 1:
                if debug:
                    self.logger.info(f"Agent {self.agent_id} ignored event '{event_type}' as it does not have the badge (badge_count: {badge_count}).")
                return
            if debug:
                self.logger.info(f"Agent {self.agent_id} processing special event '{event_type}' with badge_count: {badge_count}.")

        # 执行动作并返回 action
        if debug:
            self.logger.info(f"Agent {self.agent_id} preparing to act on event '{event_type}'.")
        action = self.act(event)
        if debug:
            self.logger.info(f"Agent {self.agent_id} generated action: {action}")

        # 发布动作
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
        rounds = 0
        while True:
            rounds += 1
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o",  # 使用 gpt-4o-mini 模型
                    messages=messages,
                    tools=tools,
                    tool_choice="required",
                    temperature=1.0,  # 设置温度为1以增加生成的多样性
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
        # Step 1: 获取事件类型
        event_type = event.get("event_type", "")

        # Step 2: 定义 YAML 模板路径
        yaml_paths = {
            "werewolf_action": r"marble\agent\werewolf_prompts\werewolf_action.yaml",
            "werewolf_discussion": r"marble\agent\werewolf_prompts\werewolf_discussion.yaml"
        }
        yaml_path = yaml_paths.get(event_type, None)
        if not yaml_path:
            self.logger.error(f"Invalid event type for werewolf action: {event_type}")
            return {"action": "no_action", "target": None}

        # Step 3: 加载 YAML 模板
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                action_template = yaml.safe_load(f)
            prompt_template = action_template.get('user', '')
            tools = action_template.get('tools', [])
        except Exception as e:
            self.logger.error(f"Failed to load prompt template for {event_type}: {e}")
            return {"action": "no_action", "target": None}

        # Step 4: 读取共享内存中的游戏状态
        try:
                
            public_state = self.shared_memory.get("public_state", {})
            private_state = self.shared_memory.get("private_state", {}).get("players", {}).get(self.agent_id, {})
            personal_event_log = private_state.get("personal_event_log", "")

            # 构建游戏状态（从 public_state 中）
            game_state = {
                "days": public_state.get("days", 0),
                "day/night": public_state.get("day/night", "night"),
                "alive_players": public_state.get("alive_players", []),
                "sheriff": public_state.get("sheriff", None)
            }

            # 使用个人事件日志作为狼人讨论内容的基础
            public_chat = personal_event_log
        except Exception as e:
            self.logger.error(f"Error retrieving game state or personal event log from shared memory: {e}")
            return {"action": "no_action", "target": None}

        # Step 5: 针对 werewolf_action 和 werewolf_discussion 分别填充 prompt
        filled_prompt = ""

            # Werewolf Action: 第一次选择目标
        if event_type == "werewolf_action":
            # 获取当前夜晚的存活玩家信息
            player_info = event["content"]["player_info"]
            alive_players_str = player_info["alive_players"]
            alive_werewolves_str = player_info["alive_werewolves"]

            # 填充狼人行动的特定信息
            filled_prompt = prompt_template.replace("<<public_chat>>", public_chat)
            filled_prompt = filled_prompt.replace("<<game_state>>", json.dumps(game_state, indent=2))
            filled_prompt = prompt_template.replace("<<player info>>", f"Alive players: {alive_players_str}\nAlive werewolves: {alive_werewolves_str}")

        # Werewolf Discussion: 统一目标
        elif event_type == "werewolf_discussion":
            # 获取存活玩家、存活狼人以及上一次讨论选择的信息
            player_info = event.get("content", {}).get("allies_info", {})
            alive_players_str = player_info.get("alive_players", "")
            alive_werewolves_str = player_info.get("alive_werewolves", "")
            last_round_targets = player_info.get("last_round_targets", {})
            rounds_remaining = event.get("content", {}).get("rounds_remaining")
            # 构建 last_round_targets 的格式化字符串
            last_round_targets_str = "\n".join(f"{wolf_id}: {target}" for wolf_id, target in last_round_targets.items())

            # 填充狼人讨论的特定信息
            filled_prompt = prompt_template.replace("<<public_chat>>", public_chat)
            filled_prompt = filled_prompt.replace("<<game_state>>", json.dumps(game_state, indent=2))
            filled_prompt = filled_prompt.replace("<<player info>>", f"Alive players: {alive_players_str}\nAlive werewolves: {alive_werewolves_str}\nLast round targets:\n{last_round_targets_str}")
            filled_prompt = filled_prompt.replace("<<rounds_remaining>>", str(rounds_remaining))


        # Step 6: 准备传递给工具的消息内容
        messages = [
            {'role': 'system', 'content': action_template.get('system', '')},
            {'role': 'user', 'content': filled_prompt}
        ]

        # Step 7: 调用 GPT 工具来决定行动
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
            
        # Step 6: Create messages to pass to the tool
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
