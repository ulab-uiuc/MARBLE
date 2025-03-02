# solution.py

import random
import time
import json

class Node:
    """Represents a single node in the grid."""
    def __init__(self, x, y):
        self.x = x  # x-coordinate of the node
        self.y = y  # y-coordinate of the node
        self.active = False  # Activation state of the node
        self.activation_requirement = random.randint(1, 4)  # Number of adjacent nodes required to activate

    def activate(self):
        """Activates the node if the activation requirement is met."""
        if self.active:
            return False  # Node is already active
        self.active = True  # Activate the node
        return True

class Grid:
    """Represents the game grid containing nodes."""
    def __init__(self, width, height):
        self.width = width  # Width of the grid
        self.height = height  # Height of the grid
        self.nodes = [[Node(x, y) for y in range(height)] for x in range(width)]  # Create a grid of nodes

    def get_adjacent_nodes(self, node):
        """Returns a list of adjacent nodes for a given node."""
        adjacent = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue  # Skip the node itself
                x, y = node.x + dx, node.y + dy
                if 0 <= x < self.width and 0 <= y < self.height:
                    adjacent.append(self.nodes[x][y])
        return adjacent

    def activate_node(self, x, y):
        """Activates a node at the specified coordinates if requirements are met."""
        node = self.nodes[x][y]
        adjacent_nodes = self.get_adjacent_nodes(node)
        active_count = sum(1 for n in adjacent_nodes if n.active)

        if active_count >= node.activation_requirement:
            return node.activate()
        return False

class Player:
    """Represents a player in the game."""
    def __init__(self, name, grid, area):
        self.name = name  # Player's name
        self.grid = grid  # Reference to the game grid
        self.area = area  # Area of the grid the player is responsible for

    def activate_nodes(self):
        """Activates nodes in the player's area."""
        for x in range(self.area[0], self.area[1]):
            for y in range(self.area[2], self.area[3]):
                self.grid.activate_node(x, y)

class Game:
    """Main game class to manage the game state."""
    def __init__(self, width, height):
        self.grid = Grid(width, height)  # Initialize the game grid
        self.players = []  # List of players
        self.start_time = None  # Timer start time
        self.level = 1  # Current level
        self.progress = {}  # Save progress

    def add_player(self, player):
        """Adds a player to the game."""
        self.players.append(player)

    def start_timer(self):
        """Starts the timer for the game."""
        self.start_time = time.time()

    def stop_timer(self):
        """Stops the timer and returns the elapsed time."""
        return time.time() - self.start_time

    def save_progress(self, filename):
        """Saves the current game progress to a file."""
        self.progress = {
            'level': self.level,
            'grid': [[node.active for node in row] for row in self.grid.nodes],
            'time': self.stop_timer()
        }
        with open(filename, 'w') as f:
            json.dump(self.progress, f)

    def load_progress(self, filename):
        """Loads game progress from a file."""
        with open(filename, 'r') as f:
            self.progress = json.load(f)
            self.level = self.progress['level']
            for x in range(len(self.grid.nodes)):
                for y in range(len(self.grid.nodes[0])):
                    self.grid.nodes[x][y].active = self.progress['grid'][x][y]

    def hint_system(self):
        """Provides hints to players if they are stuck."""
        # Simple hint: Suggest activating a random inactive node
        inactive_nodes = [(node.x, node.y) for row in self.grid.nodes for node in row if not node.active]
        if inactive_nodes:
            return random.choice(inactive_nodes)
        return None

# Example of how to set up the game
if __name__ == "__main__":
    game = Game(5, 5)  # Create a 5x5 grid
    player1 = Player("Player A", game.grid, (0, 3, 0, 5))  # Player A's area
    player2 = Player("Player B", game.grid, (3, 5, 0, 5))  # Player B's area
    game.add_player(player1)
    game.add_player(player2)

    game.start_timer()  # Start the timer
    player1.activate_nodes()  # Player A activates their nodes
    player2.activate_nodes()  # Player B activates their nodes
    elapsed_time = game.stop_timer()  # Stop the timer

    print(f"Game completed in {elapsed_time:.2f} seconds.")
    game.save_progress("game_progress.json")  # Save progress