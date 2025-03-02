# solution.py

import random
from typing import List, Dict, Any

class AI_Agent:
    """Class representing an AI agent in the Galactic Dominion game."""
    
    def __init__(self, name: str):
        self.name = name
        self.resources = 100  # Starting resources
        self.territory = 0  # Starting territory
        self.technology_level = 1  # Starting technology level
        self.alliance = None  # Current alliance status
        self.performance_score = 0  # Performance score

    def build_structure(self):
        """Build a structure if enough resources are available."""
        if self.resources >= 20:
            self.resources -= 20
            self.territory += 1
            print(f"{self.name} built a structure. Territory: {self.territory}, Resources: {self.resources}")
        else:
            print(f"{self.name} does not have enough resources to build a structure.")

    def research_technology(self):
        """Research technology to improve capabilities."""
        if self.resources >= 30:
            self.resources -= 30
            self.technology_level += 1
            print(f"{self.name} researched technology. Technology Level: {self.technology_level}, Resources: {self.resources}")
        else:
            print(f"{self.name} does not have enough resources to research technology.")

    def command_fleet(self):
        """Command fleet to expand territory."""
        if self.resources >= 15:
            self.resources -= 15
            self.territory += 1
            print(f"{self.name} commanded fleet. Territory: {self.territory}, Resources: {self.resources}")
        else:
            print(f"{self.name} does not have enough resources to command fleet.")

    def evaluate_performance(self):
        """Evaluate performance based on territory, technology, and resources."""
        self.performance_score = self.territory * 2 + self.technology_level + self.resources // 10
        print(f"{self.name}'s performance score: {self.performance_score}")

class GameEngine:
    """Class representing the game engine for Galactic Dominion."""
    
    def __init__(self, agents: List[AI_Agent]):
        self.agents = agents
        self.turn = 0

    def adaptive_difficulty(self):
        """Adjust difficulty based on agents' performance."""
        avg_score = sum(agent.performance_score for agent in self.agents) / len(self.agents)
        if avg_score < 50:
            print("Difficulty level: Easy")
        elif avg_score < 100:
            print("Difficulty level: Medium")
        else:
            print("Difficulty level: Hard")

    def dynamic_event(self):
        """Introduce a random event that affects all agents."""
        events = ["Natural Disaster", "Alien Invasion", "Resource Boom"]
        event = random.choice(events)
        print(f"Event occurred: {event}")
        for agent in self.agents:
            if event == "Natural Disaster":
                agent.resources -= 10
                print(f"{agent.name} lost resources due to a natural disaster.")event_effects = {
            "Natural Disaster": lambda agent: agent.resources := max(0, agent.resources - 10),
            "Alien Invasion": lambda agent: agent.territory := max(0, agent.territory - 1),
            "Resource Boom": lambda agent: agent.resources += 20
        }
        for agent in self.agents:
            if event in event_effects:
                event_effects[event](agent)
                print(f"{agent.name} {'lost resources due to a natural disaster.' if event == 'Natural Disaster' else 'lost territory due to an alien invasion.' if event == 'Alien Invasion' else 'gained resources from a resource boom.'}")                print(f"{agent.name} gained resources from a resource boom.")

    def play_turn(self):
        """Execute a turn for all agents."""
        print(f"\n--- Turn {self.turn + 1} ---")
        for agent in self.agents:
            agent.build_structure()
            agent.research_technology()
            agent.command_fleet()
            agent.evaluate_performance()
        self.dynamic_event()
        self.adaptive_difficulty()
        self.turn += 1

def main():
    """Main function to run the Galactic Dominion game."""
    # Create AI agents
    agents = [AI_Agent("AI_1"), AI_Agent("AI_2"), AI_Agent("AI_3")]
    
    # Initialize the game engine
    game = GameEngine(agents)
    
    # Simulate a number of turns
    for _ in range(5):
        game.play_turn()

if __name__ == "__main__":
    main()