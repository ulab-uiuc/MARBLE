# team_treasure_hunt.py
# Main implementation of the Team Treasure Hunt game

import random
import time

class Player:
    """Represents a player in the game with unique abilities."""
    
    def __init__(self, name, ability):
        """
        Initializes a player with a name and an ability.
        
        Args:
            name (str): The player's name.
            ability (str): The player's ability (strength, agility, intelligence, or stealth).
        """
        self.name = name
        self.ability = ability
        self.treasures = 0

class Environment:
    """Represents an environment in the game with puzzles and challenges."""
    
    def __init__(self, name, difficulty):
        """
        Initializes an environment with a name and a difficulty level.
        
        Args:
            name (str): The environment's name.
            difficulty (int): The environment's difficulty level (1-5).
        """
        self.name = name
        self.difficulty = difficulty
        self.puzzle = None

class Game:
    """Represents the game with multiplayer functionalities and a scoring system."""
    
    def __init__(self):
        """
        Initializes the game with four teams, each with four players.
        """
        self.teams = []
        for i in range(4):
            team = []
            for j in range(4):
                player = Player(f"Player {i*4+j+1}", random.choice(["strength", "agility", "intelligence", "stealth"]))
                team.append(player)
            self.teams.append(team)

    def add_environment(self, environment):
        """
        Adds an environment to the game.
        
        Args:
            environment (Environment): The environment to add.
        """
        self.environments = [environment]

    def start_game(self):
        """
        Starts the game and begins the treasure hunt.
        """
        print("Game started!")
        for team in self.teams:
            print(f"Team {self.teams.index(team)+1} is ready to start the treasure hunt!")
        for environment in self.environments:
            print(f"Team {self.teams.index(self.teams[0])+1} is now in the {environment.name} environment.")
            self.solve_puzzle(environment)
            self.collect_treasures(environment)
        self.calculate_score()

    def solve_puzzle(self, environment):
        """
        Solves a puzzle in the environment.
        
        Args:
            environment (Environment): The environment with the puzzle.
        """
        print(f"Team {self.teams.index(self.teams[0])+1} is trying to solve the puzzle in the {environment.name} environment.")
        # Simulate puzzle solving
        time.sleep(2)
        print(f"Team {self.teams.index(self.teams[0])+1} has solved the puzzle in the {environment.name} environment!")

    def collect_treasures(self, environment):
        """
        Collects treasures in the environment.
        
        Args:
            environment (Environment): The environment with the treasures.
        """
        print(f"Team {self.teams.index(self.teams[0])+1} is collecting treasures in the {environment.name} environment.")
        # Simulate treasure collection
        time.sleep(1)
        print(f"Team {self.teams.index(self.teams[0])+1} has collected {random.randint(1, 5)} treasures in the {environment.name} environment!")

    def calculate_score(self):
        """
        Calculates the score of each team based on the number of treasures collected and the time taken to reach the final chamber.
        """
        print("Calculating scores...")
        for team in self.teams:
            score = sum(player.treasures for player in team)
            print(f"Team {self.teams.index(team)+1} has a score of {score}.")

def main():
    # Create environments
    forest = Environment("Forest", 2)
    cave = Environment("Cave", 3)
    ancient_ruins = Environment("Ancient Ruins", 4)

    # Create game
    game = Game()
    game.add_environment(forest)
    game.add_environment(cave)
    game.add_environment(ancient_ruins)

    # Start game
    game.start_game()

if __name__ == "__main__":
    main()