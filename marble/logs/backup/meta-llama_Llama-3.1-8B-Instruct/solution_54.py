# solution.py

import random
import time
import pickle
import os

class Node:
    """Represents a node in the grid with its activation requirements."""
    
    def __init__(self, x, y, activation_requirement):
        """
        Initializes a Node object.

        Args:
            x (int): The x-coordinate of the node.
            y (int): The y-coordinate of the node.
            activation_requirement (int): The number of adjacent nodes that must be activated before this node.
        """
        self.x = x
        self.y = y
        self.activation_requirement = activation_requirement
        self.is_activated = False

class Player:
    """Represents a player in the game with their assigned area of the grid."""
    
    def __init__(self, name, area):
        """
        Initializes a Player object.

        Args:
            name (str): The name of the player.
            area (list): A list of Node objects representing the player's assigned area of the grid.
        """
        self.name = name
        self.area = area

class Game:
    """Represents the Chain Reaction game with its grid, players, and level generation system."""
    
    def __init__(self):
        """
        Initializes a Game object.
        """
        self.grid_size = 10
        self.grid = self.generate_grid()
        self.players = self.assign_players()
        self.level = 1
        self.timer = 0
        self.save_file = "save.dat"

    def generate_grid(self):
        """
        Generates a grid of nodes with random activation requirements.

        Returns:
            list: A 2D list of Node objects representing the grid.
        """
        grid = [[Node(x, y, random.randint(1, 3)) for y in range(self.grid_size)] for x in range(self.grid_size)]
        return grid

    def assign_players(self):
        """
        Assigns players to specific areas of the grid.

        Returns:
            list: A list of Player objects representing the players and their assigned areas.
        """
        players = []
        for i in range(3):
            area = [self.grid[x][y] for x in range(self.grid_size // 3 * i, self.grid_size // 3 * (i + 1)) for y in range(self.grid_size)]
            players.append(Player(f"Player {i + 1}", area))
        return players

    def activate_node(self, node):
        """
        Activates a node if its activation requirement is met.

        Args:
            node (Node): The node to be activated.

        Returns:
            bool: True if the node is activated, False otherwise.
        """
        adjacent_nodes = self.get_adjacent_nodes(node)
        if len(adjacent_nodes) >= node.activation_requirement:
            node.is_activated = True
            return True
        return False

    def get_adjacent_nodes(self, node):
        """
        Gets the adjacent nodes of a given node.

        Args:
            node (Node): The node to get adjacent nodes for.

        Returns:
            list: A list of Node objects representing the adjacent nodes.
        """
        adjacent_nodes = []
        for x in range(max(0, node.x - 1), min(self.grid_size, node.x + 2)):
            for y in range(max(0, node.y - 1), min(self.grid_size, node.y + 2)):
                if (x, y) != (node.x, node.y):
                    adjacent_nodes.append(self.grid[x][y])
        return adjacent_nodes

    def check_win(self):
        """
        Checks if the game is won by checking if all nodes are activated.

        Returns:
            bool: True if the game is won, False otherwise.
        """
        for row in self.grid:
            for node in row:
                if not node.is_activated:
                    return False
        return True

    def play(self):
        """
        Plays the game by iterating through each level and allowing players to activate nodes.
        """
        while True:
            print(f"Level {self.level}")
            self.timer = time.time()
            for player in self.players:
                print(f"{player.name}'s turn:")
                for node in player.area:
                    if not node.is_activated:
                        if self.activate_node(node):
                            print(f"Activated node at ({node.x}, {node.y})")
                        else:
                            print(f"Cannot activate node at ({node.x}, {node.y})")
                if self.check_win():
                    print("Game won!")
                    self.save_progress()
                    break
            self.level += 1
            self.timer = time.time() - self.timer
            print(f"Time taken: {self.timer} seconds")
            self.save_progress()

    def save_progress(self):
        """
        Saves the current game progress to a file.
        """
        with open(self.save_file, "wb") as f:
            pickle.dump((self.level, self.timer, self.grid, self.players), f)

    def load_progress(self):
        """
        Loads the saved game progress from a file.
        """
        if os.path.exists(self.save_file):
            with open(self.save_file, "rb") as f:
                self.level, self.timer, self.grid, self.players = pickle.load(f)
        else:
            print("No saved progress found.")

def main():
    game = Game()
    game.load_progress()
    game.play()

if __name__ == "__main__":
    main()