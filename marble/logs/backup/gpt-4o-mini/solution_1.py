# solution.py

import random
import time

class Player:
    """Class representing a player in the game."""
    
    def __init__(self, name, ability):
        self.name = name
        self.ability = ability
        self.treasures_collected = 0

    def collect_treasure(self):
        """Method to collect a treasure."""
        self.treasures_collected += 1

class Team:
    """Class representing a team of players."""
    
    def __init__(self, team_name):
        self.team_name = team_name
        self.players = []
        self.score = 0

    def add_player(self, player):
        """Method to add a player to the team."""
        if len(self.players) < 4:
            self.players.append(player)
        else:
            raise Exception("Team is full. Cannot add more players.")

    def calculate_score(self):
        """Calculate the team's score based on treasures collected."""
        self.score = sum(player.treasures_collected for player in self.players)

class Environment:
    """Class representing an environment in the game."""
    
    def __init__(self, name, difficulty):
        self.name = name
        self.difficulty = difficulty
        self.puzzles = self.create_puzzles()

    def create_puzzles(self):
        """Create puzzles based on the environment's difficulty."""
        return [f"Puzzle {i+1} (Difficulty: {self.difficulty})" for i in range(self.difficulty)]

class Game:
    """Main class to manage the game."""
    
    def __init__(self):
        self.teams = []
        self.current_environment = None
        self.start_time = None

    def add_team(self, team):
        """Add a team to the game."""
        self.teams.append(team)

    def start_game(self):
        """Start the game by initializing the environment and timer."""
        self.current_environment = Environment("Ancient Ruins", random.randint(1, 5))
        self.start_time = time.time()
        print(f"Game started in environment: {self.current_environment.name}")

    def end_game(self):
        """End the game and calculate scores."""
        elapsed_time = time.time() - self.start_time
        for team in self.teams:
            team.calculate_score()team.score = max(0, team.score - (elapsed_time // 10))  # Apply penalty to prevent negative scores        self.declare_winner()

    def declare_winner(self):
        """Declare the winning team based on scores."""
        winner = max(self.teams, key=lambda team: team.score)
        print(f"The winning team is {winner.team_name} with a score of {winner.score}!")

# Example usage
if __name__ == "__main__":
    # Create teams
    team1 = Team("Team Alpha")
    team2 = Team("Team Beta")

    # Add players to teams
    team1.add_player(Player("Alice", "Strength"))
    team1.add_player(Player("Bob", "Agility"))
    team2.add_player(Player("Charlie", "Intelligence"))
    team2.add_player(Player("Diana", "Stealth"))

    # Start the game
    game = Game()
    game.add_team(team1)
    game.add_team(team2)
    game.start_game()

    # Simulate treasure collection
    team1.players[0].collect_treasure()  # Alice collects a treasure
    team1.players[1].collect_treasure()  # Bob collects a treasure
    team2.players[0].collect_treasure()  # Charlie collects a treasure

    # End the game
    game.end_game()