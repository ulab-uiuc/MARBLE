# solution.py

import random
import time
import json

class Node:
    """Class representing a single node in the grid."""
    def __init__(self, x, y):
        self.x = x  # x-coordinate of the node
        self.y = y  # y-coordinate of the node
        self.active = False  # Activation state of the node
        self.activation_requirement = random.randint(1, 4)  # Number of adjacent nodes required to activate

    def activate(self):
        """Activate the node if the activation requirement is met."""
        if self.active:
            return False  # Node is already active
        self.active = True  # Activate the node
        return True

class Grid:
    """Class representing the game grid."""
    def __init__(self, size):
        self.size = size  # Size of the grid
        self.nodes = [[Node(x, y) for y in range(size)] for x in range(size)]  # Create a grid of nodes

    def activate_node(self, x, y):
        """Activate a node at the specified coordinates."""
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.nodes[x][y].activate()
        return False

    def get_adjacent_nodes(self, x, y):
        """Get a list of adjacent nodes for a given node."""
        adjacent = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if (dx != 0 or dy != 0) and 0 <= x + dx < self.size and 0 <= y + dy < self.size:
                    adjacent.append(self.nodes[x + dx][y + dy])
        return adjacent

class Player:
    """Class representing a player in the game."""
    def __init__(self, name, grid, area):
        self.name = name  # Player's name
        self.grid = grid  # Reference to the game grid
        self.area = area  # Area assigned to the playerdef activate_nodes(self):
        """Activate nodes in the player's area based on the player's turn."""
        for x in range(self.area[0], self.area[2]):
            for y in range(self.area[1], self.area[3]):
                node = self.grid.nodes[x][y]
                if not node.active:
                    # Check if the activation requirement is met
                    adjacent_active_count = sum(1 for adj in self.grid.get_adjacent_nodes(x, y) if adj.active)
                    if adjacent_active_count >= node.activation_requirement:
                        node.activate()class Game:
    """Class representing the game logic."""
    def __init__(self, size, players):
        self.grid = Grid(size)  # Initialize the game grid
        self.players = players  # List of players
        self.level = 1  # Current level
        self.start_time = None  # Timer start time
        self.progress = {}  # Save progress

    def start_timer(self):
        """Start the timer for the game."""
        self.start_time = time.time()

    def stop_timer(self):
        """Stop the timer and return the elapsed time."""
        return time.time() - self.start_time

    def save_progress(self):
        """Save the current game progress to a file."""
        with open('progress.json', 'w') as f:
            json.dump(self.progress, f)

    def load_progress(self):
        """Load game progress from a file."""
        try:
            with open('progress.json', 'r') as f:
                self.progress = json.load(f)
        except FileNotFoundError:
            self.progress = {}

    def play_level(self):
        """Play the current level of the game."""
        self.start_timer()for player in self.players:
            player.activate_nodes()  # Each player activates their nodes
            if player.name == self.players[-1].name:
                break  # End of turn for the last player        elapsed_time = self.stop_timer()
        print(f"Level {self.level} completed in {elapsed_time:.2f} seconds.")

# Example usage
if __name__ == "__main__":
    # Define players and their areas
    player1 = Player("Player A", None, (0, 0, 5, 5))  # Player A controls the top-left area
    player2 = Player("Player B", None, (5, 5, 10, 10))  # Player B controls the bottom-right area

    # Create a game instance
    game = Game(size=10, players=[player1, player2])
    player1.grid = game.grid  # Assign the grid to players
    player2.grid = game.grid

    # Load progress if available
    game.load_progress()

    # Play the level
    game.play_level()

    # Save progress after playing
    game.save_progress()