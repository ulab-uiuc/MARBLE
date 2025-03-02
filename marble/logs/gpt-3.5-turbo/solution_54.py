# Chain Reaction Puzzle Game

import random
import time

class Node:
    def __init__(self, activation_requirement):
        self.activated = False
        self.activation_requirement = activation_requirement
        self.adjacent_nodes = []

    def activate(self):
        if not self.activated:
            self.activated = True
            for node in self.adjacent_nodes:
                node.activation_requirement -= 1
                if node.activation_requirement <= 0:
                    node.activate()

class Player:
    def __init__(self, name, grid, start_row, start_col, end_row, end_col):
        self.name = name
        self.grid = grid
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col

    def activate_nodes(self):
        for i in range(self.start_row, self.end_row + 1):
        for i in range(self.start_row, self.end_row + 1):
            for j in range(self.start_col, self.end_col + 1):
                for adj_node in self.grid[i][j].adjacent_nodes:
                    if not adj_node.activated:
                        print(f'Player {self.name} waiting for adjacent node ({i}, {j}) to be activated')
                        return False
        return True


            for j in range(self.start_col, self.end_col + 1):
                self.grid[i][j].activate()

class ChainReactionGame:
    def __init__(self, rows, cols, num_players):
        self.rows = rows
        self.cols = cols
        self.num_players = num_players
        self.grid = [[Node(random.randint(1, 3)) for _ in range(cols)] for _ in range(rows)]
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def print_grid(self):
        for row in self.grid:
            for node in row:
                print("X" if node.activated else "O", end=" ")
            print()

    def check_win(self):
        for row in self.grid:
            for node in row:
                if not node.activated:
                    return False
        return True

    def play(self):
        start_time = time.time()
        while not self.check_win():
            for player in self.players:
                player.activate_nodes()
                self.print_grid()
                time.sleep(1)  # Simulating player actions with a delay
        end_time = time.time()
        print("Congratulations! All nodes activated.")
        print("Time taken:", end_time - start_time, "seconds")

# Create a Chain Reaction game with a 5x5 grid and 2 players
game = ChainReactionGame(5, 5, 2)

# Define player areas
player1 = Player("Player A", game.grid, 0, 0, 2, 4)
player2 = Player("Player B", game.grid, 3, 0, 4, 4)

# Add players to the game
game.add_player(player1)
game.add_player(player2)

# Play the game
game.play()