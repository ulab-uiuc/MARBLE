# team_treasure_hunt.py

import random
import time

# Define a class for the game environment
class Environment:
    def __init__(self, name, difficulty):
        self.name = name
        self.difficulty = difficulty
        self.puzzle = None

    def set_puzzle(self, puzzle):
        self.puzzle = puzzle

# Define a class for puzzles
class Puzzle:
    def __init__(self, description, solution):
    def __init__(self, description, solution, solution_ability):
        self.description = description
        self.solution = solution
        self.solution_ability = solution_ability

    def solve(self, answer):
        return answer == self.solution

# Define a class for character abilities
class Ability:
    def __init__(self, name, description):
        self.name = name
        self.description = description

# Define a class for characters
class Character:
    def __init__(self, name, ability):
        self.name = name
        self.ability = ability

# Define a class for the game
class Game:def start_game(self):
    self.time_taken = time.time()
    for environment in self.environments:
        print(f"Environment: {environment.name}")
        print(f"Difficulty: {environment.difficulty}")
        if environment.puzzle:
            print(f"Puzzle: {environment.puzzle.description}")
            for team in self.teams:
                # Check if a character in the team has an ability that matches the puzzle's requirements
                for character in team.members:
                    if character.ability.name == environment.puzzle.solution_ability:
                        print(f"{character.name} has the ability to solve this puzzle!")
                        # Solve the puzzle automatically or with a higher chance of success
                        if random.random() < 0.9:  # 90% chance of success
                            print("Correct answer! You found a treasure.")
                            team.score += 1
                        else:
                            print("Incorrect answer. You lost a treasure.")
                            team.score -= 1
                        break
                else:
                    # If no character has the required ability, ask the player for input
                    answer = input("Enter your answer: ")
                    if environment.puzzle.solve(answer):
                        print("Correct answer! You found a treasure.")
                        team.score += 1
                    else:
                        print("Incorrect answer. You lost a treasure.")
                        team.score -= 1
        print()
    self.time_taken = time.time() - self.time_taken
    print(f"Game over. Team scores:")
    for team in self.teams:
        print(f"{team.name}: {team.score}")self.time_taken = time.time()
        for environment in self.environments:
            print(f"Environment: {environment.name}")
            print(f"Difficulty: {environment.difficulty}")
            if environment.puzzle:
                print(f"Puzzle: {environment.puzzle.description}")
                # Check if a character in the team has an ability that matches the puzzle's requirements
                for team in self.teams:
                    for character in team.members:
                        if character.ability.name == environment.puzzle.solution_ability:
                            print(f"{character.name} has the ability to solve this puzzle!")
                            # Solve the puzzle automatically or with a higher chance of success
                            if random.random() < 0.9:  # 90% chance of success
                                print("Correct answer! You found a treasure.")
                                self.treasures += 1
                            else:
                                print("Incorrect answer. You lost a treasure.")
                                self.treasures -= 1
                            break
                    else:
                        # If no character has the required ability, ask the player for input
                        answer = input("Enter your answer: ")
                        if environment.puzzle.solve(answer):
                            print("Correct answer! You found a treasure.")
                            self.treasures += 1
                        else:
                            print("Incorrect answer. You lost a treasure.")
                            self.treasures -= 1
                        break
            print()
        self.time_taken = time.time() - self.time_taken
        print(f"Game over. You found {self.treasures} treasures in {self.time_taken} seconds.")        self.time_taken = time.time()
        for environment in self.environments:
            print(f"Environment: {environment.name}")
            print(f"Difficulty: {environment.difficulty}")
            if environment.puzzle:
                print(f"Puzzle: {environment.puzzle.description}")
                answer = input("Enter your answer: ")
                if environment.puzzle.solve(answer):
                    print("Correct answer! You found a treasure.")
                    self.treasures += 1
                else:
                    print("Incorrect answer. You lost a treasure.")
                    self.treasures -= 1
            print()
        self.time_taken = time.time() - self.time_taken
        print(f"Game over. You found {self.treasures} treasures in {self.time_taken} seconds.")

# Define a class for teams
class Team:
    def __init__(self, name):
        self.name = name
self.score = 0
        self.members = []

    def add_member(self, member):
        self.members.append(member)

# Create environments
forest = Environment("Forest", "Easy")
cave = Environment("Cave", "Medium")
ruins = Environment("Ancient Ruins", "Hard")

# Create puzzles
forest_puzzle = Puzzle("What is the capital of France?", "Paris")
cave_puzzle = Puzzle("What is the largest planet in our solar system?", "Jupiter")
forest_puzzle = Puzzle("What is the capital of France?", "Paris", "Intelligence")
ruins_puzzle = Puzzle("What is the smallest country in the world?", "Vatican City")
cave_puzzle = Puzzle("What is the largest planet in our solar system?", "Jupiter", "Intelligence")

# Set puzzles for environments
ruins_puzzle = Puzzle("What is the smallest country in the world?", "Vatican City", "Intelligence")
forest.set_puzzle(forest_puzzle)
cave.set_puzzle(cave_puzzle)
ruins.set_puzzle(ruins_puzzle)

# Create characters
character1 = Character("John", Ability("Strength", "Can move heavy objects"))
character2 = Character("Alice", Ability("Agility", "Can navigate tight spaces"))
character3 = Character("Bob", Ability("Intelligence", "Can solve complex puzzles"))
character4 = Character("Charlie", Ability("Stealth", "Can avoid traps"))

# Create teams
team1 = Team("Team 1")
team1.add_member(character1)
team1.add_member(character2)

team2 = Team("Team 2")
team2.add_member(character3)
team2.add_member(character4)

# Create game
game = Game()
game.add_environment(forest)
game.add_environment(cave)
game.add_environment(ruins)
game.add_character(character1)
game.add_character(character2)
game.add_character(character3)
game.add_character(character4)
game.add_team(team1)
game.add_team(team2)

# Start game
game.start_game()