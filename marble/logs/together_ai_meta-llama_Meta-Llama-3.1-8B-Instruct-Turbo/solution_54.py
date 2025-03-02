# chain_reaction.py
# Main implementation of the Chain Reaction game

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
        activation_requirement (int): The number of adjacent nodes that must be activated first.
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
        self.is_turn = False

class ChainReaction:
    """Represents the Chain Reaction game environment."""
    
    def __init__(self, grid_size, num_players):
        """
        Initializes a ChainReaction object.
        
        Args:
        grid_size (int): The size of the grid.
        num_players (int): The number of players in the game.
        """
        self.grid_size = grid_size
        self.num_players = num_players
        self.nodes = self.generate_nodes()
        self.players = self.assign_players()
        self.timer = time.time()
        self.save_file = "save.dat"

    def generate_nodes(self):
        """
        Generates a list of Node objects representing the grid.
        
        Returns:
        list: A list of Node objects.
        """
        nodes = []
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                activation_requirement = random.randint(1, 3)
                nodes.append(Node(x, y, activation_requirement))
        return nodes

    def assign_players(self):
        """
        Assigns a specific area of the grid to each player.
        
        Returns:
        list: A list of Player objects.
        """
        players = []
        for i in range(self.num_players):
            area = [node for node in self.nodes if node.x % (self.num_players - i) == 0]
            players.append(Player(f"Player {i+1}", area))
        return players

    def activate_node(self, node):
        """
        Activates a node if its activation requirement is met.
        
        Args:
        node (Node): The node to be activated.
        """
        adjacent_nodes = [n for n in self.nodes if abs(n.x - node.x) + abs(n.y - node.y) == 1]
        if len([n for n in adjacent_nodes if n.is_activated]) >= node.activation_requirement:
            node.is_activated = True

    def check_win(self):
        """
        Checks if the game is won.
        
        Returns:
        bool: True if the game is won, False otherwise.
        """
        return all(node.is_activated for node in self.nodes)

    def play(self):
        """
        Starts the game.
        """
        print("Welcome to Chain Reaction!")
        while True:
            for player in self.players:
                if player.is_turn:
                    print(f"\n{player.name}'s turn:")
                    for node in player.area:
                        if not node.is_activated:
                            print(f"{node.x}, {node.y} - Activation requirement: {node.activation_requirement}")
                            choice = input("Enter the node to activate (or 'q' to quit): ")
                            if choice.lower() == 'q':
                                break
                            try:
                                x, y = map(int, choice.split(','))
                                node = next(n for n in self.nodes if n.x == x and n.y == y)
                                self.activate_node(node)
                                if self.check_win():
                                    print("Congratulations, you won!")
                                    return
                            except ValueError:
                                print("Invalid input. Please enter the node coordinates (e.g., 1, 2).")
                    player.is_turn = False
                    for p in self.players:
                        if not p.is_turn:
                            p.is_turn = True
                            break
                time.sleep(1)
            self.timer = time.time() - self.timer
            print(f"\nTime taken: {self.timer:.2f} seconds")
            save = input("Save progress? (y/n): ")
            if save.lower() == 'y':
                with open(self.save_file, 'wb') as f:
                    pickle.dump(self, f)
                print("Progress saved.")
            play_again = input("Play again? (y/n): ")
            if play_again.lower() == 'y':
                self.__init__(self.grid_size, self.num_players)
            else:
                break

def load_game():
    """
    Loads a saved game.
    
    Returns:
    ChainReaction: The loaded game object.
    """
    if os.path.exists("save.dat"):
        with open("save.dat", 'rb') as f:
            game = pickle.load(f)
            return game
    else:
        return None

def main():
    grid_size = int(input("Enter the grid size: "))
    num_players = int(input("Enter the number of players: "))
    game = ChainReaction(grid_size, num_players)
    if load_game():
        print("Loading saved game...")
        game = load_game()
    else:
        print("Starting new game...")
    game.play()

if __name__ == "__main__":
    main()