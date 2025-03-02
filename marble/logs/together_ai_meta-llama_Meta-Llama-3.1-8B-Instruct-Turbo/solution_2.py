# team_tactics.py
# Main implementation of the Team_Tactics game

import random
import time

# Define the game environment with multiple levels
class GameEnvironment:
    def __init__(self):
        self.levels = {
            "level1": {"objective": "capture the flag", "enemies": 5, "flag_location": (10, 10)},
            "level2": {"objective": "defend the base", "enemies": 10, "base_location": (20, 20)},
            "level3": {"objective": "eliminate all enemies", "enemies": 15, "enemy_locations": [(30, 30), (40, 40), (50, 50)]}
        }

    def get_level(self, level_name):
        return self.levels.get(level_name)

# Define the AI agent with different roles and abilities
class AIAgent:
    def __init__(self, role, abilities=None):
        self.role = role
        self.abilities = abilities if abilities else {}
        self.speed = 1
        self.health = 100

    def move(self, x, y):
        print(f"Agent {self.role} is moving to ({x}, {y})")

    def communicate(self, message):
        print(f"Agent {self.role} is communicating: {message}")

    def use_ability(self, ability_name):
        if ability_name in self.abilities:
            print(f"Agent {self.role} is using ability: {ability_name}")
        else:
            print(f"Agent {self.role} does not have ability: {ability_name}")

# Define the communication system
class CommunicationSystem:
    def __init__(self):
        self.agents = []

    def add_agent(self, agent):
        self.agents.append(agent)

    def broadcast_message(self, message):
        for agent in self.agents:
            agent.communicate(message)

# Define the scoring system
class ScoringSystem:
    def __init__(self):
        self.score = 0

    def update_score(self, points):
        self.score += points

    def get_score(self):
        return self.score

# Define the game logic
class GameLogic:
    def __init__(self, environment, agents, communication_system, scoring_system):
        self.environment = environment
        self.agents = agents
        self.communication_system = communication_system
        self.scoring_system = scoring_system

    def start_game(self, level_name):
        level = self.environment.get_level(level_name)
        print(f"Starting game: {level['objective']}")

        for agent in self.agents:
            agent.move(level["flag_location"][0], level["flag_location"][1])

        self.communication_system.broadcast_message(f"Objective: {level['objective']}")

        for agent in self.agents:
            agent.use_ability("speed")

        time.sleep(2)

        for agent in self.agents:
            agent.move(level["base_location"][0], level["base_location"][1])

        self.scoring_system.update_score(100)

        print(f"Game over. Score: {self.scoring_system.get_score()}")

# Define the test cases
class TestCases:
    def __init__(self, game_logic):
        self.game_logic = game_logic

    def test_capture_flag(self):
        self.game_logic.start_game("level1")

    def test_defend_base(self):
        self.game_logic.start_game("level2")

    def test_eliminate_enemies(self):
        self.game_logic.start_game("level3")

# Create the game environment
environment = GameEnvironment()

# Create the AI agents
agents = [
    AIAgent("attacker", {"speed": 2}),
    AIAgent("defender", {"shielding": 1}),
    AIAgent("scout", {"healing": 1})
]

# Create the communication system
communication_system = CommunicationSystem()
for agent in agents:
    communication_system.add_agent(agent)

# Create the scoring system
scoring_system = ScoringSystem()

# Create the game logic
game_logic = GameLogic(environment, agents, communication_system, scoring_system)

# Create the test cases
test_cases = TestCases(game_logic)

# Run the test cases
test_cases.test_capture_flag()
test_cases.test_defend_base()
test_cases.test_eliminate_enemies()