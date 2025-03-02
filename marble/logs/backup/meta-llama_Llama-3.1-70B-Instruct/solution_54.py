
# node.py

class Node:
    # ...
    def can_activate(self, grid):
        if self.activation_requirement == 0:
            return True
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                if grid[nx][ny].activated and grid[nx][ny].activation_requirement < self.activation_requirement:
                    return False
        return True# solution.py

import random
import time
import json
import os

# game_constants.py
class GameConstants:
    GRID_SIZE = 10
    MAX_LEVEL = 5
    TIMER = 60  # in seconds

# node.py
class Node:
    def __init__(self, x, y, activation_requirement):
        """
        Initialize a node with its position and activation requirement.

        Args:
            x (int): The x-coordinate of the node.
            y (int): The y-coordinate of the node.
            activation_requirement (int): The number of adjacent nodes that must be activated first.
        """
        self.x = x
        self.y = y
        self.activation_requirement = activation_requirement
        self.activated = False

    def activate(self):if self.activation_requirement == 0 or (self.activation_requirement > 0 and self.count_activated_adjacent_nodes(grid) >= self.activation_requirement):self.activated = True
            return True
        return False

    def count_activated_adjacent_nodes(self, grid):
        """
        Count the number of activated adjacent nodes.

        Args:
            grid (list): The game grid.

        Returns:
            int: The number of activated adjacent nodes.
        """
        count = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                if grid[nx][ny].activated:
                    count += 1
        return count

# player.py
class Player:
    def __init__(self, name, area):
        """
        Initialize a player with their name and assigned area.

        Args:
            name (str): The player's name.
            area (list): The player's assigned area.
        """
        self.name = name
        self.area = area

    def activate_node(self, node, grid):
        """
        Activate a node in the player's area.

        Args:
            node (Node): The node to activate.
            grid (list): The game grid.

        Returns:
            bool: Whether the node was activated successfully.
        """
        if node in self.area:
            return node.activate()
        return False

# game.py
class Game:
    def __init__(self, level):
        """
        Initialize a game with a level.

        Args:
            level (int): The level number.
        """
        self.level = level
        self.grid = self.generate_grid(level)
        self.players = self.assign_players(level)
        self.timer = GameConstants.TIMER
        self.start_time = time.time()

    def generate_grid(self, level):
        """
        Generate a grid for the given level.

        Args:
            level (int): The level number.

        Returns:
            list: The generated grid.
        """
        grid_size = GameConstants.GRID_SIZE + level * 2
        grid = [[Node(x, y, random.randint(1, 4)) for y in range(grid_size)] for x in range(grid_size)]
        return grid

    def assign_players(self, level):
        """
        Assign players to areas of the grid.

        Args:
            level (int): The level number.

        Returns:
            list: The assigned players.
        """
        num_players = level + 1
        players = []
        area_size = GameConstants.GRID_SIZE // num_players
        for i in range(num_players):
            area = [node for x in range(i * area_size, (i + 1) * area_size) for node in self.grid[x]]
            players.append(Player(f"Player {i+1}", area))
        return players

    def play(self):
        """
        Play the game.
        """
        while True:
            for player in self.players:
                print(f"\n{player.name}'s turn:")
                for node in player.area:
                    print(f"Node ({node.x}, {node.y}) - Activated: {node.activated}")
                node_to_activate = input("Enter the node to activate (x y): ")
                x, y = map(int, node_to_activate.split())
                node = self.grid[x][y]
                if player.activate_node(node, self.grid):
                    print("Node activated successfully!")
                else:
                    print("Node cannot be activated yet.")
            if self.check_win():
                print("Congratulations, you won!")
                break
            self.timer -= 1
            print(f"\nTime remaining: {self.timer} seconds")
            if self.timer <= 0:
                print("Time's up! Game over.")
                break

    def check_win(self):
        """
        Check if the game is won.

        Returns:
            bool: Whether the game is won.
        """
        for row in self.grid:
            for node in row:
                if not node.activated:
                    return False
        return True

    def save_progress(self):
        """
        Save the game progress.
        """
        progress = {
            "level": self.level,
            "grid": [[node.__dict__ for node in row] for row in self.grid],
            "players": [player.__dict__ for player in self.players],
            "timer": self.timer
        }
        with open("progress.json", "w") as f:
            json.dump(progress, f)

    def load_progress(self):
        """
        Load the game progress.
        """
        if os.path.exists("progress.json"):
            with open("progress.json", "r") as f:
                progress = json.load(f)
            self.level = progress["level"]
            self.grid = [[Node(node["x"], node["y"], node["activation_requirement"]) for node in row] for row in progress["grid"]]
            self.players = [Player(player["name"], [Node(node["x"], node["y"], node["activation_requirement"]) for node in player["area"]]) for player in progress["players"]]
            self.timer = progress["timer"]
        else:
            print("No saved progress found.")

    def hint(self):
        """
        Provide a hint to the players.
        """
        for player in self.players:
            for node in player.area:
                if not node.activated and node.activation_requirement == 0:
                    print(f"Hint: Node ({node.x}, {node.y}) can be activated now.")

# main.py
def main():
    game = Game(1)
    while True:
        print("\n1. Play Game")
        print("2. Load Progress")
        print("3. Save Progress")
        print("4. Hint")
        print("5. Quit")
        choice = input("Enter your choice: ")
        if choice == "1":
            game.play()
        elif choice == "2":
            game.load_progress()
        elif choice == "3":
            game.save_progress()
        elif choice == "4":
            game.hint()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()