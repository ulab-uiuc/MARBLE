# solution.py

import random
import json
from collections import defaultdict

class BoardGameTeamCollaborator:
    def __init__(self):
        # Initialize teams, scores, and game settings
        self.teams = {}
        self.scores = defaultdict(int)
        self.game_settings = {}
        self.current_turn = None
        self.leaderboard = []

    def create_team(self, team_name):
        """Create a new team with the given name."""
        if team_name not in self.teams:
            self.teams[team_name] = []
            print(f"Team '{team_name}' created.")
        else:
            print(f"Team '{team_name}' already exists.")

    def assign_player(self, team_name, player_name, role):
        """Assign a player to a team with a specific role."""
        if team_name in self.teams:
            self.teams[team_name].append({'name': player_name, 'role': role})
            print(f"Player '{player_name}' assigned to team '{team_name}' as '{role}'.")
        else:
            print(f"Team '{team_name}' does not exist.")

    def input_score(self, team_name, score):
        """Input the score for a team and update the leaderboard."""
        if team_name in self.teams:
            self.scores[team_name] += score
            self.update_leaderboard()
            print(f"Score for team '{team_name}' updated to {self.scores[team_name]}.")
        else:
            print(f"Team '{team_name}' does not exist.")

    def update_leaderboard(self):
        """Update the leaderboard based on current scores."""
        self.leaderboard = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)

    def display_leaderboard(self):
        """Display the current leaderboard."""
        print("Current Leaderboard:")
        for team, score in self.leaderboard:
            print(f"Team: {team}, Score: {score}")

    def set_game_settings(self, game_type, num_players, scoring_rules):
        """Set customizable game settings."""
        self.game_settings = {
            'game_type': game_type,
            'num_players': num_players,
            'scoring_rules': scoring_rules
        }
        print(f"Game settings updated: {self.game_settings}")

    def suggest_strategy(self, team_name):
        """Suggest strategies based on previous performance."""
        if team_name in self.teams:            # Placeholder for machine learning analysis
            historical_data = self.get_historical_data(team_name)
            suggestions = self.analyze_performance(historical_data)
            print(f"Suggestions for team '{team_name}': {suggestions}")            print(f"Suggestions for team '{team_name}': {random.choice(suggestions)}")
        else:
            print(f"Team '{team_name}' does not exist.")

    def notify_turn(self):
        """Notify the current team whose turn it is to play."""
        if self.current_turn:
            print(f"It's {self.current_turn}'s turn to play!")
        else:
            print("No current turn set.")

    def next_turn(self):
        """Set the next turn based on the current turn."""
        if not self.current_turn:
            self.current_turn = list(self.teams.keys())[0]  # Start with the first team
        else:
            current_index = list(self.teams.keys()).index(self.current_turn)
            self.current_turn = list(self.teams.keys())[(current_index + 1) % len(self.teams)]
        self.notify_turn()

# Example usage
if __name__ == "__main__":
    collaborator = BoardGameTeamCollaborator()
    collaborator.create_team("Red Team")
    collaborator.create_team("Blue Team")
    collaborator.assign_player("Red Team", "Alice", "Leader")
    collaborator.assign_player("Blue Team", "Bob", "Leader")
    collaborator.set_game_settings("Strategy Game", 4, "Points per action")
    collaborator.input_score("Red Team", 10)
    collaborator.input_score("Blue Team", 15)
    collaborator.display_leaderboard()
    collaborator.suggest_strategy("Red Team")
    collaborator.next_turn()