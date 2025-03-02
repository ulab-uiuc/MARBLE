# solution.py
import random
import time
import json
import os

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
        # Generate a level with more nodes and complex dependency patterns
        level = []
        for x in range(self.width):
            for y in range(self.height):
                node = self.grid[x][y]
                node.requirement = random.randint(1, level_num + 1)
                level.append(node)
        self.levels.append(level)

    def assign_areas(self):
        """Assigns areas of the grid to each player."""
        # Assign areas of the grid to each player
        area_size = (self.width * self.height) // self.num_players
        for i, player in enumerate(self.players):
            player.area = [(x, y) for x in range(self.width) for y in range(self.height) if (x * self.height + y) // area_size == i]

    def start_game(self):
        """Starts the game and begins the timer."""
        # Start the game and begin the timer
        self.timer = time.time()
        for i in range(1, 11):  # Generate 10 levels
            self.generate_level(i)
        self.assign_areas()

    def activate_node(self, player, x, y):
        """Activates a node in the grid if the player has the required adjacent nodes."""
        # Activate a node in the grid if the player has the required adjacent nodes
        node = self.grid[x][y]
        if node.activated:
            return False
        adjacent_nodes = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]adjacent_nodes = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
activated_adjacent = sum(1 for ax, ay in adjacent_nodes if 0 <= ax < self.width and 0 <= ay < self.height and self.grid[ax][ay].activated)
if (x, y) in player.area and activated_adjacent >= node.requirement:
    node.activated = True
    return Truereturn False

    def check_win(self):
        """Checks if all nodes in the grid are activated."""
        # Check if all nodes in the grid are activated
        return all(node.activated for row in self.grid for node in row)

    def save_progress(self):
        """Saves the current progress of the game."""
        # Save the current progress of the game
        self.progress = {(x, y): node.activated for x in range(self.width) for y in range(self.height) for node in [self.grid[x][y]]}
        with open("progress.json", "w") as f:
            json.dump(self.progress, f)

    def load_progress(self):
        """Loads the saved progress of the game."""
        # Load the saved progress of the game
        if os.path.exists("progress.json"):
            with open("progress.json", "r") as f:
                self.progress = json.load(f)
            for x in range(self.width):
                for y in range(self.height):
                    self.grid[x][y].activated = self.progress.get((x, y), False)

    def hint(self):
        """Provides a hint to the players by suggesting a node to activate."""
        # Provide a hint to the players by suggesting a node to activate
        for x in range(self.width):
            for y in range(self.height):
                node = self.grid[x][y]
                if not node.activated:
                    adjacent_nodes = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
                    activated_adjacent = sum(1 for ax, ay in adjacent_nodes if 0 <= ax < self.width and 0 <= ay < self.height and self.grid[ax][ay].activated)
                    if activated_adjacent == node.requirement - 1:
                        return (x, y)
        return None

def main():
    game = Game(10, 10, 2)
    game.start_game()
    while True:
        print("1. Activate node")
        print("2. Check win")
        print("3. Save progress")
        print("4. Load progress")
        print("5. Hint")
        print("6. Quit")
        choice = input("Choose an option: ")
        if choice == "1":
            player_num = int(input("Enter player number: ")) - 1
            x = int(input("Enter x coordinate: "))
            y = int(input("Enter y coordinate: "))
            if game.activate_node(game.players[player_num], x, y):
                print("Node activated successfully!")
            else:
                print("Cannot activate node!")
        elif choice == "2":
            if game.check_win():
                print("Congratulations, you won!")
                break
            else:
                print("Not all nodes are activated yet!")
        elif choice == "3":
            game.save_progress()
            print("Progress saved!")
        elif choice == "4":
            game.load_progress()
            print("Progress loaded!")
        elif choice == "5":
            hint = game.hint()
            if hint:
                print(f"Hint: Activate node at ({hint[0]}, {hint[1]})")
            else:
                print("No hint available!")
        elif choice == "6":
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()