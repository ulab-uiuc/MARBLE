# solution.py

# Importing required libraries
import random
import time
import threading

# Defining a class for the game
class MultiAgentMaze:
    def __init__(self):
        # Initializing game state
        self.players = {}
        self.maze = self.generate_maze()
        self.paths = {}
        self.actions = {}
        self.score = 0
        self.level = 1

    # Function to generate a random maze
    def generate_maze(self):
        # For simplicity, we'll use a 5x5 maze
        maze = [[0 for _ in range(5)] for _ in range(5)]
        for i in range(5):
            for j in range(5):
                if random.random() < 0.2:
                    maze[i][j] = 1  # 1 represents a block
        return maze

    # Function to add a player to the game
    def add_player(self, player_id, role):
        self.players[player_id] = role

    # Function to update the game state
    def update_state(self, player_id, action):
        # Update the actions dictionary
        self.actions[player_id] = action

        # Update the maze based on the action
        if action == "move_up":
            if self.maze[player_id[0] - 1][player_id[1]] == 0:
                self.maze[player_id[0] - 1][player_id[1]] = 1
                self.maze[player_id[0]][player_id[1]] = 0
        elif action == "move_down":
            if self.maze[player_id[0] + 1][player_id[1]] == 0:
                self.maze[player_id[0] + 1][player_id[1]] = 1
                self.maze[player_id[0]][player_id[1]] = 0
        elif action == "move_left":
            if self.maze[player_id[0]][player_id[1] - 1] == 0:
                self.maze[player_id[0]][player_id[1] - 1] = 1
                self.maze[player_id[0]][player_id[1]] = 0
        elif action == "move_right":
            if self.maze[player_id[0]][player_id[1] + 1] == 0:
                self.maze[player_id[0]][player_id[1] + 1] = 1
                self.maze[player_id[0]][player_id[1]] = 0

        # Update the paths dictionary
        self.paths[player_id] = self.get_path(player_id)

    # Function to get the path for a player
    def get_path(self, player_id):
        path = []
        for i in range(5):
            for j in range(5):
                if self.maze[i][j] == 1:
                    path.append((i, j))
        return path

    # Function to check if the game is won
    def is_won(self):
        # For simplicity, we'll check if all blocks are removed
        for i in range(5):
            for j in range(5):
                if self.maze[i][j] == 1:
                    return False
        return True

    # Function to update the score
    def update_score(self):
        self.score += 10
        if self.is_won():
            self.score += 100
            self.level += 1

    # Function to display the game state
    def display_state(self):
        print("Maze:")
        for i in range(5):
            for j in range(5):
                print(self.maze[i][j], end=" ")
            print()
        print("Paths:")
        for player_id in self.paths:
            print(f"Player {player_id}: {self.paths[player_id]}")
        print("Actions:")
        for player_id in self.actions:
            print(f"Player {player_id}: {self.actions[player_id]}")
        print("Score:", self.score)
        print("Level:", self.level)

# Function to simulate player actions
def simulate_player_actions(maze, player_id, role):
    while True:
        action = input(f"Player {player_id} ({role}): ")
        maze.update_state(player_id, action)

# Function to start the game
def start_game():
    maze = MultiAgentMaze()
    maze.add_player("1", "pathfinder")
    maze.add_player("2", "blocker")
    maze.add_player("3", "swapper")

    # Create threads for each player
    threads = []
    for player_id in maze.players:
        thread = threading.Thread(target=simulate_player_actions, args=(maze, player_id, maze.players[player_id]))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Display the final game state
    maze.display_state()

# Start the game
start_game()