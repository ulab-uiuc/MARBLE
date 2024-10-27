import json
import os
import random
import time
import yaml
from typing import Any, Dict
from ..agent.werewolf_agent import WerewolfAgent
from colorama import Fore, Style, init  # 引入 colorama 库

from marble.environments.base_env import BaseEnvironment

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
        广播事件，自动调用所有订阅者的处理方法。
        """
        for handler in self.subscribers:
            handler(event)  # 调用订阅者的实例方法


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
                "event_log": game_introduction  # 公开事件日志初始化为game_introduction内容
            },
            "private_state": {
                "players": {},  # 每个玩家的状态和身份
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
            agent = WerewolfAgent(config=agent_config, role=role, log_path=game_log_dir, event_bus=self.event_bus)
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

            self.shared_memory["private_state"]["players"][agent_id] = {
                "role": role,  # 记录角色身份
                "status": {
                    "health": 1,  # 默认血量为 1
                    "protection_count": 0,  # 默认守护数量为 0
                    "poison_count": 1 if role == "witch" else 0,  # 女巫有1个毒药
                    "antidote_count": 1 if role == "witch" else 0,  # 女巫有1个解药
                    "badge_count": 0  # 默认警徽数量为 0
                },
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
        print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")

    def _log_event(self, message: str):
        """
        使用绿色文本输出事件消息。

        Args:
            message (str): 事件消息内容。
        """
        print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")

    def _log_player(self, player_id: str, message: str):
        """
        使用蓝色文本输出玩家发言。

        Args:
            player_id (str): 玩家ID。
            message (str): 玩家发言内容。
        """
        print(f"{Fore.BLUE}[{player_id}]: {message}{Style.RESET_ALL}")
