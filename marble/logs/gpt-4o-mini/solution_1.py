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
        self.score = sum(player.treasures_collected for player in self.players)self.score = sum(player.treasures_collected for player in self.players) - (duration / 60)def end_game(self):
        """End the game and calculate scores."""
        for team in self.teams:
            team.calculate_score()team.calculate_score(duration)end_time = time.time()
        duration = end_time - self.start_time
        print(f"Game ended! Duration: {duration:.2f} seconds")
        self.display_scores()

    def display_scores(self):
        """Display the scores of all teams."""
        for team in self.teams:
            print(f"Team {team.team_name} Score: {team.score}")

# Example of how to use the classes to create a game
if __name__ == "__main__":
    # Create teams
    team1 = Team("Explorers")
    team2 = Team("Adventurers")

    # Create players with unique abilities
    player1 = Player("Alice", "Strength")
    player2 = Player("Bob", "Agility")
    player3 = Player("Charlie", "Intelligence")
    player4 = Player("Diana", "Stealth")

    # Add players to teams
    team1.add_player(player1)
    team1.add_player(player2)
    team2.add_player(player3)
    team2.add_player(player4)

    # Initialize game
    game = Game()
    game.add_team(team1)
    game.add_team(team2)

    # Start the game
    game.start_game()

    # Simulate treasure collection
    player1.collect_treasure()
    player2.collect_treasure()
    player3.collect_treasure()
    player4.collect_treasure()
    player1.collect_treasure()  # Alice collects another treasure

    # End the game
    game.end_game()