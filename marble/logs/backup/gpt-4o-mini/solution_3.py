# solution.py

import random
import time

# Constants for the game
MAX_HEALTH = 100
WEAPONS = ['Laser', 'Rocket', 'Melee']
OBJECTIVES = ['Capture Flag', 'Defend Base', 'Escort Payload']
POWER_UPS = ['Speed Boost', 'Shield', 'Health Pack']

class Robot:
    """Class representing a robot in the CyberArena."""
    
    def __init__(self, name, team):
        self.name = name
        self.team = team
        self.health = MAX_HEALTH
        self.weapon = random.choice(WEAPONS)
        self.position = (0, 0)  # Starting position
        self.score = 0

    def attack(self, target):
        """Simulate an attack on another robot."""
        damage = random.randint(10, 30)  # Random damage
        target.health -= damage
        print(f"{self.name} attacks {target.name} with {self.weapon} for {damage} damage!")

    def move(self, new_position):
        """Move the robot to a new position."""
        self.position = new_position
        print(f"{self.name} moves to {self.position}.")

    def is_alive(self):
        """Check if the robot is still alive."""
        return self.health > 0

    def collect_power_up(self, power_up):
        """Collect a power-up and apply its effect."""
        if power_up == 'Speed Boost':
            print(f"{self.name} collects a Speed Boost!")
        elif power_up == 'Shield':
            print(f"{self.name} collects a Shield!")
        elif power_up == 'Health Pack':
            self.health = min(self.health + 20, MAX_HEALTH)
            print(f"{self.name} collects a Health Pack! Health is now {self.health}.")

class Team:
    """Class representing a team of robots."""
    
    def __init__(self, name):
        self.name = name
        self.robots = []

    def add_robot(self, robot):
        """Add a robot to the team."""
        self.robots.append(robot)

    def team_attack(self, target_team):
        """Attack a target team with all robots."""
        for robot in self.robots:
            if robot.is_alive():
                target_robot = random.choice(target_team.robots)
                if target_robot.is_alive():
                    robot.attack(target_robot)

class Game:
    """Class to manage the CyberArena game."""
    
    def __init__(self):
        self.teams = []
        self.rounds = 5  # Number of rounds in the game    def start_game(self):
        """Start the game and manage rounds with objectives."""
        for round_number in range(1, self.rounds + 1):
            print(f"\n--- Round {round_number} ---")
            objective = random.choice(OBJECTIVES)
            print(f"Objective for this round: {objective}")
            for team in self.teams:
                if objective == 'Capture Flag':
                    # Logic for capturing flag
                    print(f"{team.name} is attempting to capture the flag!")
                elif objective == 'Defend Base':
                    # Logic for defending base
                    print(f"{team.name} is defending their base!")
                elif objective == 'Escort Payload':
                    # Logic for escorting payload
                    print(f"{team.name} is escorting the payload!")
                target_team = self.teams[1] if team == self.teams[0] else self.teams[0]
                team.team_attack(target_team)
            time.sleep(1)  # Simulate time between rounds
            self.check_health()            time.sleep(1)  # Simulate time between rounds
            self.check_health()    def check_health(self):
        """Check the health of robots and determine if any team has won."""
        for team in self.teams:
            if all(not robot.is_alive() for robot in team.robots):
                print(f"{team.name} has been defeated!")
                return
        print("All teams are still in the game!")

# Example usage
if __name__ == "__main__":
    # Create teams
    team_a = Team("Team A")
    team_b = Team("Team B")

    # Add robots to teams
    for i in range(3):
        team_a.add_robot(Robot(f"Robot A{i+1}", team_a.name))
        team_b.add_robot(Robot(f"Robot B{i+1}", team_b.name))

    # Create and start the game
    arena = Game()
    arena.add_team(team_a)    arena.start_game()    arena.add_team(team_b)
    arena.start_game()