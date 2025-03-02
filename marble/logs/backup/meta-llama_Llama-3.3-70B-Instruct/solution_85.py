# solution.py
import threading
import time
from datetime import datetime
import matplotlib.pyplot as plt
from getpass import getpass
import hashlib

# User class to store user credentials
class User:class Analyst:def input_data(self, player_name, score, assists):def update_data(self, player_name, score, assists):
        with self.lock:
            if player_name in self.centralized_data:
                self.centralized_data[player_name]['score'] = score
                self.centralized_data[player_name]['assists'] = assistsdef visualize(self, analyst):
        # Visualizing data
        scores = [stats['score'] for stats in analyst.data.values()]
        assists = [stats['assists'] for stats in analyst.data.values()]
        players = list(analyst.data.keys())

        plt.bar(players, scores, label='Scores')
        plt.bar(players, assists, label='Assists')
        plt.xlabel('Players')
        plt.ylabel('Stats')
        plt.title('Player Performance Chart')
        plt.legend()
        plt.show()


# Test cases
def test_create_account(sport_game):
    sport_game.create_account('analyst1', 'password1')
    sport_game.create_account('analyst2', 'password2')

def test_authenticate(sport_game):
    assert sport_game.authenticate('analyst1', 'password1')
    assert not sport_game.authenticate('analyst1', 'wrong_password')

def test_add_analyst(sport_game):
    analyst1 = sport_game.add_analyst('analyst1')
    analyst2 = sport_game.add_analyst('analyst2')
    assert analyst1 is not None
    assert analyst2 is not None

def test_collaborate(sport_game):
    analyst1 = sport_game.add_analyst('analyst1')
    analyst2 = sport_game.add_analyst('analyst2')
    analyst1.input_data('Player1', 10, 5)
    sport_game.collaborate(analyst1, analyst2)
    assert analyst1.data == analyst2.data

def test_visualize(sport_game):
    analyst = sport_game.add_analyst('analyst1')
    analyst.input_data('Player1', 10, 5)
    analyst.input_data('Player2', 20, 10)
    sport_game.visualize(analyst)

def test_edge_cases(sport_game):
    # Simulating network latency
    time.sleep(1)
    analyst1 = sport_game.add_analyst('analyst1')
    analyst2 = sport_game.add_analyst('analyst2')
    analyst1.input_data('Player1', 10, 5)
    sport_game.collaborate(analyst1, analyst2)
    assert analyst1.data == analyst2.data

    # Simulating data conflicts
    analyst1.input_data('Player1', 20, 10)
    analyst2.input_data('Player1', 30, 15)
    sport_game.collaborate(analyst1, analyst2)
    assert analyst1.data == analyst2.data

    # Simulating user disconnections
    del analyst1
    del analyst2
    try:
        sport_game.collaborate(analyst1, analyst2)
    except NameError:
        print("Analysts have been disconnected.")

def main():
    sport_game = SportGameCollaborativeAnalytics()
    test_create_account(sport_game)
    test_authenticate(sport_game)
    test_add_analyst(sport_game)
    test_collaborate(sport_game)
    test_visualize(sport_game)
    test_edge_cases(sport_game)

if __name__ == "__main__":
    main()