import json
import os
import re
import sys
import random
import sys
import time
from threading import Condition, Lock

import names
import yaml
import argparse
from typing import Any, Dict, List
from threading import Condition, Lock
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from colorama import Fore, Style, init  # 引入 colorama 库

from marble.agent.werewolf_agent import WerewolfAgent
from marble.utils.eventbus import EventBus
from colorama import Fore, Style, init





class WerewolfEnv:
    def __init__(self, name: str, config_path: str, log_dir="werewolf_log"):
        """
        Initialize the Werewolf environment.

        Args:
            name (str): The name of the environment.
            config_path (str): Path to the config.json file.
        """
        self.id = "SYSTEM"
        init(autoreset=True)  # Initialize colorama to automatically reset colors
        self.name = name
        self.agents = []

        # Load the configuration file
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        self.config = config

        # Load the system_prompt.yaml file
        system_prompt_path = self.config.get("system_prompt_path")
        if not system_prompt_path or not os.path.exists(system_prompt_path):
            raise FileNotFoundError(f"System prompt file '{system_prompt_path}' not found.")

        with open(system_prompt_path, 'r', encoding='utf-8') as f:
            system_prompt = yaml.safe_load(f)

        game_introduction = system_prompt.get("game_introduction", "")
        self.condition = Condition(Lock())
        self.current_event = None
        self.event_completed = False
        self.daily_tasks = {}
        # All role introductions
        role_introductions = {
            "wolf": system_prompt.get("werewolf_introduction", ""),
            "villager": system_prompt.get("villager_introduction", ""),
            "seer": system_prompt.get("seer_introduction", ""),
            "witch": system_prompt.get("witch_introduction", ""),
            "guard": system_prompt.get("guard_introduction", "")
        }

        self.scores = {
            "villager": {"total": 0, "details": []},
            "werewolf": {"total": 0, "details": []},
        }
        # Initialize EventBus
        self.event_bus = EventBus()
        self.event_bus.subscribe(self, self.receive_action)

        # Create the werewolf_log folder if it does not exist
        base_log_dir = log_dir
        if not os.path.exists(base_log_dir):
            os.makedirs(base_log_dir)

        # Create a subfolder named with the current timestamp to store the game data
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        game_log_dir = os.path.join(base_log_dir, f"game_{timestamp}")
        os.makedirs(game_log_dir)

        # Define the shared memory file path
        self.shared_memory_path = os.path.join(game_log_dir, "shared_memory.json")

        # Load roles and configuration options
        roles = self.config.get("roles", ['wolf', 'wolf', 'wolf', 'villager', 'villager', 'villager', 'seer', 'witch', 'guard'])
        randomize_roles = self.config.get("randomize_roles", True)
        if randomize_roles:
            random.shuffle(roles)

        num_players = len(roles)  # Number of players in the game
        use_random_names = self.config.get("use_random_names", False)

        # Initialize shared memory
        self.shared_memory = {
            "public_state": {
                "days": 0,
                "day/night": "night",
                "alive_players": [],
                "sheriff": None,
                "event_log": game_introduction,
                "speech_order": {},
                "day_cache": []
            },
            "private_state": {
                "players": {},
                "guard_last_night_protect": None,
                "werewolf_action": {
                    "rounds_remaining": 5,
                    "alive_werewolves": [],
                    "round_targets": [],
                    "final_target": None
                },
                "night_cache": []
            },
            "public_event_log": game_introduction,
            "private_event_log": game_introduction
        }

        used_names = set()  # To record the names that have already been used
        for i in range(num_players):
            # Ensure that the generated name is unique
            while True:
                agent_id = names.get_first_name() if use_random_names else f"agent_{i + 1}"
                if agent_id not in used_names:
                    used_names.add(agent_id)
                    break
            role = roles[i]

            # Check if it is a villager configuration
            is_villager = role in ["villager", "seer", "witch", "guard"]

            # Get the corresponding role configuration from the config
            agent_config = {
                "agent_id": agent_id,
                "villager_config": self.config.get("villager_config", {}),
                "werewolf_config": self.config.get("werewolf_config", {})
            }

            agent = WerewolfAgent(
                config=agent_config,
                role=role,
                log_path=game_log_dir,
                event_bus=self.event_bus,
                shared_memory=self.shared_memory,
                env=self,
                number=i + 1,
                is_villager=is_villager
            )
            self.agents.append(agent)
            self.shared_memory["public_state"]["alive_players"].append(agent_id)

            # Initialize each player's private state
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
                "health": 1,
                "protection_count": 0,
                "poison_count": 1 if role == "witch" else 0,
                "antidote_count": 1 if role == "witch" else 0,
                "badge_count": 0
            }

            if role == "seer":
                status["check_history"] = {}

            self.shared_memory["private_state"]["players"][agent_id] = {
                "role": role,
                "status": status,
                "personal_event_log": personal_event_log
            }

        # Write the shared memory to a JSON file
        with open(self.shared_memory_path, 'w', encoding='utf-8') as f:
            json.dump(self.shared_memory, f, indent=4)

        # Print initialization log
        self._log_system(f"Werewolf environment '{self.name}' initialized with {num_players} agents and shared memory.")
        self._log_system(f"Game data stored in: {game_log_dir}")

    def to_dict(self, day_night_info: str = "") -> Dict[str, Any]:
        """
        Serialize the main state of WerewolfEnv and return it in a JSON-compatible format.
        Does not include non-serializable objects like thread locks, Condition, etc.,
        and temporary process variables that don't need to be saved.

        Args:
            day_night_info (str): To indicate which day/night this snapshot is for, such as "Day2" or "Night3".
                                  It will be appended to the env_name.
        """
        # If day_night_info is empty, use the original name; otherwise, append it
        combined_name = self.name if not day_night_info else f"{self.name}_{day_night_info}"

        env_dict = {
            "config": self.config,          # Game initialization configuration
            "shared_memory": self.shared_memory,   # Main game state
            "scores": self.scores,          # Current scores for villagers/werewolves
            "env_name": combined_name,       # Append "DayX"/"NightY" to the original name
            "agents": [agent.to_dict() for agent in self.agents],
            "shared_memory_path": self.shared_memory_path,
            # Additional fields like log directories can be added here if necessary
            "some_log_dir": getattr(self, "some_log_dir", None),
        }

        return env_dict
    
    @classmethod
    def load_from_file(cls, file_path: str, log_dir="werewolf_log", override_config_path=None) -> "WerewolfEnv":
        """
        Load WerewolfEnv from an existing snapshot (JSON). If override_config_path is provided,
        the env.config and each agent_data's villager_config / werewolf_config will be overridden or merged.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Env snapshot file not found: {file_path}")

        # 1. Read env_data from the snapshot JSON
        with open(file_path, "r", encoding="utf-8") as f:
            env_data = json.load(f)
        # 2. Create a new WerewolfEnv instance (without calling __init__)
        env = cls.__new__(cls)
        env.original_data = env_data

        # 3. Restore basic information
        original_env_name = env_data.get("env_name", "RecoveredEnv")
        env.name = f"continued_{original_env_name}"
        env.config = env_data.get("config", {})
        env.shared_memory = env_data.get("shared_memory", {})
        env.scores = env_data.get("scores", {})

        # 4. If override_config_path is provided, read the new YAML
        agent_overrides = {}
        if override_config_path and os.path.isfile(override_config_path):
            with open(override_config_path, "r", encoding="utf-8") as f:
                new_conf = yaml.safe_load(f)
            # Optionally merge new_conf into env.config
            env.config.update(new_conf)
            # Assuming "agent_overrides" from new_conf is used if present
            villager_overrides = new_conf.get("villager_config", {})
            werewolf_overrides = new_conf.get("werewolf_config", {})

        # 5. Restore agents_data
        agents_data = env_data.get("agents", [])

        # 6. Create a new log directory
        snapshot_filename = os.path.splitext(os.path.basename(file_path))[0]
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        game_log_dir_name = f"load_from_{snapshot_filename}_{timestamp}"
        game_log_dir = os.path.join(log_dir, game_log_dir_name)
        os.makedirs(game_log_dir, exist_ok=True)

        # Update shared_memory_path
        env.shared_memory_path = os.path.join(game_log_dir, "shared_memory.json")

        # Initialize some properties
        env.event_bus = EventBus()
        env.event_bus.subscribe(env, env.receive_action)
        env.daily_tasks = {}
        env.agents = []

        # 7. cooperation_mode (example)
        cooperation_mode = env.config.get("cooperation_mode", "independent")

        # ========== Core: Merge config for each agent_data ==========
        for agent_data in agents_data:

            agent_config = agent_data.get("config", {})
            # 1) Retain other fields (e.g., agent_id, other keys),
            #    only merge "villager_config"/"werewolf_config"

            # - If "agent_overrides.villager_config" exists in the YAML, merge it with agent_config["villager_config"]
            if villager_overrides:
                agent_config["villager_config"].update(villager_overrides)

            # - If "agent_overrides.werewolf_config" exists in the YAML, merge it with agent_config["werewolf_config"]
            if werewolf_overrides:
                agent_config["werewolf_config"].update(werewolf_overrides)

            # Finally, write the merged agent_config back to agent_data
            agent_data["config"] = agent_config
            # 2) Create a new WerewolfAgent
            new_agent = WerewolfAgent.from_dict(
                agent_data=agent_data,
                log_path=game_log_dir,
                event_bus=env.event_bus,
                shared_memory=env.shared_memory,
                env=env,
                strategy=cooperation_mode
            )
            env.agents.append(new_agent)

        # 8. Complete instantiation
        env.id = "SYSTEM"
        env._log_system(f"Successfully loaded WerewolfEnv from '{file_path}'.")
        env._log_system(f"Logs for this recovered game will be stored in: {game_log_dir}")
        return env

    def _log_system(self, message: str):
        """
        Outputs a system message in yellow text.

        Args:
            message (str): The system message content.
        """
        print(f"{Fore.YELLOW}System: {message}{Style.RESET_ALL}")

    def _log_event(self, message: str):
        """
        Outputs an event message in green text.

        Args:
            message (str): The event message content.
        """
        print(f"{Fore.GREEN}Event: {message}{Style.RESET_ALL}")

    def _log_player(self, player_id: str, message: str):
        """
        Outputs a player's speech in blue text.

        Args:
            player_id (str): The player ID.
            message (str): The player's speech content.
        """
        print(f"{Fore.BLUE}[{player_id} ({self.get_player_role(player_id)})]: {message}{Style.RESET_ALL}")

    def publish_event(self, event: dict):
        """
        Publishes an event and waits for its completion using a flag.
        """
        self.current_event = event["event_type"]
        self.event_completed = False  # Reset completion flag
        self.event_bus.publish(event)  # Publish event
        
        while not self.event_completed:
            time.sleep(0.01)  # Avoid excessive CPU usage

    def mark_event_complete(self, event_type: str):
        """
        Marks the current event as complete by updating the flag.
        """
        if self.current_event == event_type:
            self.event_completed = True
            self.current_event = None
        else:
            # If event types do not match, log an error
            self._log_event(
                f"Attempted to mark event '{event_type}' as complete, "
                f"but current event is '{self.current_event}'. No action taken."
            )
            
    def save_checkpoint(self, snapshot: Dict[str, Any], filename: str) -> None:
        # Decide a directory to save these checkpoint JSONs, maybe in the same game_log_dir
        checkpoint_path = os.path.join(os.path.dirname(self.shared_memory_path), filename)
        with open(checkpoint_path, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=4, ensure_ascii=False)
        self._log_system(f"Checkpoint saved to {checkpoint_path}")

    def start(self) -> dict:
        """
        Start the werewolf game environment and run the simulation in a day-night cycle.
        """
        start_message = "Werewolf game starting. Initializing day-night cycle."
        self._log_system(start_message)
        self.log_event(is_private=False, agent_id="system", content=start_message)

        try:
            while not self.should_terminate()["terminated"]:
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

                night_info_str = f"Night{current_day}"
                snapshot_night = self.to_dict(day_night_info=night_info_str)
                self.save_checkpoint(snapshot_night, f"checkpoint_{night_info_str}.json")

                # Check termination condition after night phase
                if self.should_terminate()["terminated"]:
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
                if self.config.get("use_daily_tasks", False):
                    private_tasks, public_tasks = self.generate_daily_tasks()
                    self.daily_tasks = {
                        "private": private_tasks,
                        "public": public_tasks
                    }
                    # Optionally, log a private system message indicating tasks have been generated
                    self.log_event(
                        is_private=True,
                        agent_id="system",
                        content=(
                            f"[start] Daily tasks for Day {current_day}: "
                            f"private={private_tasks}, public={public_tasks}"
                        )
                    )
                self.day()

                day_info_str = f"Day{current_day}"
                snapshot_day = self.to_dict(day_night_info=day_info_str)
                self.save_checkpoint(snapshot_day, f"checkpoint_{day_info_str}.json")

                # Check termination condition after day phase
                game_result = self.should_terminate()
                if game_result["terminated"]:
                    termination_message = "SYSTEM: Game termination condition met after day phase."
                    self._log_system(termination_message)
                    try:
                        with open(self.shared_memory_path, 'w', encoding='utf-8') as f:
                            json.dump(self.shared_memory, f, indent=4)
                        self._log_system(f"Shared memory successfully written to {self.shared_memory_path}")
                    except Exception as e:
                        self._log_system(f"Failed to write shared memory to {self.shared_memory_path}: {e}")
                    return game_result

        except Exception as e:
            error_message = f"An error occurred during the game cycle: {e}"
            self._log_system(error_message)
            try:
                with open(self.shared_memory_path, 'w', encoding='utf-8') as f:
                    json.dump(self.shared_memory, f, indent=4)
                self._log_system(f"Shared memory successfully written to {self.shared_memory_path}")
            except Exception as e:
                self._log_system(f"Failed to write shared memory to {self.shared_memory_path}: {e}")
            raise

    def night(self) -> None:
        """
        Executes the night phase of the game. Werewolves select a target, and special
        roles (witch, seer, guard) may take actions.
        """
        try:
            # Record the current night number
            current_night = self.shared_memory["public_state"]["days"]  # Which night (game round + 1)
            self.reset_guard_protection()
            # Add a new dictionary to night_cache to record the current night
            night_event = {}
            self.shared_memory["private_state"]["night_cache"].append(night_event)

            # Guard action
            self._log_event("Guard action starts.")
            self.guard_action()
            self.log_event(is_private=False, agent_id="system", content="Guard has chosen to protect a player.")

            # Werewolf action
            self._log_event("Werewolves are selecting a target.")
            self.werewolf_action()
            self.log_event(is_private=False, agent_id="system", content="Werewolves have chosen their target.")

            # Seer action
            self._log_event("Seer is performing their action.")
            self.seer_action()
            self.log_event(is_private=False, agent_id="system", content="Seer has checked a player's identity.")

            # Witch action
            self._log_event("Witch is deciding on antidote and poison usage.")
            self.witch_action()
            self.log_event(is_private=False, agent_id="system", content="Witch has made her decision on potion use.")

            self._log_system("Night phase actions are completed.")

            # Save shared memory to file
            with open(self.shared_memory_path, 'w', encoding='utf-8') as f:
                json.dump(self.shared_memory, f, indent=4)
            self._log_system(f"Shared memory successfully written to {self.shared_memory_path}")

        except Exception as e:
            # Capture all exceptions and write shared memory to a JSON file
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

            # Get the current day
            current_day = self.shared_memory["public_state"]["days"]

            # Initialize the day's cache
            self.shared_memory["public_state"]["day_cache"].append({})

            # Get the current day's cache dictionary
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
                        self._log_system(f"Speech order retrieval failed. Current speech order: {speech_order}")
                        day_cache["speech_order_decision"] = speech_order
                    if speech_order is None:
                        alive_players = self.shared_memory["public_state"]["alive_players"]
                        speech_order = sorted(alive_players)
                        self._log_system(f"Speech order retrieval failed again. Current speech order: {speech_order}")
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
                seer_id = self.get_player_id("seer")[0]
                if seer_id in self.shared_memory["public_state"]["alive_players"]:
                    self.scores["villager"]["total"] += 1
                    self.scores["villager"]["details"].append(
                        f"Day {current_day}: Seer {seer_id} survived. +1 point."
                    )
                if self.shared_memory["public_state"]["sheriff"]:
                    self._log_event("Sheriff is deciding the speech order.")
                    speech_order = self.sheriff_decide_speech_order()
                    if speech_order is None:
                        speech_order = self.shared_memory["public_state"]["day_cache"].get(current_day - 1, {}).get("speech_order_decision", None)
                        self._log_system(f"Speech order retrieval failed. Current speech order: {speech_order}")
                        day_cache["speech_order_decision"] = speech_order
                    if speech_order is None:
                        alive_players = self.shared_memory["public_state"]["alive_players"]
                        speech_order = sorted(alive_players)
                        day_cache["speech_order_decision"] = speech_order
                        self._log_system(f"Speech order retrieval failed again. Current speech order: {speech_order}")
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
            # Capture all exceptions and write shared memory to a JSON file
            self._log_system(f"An error occurred during the day phase: {e}")
            with open(f"{self.shared_memory_path}_error_dump.json", 'w', encoding='utf-8') as f:
                json.dump(self.shared_memory, f, indent=4)
            self._log_system(f"Shared memory dumped to {self.shared_memory_path}_error_dump.json for debugging.")
            raise

    def should_terminate(self) -> dict:
        """
        Checks if the game should terminate based on the number of remaining players
        and their roles. The game ends if:
        1. All werewolves are eliminated (villager victory).
        2. All non-werewolf players are eliminated (werewolf victory).

        Returns:
            dict: Contains game termination status and relevant details.
                - "terminated" (bool): True if the game ends, False otherwise.
                - "result" (str): The result of the game (e.g., "Villagers win", "Werewolves win").
                - "details" (str): Detailed game summary.
        """
        self._log_system("Checking if the game should terminate.")

        # Get the list of alive players and werewolf count
        alive_players = self.shared_memory["public_state"]["alive_players"]
        surviving_players = [
            {"player_id": player_id, "role": self.get_player_role(player_id)}
            for player_id in alive_players
        ]
        werewolves = [
            player for player in surviving_players if player["role"] == "wolf"
        ]
        non_werewolves = [
            player for player in surviving_players if player["role"] != "wolf"
        ]

        werewolf_count = len(werewolves)
        non_werewolf_count = len(non_werewolves)

        # Log the number of alive players, werewolves, and non-werewolves
        self._log_system(f"Alive players: {alive_players}")
        self._log_system(f"Number of werewolves: {werewolf_count}")
        self._log_system(f"Number of non-werewolves: {non_werewolf_count}")

        # Define the return result
        result = {
            "terminated": False,
            "result": None,
            "details": None
        }

        # Check if game termination conditions are met
        if werewolf_count > 0 and non_werewolf_count == 0:
            result["terminated"] = True
            result["result"] = "Werewolves win"
            result["details"] = {
                "game_status": "Game ends: All non-werewolf players are eliminated.",
                "winner": "Werewolves",
                "alive_players": alive_players,
                "werewolf_count": werewolf_count,
                "non_werewolf_count": non_werewolf_count
            }
            self.shared_memory["public_state"]["game_result"] = result["result"]

        elif werewolf_count == 0:
            result["terminated"] = True
            result["result"] = "Villagers win"
            result["details"] = {
                "game_status": "Game ends: All werewolves are eliminated.",
                "winner": "Villagers",
                "alive_players": alive_players,
                "werewolf_count": werewolf_count,
                "non_werewolf_count": non_werewolf_count
            }
            self.shared_memory["public_state"]["game_result"] = result["result"]

        # Logic when the game ends
        if result["terminated"]:
            # Calculate the result score
            surviving_good = len(non_werewolves)
            surviving_wolves = len(werewolves)
            result_score = surviving_good - surviving_wolves
            result["scores"] = {
                "process_scores": self.scores,  # Process scores
                "result_score": result_score,   # Result score                
            }
            # Update the final result JSON file content
            final_result = {
                "config": self.config,  # Game initialization configuration
                "process_scores": self.scores,  # Process scores
                "result_score": result_score,   # Result score
                "surviving_players": surviving_players,  # List of surviving players
                "game_result": result["result"],  # Game result (Villagers win or Werewolves win)
            }

            # Write the result to a JSON file
            result_path = self.shared_memory_path.replace("shared_memory.json", "result.json")
            with open(result_path, "w", encoding="utf-8") as result_file:
                json.dump(final_result, result_file, indent=4)

            self._log_system(f"Final result saved to {result_path}")

            # Construct the game end message
            survivor_info = "\n".join([
                f"{player['player_id']} ({player['role']})"
                for player in surviving_players
            ])
            final_message = (
                f"\n======================================================\n"
                f"GAME END! {result['result']}\n\n"
                f"Remaining players:\n{survivor_info}\n\n"
                f"Scores:\nVillagers: {self.scores['villager']['total']}\n"
                f"Werewolves: {self.scores['werewolf']['total']}\n"
                f"Result Score: {result_score}\n"
                f"======================================================\n"
            )
            # Print game end message in red font
            print(Fore.RED + final_message + Style.RESET_ALL)

            # Rename the log folder
            current_log_dir = os.path.dirname(self.shared_memory_path)
            new_log_dir = f"{current_log_dir}_{result['result'].replace(' ', '_')}"
            try:
                os.rename(current_log_dir, new_log_dir)
                self._log_system(f"Log folder renamed to '{new_log_dir}'.")
            except Exception as e:
                self._log_system(f"Error renaming log folder: {e}")

        return result

    
    def continue_game(self, simulate_one_cycle: bool = False) -> dict:
        """
        Continue the game after loading from an external save.
        This method supports a full "day->night" or "night->day" cycle.

        If 'simulate_one_cycle' is True, the environment will only execute 
        one full cycle (which involves running both day and night) and then stop.
        Otherwise, it will keep alternating day/night until the game ends.

        Returns:
            dict: A combined result containing the final game state plus 
                  the daily stage task analysis result.
        """

        # Step 0: Check if the game has already terminated
        game_result = self.should_terminate()
        if game_result["terminated"]:
            termination_message = (
                "[continue_game] Warning: The loaded save indicates the game "
                f"has already ended. Result: {game_result['result']}"
            )
            self._log_system(termination_message)
            self.log_event(is_private=False, agent_id="system", content=termination_message)
            return game_result

        # Step 1: Retrieve the current day and phase
        current_day = self.shared_memory["public_state"]["days"]
        current_phase = self.shared_memory["public_state"]["day/night"]


        self._log_system(
            f"[continue_game] Resuming from save. The environment was at Day {current_day}, "
            f"in the {current_phase} phase (already completed)."
        )
        self.log_event(
            is_private=False,
            agent_id="system",
            content=(
                f"[continue_game] Resuming from save at Day {current_day}, after finishing {current_phase}."
                " Proceeding to the next phase..."
            ),
        )
        
        while True:
            # Check termination before starting a new phase
            game_result = self.should_terminate()
            if game_result["terminated"]:
                break

            if current_phase == "day":
                # 1) Night of the current day
                self.shared_memory["public_state"]["days"] += 1
                self.shared_memory["public_state"]["day/night"] = "night"
                self.log_event(
                    is_private=False,
                    agent_id="system",
                    content=f"[continue_game] Entering Night of Day {current_day}."
                )
                if self.config.get("use_daily_tasks", True):
                    # If use_daily_tasks = True, generate tasks via generate_daily_tasks()
                    private_tasks, public_tasks = self.generate_daily_tasks()
                    self.daily_tasks = {
                        "private": private_tasks,
                        "public": public_tasks
                    }
                    # For final evaluation, we might use public tasks
                    tasks_for_evaluation = private_tasks
                self.night()

                # Save checkpoint after night
                night_info_str = f"Night{current_day}"
                snapshot_night = self.to_dict(day_night_info=night_info_str)
                self.save_checkpoint(snapshot_night, f"checkpoint_{night_info_str}.json")

                if self.should_terminate()["terminated"]:
                    break

                # 2) Day of the next day
                current_day = self.shared_memory["public_state"]["days"]
                current_phase = "day"
                self.shared_memory["public_state"]["day/night"] = current_phase

                self.log_event(
                    is_private=False,
                    agent_id="system",
                    content=f"[continue_game] Entering Day {current_day}."
                )
                self.day()

                # Save checkpoint after day
                day_info_str = f"Day{current_day}"
                snapshot_day = self.to_dict(day_night_info=day_info_str)
                self.save_checkpoint(snapshot_day, f"checkpoint_{day_info_str}.json")

                current_phase = "day"
                if simulate_one_cycle:
                    self._log_system("[continue_game] Finished one 'night->day' cycle. Stopping as requested.")
                    break

            else:
                # If night was the last completed, do "day -> night"
                current_day = self.shared_memory["public_state"]["days"]
                current_phase = "day"
                self.shared_memory["public_state"]["day/night"] = current_phase
                if self.config.get("use_daily_tasks", True):
                    # If use_daily_tasks = True, generate tasks via generate_daily_tasks()
                    private_tasks, public_tasks = self.generate_daily_tasks()
                    self.daily_tasks = {
                        "private": private_tasks,
                        "public": public_tasks
                    }
                    # For final evaluation, we might use public tasks
                    tasks_for_evaluation = private_tasks
                self.log_event(
                    is_private=False,
                    agent_id="system",
                    content=f"[continue_game] Entering Day {current_day}."
                )
                self.day()

                day_info_str = f"Day{current_day}"
                snapshot_day = self.to_dict(day_night_info=day_info_str)
                self.save_checkpoint(snapshot_day, f"checkpoint_{day_info_str}.json")

                game_result = self.should_terminate()
                if game_result["terminated"]:
                    break

                self.shared_memory["public_state"]["day/night"] = "night"
                self.log_event(
                    is_private=False,
                    agent_id="system",
                    content=f"[continue_game] Entering Night of Day {current_day}."
                )
                self.shared_memory["public_state"]["days"] += 1
                if self.config.get("use_daily_tasks", True):
                    # If use_daily_tasks = True, generate tasks via generate_daily_tasks()
                    private_tasks, public_tasks = self.generate_daily_tasks()
                    self.daily_tasks = {
                        "private": private_tasks,
                        "public": public_tasks
                    }
                    # For final evaluation, we might use public tasks
                    tasks_for_evaluation = private_tasks
                self.night()

                night_info_str = f"Night{current_day}"
                snapshot_night = self.to_dict(day_night_info=night_info_str)
                self.save_checkpoint(snapshot_night, f"checkpoint_{night_info_str}.json")

                current_phase = "night"

                if simulate_one_cycle:
                    self._log_system("[continue_game] Finished one 'day->night' cycle. Stopping as requested.")
                    break


        # Now call the daily stage tasks function, e.g. for Day <current_day>
        # You can customize the tasks or day_label as needed
        day_label_str = f"Day{current_day}"
        if self.config.get("use_daily_tasks", True):
            stage_result = self.evaluate_daily_stage_tasks(day_label=day_label_str, tasks=tasks_for_evaluation)

        # Return both results
        if self.config.get("use_daily_tasks", True):
            combined_result = {
                "game_result": game_result,
                "stage_result": stage_result
            }
        else:
            combined_result = game_result
        return combined_result

    def log_event(self, is_private: bool, agent_id: str, content: str, log_to_system: bool = True, print_to_system: bool = True) -> None:
        """
        Logs events for the game and synchronizes the logs to each agent's corresponding file.

        Args:
            is_private (bool): If True, the event is only logged in the specified private logs.
                            If False, it will be logged in the public, private, and each agent's personal logs.
            agent_id (str): The ID of the agent performing the action. Use "system" for system messages.
            content (str): The content to be logged.
            log_to_system (bool): If True, the event will also be logged in the system log. Defaults to True.
        """
        def write_to_agent_log(agent_id: str, message: str):
            """Write a log message to the corresponding agent's file using _write_log_entry."""
            agent_instance = next((agent for agent in self.agents if agent.agent_id == agent_id), None)
            if agent_instance:
                agent_instance._write_log_entry(message)

        # Handle messages for normal agents
        if agent_id != "system":
            if agent_id in self.shared_memory["private_state"]["players"]:
                # Update the agent's personal log in shared memory
                player_log = self.shared_memory["private_state"]["players"][agent_id]["personal_event_log"]
                self.shared_memory["private_state"]["players"][agent_id]["personal_event_log"] = f"{player_log}\n{content}"
                write_to_agent_log(agent_id, content)  # Sync to agent's file

            if is_private:
                # Private messages go only to private logs and corresponding agent file
                if log_to_system:
                    private_log = self.shared_memory["private_event_log"]
                    self.shared_memory["private_event_log"] = f"{private_log}\n{content}"
                if print_to_system:
                    self._log_player(agent_id, f"{agent_id}: {content}")
            else:
                # Public messages go to both public and private logs
                if log_to_system:
                    public_log = self.shared_memory["public_event_log"]
                    private_log = self.shared_memory["private_event_log"]
                    self.shared_memory["public_event_log"] = f"{public_log}\n{content}"
                    self.shared_memory["private_event_log"] = f"{private_log}\n{content}"

                # Write to every agent's log
                for agent in self.shared_memory["private_state"]["players"]:
                    personal_log = self.shared_memory["private_state"]["players"][agent]["personal_event_log"]
                    self.shared_memory["private_state"]["players"][agent]["personal_event_log"] = f"{personal_log}\n{content}"
                    write_to_agent_log(agent, content)  # Sync to agent's file
                if print_to_system:
                    self._log_player(agent_id, f"{agent_id}: {content}")

        # Handle system messages
        else:
            if is_private:
                # Private system messages go to private logs
                if log_to_system:
                    private_log = self.shared_memory["private_event_log"]
                    self.shared_memory["private_event_log"] = f"{private_log}\n{content}"
                if print_to_system:
                    self._log_event(f"SYSTEM: {content}")
            else:
                # Public system messages go to all logs
                if log_to_system:
                    public_log = self.shared_memory["public_event_log"]
                    private_log = self.shared_memory["private_event_log"]
                    self.shared_memory["public_event_log"] = f"{public_log}\n{content}"
                    self.shared_memory["private_event_log"] = f"{private_log}\n{content}"

                # Write to every agent's log
                for agent in self.shared_memory["private_state"]["players"]:
                    personal_log = self.shared_memory["private_state"]["players"][agent]["personal_event_log"]
                    self.shared_memory["private_state"]["players"][agent]["personal_event_log"] = f"{personal_log}\n{content}"
                    write_to_agent_log(agent, content)  # Sync to agent's file
                if print_to_system:
                    self._log_event(f"SYSTEM: {content}")
                    
    def evaluate_daily_stage_tasks(self, day_label: str, tasks: List[str]) -> Dict[str, Any]:
        """
        Evaluate daily stage tasks after a single day-night cycle, then print the final
        results in a multi-line style. This includes the outcome of each task in the tasks list.

        Args:
            day_label (str): For example "Day3".
            tasks (List[str]): e.g. ["protect_seer", "rescue_villager", "run_for_sheriff",
                                    "exile_werewolf", "poison_werewolf"].

        Returns:
            dict: Summarized daily result, with final multi-line console printout.
        """


        # 1) Retrieve original and current scores
        original_scores = self.original_data.get("scores", {})
        current_scores = self.scores

        # 2) Identify newly added lines for villager
        villager_original_details = original_scores.get("villager", {}).get("details", [])
        villager_current_details = current_scores.get("villager", {}).get("details", [])
        old_len_v = len(villager_original_details)
        new_villager_entries = villager_current_details[old_len_v:]

        # 3) Compute daily decimal score for villager and werewolf
        villager_original_total = original_scores.get("villager", {}).get("total", 0.0)
        villager_current_total  = current_scores.get("villager", {}).get("total", 0.0)
        daily_score_villager = villager_current_total - villager_original_total

        werewolf_original_total = original_scores.get("werewolf", {}).get("total", 0.0)
        werewolf_current_total  = current_scores.get("werewolf", {}).get("total", 0.0)
        daily_score_werewolf = werewolf_current_total - werewolf_original_total

        # 4) Use regex to detect major-scoring lines (≥1 point)
        pattern = re.compile(r'.*([\+\-]\d+(?:\.\d+)?)\s*points?\.$')
        major_score_events = []
        for entry in new_villager_entries:
            match = pattern.match(entry.strip())
            if match:
                try:
                    pts_val = float(match.group(1))
                    if abs(pts_val) >= 1.0:
                        major_score_events.append(entry)
                except ValueError:
                    pass

        # 5) completed_tasks dictionary
        completed_tasks = {
            "protect_seer": False,
            "rescue_villager": False,
            "run_for_sheriff": False,
            "exile_werewolf": False,
            "poison_werewolf": False
        }

        # Example logic for protect_seer if seer is alive
        if "protect_seer" in tasks:
            seer_ids = self.get_player_id("seer")
            if seer_ids:
                seer_id = seer_ids[0]
                alive_players = self.shared_memory["public_state"].get("alive_players", [])
                if seer_id in alive_players:
                    completed_tasks["protect_seer"] = True

        # Additional pattern-based logic for rescue_villager, run_for_sheriff,
        # exile_werewolf, poison_werewolf
        rescue_pattern = re.compile(r'Witch\s+saved\s+(.+)\s+from\s+werewolf\s+attack\.\s*\+2\s+points?\.')
        sheriff_pattern = re.compile(r'Villager-aligned\s+sheriff\s+(.+)\s+elected\.\s*\+2\s+points?\.')
        exile_pattern   = re.compile(r'Werewolf\s+(.+)\s+was\s+banished\.\s*\+2\s+points?\.')
        poison_pattern  = re.compile(r'Witch\s+killed\s+werewolf\s+(.+)\s+with\s+poison\.\s*\+2\s+points?\.')

        for evt in major_score_events:
            evt_str = evt.strip()
            if "rescue_villager" in tasks and not completed_tasks["rescue_villager"]:
                if rescue_pattern.match(evt_str):
                    completed_tasks["rescue_villager"] = True
            if "run_for_sheriff" in tasks and not completed_tasks["run_for_sheriff"]:
                if sheriff_pattern.match(evt_str):
                    completed_tasks["run_for_sheriff"] = True
            if "exile_werewolf" in tasks and not completed_tasks["exile_werewolf"]:
                if exile_pattern.match(evt_str):
                    completed_tasks["exile_werewolf"] = True
            if "poison_werewolf" in tasks and not completed_tasks["poison_werewolf"]:
                if poison_pattern.match(evt_str):
                    completed_tasks["poison_werewolf"] = True

        # 6) Daily theoretical max
        def task_points(tname: str) -> int:
            if tname == "protect_seer":
                return 1
            else:
                return 2

        daily_theoretical = sum(task_points(t) for t in tasks)
        if "rescue_villager" in tasks and "poison_werewolf" in tasks:
            daily_theoretical -= 2
        if daily_theoretical > 7:
            daily_theoretical = 7

        # 7) daily_actual_major_score
        daily_major_score = 0.0
        for evt_line in major_score_events:
            match2 = pattern.match(evt_line.strip())
            if match2:
                daily_major_score += float(match2.group(1))
        if completed_tasks["rescue_villager"] and completed_tasks["poison_werewolf"]:
            daily_major_score -= 2
        if daily_major_score > 7:
            daily_major_score = 7

        # 8) Surviving players
        alive_players_list = self.shared_memory["public_state"].get("alive_players", [])
        surviving_players = [
            {"player_id": pid, "role": self.get_player_role(pid)}
            for pid in alive_players_list
        ]

        # 9) Build the main result
        result = {
            "title": f"{day_label}-stage-result",
            "daily_score_villager": daily_score_villager,
            "daily_score_werewolf": daily_score_werewolf,
            "major_score_events": major_score_events,
            "task_completion": {t: completed_tasks[t] for t in tasks},
            "daily_theoretical_max": daily_theoretical,
            "daily_actual_major_score": daily_major_score,
            "surviving_players": surviving_players,
            "config": self.config
        }

        # 10) File saving logic
        label_str = day_label.strip().lower()
        day_number = 0
        if label_str.startswith("day"):
            num_part = label_str[3:].strip()
            try:
                day_number = int(num_part)
            except ValueError:
                day_number = 0
        day_result_filename = f"Day_{day_number}_to_Day_{day_number + 1}_result.json"
        result_path = self.shared_memory_path.replace("shared_memory.json", day_result_filename)

        try:
            with open(result_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)
        except (FileNotFoundError, OSError) as e:
            self._log_system(f"Failed to write final result to {result_path}: {e}. "
                            f"Attempting to rename file with game outcome...")
            fallback_path = result_path.replace(".json", "_Villagers_win.json")
            try:
                with open(fallback_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=4, ensure_ascii=False)
                self._log_system(f"Final result successfully written to fallback file {fallback_path}")
            except Exception as e2:
                self._log_system(f"Failed to write final result to {result_path}: {e2}. "
                            f"Attempting to rename file with game outcome...")
                fallback_path = result_path.replace(".json", "_werewolves_win.json")
                try:
                    with open(fallback_path, "w", encoding="utf-8") as f:
                        json.dump(result, f, indent=4, ensure_ascii=False)
                    self._log_system(f"Final result successfully written to fallback file {fallback_path}")
                except Exception as e3:
                    self._log_system(f"Failed to write final result to {result_path}: {e3}. ")
        # 11) Build the final_message string in a multi-line format, including each task's result
        #     in the style of "GAME END!" separation lines
        survivor_info = "\n".join(
            f"{player['player_id']} ({player['role']})"
            for player in surviving_players
        )

        # We'll also list each task's completion
        tasks_info_str = ""
        for t in tasks:
            status_str = "Completed" if completed_tasks[t] else "Not Completed"
            tasks_info_str += f"- {t}: {status_str}\n"

        final_message = (
            f"\n======================================================\n"
            f"DAILY TASKS RESULT FOR {day_label}\n\n"
            f"Remaining players:\n{survivor_info}\n\n"
            f"Scores:\n"
            f"Villagers: {daily_score_villager:.2f}\n"
            f"Werewolves: {daily_score_werewolf:.2f}\n"
            f"Result Score: {daily_major_score:.2f}\n\n"
            f"Task Completion:\n{tasks_info_str}"
            f"======================================================\n"
        )

        # 12) Print final_message in red, then reset color
        print(Fore.RED + final_message + Style.RESET_ALL)

        return result

    def generate_daily_tasks(self):
        """
        Generate two lists of tasks for the current day:
        1) A private task list (for system determination)
        2) A public task list (for agents, which may omit or disguise certain info)

        The task definitions follow previous naming:
        - "protect_seer"
        - "rescue_villager"
        - "run_for_sheriff"
        - "exile_werewolf"
        - "poison_werewolf"

        Logic for the private task list:
        1) If the seer is alive, add "protect_seer".
        2) If the witch has poison_count == 1, add "poison_werewolf".
        3) If the witch has antidote_count == 1, add "rescue_villager".
        4) If current day == 1, add "run_for_sheriff".
        5) Always add "exile_werewolf".

        Logic for the public task list:
        1) If the witch has poison_count == 1, add "poison_werewolf".
        2) If the witch has antidote_count == 1, add "rescue_villager".
        3) If current day == 1, add "run_for_sheriff".
        4) Always add "exile_werewolf".
        5) Always add "protect_seer".

        Returns:
            tuple(list, list): (private_task_list, public_task_list)
        """

        private_tasks = []
        public_tasks = []

        # 1) Identify current day
        current_day = self.shared_memory["public_state"].get("days", 0)

        # 2) Check if the seer is alive
        seer_alive = False
        seer_ids = self.get_player_id("seer")
        if seer_ids:
            seer_id = seer_ids[0]
            alive_players = self.shared_memory["public_state"].get("alive_players", [])
            if seer_id in alive_players:
                seer_alive = True

        # 3) Get witch's poison_count and antidote_count
        #    We search for the "witch" role among players in private_state
        poison_count = 0
        antidote_count = 0
        players_info = self.shared_memory["private_state"].get("players", {})
        for pid, pinfo in players_info.items():
            if pinfo.get("role") == "witch":
                status = pinfo.get("status", {})
                poison_count = status.get("poison_count", 0)
                antidote_count = status.get("antidote_count", 0)
                break  # assume only one witch

        # ===== Private tasks logic =====
        # a) protect_seer if seer is alive
        if seer_alive:
            private_tasks.append("protect_seer")

        # b) poison_werewolf if witch has poison_count == 1
        if poison_count == 1:
            private_tasks.append("poison_werewolf")

        # c) rescue_villager if witch has antidote_count == 1
        if antidote_count == 1:
            private_tasks.append("rescue_villager")

        # d) run_for_sheriff if current_day == 1
        if current_day == 1:
            private_tasks.append("run_for_sheriff")

        # e) always add exile_werewolf
        private_tasks.append("exile_werewolf")

        # ===== Public tasks logic =====
        # 1) poison_werewolf if witch poison == 1
        if poison_count == 1:
            public_tasks.append("poison_werewolf")
        # 2) rescue_villager if witch antidote == 1
        if antidote_count == 1:
            public_tasks.append("rescue_villager")
        # 3) run_for_sheriff if day1
        if current_day == 1:
            public_tasks.append("run_for_sheriff")
        # 4) always add exile_werewolf
        public_tasks.append("exile_werewolf")
        # 5) always add protect_seer
        public_tasks.append("protect_seer")
        self.log_event(
            is_private=True,
            agent_id="system",
            content=(
                "[generate_daily_tasks] Private tasks: "
                f"{private_tasks}\n"
                "[generate_daily_tasks] Public tasks: "
                f"{public_tasks}"
            )
        )
        return private_tasks, public_tasks
    
    def update_alive_players(self):
        """
        Updates the list of alive players based on their health status in private_state.
        Records in the personal log and log file for players whose health drops to 0.
        """
        # Get all player information
        players = self.shared_memory["private_state"]["players"]

        # Get the current list of alive players
        alive_players = [
            player_id for player_id, player_info in players.items()
            if player_info["status"].get("health", 0) == 1
        ]

        # Check which players have gone from alive to dead
        previously_alive = set(self.shared_memory["public_state"]["alive_players"])
        currently_alive = set(alive_players)
        newly_dead = previously_alive - currently_alive

        # For the dead players, log the event and update their personal log file
        for player_id in newly_dead:
            death_message = f"Player {player_id} has been eliminated from the game."
            self.log_event(
                is_private=False,
                agent_id="system",
                content=death_message)

        # Update to public_state
        self.shared_memory["public_state"]["alive_players"] = alive_players

        # Log the updated list of alive players
        self._log_system(f"Updated alive_players list: {alive_players}")

    def get_player_role(self, player_id: str) -> str:
        """
        Returns the role of the specified player.

        Args:
            player_id (str): The ID of the player whose role is to be retrieved.

        Returns:
            str: The role of the player (e.g., "wolf", "villager", "seer", etc.).
                Returns "Unknown" if the player ID is not found.
        """
        # Get player information from private state
        player_info = self.shared_memory["private_state"]["players"].get(player_id, None)
        if player_info is None:
            return "Unknown"  # Return "Unknown" if player does not exist

        # Return the player's role
        return player_info.get("role", "Unknown")

    def get_player_id(self, role: str) -> list:
        """
        Returns a list of player IDs who have the specified role.

        Args:
            role (str): The role to search for (e.g., "wolf", "villager", "seer", etc.).

        Returns:
            list: A list of player IDs who have the specified role.
        """
        players = self.shared_memory["private_state"]["players"]

        players_with_role = [
            player_id for player_id, player_info in players.items()
            if player_info.get("role") == role
        ]

        return players_with_role

    def guard_action(self) -> None:
        """
        Publishes a guard action event to the event bus. The event is directed to the player
        with the 'guard' role and 'health' status of 1, allowing them to take their action.
        """
        guard_player_instance = None
        for agent in self.agents:
            agent_id = agent.agent_id
            player_info = self.shared_memory["private_state"]["players"].get(agent_id, {})
            if player_info["role"] == "guard" and agent.agent_id in self.shared_memory["public_state"].get("alive_players", []):
                guard_player_instance = agent
                break

        if guard_player_instance:
            last_protected = self.shared_memory["private_state"].get("guard_last_night_protect", None)

            event = {
                "event_type": "guard_action",
                "sender": self,
                "recipients": [guard_player_instance],
                "content": {
                    "night_info": last_protected,
                }
            }
            self._log_event("Guard action event published.")
            self.publish_event(event)
        else:
            self._log_event("Guard action event published.")
            self.log_event(
                is_private=True,
                agent_id="system",
                content="No guard player found. Skip guard action."
            )

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

    def reset_guard_protection(self):
        """
        Resets the protection_count for all players at the beginning of each night.
        """
        for player_id, player_info in self.shared_memory["private_state"]["players"].items():
            player_info["status"]["protection_count"] = 0

        # Clear the last protected target

        # Log the reset action
        self._log_system("Guard protection reset for all players.")

    def werewolf_action(self) -> None:
        """
        Publishes a single werewolf action event to the event bus.
        The event is directed to all players with the 'wolf' role, allowing them to take their action.
        """
        alive_werewolves = []
        try:
            alive_players = self.shared_memory["public_state"].get("alive_players", [])

            for agent in self.agents:
                player_info = self.shared_memory["private_state"]["players"].get(agent.agent_id, {})
                    
                if player_info.get("role") == "wolf" and agent.agent_id in self.shared_memory["public_state"].get("alive_players", []):
                    alive_werewolves.append((agent, agent.agent_id))
            if len(alive_werewolves) != 0:
                alive_werewolves_instances = [agent for agent, _ in alive_werewolves]
                alive_werewolves_ids = [agent_id for _, agent_id in alive_werewolves]

                new_round_target = {wolf_id: None for wolf_id in alive_werewolves_ids}
                self.shared_memory["private_state"]["werewolf_action"]["round_targets"].append(new_round_target)

                alive_players_str = ", ".join(alive_players)
                alive_werewolves_ids_str = ", ".join(map(str, alive_werewolves_ids))

                event = {
                    "event_type": "werewolf_action",
                    "sender": self,  # 标识为环境实例
                    "recipients": alive_werewolves_instances,
                    "content": {
                        "player_info": {
                            "alive_players": alive_players_str, 
                            "alive_werewolves": alive_werewolves_ids_str 
                        }
                    }
                }
                self.publish_event(event)
            else:
                self.log_event(
                    is_private=True,
                    agent_id="system",
                    content="No werewolf players found. Skip guard action."
                )
        except Exception as e:
            self._log_event(f"Error in werewolf_action: {str(e)}")
            raise

    def werewolf_discussion(self) -> None:
        """
        Publishes a werewolf discussion event to the event bus.
        The event is directed to all players with the 'wolf' role, allowing them to discuss and refine their action.
        """
        alive_players = self.shared_memory["public_state"].get("alive_players", [])

        alive_werewolves = []
        for agent in self.agents:
                player_info = self.shared_memory["private_state"]["players"].get(agent.agent_id, {})
                    
                if player_info.get("role") == "wolf" and agent.agent_id in self.shared_memory["public_state"].get("alive_players", []):
                    alive_werewolves.append((agent, agent.agent_id))
        alive_werewolves_instances = [agent for agent, _ in alive_werewolves]
        alive_werewolves_ids = [agent_id for _, agent_id in alive_werewolves]

        last_round_targets = self.shared_memory["private_state"]["werewolf_action"]["round_targets"][-2]
        allies_target_info = {wolf_id: target for wolf_id, target in last_round_targets.items()}

        rounds_remaining = self.shared_memory["private_state"]["werewolf_action"]["rounds_remaining"]

        alive_players_str = ", ".join(alive_players)
        alive_werewolves_ids_str = ", ".join(alive_werewolves_ids)

        event_content = {
            "allies_info": {
                "alive_players": alive_players_str,
                "alive_werewolves": alive_werewolves_ids_str,
                "last_round_targets": allies_target_info
            },
            "rounds_remaining": rounds_remaining
        }

        event = {
            "event_type": "werewolf_discussion",
            "sender": self,
            "recipients": alive_werewolves_instances,
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

        alive_werewolves_count = len([
            agent_id for agent_id, player_info in self.shared_memory["private_state"]["players"].items()
            if player_info["role"] == "wolf" and player_info["status"].get("health", 0) == 1
        ])
        majority_target = None
        for target, count in target_counts.items():
            if count > alive_werewolves_count / 2:
                majority_target = target
                break

        if majority_target:
            self.shared_memory["private_state"]["werewolf_action"]["final_target"] = majority_target
            target_status = self.shared_memory["private_state"]["players"][majority_target]["status"]
            self.scores["werewolf"]["total"] += 1
            self.scores["werewolf"]["details"].append(
                "Werewolves has unified their goal. Werewolf +1 point."
            )
            if target_status["protection_count"] == 0:
                target_status["health"] = 0
                success = True
                kill_result = f"Target {majority_target} attacked by werewolves and health reduced."
            else:
                success = False
                kill_result = f"Target {majority_target} protected, no health reduction."
                self.scores["villager"]["total"] += 2
                self.scores["villager"]["details"].append({
                    "event": "guard_protection",
                    "target": majority_target,
                    "description": f"Guard successfully protected {majority_target} from werewolf attack."
                })


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

                alive_werewolves_ids = []
                for agent in self.agents:
                    player_info = self.shared_memory["private_state"]["players"].get(agent.agent_id, {})

                    if player_info.get("role") == "wolf" and player_info.get("status", {}).get("health", 0) == 1:
                        alive_werewolves_ids.append(agent.agent_id)
                
         
                new_round_target = {wolf_id: None for wolf_id in alive_werewolves_ids}

         
                if isinstance(self.shared_memory["private_state"]["werewolf_action"].get("round_targets"), list):
                    self.shared_memory["private_state"]["werewolf_action"]["round_targets"].append(new_round_target)
                else:
                    self._log_event("Error: round_targets is not a list. Resetting it to a new list.")
                    self.shared_memory["private_state"]["werewolf_action"]["round_targets"] = [new_round_target]
                
          
                self.werewolf_discussion()
            else:
               
                alive_werewolves = []
                for agent in self.agents:
                    player_info = self.shared_memory["private_state"]["players"].get(agent.agent_id, {})

                    if player_info.get("role") == "wolf" and player_info.get("status", {}).get("health", 0) == 1:
                            alive_werewolves.append(agent.agent_id)
                
             
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

                for wolf_id in current_round_targets.keys():
                    self.log_event(
                        is_private=True,
                        agent_id=wolf_id,
                        content=detailed_fail_result,
                        log_to_system=False,
                        print_to_system=False
                    )
                
                self.log_event(
                    is_private=True,
                    agent_id="system",
                    content=detailed_fail_result
                )

                if isinstance(self.shared_memory["private_state"].get("night_cache"), list):
                    current_night_log = self.shared_memory["private_state"]["night_cache"][-1]
                    current_night_log["werewolf_action"] = {
                        "final_target": "None",
                        "attack_successful": False,
                        "reason": "Failed due to lack of consensus"
                    }
                else:
                    self._log_event("Night cache is not initialized.")
                
               
                self.mark_event_complete(event_type="werewolf_action")

    def seer_action(self) -> None:
        """
        Publishes a seer action event to the event bus. The event is directed to the player
        with the 'seer' role and 'health' status of 1, allowing them to take their action.
        """
        seer_player_instance = None
        for agent in self.agents:
            agent_id = agent.agent_id
            player_info = self.shared_memory["private_state"]["players"].get(agent_id, {})
            if player_info["role"] == "seer" and agent.agent_id in self.shared_memory["public_state"].get("alive_players", []):
                seer_player_instance = agent
                break

        if seer_player_instance:
            event = {
                "event_type": "seer_action",
                "sender": self, 
                "recipients": [seer_player_instance],
                "content": {} 
            }

            self._log_event("Seer action event published.")
            self.publish_event(event)
        else:
            self.log_event(
                is_private=True,
                agent_id="system",
                content="No seer player found. Skip guard action."
            )
            self._log_event("Seer action event published.")

    def process_seer_action(self, event: dict) -> None:
        """
        Processes the seer action by recording the check target specified in the event.

        Args:
            event (dict): The event data containing 'check_target' information.
        """
        try:
            seer_id = event.get("sender")
            action_content = event.get("content", {})
            if isinstance(action_content, dict):
                check_target = action_content.get("check_target", None)
            else:
                check_target = None
          
            alive_players = self.shared_memory.get("public_state", {}).get("alive_players", [])
            if not alive_players:
                self.log_event(
                    is_private=True,
                    agent_id="system",
                    content="Error: Unable to retrieve alive players list from public state."
                )
                self.mark_event_complete(event_type="seer_action")
                return

            if check_target not in alive_players:
                self.log_event(
                    is_private=True,
                    agent_id=seer_id,
                    content=f"<<Private>> Seer action failed. Invalid check target: {check_target}. Not in alive players: {alive_players}.",
                    log_to_system=False
                )
                self.mark_event_complete(event_type="seer_action")
                return

            seer_status = self.shared_memory["private_state"]["players"][seer_id]["status"]
            if "check_history" not in seer_status:
                seer_status["check_history"] = {}

            current_night = self.shared_memory["public_state"]["days"]

            is_werewolf = self.shared_memory["private_state"]["players"][check_target]["role"] == "wolf"
            check_result = "werewolf" if is_werewolf else "not a werewolf"

            check_history_entry = {"player": check_target, "result": check_result}
            seer_status["check_history"][f"Night {current_night}"] = check_history_entry

            seer_log_content = (
                f"At Night {current_night}, You have checked {check_target}, the result is: {check_result}."
            )
            self.log_event(
                is_private=True,
                agent_id=seer_id,
                content=seer_log_content,
                log_to_system=False
            )

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
        witch_player_instance = None
        for agent in self.agents:
            agent_id = agent.agent_id
            player_info = self.shared_memory["private_state"]["players"].get(agent_id, {})
            if player_info["role"] == "witch" and agent.agent_id in self.shared_memory["public_state"].get("alive_players", []):
                witch_player_instance = agent
                break

        if witch_player_instance:
            final_target = self.shared_memory["private_state"]["werewolf_action"].get("final_target", "nobody")


            event = {
                "event_type": "witch_action",
                "sender": self,  
                "recipients": [witch_player_instance],
                "content": {
                    "night_info": final_target
                }
            }
            self.publish_event(event)
            self._log_event("Witch action event published.")
        else:
            self.log_event(
                is_private=True,
                agent_id="system",
                content="No witch player found. Skip guard action."
            )
            self._log_event("Witch action event published.")

    def process_witch_action(self, event: dict) -> None:
        """
        Processes the witch action based on the event content, applying antidote or poison
        to the specified targets as chosen by the witch and updating the available potion counts.

        Args:
            event (dict): The event data containing the witch's choices for using antidote and poison.
        """
        action_content = event.get("content", {})
        if isinstance(action_content, dict):
            use_antidote = action_content.get("use_antidote", False)
            use_poison = action_content.get("use_poison", False)
            poison_target = action_content.get("poison_target", None)
        else:
            use_antidote = False
            use_poison = False
            poison_target = None
            self.mark_event_complete(event_type="witch_action")
            return
    
        witch_id = event["sender"]
        witch_status = self.shared_memory["private_state"]["players"][witch_id]["status"]

        final_target = self.shared_memory["private_state"]["werewolf_action"].get("final_target")

        current_night_log = self.shared_memory["private_state"].get("night_cache", [])[-1]

        if use_antidote and final_target and witch_status["antidote_count"] > 0:
            
            player_deaths = current_night_log.get("player_dead_tonight", [])
            if final_target in player_deaths:
                
                self.shared_memory["private_state"]["players"][final_target]["status"]["health"] = 1
                witch_status["antidote_count"] = 0
                player_deaths.remove(final_target)

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

                current_night_log["witch_action"] = {
                    "action": "antidote",
                    "target": final_target
                }
                self.mark_event_complete(event_type="witch_action")
            else:
                self.log_event(
                    is_private=True,
                    agent_id=witch_id,
                    content=f"Witch tried to use antidote on {final_target}, but that player was not in the werewolf's kill list."
                )
                self.mark_event_complete(event_type="witch_action")
                return

        elif use_poison and poison_target in self.shared_memory["public_state"]["alive_players"] and witch_status["poison_count"] > 0:
          
            self.shared_memory["private_state"]["players"][poison_target]["status"]["health"] = 0
            witch_status["poison_count"] = 0

            current_night_log["player_dead_tonight"].append(poison_target)

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

            poison_target_role = self.get_player_role(poison_target)
            if poison_target_role == "wolf":
             
                self.scores["villager"]["total"] += 2
                self.scores["villager"]["details"].append(f"Witch killed werewolf {poison_target} with poison. +2 points.")
            else:
               
                self.scores["villager"]["total"] -= 2
                self.scores["villager"]["details"].append(f"Witch killed non-werewolf {poison_target} with poison. -2 points.")

            
            current_night_log["witch_action"] = {
                "action": "poison",
                "target": poison_target
            }
            self.mark_event_complete(event_type="witch_action")

        
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

            
            current_night_log["witch_action"] = {
                "action": "none",
                "target": None
            }
            self.mark_event_complete(event_type="witch_action")
        else:
            self.mark_event_complete(event_type="witch_action")
            return

    def run_for_sheriff(self) -> None:
        """
        Publishes a 'run for sheriff' event to the event bus. This event is directed to all
        Publishes a 'run for sheriff' event to the event bus. This event is directed to all
        players with a 'health' status of 1, allowing them to decide if they want to run for sheriff.
        """
        if "sheriff_election" not in self.shared_memory["private_state"]:
           
            self.shared_memory["private_state"]["sheriff_election"] = {
                "candidates": {agent.agent_id: None for agent in self.agents}
            }

        alive_players = [
            agent for agent in self.agents
            if agent.agent_id in self.shared_memory["public_state"].get("alive_players", [])
        ]

        if alive_players:
            event = {
                "event_type": "run_for_sheriff",
                "sender": self,
                "recipients": alive_players, 
                "content": {}  
            }
            self._log_event("Run for sheriff event published for all living players.")
            self.publish_event(event)
        else:
            self._log_event("No living players found to participate in sheriff election.")

    def process_run_for_sheriff(self, event: dict) -> None:
        """
        Processes each player's decision on whether or not to run for sheriff and
        Processes each player's decision on whether or not to run for sheriff and
        prepares candidates for the sheriff election once all decisions are received.

        Updates the day cache with the list of candidates and relevant events.

        Args:
            event (dict): The event data containing the player's decision on running for sheriff.
        """
        player_id = event.get("sender", None)
        if isinstance(event.get("content", {}), dict):
            run_for_sheriff = event.get("content", {}).get("run_for_sheriff", False)
        else:
            run_for_sheriff = False
        self.shared_memory["private_state"]["sheriff_election"]["candidates"][player_id] = run_for_sheriff

        if any(choice is None for choice in self.shared_memory["private_state"]["sheriff_election"]["candidates"].values()):
            self._log_system(f"current decision:{self.shared_memory['private_state']['sheriff_election']['candidates']}")
            self._log_event("Waiting for all players to decide on running for sheriff.")
            return

        current_day = self.shared_memory["public_state"]["days"]
        day_cache = self.shared_memory["public_state"]["day_cache"][current_day - 1]

        if "sheriff_candidates" not in day_cache:
            day_cache["sheriff_candidates"] = []

        candidate_ids = sorted([
            agent_id for agent_id, wants_to_run in self.shared_memory["private_state"]["sheriff_election"]["candidates"].items()
            if wants_to_run
        ])

        if candidate_ids:
            candidate_list_str = ", ".join(candidate_ids)
            self.log_event(
                is_private=False,
                agent_id="system",
                content=f"Sheriff election candidates: {candidate_list_str}"
            )

            day_cache["sheriff_candidates"] = candidate_ids

            self.shared_memory["private_state"]["sheriff_election"]["sheriff_speech"] = {candidate_id: None for candidate_id in candidate_ids}
            self.shared_memory["private_state"]["sheriff_election"]["final_candidate"] = []


            first_candidate_id = candidate_ids[0]
            self.mark_event_complete(event_type="run_for_sheriff")
            self.sheriff_speech(candidate_ids, first_candidate_id)



        else:
            self.log_event(
                is_private=False,
                agent_id="system",
                content="No candidates decided to run for sheriff. No sheriff in this game anymore.",
                )

            self.mark_event_complete(event_type="run_for_sheriff")
            return

    def sheriff_speech(self, candidate_ids: list, candidate_id: str, first=True) -> None:
        """
        Publishes a 'sheriff_speech' event for a given candidate, allowing them to make their speech for the election.

        Args:
            candidate_ids (list): List of IDs of all candidates running for sheriff, sorted by ID.
            candidate_id (str): The ID of the current candidate making their speech.
        """
        current_day = self.shared_memory["public_state"]["days"]
        day_cache = self.shared_memory["public_state"]["day_cache"][current_day - 1]

        day_cache.setdefault("sheriff_speech", {cid: None for cid in candidate_ids})
        day_cache.setdefault("final_candidate", [])

        speech_sequence = ", ".join(candidate_ids)

        speech_position = candidate_ids.index(candidate_id) + 1

        if day_cache.get("sheriff_speech") and any(speech is not None for speech in day_cache["sheriff_speech"].values()):
            election_info = "\n".join([
                f"{cid}: {speech}" for cid, speech in day_cache["sheriff_speech"].items()
                if speech is not None
            ])
        else:
            election_info = "No speeches available yet. You are the first one."

        candidate_instance = None
        for agent in self.agents:
            if agent.agent_id == candidate_id:
                candidate_instance = agent
                break
        if candidate_instance is None:
            self._log_system(f"Error: Candidate instance for {candidate_id} not found.")
            return            
        event = {
            "event_type": "sheriff_speech",
            "sender": self,
            "recipients": [candidate_instance],
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
            candidate_id = event.get("sender", "")
            action_content = event.get("content", {})
            if isinstance(action_content, dict):
                continue_running = action_content.get("continue_running", False)
                speech_content = action_content.get("speech_content", f"Error during generation for player {candidate_id}.")
            else:
                speech_content = f"Error during generation for player {candidate_id}."
                continue_running = False

            current_day = self.shared_memory["public_state"]["days"]
            day_cache = self.shared_memory["public_state"]["day_cache"][current_day - 1]

            day_cache["sheriff_speech"][candidate_id] = speech_content
            self.log_event(
                is_private=False,
                agent_id=candidate_id,
                content=f"{candidate_id}'s speech: {speech_content}"
            )

           
            if continue_running:
                
                day_cache["final_candidate"].append(candidate_id)
            else:
                
                self.log_event(
                    is_private=False,
                    agent_id="system",
                    content=f"{candidate_id} has withdrawn from the sheriff election."
                )

            
            candidate_ids = list(day_cache["sheriff_speech"].keys())
            remaining_candidates = [cid for cid in candidate_ids if day_cache["sheriff_speech"].get(cid) is None]

            if remaining_candidates:
                next_candidate_id = remaining_candidates[0]
                self.sheriff_speech(candidate_ids, next_candidate_id, first=False)

        except Exception as e:
            
            self._log_event(f"Error processing sheriff speech: {e}")

        finally:
            
            if not remaining_candidates:
                self._log_event("All candidates finish their speech. Now, remaining players will vote for sheriff.")
                self.mark_event_complete(event_type="sheriff_speech")
                self.vote_for_sheriff()

    def vote_for_sheriff(self) -> None:
        """
        Initiates the voting process for the sheriff election by broadcasting a "vote_for_sheriff" event
        to all eligible players. Eligible players are those who are alive and have not participated in the sheriff election.
        """
        # Step 1: Get the election log and list of candidates
        election_log = self.shared_memory["private_state"]["sheriff_election"].get("sheriff_speech", {})
        final_candidates = self.shared_memory["private_state"]["sheriff_election"].get("final_candidate", [])

        # Convert election log to a formatted string
        election_log_str = "\n".join([f"{candidate}: {speech}" for candidate, speech in election_log.items()])
        # Convert candidate list to a comma-separated string
        candidate_list_str = ", ".join(final_candidates)

        # Step 2: Determine the voters (alive players who have not run for sheriff)
        all_players = self.shared_memory["public_state"]["alive_players"]
        never_ran_for_sheriff = [
            player_id for player_id in all_players
            if not self.shared_memory["private_state"]["sheriff_election"]["candidates"].get(player_id)
        ]
        
        # Get player references by their player IDs
        voter_refs = [agent for agent in self.agents if agent.agent_id in never_ran_for_sheriff]
        if not voter_refs:
            self._log_event("All players have run for sheriff (or none are eligible to vote). Skipping sheriff vote.")
            self.mark_event_complete(event_type="run_for_sheriff")  # or "vote_for_sheriff" depending on your event naming
            return

        # Step 3: Build the voting event
        event = {
            "event_type": "vote_for_sheriff",
            "sender": self,  # Environment instance
            "recipients": voter_refs,  # Send player references, not IDs
            "content": {
                "election_log": election_log_str,
                "candidate_list": candidate_list_str
            }
        }

        # Step 4: Publish the voting event
        self._log_event(f"Vote for sheriff event published to eligible voters {never_ran_for_sheriff}.")
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
            sheriff_role = self.get_player_role(sheriff_id)
            if sheriff_role != "wolf":
                # Villager-aligned sheriff
                self.scores["villager"]["total"] += 2
                self.scores["villager"]["details"].append(f"Villager-aligned sheriff {sheriff_id} elected. +2 points.")
            else:
                # Werewolf sheriff
                self.scores["werewolf"]["total"] += 2
                self.scores["werewolf"]["details"].append(f"Werewolf sheriff {sheriff_id} elected. +2 points.")
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
            content=f"Sheriff election votes:\n{vote_summary}\n(Note: The voting order reflects only the system's query sequence and does not imply any strategic alignment or motive.)"
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
        # Step 1: Get all players and sheriff's choices
        all_players = sorted(self.shared_memory["private_state"]["players"].keys())  # Sort by player ID
        alive_players = self.shared_memory["public_state"].get("alive_players", [])
        sheriff_id = self.shared_memory["public_state"].get("sheriff", None)
        if isinstance(event.get("content", {}), dict):
            starting_player = event.get("content", {}).get("starting_player", sheriff_id)
            from_left = event.get("content", {}).get("from_left", True)
        else:
            starting_player = sheriff_id
            from_left = True
        # Get the day's day_cache
        day_cache = self.shared_memory["public_state"]["day_cache"][-1]

        # Initialize speech_order_decision in day_cache if not present
        if "speech_order_decision" not in day_cache:
            day_cache["speech_order_decision"] = []

        # Step 2: Check if the starting player is in the player list
        if starting_player not in all_players:
            # If starting player is invalid, default to agent_1
            starting_player = all_players[0]

        # Step 3: Generate the speech order based on the starting player and direction
        starting_index = all_players.index(starting_player)

        if from_left:  # Start from left (decreasing order)
            speech_order = all_players[starting_index:] + all_players[:starting_index]
        else:  # Start from right (increasing order)
            speech_order = all_players[starting_index::-1] + all_players[:starting_index:-1]

        # The sheriff always speaks last
        if sheriff_id in speech_order:
            speech_order.remove(sheriff_id)
            speech_order.append(sheriff_id)

        # Step 4: Remove deceased players and generate the final speech order
        speech_order = [player for player in speech_order if player in alive_players]

        # Save and record the speech order
        day_cache["speech_order_decision"] = speech_order

        # Announce the order
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
        # Step 1: Get the day's speech order
        speech_order = day_cache.get("speech_order_decision", None)
        self._log_system(f"Current speech order: {speech_order}")
        if not speech_order:
            # Get default speech order (sort alive players in ascending order)
            alive_players = self.shared_memory["public_state"]["alive_players"]
            speech_order = sorted(alive_players)

        # Step 2: Determine the current speaker
        if current_speaker_id is None:
            current_speaker_id = speech_order[0]

        # Skip deceased players
        while current_speaker_id and self.shared_memory["private_state"]["players"][current_speaker_id]["status"]["health"] == 0:
            next_index = (speech_order.index(current_speaker_id) + 1) % len(speech_order)
            current_speaker_id = speech_order[next_index]

        if not current_speaker_id:
            self.log_event(is_private=False, agent_id="system", content="All players eligible to speak are dead.")
            return

        if "speech_log" not in day_cache:
            day_cache["speech_log"] = {}

        # Build the speech content history
        speech_log = day_cache["speech_log"]
        speech_history = "\n".join([f"{pid}: {content}" for pid, content in speech_log.items()])

        # Get player instance
        player_instance = next(agent for agent in self.agents if agent.agent_id == current_speaker_id)

        # Create and publish the speech event
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
        # Step 1: Get player ID and speech content
        player_id = event.get("sender", None)
        action_content = event.get("content", {})

        # Check if action_content is "no_action"
        if isinstance(action_content, dict): 
            speech_content = action_content.get("speech_content", f"Error during generation for player {player_id}.")
        else:
            speech_content = f"Error during generation for player {player_id}."

        # Step 2: Get current day and day_cache
        day_cache = self.shared_memory["public_state"]["day_cache"][-1]

        # Initialize speech_log in day_cache if not present
        if "speech_log" not in day_cache:
            day_cache["speech_log"] = {}

        # Record the speech content in day_cache's speech_log
        day_cache["speech_log"][player_id] = speech_content

        # Step 3: Announce the speech content
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
            # Trigger the next player's speech
            next_speaker_id = remaining_speakers[0]
            self.player_speeches(current_speaker_id=next_speaker_id)
        else:
            # All players have finished speaking
            self.mark_event_complete(event_type="player_speech")
            self.log_event(is_private=False, agent_id="system", content="All players have completed their speeches for today.")

    def vote_action(self) -> None:
        """
        Initiates the exile voting process by broadcasting a "vote_action" event to all alive players.
        All alive players can participate in the vote, and no additional information is required for the voting process.
        """
        # Step 1: Determine the voters (all alive players)
        all_players = self.shared_memory["public_state"]["alive_players"]
        
        # Get player references by their player ID
        voter_refs = [agent for agent in self.agents if agent.agent_id in all_players]

        # Step 2: Build the voting event
        event = {
            "event_type": "vote_action",
            "sender": self,  # Environment instance
            "recipients": voter_refs,  # Send player references, not IDs
            "content": {}  # Exile voting does not require additional content
        }

        # Step 3: Publish the voting event
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

            banished_role = self.get_player_role(banished_player_id)
            if banished_role == "wolf":
                self.scores["villager"]["total"] += 2
                self.scores["villager"]["details"].append(f"Werewolf {banished_player_id} was banished. +2 points.")
            else:
                self.scores["werewolf"]["total"] += 1
                self.scores["werewolf"]["details"].append(f"Non-werewolf {banished_player_id} was banished. Werewolves +1 point.")

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

        for voter, choice in votes.items():
            voter_role = self.get_player_role(voter)
            choice_role = self.get_player_role(choice) if choice != "abstain" else None

            if voter_role != "wolf" and choice_role == "wolf":
                self.scores["villager"]["total"] += 0.2
                self.scores["villager"]["details"].append(f"Villager {voter} voted for werewolf {choice}. +0.2 points.")
            elif voter_role != "wolf" and choice_role != "wolf" and choice != "abstain":
                
                self.scores["villager"]["total"] -= 0.1
                self.scores["villager"]["details"].append(f"Villager {voter} voted for villager {choice}. -0.1 points.")

        # Step 6: Publish all votes publicly with the banishment announcement
        vote_summary = "\n".join([f"{voter} voted for {choice}" for voter, choice in votes.items()])
        self.log_event(
            is_private=False,
            agent_id="system",
            content=f"Banishment votes:\n{vote_summary}\n(Note: The voting order reflects only the system's query sequence and does not imply any strategic alignment or motive.)"
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
        if isinstance(action_content, dict):
            speech_content = action_content.get("speech_content", f"Error during generation for player {player_id}.")
        else:
            speech_content = f"Error during generation for player {player_id}."
        # Get the current day and the day cache
        current_day = self.shared_memory["public_state"]["days"]
        day_cache = self.shared_memory["public_state"]["day_cache"][current_day - 1]

        # Initialize the "last_words" key in the day cache if it doesn't exist
        if "last_words" not in day_cache:
            day_cache["last_words"] = {}

        # Step 2: Record the player's last words in the day cache
        day_cache["last_words"][player_id] = speech_content

        # Step 3: Log the last words to the public log
        self.log_event(
            is_private=False,
            agent_id=player_id,
            content=f"Last words from {player_id}: {speech_content}"
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
        Processes an action event received from the EventBus.
        The event contains details about the action to be taken by the agent.

        Args:
            event (dict): A dictionary containing event details, including the event type,
                        content, and any relevant information needed for action processing.
        """
        event_type = event.get("event_type", "unknown")
        if event_type != "reply_sheriff_speech" and event_type != "reply_player_speech":
            self._log_player(
                event.get("sender", ""),
                f"Received action event of type '{event_type}'. Event content: {event.get('content', 'Error when retrieving content')}"
            )

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

def start_game(name, config_path):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at {config_path}")

    try:
        env = WerewolfEnv(name=name, config_path=config_path)

        print(f"Starting game: {name}")
        env.start()

    except Exception as e:
        print(f"An error occurred while starting the game: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start werewolf simulation")
    parser.add_argument('--rounds', type=int, default=10, help="Simulation round")
    parser.add_argument('--name', type=str, default="werewolf_engine_demo", help="Game name")
    parser.add_argument('--config_path', type=str, default=os.path.join("marble", "configs", "test_config", "werewolf_config_4o.yaml"),
                        help="Config path")

    args = parser.parse_args()

    for i in range(args.rounds):
        print(f"Simulating game round {i+1}...")
        start_game(args.name, args.config_path)