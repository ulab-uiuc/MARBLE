# solution.py
import random
import time
import copy

class Node:
    """Represents a node in the grid with its activation requirement."""
    def __init__(self, x, y, requirement):
        # Initialize the node with its position and activation requirement
        self.x = x
        self.y = y
        self.requirement = requirement
        self.activated = False

class Player:
    """Represents a player with their assigned area of the grid."""
    def __init__(self, name, area):
        # Initialize the player with their name and assigned area
        self.name = name
        self.area = area

class Game:
    """Represents the Chain Reaction game with its grid, players, and levels."""
    def __init__(self, width, height, num_players):
        # Initialize the game with its grid size and number of players
        self.width = width
        self.height = height
        self.num_players = num_players
        self.grid = [[Node(x, y, random.randint(1, 3)) for y in range(height)] for x in range(width)]
        self.players = [Player(f"Player {i+1}", []) for i in range(num_players)]
        self.levels = []
        self.current_level = 0
        self.timer = 0
        self.progress = {}

    def generate_level(self, level_num):
        """Generates a level with increasing difficulty."""
        # Increase the number of nodes and complexity of dependency patterns
        level = {
            "nodes": copy.deepcopy(self.grid),
            "dependencies": []
        }
        for x in range(self.width):
            for y in range(self.height):
                # Randomly assign dependencies between nodes
                if random.random() < 0.5:
                    dependency = (x, y, random.randint(1, 3))
                    level["dependencies"].append(dependency)
        self.levels.append(level)

    def assign_areas(self):
        """Assigns areas of the grid to each player."""
        # Divide the grid into equal areas for each player
        area_size = (self.width * self.height) // self.num_players
        for i, player in enumerate(self.players):
            player.area = [(x, y) for x in range(self.width) for y in range(self.height) if (x * self.height + y) // area_size == i]

    def start_game(self):
        """Starts the game and initializes the timer."""
        # Initialize the timer and start the game
        self.timer = time.time()
        self.assign_areas()
        for i in range(10):  # Generate 10 levels
            self.generate_level(i)

    def activate_node(self, player, x, y):
        """Activates a node in the grid if the player has the required adjacent nodes."""
        # Check if the player has the required adjacent nodes
        node = self.levels[self.current_level]["nodes"][x][y]
        if node.activated:
            return False
        adjacent_nodes = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        activated_adjacent = 0
        for adjacent in adjacent_nodes:
            if 0 <= adjacent[0] < self.width and 0 <= adjacent[1] < self.height:
                if self.levels[self.current_level]["nodes"][adjacent[0]][adjacent[1]].activated:
                    activated_adjacent += 1
        if activated_adjacent >= node.requirement:
            node.activated = True
            return True
        return False

    def check_level_complete(self):
        """Checks if the current level is complete."""
        # Check if all nodes are activated
        for x in range(self.width):
            for y in range(self.height):
                if not self.levels[self.current_level]["nodes"][x][y].activated:
                    return False
        return True

    def save_progress(self):
        """Saves the current progress."""
        # Save the current level and timer
        self.progress[self.current_level] = time.time() - self.timer

    def load_progress(self):
        """Loads the saved progress."""
        # Load the saved level and timer
        if self.current_level in self.progress:
            self.timer = time.time() - self.progress[self.current_level]

    def hint(self):
        """Provides a hint to the players."""
        # Suggest a node to activate
        for x in range(self.width):
            for y in range(self.height):
                node = self.levels[self.current_level]["nodes"][x][y]
                if not node.activated:
                    return (x, y)
        return None

# Example usage
game = Game(5, 5, 2)
game.start_game()
print("Game started. Timer:", game.timer)
player1 = game.players[0]
player2 = game.players[1]
print("Player 1 area:", player1.area)
print("Player 2 area:", player2.area)
game.activate_node(player1, 0, 0)
print("Node (0, 0) activated:", game.levels[0]["nodes"][0][0].activated)
game.save_progress()
print("Progress saved.")
game.load_progress()
print("Progress loaded. Timer:", game.timer)
hint = game.hint()
print("Hint:", hint)