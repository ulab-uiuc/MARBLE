import json
import os
import sys
import random
import time
import yaml
from typing import Any, Dict
from threading import Condition, Lock
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from marble.agent.werewolf_agent import WerewolfAgent
from marble.utils.eventbus import EventBus
from colorama import Fore, Style, init  # 引入 colorama 库

from marble.environments.base_env import BaseEnvironment



class WerewolfEnv:
    def __init__(self, name: str, config_path: str):
        """
        Initialize the Werewolf environment.

        Args:
            name (str): The name of the environment.
            config_path (str): Path to the config.json file.
        """
        self.id = "SYSTEM"
        init(autoreset=True)  # 初始化 colorama 自动重置颜色
        self.name = name
        self.agents = []
        # 加载配置文件
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        self.config = config

        # 加载 system_prompt.yaml 文件
        system_prompt_path = self.config.get("system_prompt_path")
        if not system_prompt_path or not os.path.exists(system_prompt_path):
            raise FileNotFoundError(f"System prompt file '{system_prompt_path}' not found.")

        with open(system_prompt_path, 'r', encoding='utf-8') as f:
            system_prompt = yaml.safe_load(f)
        
        game_introduction = system_prompt.get("game_introduction", "")
        self.condition = Condition(Lock())  # Condition 内部封装了一个可重入锁
        self.current_event = None  # 当前正在处理的事件类型
        self.event_completed = False
        # 所有角色介绍
        role_introductions = {
            "wolf": system_prompt.get("werewolf_introduction", ""),
            "villager": system_prompt.get("villager_introduction", ""),
            "seer": system_prompt.get("seer_introduction", ""),
            "witch": system_prompt.get("witch_introduction", ""),
            "guard": system_prompt.get("guard_introduction", "")
        }

        # 初始化 EventBus
        self.event_bus = EventBus()
        self.event_bus.subscribe(self, self.receive_action)
        # 创建 werewolf_log 文件夹（如果不存在）
        base_log_dir = "werewolf_log"
        if not os.path.exists(base_log_dir):
            os.makedirs(base_log_dir)

        # 创建当前时间命名的子文件夹，用于存储该场游戏的数据
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        game_log_dir = os.path.join(base_log_dir, f"game_{timestamp}")
        os.makedirs(game_log_dir)  # 创建游戏日志文件夹
        # 定义 shared memory 文件路径
        self.shared_memory_path = os.path.join(game_log_dir, "shared_memory.json")

        # 角色列表，包含狼人、平民、特殊角色
        roles = ['wolf', 'wolf', 'wolf', 'villager', 'villager', 'villager', 'seer', 'witch', 'guard']
        random.shuffle(roles)  # 随机打乱角色分配

        # 初始化 shared memory
        self.shared_memory = {
            "public_state": {
                "days": 0,
                "day/night": "night",
                "alive_players": [],  # 存活玩家，稍后会填充
                "sheriff": None,  # 初始没有警长
                "event_log": game_introduction,  # 公开事件日志初始化为game_introduction内容
                "speech_order": {},
                "day_cache": []
            },
            "private_state": {
                "players": {},  # 每个玩家的状态和身份
                "guard_last_night_protect": None,
                "werewolf_action": {  # 狼人行动部分的初始化
                    "rounds_remaining": 5,  # 初始总共 5 轮
                    "alive_werewolves": [],  # 存活狼人名单，稍后会填充
                    "round_targets": [],  # 每一轮的狼人选择目标，稍后填充
                    "final_target": None
                },
                "night_cache": [],  # 每晚的主要事件记录，格式为列表
                "event_log": game_introduction  # 私密事件日志初始化为game_introduction内容
            },
            "public_event_log": game_introduction,  # 初始化为game_introduction内容
            "private_event_log": game_introduction  # 初始化为game_introduction内容
        }

        # 创建 9 个 WerewolfAgent，角色随机分配
        for i in range(9):
            agent_id = f"agent_{i + 1}"
            role = roles[i]

            # 基础的 agent_config（不包含角色介绍）
            agent_config = {
                "agent_id": agent_id,
                "openai_api_key": self.config.get("openai_key")  # 这里是基础配置
            }

            # 创建 WerewolfAgent 实例，将日志存储路径传入
            agent = WerewolfAgent(config=agent_config, role=role, log_path=game_log_dir, event_bus=self.event_bus, shared_memory= self.shared_memory, env = self)
            self.agents.append(agent)  # 将 agent 加入 agents 列表

            # 将 agent 添加到存活玩家列表
            self.shared_memory["public_state"]["alive_players"].append(agent_id)

            # 初始化每个玩家的私密状态（身份、状态、个人事件日志）
            personal_event_log = (
                f"{game_introduction}\n\n"
                f"--- Role Introductions ---\n"
                f"Werewolf Role Introduction:\n{role_introductions['wolf']}\n\n"
                f"Villager Role Introduction:\n{role_introductions['villager']}\n\n"
                f"Seer Role Introduction:\n{role_introductions['seer']}\n\n"
                f"Witch Role Introduction:\n{role_introductions['witch']}\n\n"
                f"Guard Role Introduction:\n{role_introductions['guard']}\n\n\n\n"
                f"You are {agent_id}, your role in this game is {role}."
            )

            status = {
                "health": 1,  # 默认血量为 1
                "protection_count": 0,  # 默认守护数量为 0
                "poison_count": 1 if role == "witch" else 0,  # 女巫有 1 个毒药
                "antidote_count": 1 if role == "witch" else 0,  # 女巫有 1 个解药
                "badge_count": 0  # 默认警徽数量为 0
            }

            # 如果角色为预言家，添加 `seer_history`
            if role == "seer":
                status["check_history"] = {}  # 初始化为空字典

            self.shared_memory["private_state"]["players"][agent_id] = {
                "role": role,  # 记录角色身份
                "status": status,
                "personal_event_log": personal_event_log  # 个人事件日志
            }
            
        # 初始化警长信息为 None，表示没有警长
        self.shared_memory["public_state"]["sheriff"] = None

        # 将共享内存写入 shared_memory.json 文件
        with open(self.shared_memory_path, 'w', encoding='utf-8') as f:
            json.dump(self.shared_memory, f, indent=4)

        # 打印环境初始化日志
        self._log_system(f"Werewolf environment '{self.name}' initialized with 9 agents and shared memory.")
        self._log_system(f"Game data stored in: {game_log_dir}")

    def _log_system(self, message: str):
        """
        使用黄色文本输出系统消息。

        Args:
            message (str): 系统消息内容。
        """
        print(f"{Fore.YELLOW}System: {message}{Style.RESET_ALL}")

    def _log_event(self, message: str):
        """
        使用绿色文本输出事件消息。

        Args:
            message (str): 事件消息内容。
        """
        print(f"{Fore.GREEN}Event: {message}{Style.RESET_ALL}")

    def _log_player(self, player_id: str, message: str):
        """
        使用蓝色文本输出玩家发言。

        Args:
            player_id (str): 玩家ID。
            message (str): 玩家发言内容。
        """
        print(f"{Fore.BLUE}[{player_id}]: {message}{Style.RESET_ALL}")

    def publish_event(self, event: dict):
        """
        Publishes an event and waits for its completion using a flag.
        """
        self.current_event = event["event_type"]
        self.event_completed = False  # 重置完成标志
        self.event_bus.publish(event)  # 发布事件
        
        while not self.event_completed:
            time.sleep(0.01)  # 避免占用过多CPU资源

    def mark_event_complete(self, event_type: str):
        """
        Marks the current event as complete by updating the flag.
        """
        if self.current_event == event_type:
            
            self.event_completed = True
            
            self.current_event = None
        else:
            # 如果事件类型不匹配，记录错误日志
            self._log_event(
                f"Attempted to mark event '{event_type}' as complete, "
                f"but current event is '{self.current_event}'. No action taken."
            )

    def start(self) -> None:
        """
        Start the werewolf game environment and run the simulation in a day-night cycle.
        """
        start_message = "Werewolf game starting. Initializing day-night cycle."
        self._log_system(start_message)
        self.log_event(is_private=False, agent_id="system", content=start_message)

        try:
            while not self.should_terminate():
                # Start a new day-night cycle
                self.shared_memory["public_state"]["days"] += 1
                current_day = self.shared_memory["public_state"]["days"]
                day_start_message = f"SYSTEM: Starting day-night cycle for Day {current_day}"
                self.log_event(is_private=False, agent_id="system", content=day_start_message)

                # Night Phase
                self.shared_memory["public_state"]["day/night"] = "night"
                night_start_message = f"SYSTEM: Night {current_day} begins. Werewolves and special roles take actions."
                self.log_event(is_private=False, agent_id="system", content=night_start_message)
                self.night()
                
                # Check termination condition after night phase
                if self.should_terminate():
                    termination_message = "SYSTEM: Game termination condition met after night phase."
                    self.log_event(is_private=False, agent_id="system", content=termination_message)
                    try:
                        with open(self.shared_memory_path, 'w', encoding='utf-8') as f:
                            json.dump(self.shared_memory, f, indent=4)
                        self._log_system(f"Shared memory successfully written to {self.shared_memory_path}")
                    except Exception as e:
                        self._log_system(f"Failed to write shared memory to {self.shared_memory_path}: {e}")
                    break

                # Day Phase
                self.shared_memory["public_state"]["day/night"] = "day"
                day_start_message = f"SYSTEM: Day {current_day} begins. Players discuss and vote on potential suspects."
                self._log_event(day_start_message)
                self.log_event(is_private=False, agent_id="system", content=day_start_message)
                self.day()
                
                # Check termination condition after day phase
                if self.should_terminate():
                    termination_message = "SYSTEM: Game termination condition met after day phase."
                    self._log_system(termination_message)
                    self.log_event(is_private=False, agent_id="system", content=termination_message)
                    try:
                        with open(self.shared_memory_path, 'w', encoding='utf-8') as f:
                            json.dump(self.shared_memory, f, indent=4)
                        self._log_system(f"Shared memory successfully written to {self.shared_memory_path}")
                    except Exception as e:
                        self._log_system(f"Failed to write shared memory to {self.shared_memory_path}: {e}")
                    break

            game_complete_message = "SYSTEM: Werewolf game completed."
            self.log_event(is_private=False, agent_id="system", content=game_complete_message)

        except Exception as e:
            error_message = f"An error occurred during the game cycle: {e}"
            self._log_system(error_message)
            raise

    def night(self) -> None:
        """
        Executes the night phase of the game. Werewolves select a target, and special 
        roles (witch, seer, guard) may take actions.
        """
        try:
            # 记录当前夜晚编号
            current_night = self.shared_memory["public_state"]["days"]  # 第几夜（游戏回合数 +1）
            
            # 在 night_cache 中添加一个新的字典以记录当前夜晚
            night_event = {}
            self.shared_memory["private_state"]["night_cache"].append(night_event)

            # 守卫行动
            self._log_event("Guard action starts.")
            self.guard_action()
            self.log_event(is_private=False, agent_id="system", content="Guard has chosen to protect a player.")

            # 狼人行动
            self._log_event("Werewolves are selecting a target.")
            self.werewolf_action()
            self.log_event(is_private=False, agent_id="system", content="Werewolves have chosen their target.")

            # 预言家行动
            self._log_event("Seer is performing their action.")
            self.seer_action()
            self.log_event(is_private=False, agent_id="system", content="Seer has checked a player's identity.")

            # 女巫行动
            self._log_event("Witch is deciding on antidote and poison usage.")
            self.witch_action()
            self.log_event(is_private=False, agent_id="system", content="Witch has made her decision on potion use.")

            self._log_system("Night phase actions are completed.")

            # 保存共享内存到文件
            with open(self.shared_memory_path, 'w', encoding='utf-8') as f:
                json.dump(self.shared_memory, f, indent=4)
            self._log_system(f"Shared memory successfully written to {self.shared_memory_path}")

        except Exception as e:
            # 捕获所有异常，写入共享内存到 JSON 文件
            self._log_system(f"An error occurred during the night phase: {e}")
            with open(f"{self.shared_memory_path}_error_dump.json", 'w', encoding='utf-8') as f:
                json.dump(self.shared_memory, f, indent=4)
            self._log_system(f"Shared memory dumped to {self.shared_memory_path}_error_dump.json for debugging.")
            raise

    def day(self) -> None:
        """
        Executes the day phase of the game. Players discuss and vote on a player to eliminate.
        """
        try:
            self._log_system("Day phase begins. Players discuss and vote on potential suspects.")

            # 获取当前的天数
            current_day = self.shared_memory["public_state"]["days"]

            # 初始化当日缓存
            self.shared_memory["public_state"]["day_cache"].append({})

            # 获取当日的缓存字典
            day_cache = self.shared_memory["public_state"]["day_cache"][-1]
            if current_day == 1:
                # Step 1: First-day special sequence
                self._log_event("First day: Sheriff election begins.")

                # Run sheriff election
                self.run_for_sheriff()

                # Step 2: Announce deceased from the previous night, if any
                deceased = self.get_night_deceased()
                if deceased:
                    self.last_words(deceased[0])
                self.update_alive_players()
                # Step 3: Sheriff decides the speech order if elected
                if self.shared_memory["public_state"]["sheriff"]:
                    self._log_event("Sheriff is deciding the speech order.")
                    speech_order = self.sheriff_decide_speech_order()
                    if speech_order is None:
                        speech_order = self.shared_memory["public_state"]["day_cache"].get(current_day - 1, {}).get("speech_order_decision", None)
                        self._log_system(f"Speech order retrieve failed. Current speech order: {speech_order}")
                        day_cache["speech_order_decision"] = speech_order
                    if speech_order is None:
                        alive_players = self.shared_memory["public_state"]["alive_players"]
                        speech_order = sorted(alive_players)
                        self._log_system(f"Speech order retrieve failed again. Current speech order: {speech_order}")
                        day_cache["speech_order_decision"] = speech_order
                else:
                    alive_players = self.shared_memory["public_state"]["alive_players"]
                    speech_order = sorted(alive_players)
                    day_cache["speech_order_decision"] = speech_order
                self._log_system(f"Speech sequence: {speech_order}")    
                self.shared_memory["public_state"]["speech_order"][current_day] = speech_order
                # Step 4: Day speeches
                self._log_event("Players begin speeches.")
                speech_order = self.shared_memory["public_state"]["speech_order"].get(current_day, [])
                self.player_speeches(speech_order[0])

                # Step 5: Vote to exile a player
                self._log_event("Players are voting to exile a suspect.")
                self.vote_action()

            else:
                deceased = self.get_night_deceased()
                if deceased:
                    self._log_event("Announcing deceased from the night. No last words will be given.")
                self.update_alive_players()
                if self.shared_memory["public_state"]["sheriff"]:
                    self._log_event("Sheriff is deciding the speech order.")
                    speech_order = self.sheriff_decide_speech_order()
                    if speech_order is None:
                        speech_order = self.shared_memory["public_state"]["day_cache"].get(current_day - 1, {}).get("speech_order_decision", None)
                        self._log_system(f"Speech order retrieve failed. Current speech order: {speech_order}")
                        day_cache["speech_order_decision"] = speech_order
                    if speech_order is None:
                        alive_players = self.shared_memory["public_state"]["alive_players"]
                        speech_order = sorted(alive_players)
                        day_cache["speech_order_decision"] = speech_order
                        self._log_system(f"Speech order retrieve failed again. Current speech order: {speech_order}")
                else:
                    alive_players = self.shared_memory["public_state"]["alive_players"]
                    speech_order = sorted(alive_players)
                    day_cache["speech_order_decision"] = speech_order
                # Day speeches
                self._log_event("Players begin speeches.")
                speech_order = day_cache.get("speech_order_decision", None)
                self.player_speeches(speech_order[0])

                # Vote to exile a player
                self._log_event("Players are voting to exile a suspect.")
                self.vote_action()

            # Log the day's cache for debugging
            self._log_system(f"Day {current_day} cache updated: {day_cache}")
            self.update_alive_players()

            # Save shared memory to file
            with open(self.shared_memory_path, 'w', encoding='utf-8') as f:
                json.dump(self.shared_memory, f, indent=4)
            self._log_system(f"Shared memory successfully written to {self.shared_memory_path}")

        except Exception as e:
            # 捕获所有异常，写入共享内存到 JSON 文件
            self._log_system(f"An error occurred during the day phase: {e}")
            with open(f"{self.shared_memory_path}_error_dump.json", 'w', encoding='utf-8') as f:
                json.dump(self.shared_memory, f, indent=4)
            self._log_system(f"Shared memory dumped to {self.shared_memory_path}_error_dump.json for debugging.")
            raise

    def should_terminate(self) -> bool:
        """
        Checks if the game should terminate based on the number of remaining players
        and their roles. The game ends if:
        1. All werewolves are eliminated (villager victory).
        2. All non-werewolf players are eliminated (werewolf victory).

        Returns:
            bool: True if the game should end, otherwise False.
        """
        self._log_system("Checking if the game should terminate.")

        # 获取存活玩家和狼人数量
        alive_players = self.shared_memory["public_state"]["alive_players"]
        werewolves = [
            agent_id for agent_id in alive_players
            if self.shared_memory["private_state"]["players"][agent_id]["role"] == "wolf"
        ]
        non_werewolves = [
            agent_id for agent_id in alive_players
            if self.shared_memory["private_state"]["players"][agent_id]["role"] != "wolf"
        ]

        werewolf_count = len(werewolves)
        non_werewolf_count = len(non_werewolves)

        # 日志记录存活玩家、狼人和非狼人数
        self._log_system(f"Alive players: {alive_players}")
        self._log_system(f"Number of werewolves: {werewolf_count}")
        self._log_system(f"Number of non-werewolves: {non_werewolf_count}")

        # 检查游戏终止条件
        if werewolf_count > 0 and non_werewolf_count == 0:
            # 狼人胜利
            termination_message = (
                f"Game ends: All non-werewolf players are eliminated. Werewolves win!"
            )
            self._log_system(termination_message)
            self.log_event(is_private=False, agent_id="system", content=termination_message)
            return True

        if werewolf_count == 0:
            # 好人胜利
            termination_message = (
                f"Game ends: All werewolves are eliminated. Villagers win!"
            )
            self._log_system(termination_message)
            self.log_event(is_private=False, agent_id="system", content=termination_message)
            return True

        # 如果未满足终止条件
        self._log_system("Game continues: No termination condition met.")
        return False


    def log_event(self, is_private: bool, agent_id: str, content: str, log_to_system: bool = True, print_to_system: bool = True) -> None:
        """
        传入内容，对象，是否私密。私密对象存在对应的私有日志中以及系统的私密日志中，公开对象存入所有日志中。
        系统的私密对象只传入系统的私密日志中。
        无论私密与否，都会打印出来。

        Args:
            is_private (bool): If True, the event is only logged in the specified private logs.
                            If False, it will be logged in the public, private, and each agent's personal logs.
            agent_id (str): The ID of the agent performing the action. Use "system" for system messages.
            content (str): The content to be logged.
            log_to_system (bool): If True, the event will also be logged in the system log. Defaults to True.
        """
        # 处理普通 agent 消息
        if agent_id != "system":
            # 将内容写入指定 agent 的个人日志
            if agent_id in self.shared_memory["private_state"]["players"]:
                player_log = self.shared_memory["private_state"]["players"][agent_id]["personal_event_log"]
                self.shared_memory["private_state"]["players"][agent_id]["personal_event_log"] = f"{player_log}\n{content}"

            if is_private:
                # 私密消息仅写入私密日志
                if log_to_system:
                    private_log = self.shared_memory["private_event_log"]
                    self.shared_memory["private_event_log"] = f"{private_log}\n{content}"
                if print_to_system:
                    self._log_player(agent_id, f"{agent_id}: {content}")
            else:
                # 公开消息写入公共和私密日志
                if log_to_system:
                    public_log = self.shared_memory["public_event_log"]
                    private_log = self.shared_memory["private_event_log"]
                    self.shared_memory["public_event_log"] = f"{public_log}\n{content}"
                    self.shared_memory["private_event_log"] = f"{private_log}\n{content}"

                # 写入每个 agent 的个人日志
                for agent in self.shared_memory["private_state"]["players"]:
                    personal_log = self.shared_memory["private_state"]["players"][agent]["personal_event_log"]
                    self.shared_memory["private_state"]["players"][agent]["personal_event_log"] = f"{personal_log}\n{content}"
                if print_to_system:
                    self._log_player(agent_id, f"{agent_id}: {content}")

        # 处理 system 消息
        else:
            if is_private:
                # 私密 system 消息仅写入私密日志
                if log_to_system:
                    private_log = self.shared_memory["private_event_log"]
                    self.shared_memory["private_event_log"] = f"{private_log}\n{content}"
                if print_to_system:
                    self._log_event(f"SYSTEM: {content}")
            else:
                # 公开 system 消息写入所有日志
                if log_to_system:
                    public_log = self.shared_memory["public_event_log"]
                    private_log = self.shared_memory["private_event_log"]
                    self.shared_memory["public_event_log"] = f"{public_log}\n{content}"
                    self.shared_memory["private_event_log"] = f"{private_log}\n{content}"

                # 写入每个 agent 的个人日志
                for agent in self.shared_memory["private_state"]["players"]:
                    personal_log = self.shared_memory["private_state"]["players"][agent]["personal_event_log"]
                    self.shared_memory["private_state"]["players"][agent]["personal_event_log"] = f"{personal_log}\n{content}"
                if print_to_system:
                    self._log_event(f"SYSTEM: {content}")

    def update_alive_players(self):
        """
        Updates the list of alive players based on their health status in private_state.
        """
        # 获取所有玩家信息
        players = self.shared_memory["private_state"]["players"]

        # 根据健康状态更新alive_players列表
        alive_players = [
            player_id for player_id, player_info in players.items()
            if player_info["status"].get("health", 0) == 1
        ]

        # 更新到public_state
        self.shared_memory["public_state"]["alive_players"] = alive_players

        # 记录日志
        self._log_system(f"Updated alive_players list: {alive_players}")

    def guard_action(self) -> None:
        """
        Publishes a guard action event to the event bus. The event is directed to the player
        with the 'guard' role and 'health' status of 1, allowing them to take their action.
        """
        # 查找存活状态（health 为 1）且身份为 "guard" 的玩家
        guard_player_instance = None
        for agent in self.agents:
            agent_id = agent.agent_id
            player_info = self.shared_memory["private_state"]["players"].get(agent_id, {})
            if player_info["role"] == "guard" and agent.agent_id in self.shared_memory["public_state"].get("alive_players", []):
                guard_player_instance = agent
                break

        if guard_player_instance:
            # 获取上次守卫的保护目标
            last_protected = self.shared_memory["private_state"].get("guard_last_night_protect", None)

            # 创建并发布守卫行动事件，仅传递 last_protected
            event = {
                "event_type": "guard_action",
                "sender": self,  # 标识为环境实例
                "recipients": [guard_player_instance],
                "content": {
                    "night_info": last_protected,
                }
            }
            self.publish_event(event)

    def process_guard_action(self, event: dict) -> None:
        """
        Processes the guard action by protecting the target specified in the event.

        Args:
            event (dict): The event data containing 'protect_target' information.
        """
        try:
            last_protected = self.shared_memory["private_state"].get("guard_last_night_protect", None)
            guard_id = event.get("sender")
            if isinstance(event.get("content", {}), dict):
                protect_target = event.get("content", {}).get("protect_target")
            else:
                protect_target = None
            # Log initial state

            # Validate protect_target
            if protect_target in self.shared_memory["private_state"]["players"]:
                if protect_target == last_protected:
                    self.log_event(
                        is_private=True, 
                        agent_id=guard_id,
                        content=f"Guard action failed. {protect_target} was protected last night and cannot be protected again tonight."
                    )
                else:
                    # Update protection count and log success
                    self.shared_memory["private_state"]["players"][protect_target]["status"]["protection_count"] = 1
                    self.shared_memory["private_state"]["guard_last_night_protect"] = protect_target
                    self.log_event(
                        is_private=True, 
                        agent_id=guard_id,
                        content=f"Guard action processed. {protect_target} is protected this night."
                    )

                    # Check and update night cache
                    if "night_cache" in self.shared_memory["private_state"]:
                        if self.shared_memory["private_state"]["night_cache"]:
                            current_night_log = self.shared_memory["private_state"]["night_cache"][-1]
                            current_night_log["guard_action"] = protect_target
                    else:
                        self._log_event("Night cache key does not exist in private state.")
            else:
                self._log_event(f"Guard action failed. Invalid protect target: {protect_target}")
            # Mark event complete
            self.mark_event_complete(event_type="guard_action")
        
        except Exception as e:
            self._log_event(f"Error processing guard action: {str(e)}")

    def werewolf_action(self) -> None:
        """
        Publishes a single werewolf action event to the event bus.
        The event is directed to all players with the 'wolf' role, allowing them to take their action.
        """
        alive_werewolves = []
        try:
            # 获取所有存活玩家的 ID 列表
            alive_players = self.shared_memory["public_state"].get("alive_players", [])

            # 获取所有存活的狼人玩家的实例索引和 ID
            for agent in self.agents:
                player_info = self.shared_memory["private_state"]["players"].get(agent.agent_id, {})
                    
                    # 检查角色是否是狼人并且健康状态是否为 1（存活）
                if player_info.get("role") == "wolf" and agent.agent_id in self.shared_memory["public_state"].get("alive_players", []):
                    alive_werewolves.append((agent, agent.agent_id))

            # 提取狼人实例和 ID 列表
            alive_werewolves_instances = [agent for agent, _ in alive_werewolves]
            alive_werewolves_ids = [agent_id for _, agent_id in alive_werewolves]

            new_round_target = {wolf_id: None for wolf_id in alive_werewolves_ids}
            self.shared_memory["private_state"]["werewolf_action"]["round_targets"].append(new_round_target)

            # 生成逗号分隔的 ID 列表字符串
            alive_players_str = ", ".join(alive_players)
            alive_werewolves_ids_str = ", ".join(map(str, alive_werewolves_ids))

            # 发布狼人行动事件，将所有存活狼人作为接收者
            event = {
                "event_type": "werewolf_action",
                "sender": self,  # 标识为环境实例
                "recipients": alive_werewolves_instances,  # 所有存活狼人实例索引
                "content": {
                    "player_info": {
                        "alive_players": alive_players_str,  # 所有存活玩家的 ID 字符串
                        "alive_werewolves": alive_werewolves_ids_str  # 所有存活狼人的 ID 字符串
                    }
                }
            }
            self.publish_event(event)
        except Exception as e:
            self._log_event(f"Error in werewolf_action: {str(e)}")
            raise

    def werewolf_discussion(self) -> None:
        """
        Publishes a werewolf discussion event to the event bus.
        The event is directed to all players with the 'wolf' role, allowing them to discuss and refine their action.
        """
        # 获取所有存活玩家的 ID 列表
        alive_players = self.shared_memory["public_state"].get("alive_players", [])

        # 获取所有存活的狼人玩家的实例索引和 ID
        alive_werewolves = []
        for agent in self.agents:
                player_info = self.shared_memory["private_state"]["players"].get(agent.agent_id, {})
                    
                    # 检查角色是否是狼人并且健康状态是否为 1（存活）
                if player_info.get("role") == "wolf" and agent.agent_id in self.shared_memory["public_state"].get("alive_players", []):
                    alive_werewolves.append((agent, agent.agent_id))
        # 提取狼人实例和 ID 列表
        alive_werewolves_instances = [agent for agent, _ in alive_werewolves]
        alive_werewolves_ids = [agent_id for _, agent_id in alive_werewolves]

        # 获取倒数第二轮的狼人目标信息
        last_round_targets = self.shared_memory["private_state"]["werewolf_action"]["round_targets"][-2]
        allies_target_info = {wolf_id: target for wolf_id, target in last_round_targets.items()}

        # 获取剩余讨论轮次数量
        rounds_remaining = self.shared_memory["private_state"]["werewolf_action"]["rounds_remaining"]

        # 生成逗号分隔的 ID 列表字符串
        alive_players_str = ", ".join(alive_players)
        alive_werewolves_ids_str = ", ".join(alive_werewolves_ids)

        # 创建讨论事件内容
        event_content = {
            "allies_info": {
                "alive_players": alive_players_str,
                "alive_werewolves": alive_werewolves_ids_str,
                "last_round_targets": allies_target_info
            },
            "rounds_remaining": rounds_remaining
        }

        # 发布狼人讨论事件，将所有存活狼人作为接收者
        event = {
            "event_type": "werewolf_discussion",
            "sender": self,  # 标识为环境实例
            "recipients": alive_werewolves_instances,  # 所有存活狼人实例索引
            "content": event_content
        }
        self.event_bus.publish(event)

    def process_werewolf_action(self, event: dict) -> None:
        """
        Processes the werewolf action by recording the target specified in the event.

        Args:
            event (dict): The event data containing 'attack' and 'target' information.
        """
        werewolf_id = event.get("sender")
        action_content = event.get("content", {})
        if isinstance(action_content, dict):
            attack = action_content.get("attack", False)
            target = action_content.get("target", None)
        else:
            attack = False
            target = None
        current_round_targets = self.shared_memory["private_state"]["werewolf_action"]["round_targets"][-1]

        if werewolf_id not in current_round_targets:
            self._log_event(f"Invalid werewolf ID: {werewolf_id}.")
            return

        if not attack:
            current_round_targets[werewolf_id] = "false"
        elif attack and target in self.shared_memory["public_state"]["alive_players"]:
            current_round_targets[werewolf_id] = target
        else:
            current_round_targets[werewolf_id] = "false"

        if any(value is None for value in current_round_targets.values()):
            self._log_event("Waiting for all werewolves to respond.")
            return

        target_counts = {}
        for choice in current_round_targets.values():
            if choice != "false":
                target_counts[choice] = target_counts.get(choice, 0) + 1

        # 检查是否有目标获得绝对多数票
        alive_werewolves_count = len([
            agent_id for agent_id, player_info in self.shared_memory["private_state"]["players"].items()
            if player_info["role"] == "wolf" and player_info["status"].get("health", 0) == 1
        ])
        majority_target = None
        for target, count in target_counts.items():
            if count > alive_werewolves_count / 2:  # 确保获得超过半数票
                majority_target = target
                break

        if majority_target:
            self.shared_memory["private_state"]["werewolf_action"]["final_target"] = majority_target
            target_status = self.shared_memory["private_state"]["players"][majority_target]["status"]
            if target_status["protection_count"] == 0:
                target_status["health"] = 0
                success = True
                kill_result = f"Target {majority_target} attacked by werewolves and health reduced."
            else:
                success = False
                kill_result = f"Target {majority_target} protected, no health reduction."

            if self.shared_memory["private_state"]["night_cache"]:
                current_night_log = self.shared_memory["private_state"]["night_cache"][-1]
                current_night_log["werewolf_action"] = {
                    "final_target": majority_target,
                    "attack_successful": success,
                }
                if "player_dead_tonight" not in current_night_log:
                    current_night_log["player_dead_tonight"] = []
                if success:
                    current_night_log["player_dead_tonight"].append(majority_target)
            else:
                self._log_event("Night cache is not initialized.")

            alive_werewolves = []
            for agent in self.agents:
                    player_info = self.shared_memory["private_state"]["players"].get(agent.agent_id, {})
                        
                        # 检查角色是否是狼人并且健康状态是否为 1（存活）
                    if player_info.get("role") == "wolf" and player_info.get("status", {}).get("health", 0) == 1:
                        alive_werewolves.append(agent.agent_id)
            round_details = {
                "round_targets": current_round_targets,
                "remaining_werewolves": alive_werewolves,
                "discussion_rounds_left": self.shared_memory["private_state"]["werewolf_action"]["rounds_remaining"],
                "final_target": majority_target,
                "attack_successful": success
            }
            detailed_kill_result_system = (
                f"Round Details:\n"
                f" - Round Targets: {round_details['round_targets']}\n"
                f" - Remaining Werewolves: {round_details['remaining_werewolves']}\n"
                f" - Discussion Rounds Left: {round_details['discussion_rounds_left']}\n"
                f" - Final Target: {round_details['final_target']}\n"
                f" - Attack Successful: {round_details['attack_successful']}\n"
                f"Result: {kill_result}"
            )
            detailed_kill_result_player = (
                f"Round Details:\n"
                f" - Round Targets: {round_details['round_targets']}\n"
                f" - Remaining Werewolves: {round_details['remaining_werewolves']}\n"
                f" - Discussion Rounds Left: {round_details['discussion_rounds_left']}\n"
                f" - Final Target: {round_details['final_target']}\n"
            )

            for wolf_id in current_round_targets.keys():
                self.log_event(
                    is_private=True,
                    agent_id=wolf_id,
                    content=detailed_kill_result_player,
                    log_to_system=False,
                    print_to_system=False
                )
            self.log_event(
                is_private=True,
                agent_id="system",
                content=detailed_kill_result_system
            )
            self.mark_event_complete(event_type="werewolf_action")
        else:
            self._log_event("Werewolf attack failed due to lack of a clear majority target.")
            self.shared_memory["private_state"]["werewolf_action"]["rounds_remaining"] -= 1

            if self.shared_memory["private_state"]["werewolf_action"]["rounds_remaining"] > 0:
                # 获取存活狼人列表
                alive_werewolves_ids = []
                for agent in self.agents:
                    player_info = self.shared_memory["private_state"]["players"].get(agent.agent_id, {})

                    if player_info.get("role") == "wolf" and player_info.get("status", {}).get("health", 0) == 1:
                        alive_werewolves_ids.append(agent.agent_id)
                
                # 创建新一轮目标字典
                new_round_target = {wolf_id: None for wolf_id in alive_werewolves_ids}

                # 确保 round_targets 是一个列表
                if isinstance(self.shared_memory["private_state"]["werewolf_action"].get("round_targets"), list):
                    self.shared_memory["private_state"]["werewolf_action"]["round_targets"].append(new_round_target)
                else:
                    self._log_event("Error: round_targets is not a list. Resetting it to a new list.")
                    self.shared_memory["private_state"]["werewolf_action"]["round_targets"] = [new_round_target]
                
                # 进入狼人讨论阶段
                self.werewolf_discussion()
            else:
                # 记录剩余狼人列表
                alive_werewolves = []
                for agent in self.agents:
                    player_info = self.shared_memory["private_state"]["players"].get(agent.agent_id, {})

                    if player_info.get("role") == "wolf" and player_info.get("status", {}).get("health", 0) == 1:
                            alive_werewolves.append(agent.agent_id)
                
                # 构造详细的失败结果
                round_details = {
                    "round_targets": current_round_targets,
                    "remaining_werewolves": alive_werewolves,
                    "discussion_rounds_left": 0,
                    "final_target": "None",
                    "attack_successful": False
                }
                detailed_fail_result = (
                    f"Round Details:\n"
                    f" - Round Targets: {round_details['round_targets']}\n"
                    f" - Remaining Werewolves: {round_details['remaining_werewolves']}\n"
                    f" - Discussion Rounds Left: {round_details['discussion_rounds_left']}\n"
                    f" - Final Target: {round_details['final_target']}\n"
                    f" - Attack Successful: {round_details['attack_successful']}\n"
                    "Result: Attack failed due to lack of consensus among werewolves."
                )

                # 向每个狼人记录私密日志
                for wolf_id in current_round_targets.keys():
                    self.log_event(
                        is_private=True,
                        agent_id=wolf_id,
                        content=detailed_fail_result,
                        log_to_system=False,
                        print_to_system=False
                    )
                
                # 系统日志记录
                self.log_event(
                    is_private=True,
                    agent_id="system",
                    content=detailed_fail_result
                )

                # 记录到夜晚缓存中
                if isinstance(self.shared_memory["private_state"].get("night_cache"), list):
                    current_night_log = self.shared_memory["private_state"]["night_cache"][-1]
                    current_night_log["werewolf_action"] = {
                        "final_target": "None",
                        "attack_successful": False,
                        "reason": "Failed due to lack of consensus"
                    }
                else:
                    self._log_event("Night cache is not initialized.")
                
                # 标记狼人行动事件完成
                self.mark_event_complete(event_type="werewolf_action")

    def seer_action(self) -> None:
        """
        Publishes a seer action event to the event bus. The event is directed to the player
        with the 'seer' role and 'health' status of 1, allowing them to take their action.
        """
        # 查找存活状态（health 为 1）且身份为 "seer" 的玩家
        seer_player_instance = None
        for agent in self.agents:
            agent_id = agent.agent_id
            player_info = self.shared_memory["private_state"]["players"].get(agent_id, {})
            if player_info["role"] == "seer" and agent.agent_id in self.shared_memory["public_state"].get("alive_players", []):
                seer_player_instance = agent
                break

        if seer_player_instance:
            # 创建并发布预言家行动事件，不包含任何额外内容
            event = {
                "event_type": "seer_action",
                "sender": self,  # 标识为环境实例
                "recipients": [seer_player_instance],
                "content": {}  # 不传入任何内容
            }
            
            self._log_event(f"Seer action event published.")
            self.publish_event(event)
        else:
            self._log_event(f"Seer action event published.")

    def process_seer_action(self, event: dict) -> None:
        """
        Processes the seer action by recording the check target specified in the event.

        Args:
            event (dict): The event data containing 'check_target' information.
        """
        try:
            # 从事件内容中获取预言家行动的选择
            seer_id = event.get("sender")
            action_content = event.get("content", {})
            if isinstance(action_content, dict):
                check_target = action_content.get("check_target", None)  # 从内容中直接获取目标
            else:
                check_target = None
            # 获取存活玩家列表
            alive_players = self.shared_memory.get("public_state", {}).get("alive_players", [])
            if not alive_players:
                self.log_event(
                    is_private=True,
                    agent_id="system",
                    content="Error: Unable to retrieve alive players list from public state."
                )
                self.mark_event_complete(event_type="seer_action")
                return

            # 检查目标是否有效
            if check_target not in alive_players:
                self.log_event(
                    is_private=True,
                    agent_id=seer_id,
                    content=f"<<Private>> Seer action failed. Invalid check target: {check_target}. Not in alive players: {alive_players}.",
                    log_to_system=False
                )
                self.mark_event_complete(event_type="seer_action")
                return

            # 确保 check_history 初始化
            seer_status = self.shared_memory["private_state"]["players"][seer_id]["status"]
            if "check_history" not in seer_status:
                seer_status["check_history"] = {}

            # 计算当前是第几夜
            current_night = self.shared_memory["public_state"]["days"]

            # 判断目标是否为狼人并记录结果
            is_werewolf = self.shared_memory["private_state"]["players"][check_target]["role"] == "wolf"
            check_result = "werewolf" if is_werewolf else "not a werewolf"

            # 更新预言家的查验历史，包含第几夜的信息
            check_history_entry = {"player": check_target, "result": check_result}
            seer_status["check_history"][f"Night {current_night}"] = check_history_entry

            # 记录事件日志到预言家的私密日志
            seer_log_content = (
                f"At Night {current_night}, You have checked {check_target}, the result is: {check_result}."
            )
            self.log_event(
                is_private=True,
                agent_id=seer_id,
                content=seer_log_content,
                log_to_system=False
            )

            # 系统私密日志记录
            system_log_content = (
                f"System log - Seer action:\n"
                f" - Seer ID: {seer_id}\n"
                f" - Night {current_night}: Checked {check_target} - Result: {check_result}"
            )
            self.log_event(
                is_private=True,
                agent_id="system",
                content=system_log_content
            )
            self.mark_event_complete(event_type="seer_action")
        except Exception as e:
            self.log_event(
                is_private=True,
                agent_id="system",
                content=f"Error processing seer action: {str(e)}"
            )
            self.mark_event_complete(event_type="seer_action")

    def witch_action(self) -> None:
        """
        Publishes a witch action event to the event bus. The event is directed to the player
        with the 'witch' role and 'health' status of 1, allowing them to take their action.
        """
        # 查找存活状态（health 为 1）且身份为 "witch" 的玩家
        witch_player_instance = None
        for agent in self.agents:
            agent_id = agent.agent_id
            player_info = self.shared_memory["private_state"]["players"].get(agent_id, {})
            if player_info["role"] == "witch" and agent.agent_id in self.shared_memory["public_state"].get("alive_players", []):
                witch_player_instance = agent
                break

        if witch_player_instance:
            # 从 werewolf_action 中获取 final_target，表示狼人当晚的袭击目标
            final_target = self.shared_memory["private_state"]["werewolf_action"].get("final_target", "nobody")


            # 创建并发布女巫行动事件，包含夜晚信息
            event = {
                "event_type": "witch_action",
                "sender": self,  # 标识为环境实例
                "recipients": [witch_player_instance],
                "content": {
                    "night_info": final_target
                }
            }
            self.publish_event(event)
            self._log_event(f"Witch action event published.")
        else:
            self._log_event(f"Witch action event published.")

    def process_witch_action(self, event: dict) -> None:
        """
        Processes the witch action based on the event content, applying antidote or poison
        to the specified targets as chosen by the witch and updating the available potion counts.

        Args:
            event (dict): The event data containing the witch's choices for using antidote and poison.
        """
        # 获取事件内容，包括解药和毒药的使用决定
        action_content = event.get("content", {})
        if isinstance(action_content, dict):
            use_antidote = action_content.get("use_antidote", False)
            use_poison = action_content.get("use_poison", False)
            poison_target = action_content.get("poison_target", None)
        else:
            use_antidote = False
            use_poison = False
            poison_target = None
        # 获取女巫 ID 及其状态信息
        witch_id = event["sender"]
        witch_status = self.shared_memory["private_state"]["players"][witch_id]["status"]

        # 从 shared memory 中获取当晚被杀的目标
        final_target = self.shared_memory["private_state"]["werewolf_action"].get("final_target")

        # 获取当前夜晚的缓存日志
        current_night_log = self.shared_memory["private_state"].get("night_cache", [])[-1]

        # 处理解药的使用
        if use_antidote and final_target and witch_status["antidote_count"] > 0:
            # 使用解药将血量恢复至 1
            self.shared_memory["private_state"]["players"][final_target]["status"]["health"] = 1
            witch_status["antidote_count"] = 0  # 更新解药数量

            # 从 death 列表中移除被救的玩家
            if final_target in current_night_log["player_dead_tonight"]:
                current_night_log["player_dead_tonight"].remove(final_target)

            # 记录事件日志
            self.log_event(
                is_private=True,
                agent_id=witch_id,
                content=f"Witch used antidote to save {final_target}."
            )
            self.log_event(
                is_private=True,
                agent_id="system",
                content=f"Witch used antidote to save {final_target}."
            )

            # 更新 night_cache 中的女巫解药行动
            current_night_log["witch_action"] = {
                "action": "antidote",
                "target": final_target
            }
            self.mark_event_complete(event_type="witch_action")


        # 处理毒药的使用
        elif use_poison and poison_target in self.shared_memory["public_state"]["alive_players"] and witch_status["poison_count"] > 0:
            # 使用毒药将目标血量设置为 0
            self.shared_memory["private_state"]["players"][poison_target]["status"]["health"] = 0
            witch_status["poison_count"] = 0  # 更新毒药数量

            # 在 death 列表中添加毒死的玩家
            current_night_log["player_dead_tonight"].append(poison_target)

            # 记录事件日志
            self.log_event(
                is_private=True,
                agent_id=witch_id,
                content=f"Witch used poison on {poison_target}."
            )
            self.log_event(
                is_private=True,
                agent_id="system",
                content=f"Witch used poison on {poison_target}."
            )

            # 更新 night_cache 中的女巫毒药行动
            current_night_log["witch_action"] = {
                "action": "poison",
                "target": poison_target
            }
            self.mark_event_complete(event_type="witch_action")

        # 若女巫未使用解药且未使用毒药，记录行动结果
        elif not use_antidote and not use_poison:
            self.log_event(
                is_private=True,
                agent_id=witch_id,
                content="Witch chose not to use antidote or poison tonight."
            )
            self.log_event(
                is_private=True,
                agent_id="system",
                content="Witch chose not to use antidote or poison tonight."
            )

            # 更新 night_cache 中的女巫未使用行动记录
            current_night_log["witch_action"] = {
                "action": "none",
                "target": None
            }
            self.mark_event_complete(event_type="witch_action")

    def run_for_sheriff(self) -> None:
        """
        Publishes a 'run for sheriff' event to the event bus. This event is directed to all 
        players with a 'health' status of 1, allowing them to decide if they want to run for sheriff.
        """
        # 初始化 sheriff_election 字段
        if "sheriff_election" not in self.shared_memory["private_state"]:
            # 初始化警长竞选状态，包含所有玩家的候选状态（默认为 None）
            self.shared_memory["private_state"]["sheriff_election"] = {
                "candidates": {agent.agent_id: None for agent in self.agents}
            }

        # 查找所有存活玩家
        alive_players = [
            agent for agent in self.agents
            if agent.agent_id in self.shared_memory["public_state"].get("alive_players", [])
        ]

        if alive_players:
            # 创建并发布竞选警长事件
            event = {
                "event_type": "run_for_sheriff",
                "sender": self,  # 标识为环境实例
                "recipients": alive_players,  # 所有存活玩家的实例引用
                "content": {}  # 不传入额外内容
            }
            self.publish_event(event)
            self._log_event("Run for sheriff event published for all living players.")
        else:
            self._log_event("No living players found to participate in sheriff election.")

    def process_run_for_sheriff(self, event: dict) -> None:
        """
        Processes each player's decision on whether or not to run for sheriff and 
        prepares candidates for the sheriff election once all decisions are received.

        Updates the day cache with the list of candidates and relevant events.

        Args:
            event (dict): The event data containing the player's decision on running for sheriff.
        """
        # 从事件内容中获取玩家的参选决定
        player_id = event.get("sender", None)
        if isinstance(event.get("content", {}), dict):
            run_for_sheriff = event.get("content", {}).get("run_for_sheriff", False)
        else:
            run_for_sheriff = False
        # 将玩家的决定e记录到 shard memory 中的 sheriff_election 中
        self.shared_memory["private_state"]["sheriff_election"]["candidates"][player_id] = run_for_sheriff

        # 检查是否所有存活玩家都做出了决定
        if any(choice is None for choice in self.shared_memory["private_state"]["sheriff_election"]["candidates"].values()):
            self._log_system(f"current decision:{self.shared_memory['private_state']['sheriff_election']['candidates']}")
            self._log_event("Waiting for all players to decide on running for sheriff.")
            return

        # 获取当前天数的 day_cache
        current_day = self.shared_memory["public_state"]["days"]
        day_cache = self.shared_memory["public_state"]["day_cache"][current_day - 1]

        # 初始化 day_cache 的 "sheriff_candidates" 键为一个空列表（如果不存在）
        if "sheriff_candidates" not in day_cache:
            day_cache["sheriff_candidates"] = []

        # 获取所有决定参选的玩家列表，并按编号从小到大排序
        candidate_ids = sorted([
            agent_id for agent_id, wants_to_run in self.shared_memory["private_state"]["sheriff_election"]["candidates"].items()
            if wants_to_run
        ])

        # 记录竞选候选人信息为公开消息
        if candidate_ids:
            candidate_list_str = ", ".join(candidate_ids)
            self.log_event(
                is_private=False,
                agent_id="system",
                content=f"Sheriff election candidates: {candidate_list_str}"
            )

            # 将候选人列表存入 day_cache 的 sheriff_candidates
            day_cache["sheriff_candidates"] = candidate_ids

            # 初始化 sheriff_speech 字典，所有候选人的演讲内容为 None
            self.shared_memory["private_state"]["sheriff_election"]["sheriff_speech"] = {candidate_id: None for candidate_id in candidate_ids}
            self.shared_memory["private_state"]["sheriff_election"]["final_candidate"] = []


            # 调用第一个候选人的演讲
            first_candidate_id = candidate_ids[0]
            self.mark_event_complete(event_type="run_for_sheriff")
            self.sheriff_speech(candidate_ids, first_candidate_id)
            
            

        else:
            # 无人参选，记录信息
            self._log_event("No candidates decided to run for sheriff.")
            self.mark_event_complete(event_type="run_for_sheriff")
            return

    def sheriff_speech(self, candidate_ids: list, candidate_id: str, first=True) -> None:
        """
        Publishes a 'sheriff_speech' event for a given candidate, allowing them to make their speech for the election.

        Args:
            candidate_ids (list): List of IDs of all candidates running for sheriff, sorted by ID.
            candidate_id (str): The ID of the current candidate making their speech.
        """
        # 获取当前天数的 day_cache
        current_day = self.shared_memory["public_state"]["days"]
        day_cache = self.shared_memory["public_state"]["day_cache"][current_day - 1]

        # 初始化 day_cache 的 "sheriff_speech" 和 "final_candidate" 键
        day_cache.setdefault("sheriff_speech", {cid: None for cid in candidate_ids})
        day_cache.setdefault("final_candidate", [])

        # 获取所有候选人的 ID 列表作为 speech_sequence，并以逗号分隔
        speech_sequence = ", ".join(candidate_ids)

        # 确定当前候选人在候选人列表中的位置（从 1 开始计数）
        speech_position = candidate_ids.index(candidate_id) + 1

        # 构建 election_info，包含所有已完成演讲的内容
        if day_cache.get("sheriff_speech") and any(speech is not None for speech in day_cache["sheriff_speech"].values()):
            election_info = "\n".join([
                f"{cid}: {speech}" for cid, speech in day_cache["sheriff_speech"].items()
                if speech is not None
            ])
        else:
            election_info = "No speeches available yet. You are the first one."

        # 获取当前候选人的实例
        candidate_instance = None
        for agent in self.agents:
            if agent.agent_id == candidate_id:
                candidate_instance = agent
                break
        if candidate_instance is None:
            self._log_system(f"Error: Candidate instance for {candidate_id} not found.")
            return            
        # 创建并发布 sheriff_speech 事件
        event = {
            "event_type": "sheriff_speech",
            "sender": self,  # 标识为环境实例
            "recipients": [candidate_instance],  # 当前候选人实例
            "content": {
                "election_info": election_info,
                "speech_sequence": speech_sequence,
                "speech_position": str(speech_position)
            }
        }
        
        self._log_system(f"Sheriff speech event published for candidate {candidate_id}.")
        if first:
            self.publish_event(event)
        else:
            self.event_bus.publish(event)
        
    def process_sheriff_speech(self, event: dict) -> None:
        """
        Processes each candidate's sheriff speech, recording their decision to continue in the election
        and their speech content. Proceeds to the next candidate's speech if there are remaining candidates.

        Updates the day cache with speech details and the list of final candidates.

        Args:
            event (dict): The event data containing the candidate's speech and decision to continue.
        """
        try:
            # 获取候选人 ID 和发言内容
            candidate_id = event.get("sender", "")
            action_content = event.get("content", {})
            if isinstance(action_content, dict):
                continue_running = action_content.get("continue_running", False)
                speech_content = action_content.get("speech_content", f"Error during generation for player {candidate_id}.")
            else:
                speech_content = f"Error during generation for player {candidate_id}."
                continue_running = False

            # 获取当前天数的 day_cache
            current_day = self.shared_memory["public_state"]["days"]
            day_cache = self.shared_memory["public_state"]["day_cache"][current_day - 1]

            # Step 1: 记录候选人的发言内容到 day_cache 的 sheriff_speech
            day_cache["sheriff_speech"][candidate_id] = speech_content
            self.log_event(
                is_private=False,
                agent_id=candidate_id,
                content=f"{candidate_id}'s speech: {speech_content}"
            )

            # Step 2: 更新候选人的状态
            if continue_running:
                # 如果候选人选择继续竞选，添加到最终候选人列表
                day_cache["final_candidate"].append(candidate_id)
            else:
                # 候选人退出竞选的决定
                self.log_event(
                    is_private=False,
                    agent_id="system",
                    content=f"{candidate_id} has withdrawn from the sheriff election."
                )

            # Step 3: 检查是否还有候选人未发言
            candidate_ids = list(day_cache["sheriff_speech"].keys())
            remaining_candidates = [cid for cid in candidate_ids if day_cache["sheriff_speech"].get(cid) is None]

            if remaining_candidates:
                next_candidate_id = remaining_candidates[0]
                self.sheriff_speech(candidate_ids, next_candidate_id, first=False)

        except Exception as e:
            # 记录错误日志
            self._log_event(f"Error processing sheriff speech: {e}")

        finally:
            # 如果没有剩余候选人，标记事件完成
            if not remaining_candidates:
                self._log_event(f"All candidates finish their speech. Now, remaining players will vote for sheriff.")
                self.mark_event_complete(event_type="sheriff_speech")
                self.vote_for_sheriff()

    def vote_for_sheriff(self) -> None:
        """
        启动警长选举的投票流程，向所有符合条件的玩家广播一条“vote_for_sheriff”事件。
        符合条件的玩家是那些未参与警长竞选的存活玩家。
        """
        # 第一步：获取选举日志和候选人列表
        election_log = self.shared_memory["private_state"]["sheriff_election"].get("sheriff_speech", {})
        final_candidates = self.shared_memory["private_state"]["sheriff_election"].get("final_candidate", [])

        # 将选举日志转换为指定格式的字符串
        election_log_str = "\n".join([f"{candidate}: {speech}" for candidate, speech in election_log.items()])
        # 将候选人列表转换为逗号分隔的字符串
        candidate_list_str = ", ".join(final_candidates)

        # 第二步：确定投票对象（从未参选的玩家中筛选存活玩家）
        all_players = self.shared_memory["public_state"]["alive_players"]
        never_ran_for_sheriff = [
            player_id for player_id in all_players 
            if not self.shared_memory["private_state"]["sheriff_election"]["candidates"].get(player_id)
        ]
        
        # 根据玩家 ID 获取对应的玩家引用
        voter_refs = [agent for agent in self.agents if agent.agent_id in never_ran_for_sheriff]

        # 第三步：构建投票事件
        event = {
            "event_type": "vote_for_sheriff",
            "sender": self,  # 环境实例
            "recipients": voter_refs,  # 发送玩家引用而非 ID
            "content": {
                "election_log": election_log_str,
                "candidate_list": candidate_list_str
            }
        }

        # 第四步：发布投票事件
        self._log_event(f"Vote for sheriff event published to eligible voters{never_ran_for_sheriff}.")
        self.publish_event(event)
        
    def process_vote_for_sheriff(self, event):
        """
        Process each sheriff election vote after receiving a vote event.
        Records each player's vote, then determines the sheriff once all votes are cast.
        If there's a tie, no sheriff is chosen. Publishes all players' votes publicly with the final sheriff announcement.

        Updates the day cache with voting details and results.

        Args:
            event (dict): Contains the voting event details, including the player ID and their vote.
        """
        # Step 1: Record the vote
        voter_id = event.get("sender", None)
        if isinstance(event.get("content", {}), dict):
            vote_choice = event.get("content", {}).get("action_vote", "abstain")
        else:
            vote_choice = "abstain"
        # Get current day and day cache
        current_day = self.shared_memory["public_state"]["days"]
        day_cache = self.shared_memory["public_state"]["day_cache"][current_day - 1]

        # Initialize day cache keys if not present
        if "sheriff_votes" not in day_cache:
            day_cache["sheriff_votes"] = {}
        if "sheriff_result" not in day_cache:
            day_cache["sheriff_result"] = None

        # Store the vote in day_cache
        day_cache["sheriff_votes"][voter_id] = vote_choice

        # Step 2: Check if all eligible players have voted
        eligible_voters = [
            player_id for player_id in self.shared_memory["public_state"]["alive_players"]
            if not self.shared_memory["private_state"]["sheriff_election"]["candidates"].get(player_id)
        ]
        all_votes_cast = all(voter in day_cache["sheriff_votes"] for voter in eligible_voters)

        if not all_votes_cast:
            # If votes are still pending, log and wait for further events
            self._log_event("Waiting for remaining players to cast their votes for sheriff.")
            return

        # Step 3: Tally the votes
        votes = day_cache["sheriff_votes"]
        vote_counts = {}
        for voter, choice in votes.items():
            if choice != "abstain":  # Ignore abstentions
                vote_counts[choice] = vote_counts.get(choice, 0) + 1

        # Step 4: Determine the player with the highest vote count
        max_votes = max(vote_counts.values(), default=0)
        candidates_with_max_votes = [candidate for candidate, count in vote_counts.items() if count == max_votes]

        if len(candidates_with_max_votes) == 1:
            # A single player has the most votes, they become the sheriff
            sheriff_id = candidates_with_max_votes[0]
            self.shared_memory["public_state"]["sheriff"] = sheriff_id
            self.shared_memory["private_state"]["players"][sheriff_id]["status"]["badge_count"] = 1

            # Record the sheriff result in day cache
            day_cache["sheriff_result"] = sheriff_id

            # Announce the sheriff result
            announcement = f"{sheriff_id} has been elected as the sheriff."
            self.log_event(
                is_private=False, 
                agent_id="system", 
                content=announcement
                )
                
        else:
            # If there's a tie or no votes, no sheriff is chosen
            self.shared_memory["public_state"]["sheriff"] = None
            day_cache["sheriff_result"] = "No sheriff due to tie"

            # Announce the tie result
            announcement = "No sheriff was elected due to a tie."
            self.log_event(
                is_private=False, 
                agent_id="system", 
                content=announcement
                )

        # Step 5: Publish all votes publicly with the sheriff announcement
        vote_summary = "\n".join([f"{voter} voted for {choice}" for voter, choice in votes.items()])
        self.log_event(
            is_private=False, 
            agent_id="system", 
            content=f"Sheriff election votes:\n{vote_summary}"
            )

        # Update day cache with vote summary
        day_cache["vote_summary"] = vote_summary
        self.mark_event_complete(event_type="vote_for_sheriff")

    def get_night_deceased(self) -> list:
        """
        Retrieves the list of players who died during the night from the night_cache.
        Logs the deceased players publicly and returns the list of deceased players.
        
        Returns:
            list: A list of player IDs who died during the night.
        """
        # Access the most recent night log from the night_cache
        current_night_log = self.shared_memory["private_state"].get("night_cache", [])[-1]
        deceased_players = current_night_log.get("player_dead_tonight", [])

        # Log deceased players publicly
        if deceased_players:
            deceased_names = ", ".join(deceased_players)
            self.log_event(is_private=False, agent_id="system", content=f"Players deceased during the night: {deceased_names}")
        else:
            self.log_event(is_private=False, agent_id="system", content="No players deceased during the night.")

        # Check if the sheriff is among the deceased players
        sheriff_id = self.shared_memory["public_state"].get("sheriff")
        if sheriff_id in deceased_players:
            self.log_event(is_private=False, agent_id="system", content=f"The deceased player {sheriff_id} was the sheriff. Processing badge flow.")
            self.badge_flow(sheriff_id=sheriff_id)
        
        return deceased_players
    
    def sheriff_decide_speech_order(self) -> None:
        """
        Publishes an event to the sheriff, allowing them to decide the speech order.
        The event includes the list of players who died during the previous night.

        Returns:
            list: A list of player IDs representing the speech order determined by the sheriff.
        """
        # Step 1: Get the current sheriff's ID and reference
        sheriff_id = self.shared_memory["public_state"]["sheriff"]
        if not sheriff_id or sheriff_id not in self.shared_memory["public_state"].get("alive_players", []):
            self._log_event("No sheriff present to decide the speech order.")
            return []

        sheriff_ref = next((agent for agent in self.agents if agent.agent_id == sheriff_id), None)
        if not sheriff_ref:
            self._log_event(f"Could not find a valid reference for the sheriff: {sheriff_id}")
            return []
        
        # Step 2: Get the list of deceased players from the previous night
        deceased = self.get_night_deceased()

        # Step 3: Create the event for the sheriff
        event = {
            "event_type": "decide_speech_sequence",
            "sender": self,  # The environment is the sender
            "recipients": [sheriff_ref],  # Reference to the sheriff's agent
            "content": {
                "dead_player_list": deceased  # Provide the deceased players
            }
        }

        # Step 4: Publish the event to the sheriff
        self.publish_event(event)
        current_day = self.shared_memory["public_state"].get("days", 0)
        day_cache = self.shared_memory["public_state"]["day_cache"][current_day - 1]
        return day_cache["speech_order_decision"]

    def process_sheriff_decide_speech_order(self, event):
        """
        Process the sheriff's decision for the speaking sequence and generate the order of speeches.
        Start from the specified player and direction, remove deceased players before finalizing the order.
        """
        # Step 1: 获取所有玩家和警长的选择
        all_players = sorted(self.shared_memory["private_state"]["players"].keys())  # 按玩家 ID 排序
        alive_players = self.shared_memory["public_state"].get("alive_players", [])
        sheriff_id = self.shared_memory["public_state"].get("sheriff", None)
        if isinstance(event.get("content", {}), dict):
            starting_player = event.get("content", {}).get("starting_player", sheriff_id)
            from_left = event.get("content", {}).get("from_left", True)
        else:
            starting_player = sheriff_id
            from_left = True
        # 获取当日的 day_cache
        day_cache = self.shared_memory["public_state"]["day_cache"][-1]

        # 初始化 day_cache 的 speech_order_decision（如果不存在）
        if "speech_order_decision" not in day_cache:
            day_cache["speech_order_decision"] = []

        # Step 2: 检查起始玩家是否在玩家列表中
        if starting_player not in all_players:
            # 如果起始玩家无效，则默认从 agent_1 开始
            starting_player = all_players[0]

        # Step 3: 按起始玩家和方向生成发言顺序
        starting_index = all_players.index(starting_player)

        if from_left:  # 从左边（数字减小方向）开始
            speech_order = all_players[starting_index:] + all_players[:starting_index]
        else:  # 从右边（数字增大方向）开始
            speech_order = all_players[starting_index::-1] + all_players[:starting_index:-1]

        # 警长始终最后发言
        if sheriff_id in speech_order:
            speech_order.remove(sheriff_id)
            speech_order.append(sheriff_id)

        # Step 4: 移除死亡玩家，生成最终发言顺序
        speech_order = [player for player in speech_order if player in alive_players]

        # 保存和记录发言顺序
        day_cache["speech_order_decision"] = speech_order

        # 公布顺序
        order_string = ", ".join(speech_order)
        self.log_event(
            is_private=False,
            agent_id="system",
            content=f"The speaking sequence for this round is: {order_string}"
        )
        self.mark_event_complete(event_type="decide_speech_sequence")

    def player_speeches(self, current_speaker_id: str = None) -> None:
        """
        Executes the daytime player speeches in the order specified by the current day's speech_order.
        Each player provides their speech, and the system logs their content.

        Args:
            current_speaker_id (str): The ID of the current player speaking. If None, starts from the first player in the order.
        """
        day_cache = self.shared_memory["public_state"]["day_cache"][-1]
        # Step 1: 获取当日的发言顺序
        speech_order = day_cache.get("speech_order_decision", None)
        self._log_system(f"current speech order: {speech_order}")
        if not speech_order:
            # 获取默认发言顺序（从存活玩家中按升序排序）
            alive_players = self.shared_memory["public_state"]["alive_players"]
            speech_order = sorted(alive_players)

        # Step 2: 确定当前发言人
        if current_speaker_id is None:
            current_speaker_id = speech_order[0]

        # 跳过已经死亡的玩家
        while current_speaker_id and self.shared_memory["private_state"]["players"][current_speaker_id]["status"]["health"] == 0:
            next_index = (speech_order.index(current_speaker_id) + 1) % len(speech_order)
            current_speaker_id = speech_order[next_index]

        if not current_speaker_id:
            self.log_event(is_private=False, agent_id="system", content="All players eligible to speak are dead.")
            return

        if "speech_log" not in day_cache:
            day_cache["speech_log"] = {}

        # 构建演讲内容的历史信息
        speech_log = day_cache["speech_log"]
        speech_history = "\n".join([f"{pid}: {content}" for pid, content in speech_log.items()])

        # 获取玩家实例
        player_instance = next(agent for agent in self.agents if agent.agent_id == current_speaker_id)

        # 创建并发布演讲事件
        event = {
            "event_type": "player_speech",
            "sender": self,
            "recipients": [player_instance],
            "content": {
                "speech_history": speech_history,
                "current_speaker": current_speaker_id,
                "speech_position": speech_order.index(current_speaker_id) + 1
            }
        }
        self.publish_event(event)

    def process_player_speech(self, event: dict) -> None:
        """
        Processes each player's daytime speech, recording their content in the public speech log.
        If there are more players in the order, it triggers the next player's speech.

        Args:
            event (dict): The event data containing the player's speech content.
        """
        # Step 1: 获取玩家 ID 和发言内容
        player_id = event.get("sender", None)
        action_content = event.get("content", {})

        # 检查 action_content 是否为 "no_action"
        if isinstance(action_content, dict): 
            speech_content = action_content.get("speech_content", f"Error during generation for player {player_id}.")
        else:
            speech_content = f"Error during generation for player {player_id}."

        # Step 2: 获取当前天数和 day_cache
        
        day_cache = self.shared_memory["public_state"]["day_cache"][-1]

        # 初始化 day_cache 的 speech_log（如果不存在）
        if "speech_log" not in day_cache:
            day_cache["speech_log"] = {}

        # 将发言内容记录到 day_cache 的 speech_log
        day_cache["speech_log"][player_id] = speech_content

        # Step 3: 公布发言内容
        self.log_event(
            is_private=False,
            agent_id=player_id,
            content=f"{player_id}'s speech: {speech_content}"
        )

        speech_order = day_cache.get("speech_order_decision", None)
        remaining_speakers = [
            pid for pid in speech_order
            if pid not in day_cache["speech_log"]
            and pid in self.shared_memory["public_state"]["alive_players"]
        ]

        if remaining_speakers:
            # 调用下一个玩家的发言
            next_speaker_id = remaining_speakers[0]
            self.player_speeches(current_speaker_id=next_speaker_id)
        else:
            # 所有玩家发言完毕
            self.mark_event_complete(event_type="player_speech")
            self.log_event(is_private=False, agent_id="system", content="All players have completed their speeches for today.")

    def vote_action(self) -> None:
        """
        启动放逐投票流程，向所有存活玩家广播一条“vote_action”事件。
        所有存活玩家均可参与投票，投票流程不需要传递额外信息。
        """
        # 第一步：确定投票对象（所有存活玩家）
        all_players = self.shared_memory["public_state"]["alive_players"]
        
        # 根据玩家 ID 获取对应的玩家引用
        voter_refs = [agent for agent in self.agents if agent.agent_id in all_players]

        # 第二步：构建投票事件
        event = {
            "event_type": "vote_action",
            "sender": self,  # 环境实例
            "recipients": voter_refs,  # 发送玩家引用而非 ID
            "content": {}  # 放逐投票无需额外内容
        }

        # 第三步：发布投票事件
        self.publish_event(event)
        self._log_event("Vote to exile event published to all alive players.")

    def process_vote_action(self, event: dict) -> None:
        """
        Processes a vote action during the banishment phase.
        Records each player's vote, determines the player to be banished once all votes are cast,
        and announces the result publicly. The sheriff's vote counts as 1.5 votes.

        Updates the day cache with voting details and results.

        Args:
            event (dict): Contains the voting event details, including the player ID and their vote.
        """
        # Step 1: Record the vote
        voter_id = event.get("sender", None)
        if isinstance(event.get("content", {}), dict):
            vote_choice = event.get("content", {}).get("action_vote", "abstain")
        else:
            vote_choice = "abstain"
        # Get current day and day cache
        day_cache = self.shared_memory["public_state"]["day_cache"][-1]

        # Initialize day cache keys if not present
        if "banishment_votes" not in day_cache:
            day_cache["banishment_votes"] = {}
        if "banishment_result" not in day_cache:
            day_cache["banishment_result"] = None

        # Store the vote in day_cache
        day_cache["banishment_votes"][voter_id] = vote_choice

        # Step 2: Check if all eligible players have voted
        eligible_voters = [
            player_id for player_id in self.shared_memory["public_state"]["alive_players"]
        ]
        all_votes_cast = all(voter in day_cache["banishment_votes"] for voter in eligible_voters)

        if not all_votes_cast:
            # If votes are still pending, log and wait for further events
            self._log_event("Waiting for remaining players to cast their votes.")
            return

        # Step 3: Tally the votes with sheriff's vote weighted
        sheriff_id = self.shared_memory["public_state"].get("sheriff")
        votes = day_cache["banishment_votes"]
        vote_counts = {}

        for voter, choice in votes.items():
            if choice != "abstain":  # Ignore abstentions
                weight = 1.5 if voter == sheriff_id else 1  # Sheriff vote counts as 1.5
                vote_counts[choice] = vote_counts.get(choice, 0) + weight

        # Step 4: Determine the player with the highest vote count
        max_votes = max(vote_counts.values(), default=0)
        candidates_with_max_votes = [candidate for candidate, count in vote_counts.items() if count == max_votes]

        if len(candidates_with_max_votes) == 1:
            # A single player has the most votes, they are banished
            banished_player_id = candidates_with_max_votes[0]
            self.shared_memory["private_state"]["players"][banished_player_id]["status"]["health"] = 0

            # Record the banishment result in day cache
            day_cache["banishment_result"] = banished_player_id

            # Check if the banished player is the sheriff
            if banished_player_id == sheriff_id:
                self._log_event(f"The banished player {banished_player_id} was the sheriff. Processing badge flow.")
                self.badge_flow(sheriff_id=banished_player_id)

            # Announce the banishment result
            announcement = f"{banished_player_id} has been banished from the game."
            self.log_event(
                is_private=False,
                agent_id="system",
                content=announcement
            )
        else:
            # If there's a tie, no player is banished
            day_cache["banishment_result"] = "No player banished due to tie"

            # Announce the tie result
            announcement = "No player was banished due to a tie."
            self.log_event(
                is_private=False,
                agent_id="system",
                content=announcement
            )

        # Step 5: Publish all votes publicly with the banishment announcement
        vote_summary = "\n".join([f"{voter} voted for {choice}" for voter, choice in votes.items()])
        self.log_event(
            is_private=False,
            agent_id="system",
            content=f"Banishment votes:\n{vote_summary}"
        )

        # Update day cache with vote summary
        day_cache["vote_summary"] = vote_summary
        self.mark_event_complete(event_type="vote_action")

    def last_words(self, agent_id: str) -> None:
        """
        Publishes a 'last_word' event for the specified agent.
        
        Args:
            agent_id (str): The ID of the agent who is giving their last word.
        """
        # Retrieve the agent instance based on the agent ID
        agent_instance = next((agent for agent in self.agents if agent.agent_id == agent_id), None)

        if not agent_instance:
            self._log_event(f"Agent {agent_id} not found. Cannot publish last word event.")
            return

        # Construct and publish the last word event
        event = {
            "event_type": "last_words",
            "sender": self,  # The environment instance
            "recipients": [agent_instance],  # The specified agent
            "content": {}
        }

        self.publish_event(event)
        self._log_event(f"Last word event published for agent {agent_id}.")

    def process_last_words(self, event: dict) -> None:
        """
        Processes the last words from an eliminated player and records their final message in the public log.
        
        Args:
            event (dict): The event data containing the player's last words content.
        """
        # Step 1: Retrieve the player ID and their final words content
        player_id = event["sender"]
        action_content = event.get("content", {})
        if action_content == "no_action":
            last_words_message = f"Error during generation for player {player_id}."
        else:
            last_words_message = action_content.get("speech_content", "")

        # Get the current day and the day cache
        current_day = self.shared_memory["public_state"]["days"]
        day_cache = self.shared_memory["public_state"]["day_cache"][current_day - 1]

        # Initialize the "last_words" key in the day cache if it doesn't exist
        if "last_words" not in day_cache:
            day_cache["last_words"] = {}

        # Step 2: Record the player's last words in the day cache
        day_cache["last_words"][player_id] = last_words_message

        # Step 3: Log the last words to the public log
        self.log_event(
            is_private=False,
            agent_id=player_id,
            content=f"Last words from {player_id}: {last_words_message}"
        )

        # Log a system message to indicate the player's last words have been recorded
        self._log_event(f"Last words from {player_id} recorded and shared with all players.")
        self.mark_event_complete(event_type="last_words")

    def badge_flow(self, sheriff_id: str) -> None:
        """
        Publishes a badge_flow event to the sheriff who is about to be eliminated, 
        allowing them to decide what to do with the sheriff's badge.

        Args:
            sheriff_id (str): The ID of the sheriff who is about to be eliminated.
        """
        # Retrieve the sheriff's agent instance
        sheriff_instance = next(agent for agent in self.agents if agent.agent_id == sheriff_id)

        # Create and publish the badge_flow event
        event = {
            "event_type": "badge_flow",
            "sender": self,
            "recipients": [sheriff_instance],
            "content": {}
        }

        # Publish the event to the event bus
        self.publish_event(event)

        # Log the badge_flow event publication
        self._log_event(f"Badge flow event published to sheriff {sheriff_id}.")

    def process_badge_flow(self, event: dict) -> None:
        """
        Processes the sheriff's decision on what to do with the badge when they are about to be eliminated.
        Updates the badge status based on the sheriff's choice and logs the result.

        Args:
            event (dict): The event data containing the sheriff's badge flow decision.
        """
        # Extract the sheriff's decision from the event
        sheriff_id = event.get("sender", None)
        action_content = event.get("content", {})
        pass_badge = action_content.get("pass_badge", False)
        badge_receiver = action_content.get("badge_receiver", None)

        # Retrieve the current day cache
        current_day = self.shared_memory["public_state"]["days"]
        day_cache = self.shared_memory["public_state"]["day_cache"][current_day - 1]

        # Initialize "badge_flow_result" in the day cache if not present
        if "badge_flow_result" not in day_cache:
            day_cache["badge_flow_result"] = {}

        if pass_badge:
            # If the sheriff decides to pass the badge
            if badge_receiver and badge_receiver in self.shared_memory["public_state"]["alive_players"]:
                # Update badge status
                self.shared_memory["private_state"]["players"][sheriff_id]["status"]["badge_count"] = 0
                self.shared_memory["public_state"]["sheriff"] = badge_receiver
                self.shared_memory["private_state"]["players"][badge_receiver]["status"]["badge_count"] = 1

                # Record the badge flow result in the day cache
                day_cache["badge_flow_result"] = {
                    "previous_sheriff": sheriff_id,
                    "new_sheriff": badge_receiver,
                    "action": "badge_passed"
                }

                # Log the result
                self.log_event(
                    is_private=False,
                    agent_id="system",
                    content=f"{sheriff_id} has passed the badge to {badge_receiver}."
                )
            else:
                # If the badge receiver is invalid, destroy the badge instead
                self.shared_memory["private_state"]["players"][sheriff_id]["status"]["badge_count"] = 0
                self.shared_memory["public_state"]["sheriff"] = None

                # Record the badge destruction in the day cache
                day_cache["badge_flow_result"] = {
                    "previous_sheriff": sheriff_id,
                    "new_sheriff": None,
                    "action": "badge_destroyed"
                }

                # Log the result
                self.log_event(
                    is_private=False,
                    agent_id="system",
                    content=f"{sheriff_id} attempted to pass the badge, but it was destroyed instead."
                )
            self.mark_event_complete(event_type="badge_flow")
        else:
            # If the sheriff decides to destroy the badge
            self.shared_memory["private_state"]["players"][sheriff_id]["status"]["badge_count"] = 0
            self.shared_memory["public_state"]["sheriff"] = None

            # Record the badge destruction in the day cache
            day_cache["badge_flow_result"] = {
                "previous_sheriff": sheriff_id,
                "new_sheriff": None,
                "action": "badge_destroyed"
            }

            # Log the result
            self.log_event(
                is_private=False,
                agent_id="system",
                content=f"{sheriff_id} has destroyed the badge."
            )
            self.mark_event_complete(event_type="badge_flow")
        
    def receive_action(self, event: dict) -> None:
        """
        Processes an action event received from the EventBus. 
        The event contains details about the action to be taken by the agent.

        Args:
            event (dict): A dictionary containing event details, including the event type,
                        content, and any relevant information needed for action processing.
        """
        # 获取事件类型
        event_type = event.get("event_type", "unknown")
        if event_type != "reply_sheriff_speech" and event_type != "reply_player_speech":
            self._log_player(
                event.get("sender", ""), 
                f"Received action event of type '{event_type}'. Event content: {event.get('content', 'Error when retrieving content')}"
            )

        # 根据事件类型处理不同的行动
        if event_type == "reply_guard_action":
            self._log_system("Processing reply_guard_action.")
            self.process_guard_action(event)
        elif event_type == "reply_werewolf_action":
            self._log_system("Processing reply_werewolf_action.")
            self.process_werewolf_action(event)
        elif event_type == "reply_seer_action":
            self._log_system("Processing reply_seer_action.")
            self.process_seer_action(event)
        elif event_type == "reply_witch_action":
            self._log_system("Processing reply_witch_action.")
            self.process_witch_action(event)
        elif event_type == "reply_run_for_sheriff":
            self._log_system("Processing reply_run_for_sheriff.")
            self.process_run_for_sheriff(event)
        elif event_type == "reply_sheriff_speech":
            self._log_system("Processing reply_sheriff_speech.")
            self.process_sheriff_speech(event)
        elif event_type == "reply_vote_for_sheriff":
            self._log_system("Processing reply_vote_for_sheriff.")
            self.process_vote_for_sheriff(event)
        elif event_type == "reply_decide_speech_sequence":
            self._log_system("Processing reply_sheriff_decide_speech_order.")
            self.process_sheriff_decide_speech_order(event)
        elif event_type == "reply_player_speech":
            self._log_system("Processing reply_player_speech.")
            self.process_player_speech(event)
        elif event_type == "reply_vote_action":
            self._log_system("Processing reply_vote_action.")
            self.process_vote_action(event)
        elif event_type == "reply_last_words":
            self._log_system("Processing reply_last_word.")
            self.process_last_words(event)
        elif event_type == "reply_badge_flow":
            self._log_system("Processing reply_badge_flow.")
            self.process_badge_flow(event)
        else:
            self._log_system(f"Unknown event type '{event_type}' received. No action taken.")



if __name__ == "__main__":

    # Game Initialization
    name = "werewolf_engine_demo"
    config_path = os.path.join("marble", "configs", "test_config", "werewolf_config.yaml")

    # Ensure the config file exists
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at {config_path}")

    try:
        # Create the Werewolf Environment
        env = WerewolfEnv(name=name, config_path=config_path)

        # Start the Game
        print(f"Starting game: {name}")
        env.start()

    except Exception as e:
        # Handle Initialization or Game Execution Errors
        print(f"An error occurred while starting the game: {e}")

