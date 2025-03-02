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
    """Represents an environment in the game with challenges and puzzles."""
    
    def __init__(self, name, difficulty):
        """
        Initializes an environment with a name and a difficulty level.
        
        Args:
            name (str): The environment's name.
            difficulty (int): The environment's difficulty level (1-5).
        """
        self.name = name
        self.difficulty = difficulty
        self.puzzle = self.generate_puzzle()

    def generate_puzzle(self):
        """
        Generates a puzzle for the environment based on its difficulty level.
        
        Returns:
            dict: A dictionary containing the puzzle's description, required ability, and solution.
        """
        if self.difficulty == 1:
            return {"description": "Find the hidden key.", "required_ability": "intelligence", "solution": "Look under the rock."}
        elif self.difficulty == 2:
            return {"description": "Move the heavy stone.", "required_ability": "strength", "solution": "Use a pulley system."}
        elif self.difficulty == 3:
            return {"description": "Navigate the maze.", "required_ability": "agility", "solution": "Use a map to find the exit."}
        elif self.difficulty == 4:
            return {"description": "Avoid the traps.", "required_ability": "stealth", "solution": "Use a disguise to sneak past."}
        elif self.difficulty == 5:
            return {"description": "Solve the complex puzzle.", "required_ability": "intelligence", "solution": "Use a combination of logic and pattern recognition."}

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

    def start_game(self):
        """
        Starts the game and begins the treasure hunt.
        """
        print("The game has started. Good luck, teams!")
        for team in self.teams:
            print(f"Team {self.teams.index(team)+1} is ready to begin.")
        self.environment = Environment("Forest", 2)
        self.treasure_chamber = Environment("Treasure Chamber", 5)
        self.scoreboard = {"Team 1": 0, "Team 2": 0, "Team 3": 0, "Team 4": 0}

    def play_round(self):
        """
        Plays a round of the game where teams navigate through the environment and solve puzzles.
        """
        print(f"\nRound {self.teams.index(self.teams[0])+1}: {self.environment.name}")
        for team in self.teams:
            print(f"Team {self.teams.index(team)+1} is navigating through the {self.environment.name}.")
            for player in team:
                print(f"{player.name} is using their {player.ability} ability to solve the puzzle.")
                if self.environment.puzzle["required_ability"] == player.ability:
                    print(f"{player.name} has solved the puzzle! The solution is {self.environment.puzzle['solution']}.")
                    self.environment.puzzle = self.environment.generate_puzzle()
                    player.treasures += 1
                else:
                    print(f"{player.name} cannot solve the puzzle. They need to use their {self.environment.puzzle['required_ability']} ability.")
        self.update_scoreboard()

    def update_scoreboard(self):
        """
        Updates the scoreboard based on the number of treasures collected by each team.
        """
        for team in self.teams:
            self.scoreboard[f"Team {self.teams.index(team)+1}"] = sum(player.treasures for player in team)

    def reach_treasure_chamber(self):
        """
        Allows the first team to reach the treasure chamber and win the game.
        """
        print("\nThe teams have reached the treasure chamber.")
        for team in self.teams:
            print(f"Team {self.teams.index(team)+1} is trying to reach the treasure.")
            for player in team:
                print(f"{player.name} is using their {player.ability} ability to reach the treasure.")
                if self.treasure_chamber.difficulty == 5:
                    print(f"{player.name} has reached the treasure! They win the game!")
                    return
                else:
                    print(f"{player.name} cannot reach the treasure. They need to use their {self.treasure_chamber.puzzle['required_ability']} ability.")
        print("No team has reached the treasure. The game is a draw.")

    def play_game(self):
        """
        Plays the game until the first team reaches the treasure chamber.
        """
        self.start_game()
        while True:
            self.play_round()
            self.update_scoreboard()
            print(f"\nCurrent Scoreboard:")
            for team, score in self.scoreboard.items():
                print(f"{team}: {score} treasures")
            if self.scoreboard["Team 1"] > 0 or self.scoreboard["Team 2"] > 0 or self.scoreboard["Team 3"] > 0 or self.scoreboard["Team 4"] > 0:
                self.reach_treasure_chamber()
                break

game = Game()
game.play_game()