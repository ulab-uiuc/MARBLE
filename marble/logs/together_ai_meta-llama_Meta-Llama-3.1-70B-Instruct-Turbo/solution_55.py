# multi_agent_maze.py

import random
import sqlite3
from enum import Enum

# Define the roles of the players
class Role(Enum):
    PATHFINDER = 1
    BLOCKER = 2
    SWAPPER = 3

# Define the game state
class GameState:
    def __init__(self):
        self.players = {}
        self.maze = []
        self.current_level = 1
        self.points = 0

    def add_player(self, player_id, role):
        self.players[player_id] = role

    def update_maze(self, maze):
        self.maze = maze

    def update_level(self, level):
        self.current_level = level

    def update_points(self, points):
        self.points += points

# Define the player profile
class PlayerProfile:
    def __init__(self, player_id, name, role):
        self.player_id = player_id
        self.name = name
        self.role = role
        self.points = 0
        self.game_history = []

    def update_points(self, points):
        self.points += points

    def update_game_history(self, game_id):
        self.game_history.append(game_id)

# Define the game database
class GameDatabase:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS players
            (player_id INTEGER PRIMARY KEY, name TEXT, role TEXT)
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_history
            (game_id INTEGER PRIMARY KEY, player_id INTEGER, points INTEGER)
        ''')
        self.conn.commit()

    def add_player(self, player_id, name, role):
        self.cursor.execute('''
            INSERT INTO players (player_id, name, role) VALUES (?, ?, ?)
        ''', (player_id, name, role))
        self.conn.commit()

    def update_player_points(self, player_id, points):
        self.cursor.execute('''
            UPDATE players SET points = points + ? WHERE player_id = ?
        ''', (points, player_id))
        self.conn.commit()

    def add_game_history(self, game_id, player_id, points):
        self.cursor.execute('''
            INSERT INTO game_history (game_id, player_id, points) VALUES (?, ?, ?)
        ''', (game_id, player_id, points))
        self.conn.commit()

# Define the game logic
class MultiAgentMaze:
    def __init__(self):
        self.game_state = GameState()
        self.database = GameDatabase('multi_agent_maze.db')

    def start_game(self):
        # Initialize the game state
        self.game_state.update_maze(self.generate_maze())
        self.game_state.update_level(1)
        self.game_state.update_points(0)

        # Add players to the game
        for i in range(3):
            player_id = i + 1
            role = Role(i + 1)
            self.game_state.add_player(player_id, role)
            self.database.add_player(player_id, f'Player {player_id}', role.name)

        # Start the game loop
        while True:
            # Get the current player
            current_player_id = self.get_current_player()
            current_player_role = self.game_state.players[current_player_id]

            # Get the player's action
            action = self.get_player_action(current_player_id, current_player_role)

            # Update the game state based on the player's action
            self.update_game_state(action)

            # Check if the game is over
            if self.is_game_over():
                break

    def generate_maze(self):
        # Generate a random maze
        maze = []
        for i in range(10):
            row = []
            for j in range(10):
                row.append(random.randint(0, 1))
            maze.append(row)
        return maze

    def get_current_player(self):
        # Get the current player based on the game state
        current_player_id = 1
        for player_id, role in self.game_state.players.items():
            if role == Role.PATHFINDER:
                current_player_id = player_id
                break
        return current_player_id

    def get_player_action(self, player_id, role):
        # Get the player's action based on their role
        if role == Role.PATHFINDER:
            action = input(f'Player {player_id}, please enter your action (move up, move down, move left, move right): ')
        elif role == Role.BLOCKER:
            action = input(f'Player {player_id}, please enter your action (block up, block down, block left, block right): ')
        elif role == Role.SWAPPER:
            action = input(f'Player {player_id}, please enter your action (swap up, swap down, swap left, swap right): ')
        return action

    def update_game_state(self, action):
        # Update the game state based on the player's action
        if action == 'move up':
            self.game_state.update_points(10)
        elif action == 'move down':
            self.game_state.update_points(-10)
        elif action == 'move left':
            self.game_state.update_points(10)
        elif action == 'move right':
            self.game_state.update_points(-10)
        elif action == 'block up':
            self.game_state.update_points(20)
        elif action == 'block down':
            self.game_state.update_points(-20)
        elif action == 'block left':
            self.game_state.update_points(20)
        elif action == 'block right':
            self.game_state.update_points(-20)
        elif action == 'swap up':
            self.game_state.update_points(30)
        elif action == 'swap down':
            self.game_state.update_points(-30)
        elif action == 'swap left':
            self.game_state.update_points(30)
        elif action == 'swap right':
            self.game_state.update_points(-30)

    def is_game_over(self):
        # Check if the game is over
        if self.game_state.points >= 100:
            return True
        return False

# Create a new game
game = MultiAgentMaze()
game.start_game()