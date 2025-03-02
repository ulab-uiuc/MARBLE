# solution.py

import random
from typing import List, Dict, Any

class AI_Agent:
    """Class representing an AI agent in the Galactic Dominion game."""
    
    def __init__(self, name: str):
        self.name = name
        self.resources = 100  # Starting resources
        self.territory = 0  # Initial territory control
        self.technology_level = 1  # Initial technology level
        self.alliances = []  # List of alliances with other agents

    def build_structure(self):
        """Build a structure if enough resources are available."""
        if self.resources >= 20:
            self.resources -= 20
            self.territory += 1  # Gain territory by building
            print(f"{self.name} built a structure. Territory: {self.territory}, Resources: {self.resources}")
        else:
            print(f"{self.name} does not have enough resources to build.")

    def research_technology(self):
        """Research technology to improve capabilities."""
        if self.resources >= 30:
            self.resources -= 30
            self.technology_level += 1  # Increase technology level
            print(f"{self.name} researched technology. Technology Level: {self.technology_level}, Resources: {self.resources}")
        else:
            print(f"{self.name} does not have enough resources to research.")

    def command_fleet(self):
        """Command fleet to explore or attack."""
        print(f"{self.name} is commanding the fleet.")

    def form_alliance(self, other_agent: 'AI_Agent'):
        """Form an alliance with another agent."""
        if other_agent not in self.alliances:
            self.alliances.append(other_agent)
            other_agent.alliances.append(self)  # Mutual alliance
            print(f"{self.name} formed an alliance with {other_agent.name}.")

class GameEngine:
    """Class to manage the game state and interactions between AI agents."""
    
    def __init__(self, agents: List[AI_Agent]):
        self.agents = agents
        self.turn = 0

    def adaptive_difficulty(self):
        """Adjust difficulty based on agents' performance."""        event_type = random.choice(['natural disaster', 'alien invasion', 'resource discovery', 'joint defense'])
        print(f"Event occurred: {event_type}")
        if event_type == 'natural disaster':
            for agent in self.agents:
                agent.resources -= 10  # All agents lose resources
                print(f"{agent.name} lost resources due to a natural disaster. Resources: {agent.resources}")
        elif event_type == 'alien invasion':
            for agent in self.agents:
                agent.command_fleet()  # Command fleet to respond to invasion
        elif event_type == 'resource discovery':
            resource_amount = random.randint(5, 20)
            for agent in self.agents:
                agent.resources += resource_amount  # All agents gain resources
                print(f"{agent.name} discovered resources. Resources: {agent.resources}")
        elif event_type == 'joint defense':
            print("Agents must collaborate to defend against a common threat!")
            for agent in self.agents:
                agent.command_fleet()  # Command fleet to respond collectively            elif event_type == 'alien invasion':
                agent.command_fleet()  # Command fleet to respond to invasion

    def play_turn(self):
        """Execute a single turn of the game."""
        print(f"\n--- Turn {self.turn + 1} ---")
        for agent in self.agents:
            agent.build_structure()
            agent.research_technology()
            agent.command_fleet()
        self.dynamic_event()
        self.adaptive_difficulty()
        self.turn += 1

    def score_agents(self) -> Dict[str, Any]:
        """Evaluate and score agents based on their performance."""
        scores = {}
        for agent in self.agents:
            score = (agent.territory * 10) + (agent.technology_level * 5) + (agent.resources)
            scores[agent.name] = score
        return scores

def main():
    """Main function to run the Galactic Dominion game."""
    # Create AI agents
    agents = [AI_Agent("Agent A"), AI_Agent("Agent B"), AI_Agent("Agent C")]
    
    # Initialize the game engine
    game = GameEngine(agents)
    
    # Simulate a number of turns
    for _ in range(5):  # Play 5 turns
        game.play_turn()
    
    # Score the agents at the end of the game
    scores = game.score_agents()
    print("\nFinal Scores:")
    for agent_name, score in scores.items():
        print(f"{agent_name}: {score}")

if __name__ == "__main__":
    main()