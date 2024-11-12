import json
import os
import random
import time

import yaml
from colorama import Fore, Style, init  # 引入 colorama 库

from ..agent.werewolf_agent import WerewolfAgent


class EventBus:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, handler):
        """
        订阅事件。handler 是对象的实例方法，例如 self.receive_event。
        """
        self.subscribers.append(handler)

    def publish(self, event: dict):
        """
        广播事件，仅调用事件接收者的处理方法。

        Args:
            event (dict): 包含事件数据的字典。必须包含 "recipients" 字段，列表格式。
        """
        recipients = event.get("recipients", [])
        for handler in self.subscribers:
            if handler.agent_id in recipients:
                handler(event)  # 仅调用事件接收者的实例方法


class WerewolfEnv:
    def __init__(self, name: str, config_path: str):
        """
        Initialize the Werewolf environment.

        Args:
            name (str): The name of the environment.
            config_path (str): Path to the config.json file.
        """
        init(autoreset=True)  # 初始化 colorama 自动重置颜色
        self.name = name
        self.agents = []
        # 加载配置文件
        with open(config_path, 'r') as f:
            config = json.load(f)
        self.config = config

        # 加载 system_prompt.yaml 文件
        system_prompt_path = self.config.get("system_prompt_path")
        if not system_prompt_path or not os.path.exists(system_prompt_path):
            raise FileNotFoundError(f"System prompt file '{system_prompt_path}' not found.")

        with open(system_prompt_path, 'r') as f:
            system_prompt = yaml.safe_load(f)

        game_introduction = system_prompt.get("game_introduction", "")

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
        self.event_bus.subscribe(self.receive_action)
        # 创建 werewolf_log 文件夹（如果不存在）
        base_log_dir = "werewolf_log"
        if not os.path.exists(base_log_dir):
            os.makedirs(base_log_dir)

        # 创建当前时间命名的子文件夹，用于存储该场游戏的数据
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        game_log_dir = os.path.join(base_log_dir, f"game_{timestamp}")
        os.makedirs(game_log_dir)  # 创建游戏日志文件夹

        # 定义 shared memory 文件路径
        shared_memory_path = os.path.join(game_log_dir, "shared_memory.json")

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
                "openai_api_key": "your-openai-api-key"  # 这里是基础配置
            }

            # 创建 WerewolfAgent 实例，将日志存储路径传入
            agent = WerewolfAgent(config=agent_config, role=role, log_path=game_log_dir, event_bus=self.event_bus, env = self)
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
                status["seer_history"] = {}  # 初始化为空字典

            self.shared_memory["private_state"]["players"][agent_id] = {
                "role": role,  # 记录角色身份
                "status": status,
                "personal_event_log": personal_event_log  # 个人事件日志
            }

        # 初始化警长信息为 None，表示没有警长
        self.shared_memory["public_state"]["sheriff"] = None

        # 将共享内存写入 shared_memory.json 文件
        with open(shared_memory_path, 'w') as f:
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
        print(f"{Fore.YELLOW}{f"System: {message}"}{Style.RESET_ALL}")

    def _log_event(self, message: str):
        """
        使用绿色文本输出事件消息。

        Args:
            message (str): 事件消息内容。
        """
        print(f"{Fore.GREEN}{f"Event: {message}"}{Style.RESET_ALL}")

    def _log_player(self, player_id: str, message: str):
        """
        使用蓝色文本输出玩家发言。

        Args:
            player_id (str): 玩家ID。
            message (str): 玩家发言内容。
        """
        print(f"{Fore.BLUE}[{player_id}]: {message}{Style.RESET_ALL}")

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
                self._log_system(day_start_message)
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
                    break

            game_complete_message = "SYSTEM: Werewolf game completed."
            self._log_system(game_complete_message)
            self.log_event(is_private=False, agent_id="system", content=game_complete_message)

        except Exception as e:
            error_message = f"An error occurred during the game cycle: {e}"
            self._log_system(error_message)
            self.log_event(is_private=True, agent_id="system", content=error_message)
            raise

    def night(self) -> None:
        """
        Executes the night phase of the game. Werewolves select a target, and special
        roles (witch, seer, guard) may take actions.
        """
        # 记录当前夜晚编号
        current_night = self.shared_memory["public_state"]["days"]  # 第几夜（游戏回合数 +1）

        # 在 night_cache 中添加一个新的字典以记录当前夜晚
        night_event = {"night": current_night,
                       "player_dead_tonight": []
                       }
        self.shared_memory["private_state"]["night_cache"].append(night_event)

        # 开始夜晚行动日志
        self._log_system(f"Night {current_night} phase begins. Werewolves and special roles take actions.")

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

    def day(self) -> None:
        """
        Executes the day phase of the game. Players discuss and vote on a player to eliminate.
        """
        self._log_system("Day phase begins. Players discuss and vote on potential suspects.")

        # 判断是否为第一天
        current_day = self.shared_memory["public_state"]["days"]
        if current_day == 1:
            # 第一日的特殊行动流程
            self._log_event("First day: Sheriff election begins.")

            # 竞选警长
            self.run_for_sheriff()

            # 获取第一夜死者信息并调用遗言
            deceased = self.get_night_deceased()
            if deceased:
                self._log_event(f"{deceased} has died. Calling last words.")
                self.last_words(deceased)

            # 警长决定发言顺序
            self._log_event("Sheriff is deciding the speech order.")
            speech_order = self.sheriff_decide_speech_order()

            # 发言环节
            self._log_event("Players begin speeches.")
            self.player_speeches(speech_order)

            # 投票放逐
            self._log_event("Players are voting to exile a suspect.")
            exiled_player = self.exile_vote()
            if exiled_player:
                self.log_event(is_private=False, agent_id="system", content=f"{exiled_player} has been exiled.")

                # 放逐者遗言
                self._log_event(f"{exiled_player} is giving their last words after being exiled.")
                self.last_words(exiled_player)
                self.log_event(is_private=False, agent_id="system", content=f"{exiled_player} gave their last words.")

        else:
            # 非第一天的正常白天流程
            # 获取前夜死者信息并调用遗言
            deceased = self.get_night_deceased()
            if deceased:
                self._log_event(f"{deceased} has died. Calling last words.")
                self.last_words(deceased)
                self.log_event(is_private=False, agent_id="system", content=f"{deceased} gave their last words.")

            # 警长决定发言顺序
            self._log_event("Sheriff is deciding the speech order.")
            self.sheriff_decide_speech_order()
            self.log_event(is_private=False, agent_id="system", content="Sheriff decided the speech order.")

            # 发言环节
            self._log_event("Players begin speeches.")
            self.player_speeches()
            self.log_event(is_private=False, agent_id="system", content="Player speeches completed.")

            # 投票放逐
            self._log_event("Players are voting to exile a suspect.")
            exiled_player = self.exile_vote()
            if exiled_player:
                self.log_event(is_private=False, agent_id="system", content=f"{exiled_player} has been exiled.")

                # 放逐者遗言
                self._log_event(f"{exiled_player} is giving their last words after being exiled.")
                self.last_words(exiled_player)
                self.log_event(is_private=False, agent_id="system", content=f"{exiled_player} gave their last words.")

    def should_terminate(self) -> bool:
        """
        Checks if the game should terminate based on the number of remaining players
        and their roles. The game ends if the number of werewolves is greater than or equal
        to half of the remaining players, rounded up.

        Returns:
            bool: True if the game should end, otherwise False.
        """
        self._log_system("Checking if the game should terminate.")

        # 获取存活玩家和狼人数量
        alive_players = self.shared_memory["public_state"]["alive_players"]
        remaining_players = len(alive_players)
        werewolf_count = sum(1 for agent_id in alive_players
                            if self.shared_memory["private_state"]["players"][agent_id]["role"] == "wolf")

        # 计算终止条件
        majority_threshold = -(-remaining_players // 2)  # 向上取整计算一半以上
        if werewolf_count >= majority_threshold:
            termination_message = (
                f"Game should terminate: Werewolves ({werewolf_count}) have reached or exceeded "
                f"half of the remaining players ({remaining_players})."
            )
            self._log_system(termination_message)
            self.log_event(is_private=False, agent_id="system", content=termination_message)
            return True

        # 如果未满足终止条件
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
                    self._log_player(f"{agent_id}: {content}")
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
                    self._log_player(f"{agent_id}: {content}")

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
            if player_info["role"] == "guard" and player_info["status"].get("health", 0) == 1:
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
            self.event_bus.publish(event)
            self._log_event("Guard action event published.")
        else:
            self._log_event("Guard action event published.")

    def process_guard_action(self, event: dict) -> None:
        """
        Processes the guard action by protecting the target specified in the event.

        Args:
            event (dict): The event data containing 'protect_target' information.
        """
        # 从事件内容中获取守卫目标
        protect_target = event.get("content", {}).get("protect_target")
        last_protected = self.shared_memory["private_state"].get("guard_last_night_protect", None)

        # 检查 protect_target 是否有效且不与上次保护的目标相同
        if protect_target in self.shared_memory["private_state"]["players"]:
            if protect_target == last_protected:
                # 无效操作，记录错误日志
                self.log_event(
                    is_private=True,
                    agent_id=self.agent_id,
                    content=f"Guard action failed. {protect_target} was protected last night and cannot be protected again tonight."
                )
            else:
                # 更新守卫目标信息，将 protection_count 设置为 1
                self.shared_memory["private_state"]["players"][protect_target]["status"]["protection_count"] = 1

                # 更新 last_protected 信息
                self.shared_memory["private_state"]["guard_last_night_protect"] = protect_target

                # 记录事件日志到私有日志
                self.log_event(
                    is_private=True,
                    agent_id=self.agent_id,  # 守卫的 ID
                    content=f"Guard action processed. {protect_target} is protected this night."
                )

                # 将守卫目标添加到 night_cache 的当夜日志
                if self.shared_memory["private_state"]["night_cache"]:
                    current_night_log = self.shared_memory["private_state"]["night_cache"][-1]
                    current_night_log["guard_action"] = protect_target
                else:
                    self._log_event("Night cache is not initialized.")

        else:
            # 目标无效，记录错误日志
            self._log_event(f"Guard action failed. Invalid protect target: {protect_target}")

    def werewolf_action(self) -> None:
        """
        Publishes a single werewolf action event to the event bus.
        The event is directed to all players with the 'wolf' role, allowing them to take their action.
        """
        # 获取所有存活玩家的 ID 列表
        alive_players = self.shared_memory["public_state"].get("alive_players", [])

        # 获取所有存活的狼人玩家的实例索引和 ID
        alive_werewolves = [
            (agent, agent_id) for agent_id, agent in self.agents.items()  # 假设 self.agents 是包含所有代理实例的字典
            if self.shared_memory["private_state"]["players"][agent_id]["role"] == "wolf" and
            self.shared_memory["private_state"]["players"][agent_id]["status"].get("health", 0) == 1
        ]

        # 提取狼人实例和 ID 列表
        alive_werewolves_instances = [agent for agent, _ in alive_werewolves]
        alive_werewolves_ids = [agent_id for _, agent_id in alive_werewolves]

        # 在 round_targets 中添加一个新字典，键为存活狼人的 ID，值初始化为 None
        new_round_target = {wolf_id: None for wolf_id in alive_werewolves_ids}
        self.shared_memory["private_state"]["werewolf_action"]["round_targets"].append(new_round_target)

        # 生成逗号分隔的 ID 列表字符串
        alive_players_str = ", ".join(alive_players)
        alive_werewolves_ids_str = ", ".join(alive_werewolves_ids)

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
        self.event_bus.publish(event)
        self._log_event("Werewolf action event published for all living werewolf players.")

    def werewolf_discussion(self) -> None:
        """
        Publishes a werewolf discussion event to the event bus.
        The event is directed to all players with the 'wolf' role, allowing them to discuss and refine their action.
        """
        # 获取所有存活玩家的 ID 列表
        alive_players = self.shared_memory["public_state"].get("alive_players", [])

        # 获取所有存活的狼人玩家的实例索引和 ID
        alive_werewolves = [
            (agent, agent_id) for agent_id, agent in self.agents.items()  # 假设 self.agents 是包含所有代理实例的字典
            if self.shared_memory["private_state"]["players"][agent_id]["role"] == "wolf" and
            self.shared_memory["private_state"]["players"][agent_id]["status"].get("health", 0) == 1
        ]

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
        # 从事件内容中获取狼人行动的选择
        werewolf_id = event.get("sender")
        action_content = event.get("content", {})
        attack = action_content.get("attack")
        target = action_content.get("target")

        # 获取当轮狼人目标字典，即 `round_targets` 的最后一个元素
        current_round_targets = self.shared_memory["private_state"]["werewolf_action"]["round_targets"][-1]

        # 确保狼人 ID 在 `current_round_targets` 中
        if werewolf_id not in current_round_targets:
            self._log_event(f"Invalid werewolf ID: {werewolf_id}.")
            return

        # 根据 `attack` 和 `target` 更新 `current_round_targets`
        if not attack:
            current_round_targets[werewolf_id] = "false"
        elif attack and target in self.shared_memory["public_state"]["alive_players"]:
            current_round_targets[werewolf_id] = target
        else:
            current_round_targets[werewolf_id] = "false"

        # 检查是否所有狼人都已作出选择
        if any(value is None for value in current_round_targets.values()):
            self._log_event("Waiting for all werewolves to respond.")
            return

        # 统计每个有效目标的选择次数（排除 "false"）
        target_counts = {}
        for choice in current_round_targets.values():
            if choice != "false":
                target_counts[choice] = target_counts.get(choice, 0) + 1

        # 找出票数最高的目标
        if target_counts:
            majority_target = max(target_counts, key=target_counts.get)

            # 将达成共识的最终目标记录在 shared memory 中
            self.shared_memory["private_state"]["werewolf_action"]["final_targets"] = majority_target

            # 获取目标的状态并判断是否受到保护
            target_status = self.shared_memory["private_state"]["players"][majority_target]["status"]
            if target_status["protection_count"] == 0:
                # 目标未受保护，减少其血量
                target_status["health"] == 0
                success = True
                kill_result = f"Target {majority_target} attacked by werewolves and health reduced."
            else:
                # 目标受保护，无伤害
                success = False
                kill_result = f"Target {majority_target} protected, no health reduction."

            # 记录狼人行动到 night_cache 的当夜日志
            if self.shared_memory["private_state"]["night_cache"]:
                current_night_log = self.shared_memory["private_state"]["night_cache"][-1]
                current_night_log["werewolf_action"] = {
                    "final_target": majority_target,
                    "attack_successful": success,
                }
                current_night_log["player_dead_tonight"].append(majority_target)
            else:
                self._log_event("Night cache is not initialized.")

            # 获取狼人行动的详细信息
            remaining_werewolves = [
                agent_id for agent_id, player_info in self.shared_memory["private_state"]["players"].items()
                if player_info["role"] == "wolf" and player_info["status"].get("health", 0) == 1
            ]
            round_details = {
                "round_targets": current_round_targets,
                "remaining_werewolves": remaining_werewolves,
                "discussion_rounds_left": self.shared_memory["private_state"]["werewolf_action"]["rounds_remaining"],
                "final_target": majority_target,
                "attack_successful": success
            }
            detailed_kill_result = (
                f"Round Details:\n"
                f" - Round Targets: {round_details['round_targets']}\n"
                f" - Remaining Werewolves: {round_details['remaining_werewolves']}\n"
                f" - Discussion Rounds Left: {round_details['discussion_rounds_left']}\n"
                f" - Final Target: {round_details['final_target']}\n"
                f" - Attack Successful: {round_details['attack_successful']}\n"
                f"Result: {kill_result}"
            )

            # 记录详细击杀结果到每个狼人的私密日志
            for wolf_id in current_round_targets.keys():
                self.log_event(
                    is_private=True,
                    agent_id=wolf_id,
                    content=detailed_kill_result,
                    log_to_system=False
                )

            # 系统私密日志记录
            self.log_event(
                is_private=True,
                agent_id="system",
                content=detailed_kill_result
            )

        else:
            # 没有有效目标，记录攻击未达成共识的情况
            self._log_event("Werewolf attack failed due to lack of a clear majority target.")
            # 剩余讨论轮次减 1
            self.shared_memory["private_state"]["werewolf_action"]["rounds_remaining"] -= 1

            # 检查剩余讨论轮次
            if self.shared_memory["private_state"]["werewolf_action"]["rounds_remaining"] > 0:
                # 在 `round_targets` 中添加新的空轮次字典
                alive_werewolves_ids = [
                    agent_id for agent_id, player_info in self.shared_memory["private_state"]["players"].items()
                    if player_info["role"] == "wolf" and player_info["status"].get("health", 0) == 1
                ]
                new_round_target = {wolf_id: None for wolf_id in alive_werewolves_ids}
                self.shared_memory["private_state"]["werewolf_action"]["round_targets"].append(new_round_target)

                # 调用 `werewolf_discussion` 进行下一轮讨论
                self.werewolf_discussion()

            else:
                # 若剩余讨论轮次为 0，记录行动失败信息
                remaining_werewolves = [
                    agent_id for agent_id, player_info in self.shared_memory["private_state"]["players"].items()
                    if player_info["role"] == "wolf" and player_info["status"].get("health", 0) == 1
                ]
                round_details = {
                    "round_targets": current_round_targets,
                    "remaining_werewolves": remaining_werewolves,
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

                # 记录失败结果到每个狼人的私密日志
                for wolf_id in current_round_targets.keys():
                    self.log_event(
                        is_private=True,
                        agent_id=wolf_id,
                        content=detailed_fail_result,
                        log_to_system=False
                    )

                # 系统私密日志记录
                self.log_event(
                    is_private=True,
                    agent_id="system",
                    content=detailed_fail_result
                )

                # 记录到 night_cache
                if self.shared_memory["private_state"]["night_cache"]:
                    current_night_log = self.shared_memory["private_state"]["night_cache"][-1]
                    current_night_log["werewolf_action"] = {
                        "final_target": "None",
                        "attack_successful": False,
                        "reason": "Failed due to lack of consensus"
                    }
                else:
                    self._log_event("Night cache is not initialized.")

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
            if player_info["role"] == "seer" and player_info["status"].get("health", 0) == 1:
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
            self.event_bus.publish(event)
            self._log_event("Seer action event published.")
        else:
            self._log_event("Seer action event published.")

    def process_seer_action(self, event: dict) -> None:
        """
        Processes the seer action by recording the check target specified in the event.

        Args:
            event (dict): The event data containing 'check_target_thought', 'final_thought', and 'action' information.
        """
        # 从事件内容中获取预言家行动的选择
        seer_id = event.get("sender")
        action_content = event.get("content", {})
        check_target = action_content.get("action", {}).get("check_target")

        # 检查目标是否有效
        if check_target not in self.shared_memory["public_state"]["alive_players"]:
            self.log_event(
                is_private=True,
                agent_id=seer_id,
                content=f"<<Private>> Seer action failed. Invalid check target: {check_target}.",
                log_to_system=False
            )
            return

        # 计算当前是第几夜
        current_night = self.shared_memory["public_state"]["days"]

        # 判断目标是否为狼人并记录结果
        is_werewolf = self.shared_memory["private_state"]["players"][check_target]["role"] == "wolf"
        check_result = "werewolf" if is_werewolf else "not a werewolf"

        # 更新预言家的查验历史，包含第几夜的信息
        check_history_entry = {"player": check_target, "result": check_result}
        self.shared_memory["private_state"]["players"][seer_id]["status"]["check_history"][f"Night {current_night}"] = check_history_entry

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
            if player_info["role"] == "witch" and player_info["status"].get("health", 0) == 1:
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
            self.event_bus.publish(event)
            self._log_event("Witch action event published.")
        else:
            self._log_event("Witch action event published.")

    def process_witch_action(self, event: dict) -> None:
        """
        Processes the witch action based on the event content, applying antidote or poison
        to the specified targets as chosen by the witch and updating the available potion counts.

        Args:
            event (dict): The event data containing the witch's choices for using antidote and poison.
        """
        # 获取事件内容，包括解药和毒药的使用决定
        action_content = event.get("content", {}).get("action", {})
        use_antidote = action_content.get("use_antidote", False)
        use_poison = action_content.get("use_poison", False)
        poison_target = action_content.get("poison_target", None)

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

        # 处理毒药的使用
        if use_poison and poison_target in self.shared_memory["public_state"]["alive_players"] and witch_status["poison_count"] > 0:
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

        # 若女巫未使用解药且未使用毒药，记录行动结果
        if not use_antidote and not use_poison:
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
            if self.shared_memory["private_state"]["players"][agent.agent_id]["status"].get("health", 0) == 1
        ]

        if alive_players:
            # 创建并发布竞选警长事件
            event = {
                "event_type": "run_for_sheriff",
                "sender": self,  # 标识为环境实例
                "recipients": alive_players,  # 所有存活玩家的实例引用
                "content": {}  # 不传入额外内容
            }
            self.event_bus.publish(event)
            self._log_event("Run for sheriff event published for all living players.")
        else:
            self._log_event("No living players found to participate in sheriff election.")

    def process_run_for_sheriff(self, event: dict) -> None:
        """
        Processes each player's decision on whether or not to run for sheriff and
        prepares candidates for the sheriff election once all decisions are received.

        Args:
            event (dict): The event data containing the player's decision on running for sheriff.
        """
        # 从事件内容中获取玩家的参选决定
        player_id = event["sender"]
        action_content = event.get("content", {}).get("action", {})
        run_for_sheriff = action_content.get("run_for_sheriff", False)

        # 将玩家的决定记录到 shared memory 中的 sheriff_election 中
        self.shared_memory["private_state"]["sheriff_election"]["candidates"][player_id] = run_for_sheriff

        # 检查是否所有存活玩家都做出了决定
        if any(choice is None for choice in self.shared_memory["private_state"]["sheriff_election"]["candidates"].values()):
            self._log_event("Waiting for all players to decide on running for sheriff.")
            return

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

            # 初始化 sheriff_speech 字典，所有候选人的演讲内容为 None
            self.shared_memory["private_state"]["sheriff_election"]["sheriff_speech"] = {candidate_id: None for candidate_id in candidate_ids}
            self.shared_memory["private_state"]["sheriff_election"]["final_candidate"] = []

            # 调用第一个候选人的演讲
            first_candidate_id = candidate_ids[0]
            self.sheriff_speech(candidate_ids, first_candidate_id)
        else:
            # 无人参选，记录信息
            self._log_event("No candidates decided to run for sheriff.")
            return

    def sheriff_speech(self, candidate_ids: list, candidate_id: str) -> None:
        """
        Publishes a 'sheriff_speech' event for a given candidate, allowing them to make their speech for the election.

        Args:
            candidate_ids (list): List of IDs of all candidates running for sheriff, sorted by ID.
            candidate_id (str): The ID of the current candidate making their speech.
        """
        # 获取所有候选人的 ID 列表作为 speech_sequence，并以逗号分隔
        speech_sequence = ", ".join(candidate_ids)

        # 确定当前候选人在候选人列表中的位置（从 1 开始计数）
        speech_position = candidate_ids.index(candidate_id) + 1

        # 构建 election_info，包含所有已完成演讲的内容
        election_info = "\n".join([
            f"{cid}: {speech}" for cid, speech in self.shared_memory["private_state"]["sheriff_election"]["sheriff_speech"].items()
            if speech is not None
        ])

        # 获取当前候选人的实例
        candidate_instance = self.agents[candidate_ids.index(candidate_id)]

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

        self.event_bus.publish(event)
        self._log_event(f"Sheriff speech event published for candidate {candidate_id}.")

    def process_sheriff_speech(self, event: dict) -> None:
        """
        Processes each candidate's sheriff speech, recording their decision to continue in the election
        and their speech content. Proceeds to the next candidate's speech if there are remaining candidates.

        Args:
            event (dict): The event data containing the candidate's speech and decision to continue.
        """
        # 获取候选人 ID 和发言内容
        candidate_id = event["sender"]
        action_content = event.get("content", {}).get("action", {})
        continue_running = action_content.get("continue_running", False)
        speech_content = action_content.get("speech_content", "")

        # 记录候选人的发言内容
        self.shared_memory["private_state"]["sheriff_election"]["sheriff_speech"][candidate_id] = speech_content
        self.log_event(
            is_private=False,
            agent_id=candidate_id,
            content=f"{candidate_id}'s speech: {speech_content}"
        )

        if continue_running:
            # 如果候选人选择继续竞选，添加到最终候选人列表
            self.shared_memory["private_state"]["sheriff_election"]["final_candidate"].append(candidate_id)
        else:
            # 候选人退出竞选的决定
            self.log_event(
                is_private=False,
                agent_id="system",
                content=f"{candidate_id} has withdrawn from the sheriff election."
            )

        # 检查是否还有候选人未发言
        candidate_ids = list(self.shared_memory["private_state"]["sheriff_election"]["sheriff_speech"].keys())
        remaining_candidates = [cid for cid in candidate_ids if self.shared_memory["private_state"]["sheriff_election"]["sheriff_speech"][cid] is None]

        if remaining_candidates:
            # 调用下一个候选人的演讲
            next_candidate_id = remaining_candidates[0]
            self.sheriff_speech(candidate_ids, next_candidate_id)
        else:
            # 所有候选人已发言，开始投票
            self.vote_for_sheriff()
    def vote_for_sheriff(self) -> None:
        """
        Initiates the voting process for electing a sheriff by broadcasting a
        'vote_for_sheriff' event to all eligible players who did not participate
        in the sheriff election.
        """
        # Step 1: 获取选举日志和候选人列表
        election_log = self.shared_memory["private_state"]["sheriff_election"].get("sheriff_speech", {})
        final_candidates = self.shared_memory["private_state"]["sheriff_election"].get("final_candidate", [])

        # 将选举日志转化为指定格式的字符串
        election_log_str = "\n".join([f"{candidate}: {speech}" for candidate, speech in election_log.items()])
        # 将候选人列表转化为逗号分隔的字符串
        candidate_list_str = ", ".join(final_candidates)

        # Step 2: 确定投票对象（从未参选的玩家）
        all_players = self.shared_memory["public_state"]["alive_players"]
        never_ran_for_sheriff = [
            player_id for player_id in all_players
            if not self.shared_memory["private_state"]["sheriff_election"]["candidates"].get(player_id)
        ]

        # Step 3: 构建投票事件
        event = {
            "event_type": "vote_for_sheriff",
            "sender": self,  # 环境实例
            "recipients": never_ran_for_sheriff,  # 投票对象列表
            "content": {
                "election_log": election_log_str,
                "candidate_list": candidate_list_str
            }
        }

        # Step 4: 发布投票事件
        self.event_bus.publish(event)

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

        # 根据事件类型处理不同的行动
        if event_type == "reply_guard_action":
            # 处理守卫的行动
            self.process_guard_action(event)
        elif event_type == "reply_werewolf_action":
            # 处理狼人行动
            self.process_werewolf_action(event)
        elif event_type == "reply_seer_action":
            # 处理预言家的行动
            self.process_seer_action(event)
        elif event_type == "reply_witch_action":
            # 处理女巫的行动
            self.process_witch_action(event)
        elif event_type == "reply_run_for_sheriff":
            # 处理警长竞选
            self.process_run_for_sheriff(event)
        elif event_type == "reply_sheriff_speech":
            # 处理警长演讲
            self.process_sheriff_speech(event)
        else:
            # 未知的事件类型
            pass

        # 可以添加任何进一步的日志或其他辅助功能
