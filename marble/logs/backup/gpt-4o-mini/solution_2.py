# solution.py

import random
from typing import List, Dict, Any

# Define the base class for the game environment
class GameEnvironment:
    def __init__(self, level: int, objective: str):
        self.level = level  # Level number
        self.objective = objective  # Objective of the level
        self.agents = []  # List to hold agents in the environment
        self.score = 0  # Score for the current level

    def add_agent(self, agent: 'Agent'):
        """Add an agent to the game environment."""
        self.agents.append(agent)

    def complete_objective(self):
        """Complete the objective and update the score."""def complete_objective(self):
        """Complete the objective and update the score if achieved."""
        if self.check_objective_completion():
            self.score += 100  # Reward for completing the objective
            print(f"Objective '{self.objective}' completed! Score: {self.score}")
        else:
            print(f"Objective '{self.objective}' not completed yet.")

    def check_objective_completion(self):
        """Check if the objective has been completed based on agent actions."""
        # Implement logic to verify if the objective is achieved
        return all(agent.health > 0 for agent in self.agents)  # Example condition        print(f"Objective '{self.objective}' completed! Score: {self.score}")

# Define the base class for agents
class Agent:
    def __init__(self, name: str, role: str, abilities: List[str]):
        self.name = name  # Name of the agent
        self.role = role  # Role of the agent (attacker, defender, scout)
        self.abilities = abilities  # List of abilities
        self.health = 100  # Health of the agent

    def communicate(self, message: str):
        """Simulate communication between agents."""
        print(f"{self.name} ({self.role}): {message}")

    def perform_action(self, action: str):
        """Perform an action based on the agent's role."""
        print(f"{self.name} is performing action: {action}")

# Define specific agent roles
class Attacker(Agent):
    def __init__(self, name: str):
        super().__init__(name, "Attacker", ["increased speed"])

    def attack(self):
        """Perform an attack action."""
        self.perform_action("Attack the enemy!")

class Defender(Agent):
    def __init__(self, name: str):
        super().__init__(name, "Defender", ["shielding"])

    def defend(self):
        """Perform a defend action."""
        self.perform_action("Defend the base!")

class Scout(Agent):
    def __init__(self, name: str):
        super().__init__(name, "Scout", ["increased speed", "reconnaissance"])

    def scout(self):
        """Perform a scouting action."""
        self.perform_action("Scout the area for enemies!")

# Define the game logic
class TeamTacticsGame:
    def __init__(self):
        self.environments = []  # List of game environments
        self.current_environment = None  # Current environment being played

    def create_environment(self, level: int, objective: str):
        """Create a new game environment."""
        env = GameEnvironment(level, objective)
        self.environments.append(env)
        self.current_environment = env

    def start_game(self):
        """Start the game and run through the environments."""
        for env in self.environments:
            print(f"Starting level {env.level} with objective: {env.objective}")
            env.complete_objective()  # Simulate completing the objective

# Example test cases to validate functionality
def run_tests():
    # Create a game instance
    game = TeamTacticsGame()

    # Create environments
    game.create_environment(1, "Capture the Flag")
    game.create_environment(2, "Defend the Base")
    game.create_environment(3, "Eliminate Enemies")

    # Create agents
    attacker = Attacker("Attacker1")
    defender = Defender("Defender1")
    scout = Scout("Scout1")

    # Add agents to the current environment
    game.current_environment.add_agent(attacker)
    game.current_environment.add_agent(defender)
    game.current_environment.add_agent(scout)

    # Simulate actions
    attacker.attack()
    defender.defend()
    scout.scout()

    # Run the game
    game.start_game()

# Run the tests
if __name__ == "__main__":
    run_tests()