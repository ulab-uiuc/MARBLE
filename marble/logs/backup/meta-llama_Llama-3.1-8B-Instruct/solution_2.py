# team_tactics.py
# Main implementation of the Team_Tactics game

import random
import time

# Define the game environment with multiple levels
class Level:
    def __init__(self, name, objective):
        self.name = name
        self.objective = objective
        self.enemies = []
        self.flag = None

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def add_flag(self, flag):
        self.flag = flag

# Define the AI agents with different roles and abilities
class Agent:
    def __init__(self, name, role, speed=1, health=100, shield=0):
        self.name = name
        self.role = role
        self.speed = speed
        self.health = health
        self.shield = shield
        self.position = (0, 0)

    def move(self, x, y):
        self.position = (x, y)

    def communicate(self, message):
        print(f"{self.name} says: {message}")

# Define the communication system
class CommunicationSystem:
    def __init__(self):
        self.messages = []

    def send_message(self, message):
        self.messages.append(message)

    def receive_message(self):
        return self.messages.pop(0)

# Define the scoring system
class ScoringSystem:
    def __init__(self):
        self.score = 0

    def reward(self, points):
        self.score += points

    def penalize(self, points):
        self.score -= points

# Define the game
class Game:
    def __init__(self):
        self.levels = []
        self.agents = []
        self.communication_system = CommunicationSystem()
        self.scoring_system = ScoringSystem()

    def add_level(self, level):
        self.levels.append(level)

    def add_agent(self, agent):
        self.agents.append(agent)

    def start_game(self):
        for level in self.levels:
            print(f"Level: {level.name}")
            for agent in self.agents:
                agent.move(random.randint(0, 10), random.randint(0, 10))
                agent.communicate(f"I'm at position ({agent.position[0]}, {agent.position[1]})")
            for agent in self.agents:
                message = self.communication_system.receive_message()
                print(f"{agent.name} received message: {message}")
            if level.objective == "capture_flag":
                for agent in self.agents:
                    if agent.role == "attacker":
                        agent.move(level.flag.position[0], level.flag.position[1])
                        agent.communicate(f"I'm capturing the flag!")
                        self.scoring_system.reward(10)
            elif level.objective == "defend_base":
                for agent in self.agents:
                    if agent.role == "defender":
                        agent.move(level.flag.position[0], level.flag.position[1])
                        agent.communicate(f"I'm defending the base!")
                        self.scoring_system.reward(10)
            elif level.objective == "eliminate_enemies":
                for agent in self.agents:
                    if agent.role == "scout":
                        agent.move(random.randint(0, 10), random.randint(0, 10))
                        agent.communicate(f"I've found an enemy!")
                        self.scoring_system.reward(10)
            print(f"Score: {self.scoring_system.score}")
            time.sleep(2)

# Create the game environment
level1 = Level("Level 1", "capture_flag")
level1.add_flag(Flag((5, 5)))
level1.add_enemy(Enemy((3, 3)))
level1.add_enemy(Enemy((7, 7))

level2 = Level("Level 2", "defend_base")
level2.add_flag(Flag((5, 5))
level2.add_enemy(Enemy((3, 3))
level2.add_enemy(Enemy((7, 7))

level3 = Level("Level 3", "eliminate_enemies")
level3.add_flag(Flag((5, 5))
level3.add_enemy(Enemy((3, 3))
level3.add_enemy(Enemy((7, 7))

# Create the AI agents
agent1 = Agent("Agent 1", "attacker", speed=2, health=150, shield=10)
agent2 = Agent("Agent 2", "defender", speed=1, health=120, shield=5)
agent3 = Agent("Agent 3", "scout", speed=3, health=100, shield=0)

# Create the game
game = Game()
game.add_level(level1)
game.add_level(level2)
game.add_level(level3)
game.add_agent(agent1)
game.add_agent(agent2)
game.add_agent(agent3)

# Start the game
game.start_game()

# Define the Flag class
class Flag:
    def __init__(self, position):
        self.position = position

# Define the Enemy class
class Enemy:
    def __init__(self, position):
        self.position = position