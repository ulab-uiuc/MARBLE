# solution.py
import time
from enum import Enum
from typing import List, Dictclass Environment:
class Ability(Enum):
    STRENGTH = 1
    AGILITY = 2
    INTELLIGENCE = 3
    STEALTH = 4
    def __init__(self, name: str, difficulty: int, puzzle: str, required_abilities: List[Ability]):
        self.name = name
        self.difficulty = difficulty
        self.puzzle = puzzle
        self.required_abilities = required_abilities        self.name = name
        self.difficulty = difficulty
        self.puzzle = puzzle

# Define a class for teams
class Team:
    def __init__(self, name: str):
        """
        Initialize a team with a name.
        
        Args:
        name (str): The team's name.
        """
        self.name = name
        self.characters: List[Character] = []
        self.treasures: int = 0
        self.time_taken: float = 0.0

    def add_character(self, character: Character):
        """
        Add a character to the team.
        
        Args:
        character (Character): The character to add.
        """
        self.characters.append(character)

# Define a class for the game engine
class GameEngine:
class Character:
    def __init__(self, name: str, ability: Ability):
        self.name = name
        self.ability = abilitydef start_game(self):
def add_team(self, team: Team):
        self.teams.append(team)

    def add_environment(self, environment: Environment):
        self.environments.append(environment)
def __init__(self):
        self.environments: List[Environment] = []
        self.teams: List[Team] = []
        self.current_environment: Environment = None
    if self.environments:
        self.current_environment = self.environments[0]
        print(f"Game started. Current environment: {self.current_environment.name}")
    else:
        print("No environments added to the game.")def solve_puzzle(self, team: Team, puzzle_solution: str):
    # Check if the team has the required abilities to solve the puzzle
    team_abilities = [character.ability for character in team.characters]
    if all(ability in team_abilities for ability in self.current_environment.required_abilities):
        if puzzle_solution == self.current_environment.puzzle:
            print(f"Puzzle solved correctly by team {team.name}!")
            team.treasures += 1
            return True
        else:
            print(f"Puzzle solved incorrectly by team {team.name}.")
            return False
    else:
        print(f"Team {team.name} does not have the required abilities to solve the puzzle.")
        return False    if puzzle_solution == self.current_environment.puzzle:
            print(f"Puzzle solved correctly by team {team.name}!")
            team.treasures += 1
            return True
        else:
            print(f"Puzzle solved incorrectly by team {team.name}.")
            return False

    def move_to_next_environment(self):
        """
        Move to the next environment in the game.
        """
        current_index = self.environments.index(self.current_environment)
        if current_index < len(self.environments) - 1:
            self.current_environment = self.environments[current_index + 1]
            print(f"Moved to next environment: {self.current_environment.name}")
        else:
            print("Game over. Final scores:")
            for team in self.teams:
                print(f"Team {team.name}: {team.treasures} treasures, {team.time_taken} seconds")

    def calculate_score(self, team: Team):
        """
        Calculate the score for a team.
        
        Args:
        team (Team): The team to calculate the score for.
        
        Returns:
        int: The team's score.
        """
        return team.treasures * 10 - int(team.time_taken)

# Define a function to test the game
def test_game():
    game_engine = GameEngine()

    # Create teams
    team1 = Team("Team 1")
    team2 = Team("Team 2")

    # Create characters
    character1 = Character("Character 1", Ability.STRENGTH)
    character2 = Character("Character 2", Ability.AGILITY)
    character3 = Character("Character 3", Ability.INTELLIGENCE)
    character4 = Character("Character 4", Ability.STEALTH)

    # Add characters to teams
    team1.add_character(character1)
    team1.add_character(character2)
    team2.add_character(character3)
    team2.add_character(character4)

    # Add teams to game engine
    game_engine.add_team(team1)
    game_engine.add_team(team2)environment1 = Environment("Forest", 1, "puzzle1", [Ability.STRENGTH, Ability.AGILITY])
environment2 = Environment("Cave", 2, "puzzle2", [Ability.INTELLIGENCE, Ability.STEALTH])
environment3 = Environment("Ancient Ruins", 3, "puzzle3", [Ability.STRENGTH, Ability.INTELLIGENCE])game_engine.add_environment(environment1)
    game_engine.add_environment(environment2)
    game_engine.add_environment(environment3)

    # Start game
    game_engine.start_game()

    # Solve puzzles
    start_time = time.time()
    game_engine.solve_puzzle(team1, "puzzle1")
    game_engine.solve_puzzle(team2, "puzzle2")
    end_time = time.time()
    team1.time_taken = end_time - start_time
    team2.time_taken = end_time - start_time

    # Move to next environment
    game_engine.move_to_next_environment()

    # Calculate scores
    team1_score = game_engine.calculate_score(team1)
    team2_score = game_engine.calculate_score(team2)

    print(f"Team 1 score: {team1_score}")
    print(f"Team 2 score: {team2_score}")

# Run the test
test_game()