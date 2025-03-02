# cyber_arena.py

import random
import time

class Robot:
    """Represents a robot in the CyberArena."""
    
    def __init__(self, name, team, health=100, damage=10):
        """
        Initializes a Robot object.

        Args:
            name (str): The name of the robot.
            team (str): The team the robot belongs to.
            health (int, optional): The initial health of the robot. Defaults to 100.
            damage (int, optional): The initial damage of the robot. Defaults to 10.
        """
        self.name = name
        self.team = team
        self.health = health
        self.damage = damage
        self.score = 0

    def is_alive(self):
        """Checks if the robot is alive."""
        return self.health > 0

    def attack(self, other_robot):
        """Attacks another robot."""
        if self.is_alive():
            other_robot.health -= self.damage
            print(f"{self.name} attacks {other_robot.name} for {self.damage} damage.")

    def use_power_up(self, power_up):
        """Uses a power-up."""
        if power_up == "health":
            self.health += 20
            print(f"{self.name} uses health power-up.")
        elif power_up == "damage":
            self.damage += 10
            print(f"{self.name} uses damage power-up.")

    def update_score(self, points):
        """Updates the robot's score."""
        self.score += points


class Team:
    """Represents a team in the CyberArena."""
    
    def __init__(self, name):
        """
        Initializes a Team object.

        Args:
            name (str): The name of the team.
        """
        self.name = name
        self.robots = []
        self.score = 0

    def add_robot(self, robot):
        """Adds a robot to the team."""
        self.robots.append(robot)

    def update_score(self, points):
        """Updates the team's score."""
        self.score += points


class CyberArena:
    """Represents the CyberArena."""
    
    def __init__(self):
        """Initializes the CyberArena."""
        self.teams = []
        self.power_ups = ["health", "damage"]
        self.environmental_hazards = ["laser", "trap"]

    def add_team(self, team):
        """Adds a team to the CyberArena."""
        self.teams.append(team)

    def simulate_battle(self):
        """Simulates a battle between teams."""
        for team in self.teams:
            for robot in team.robots:
                if robot.is_alive():
                    opponent_team = random.choice([t for t in self.teams if t != team])alive_opponent_robots = [r for r in opponent_team.robots if r.is_alive()]
if alive_opponent_robots:
    opponent_robot = random.choice(alive_opponent_robots)robot.attack(opponent_robot)
                    if not opponent_robot.is_alive():
                        team.update_score(10)
                        print(f"{opponent_robot.name} has been defeated. {team.name} earns 10 points.")

    def use_power_up(self, robot):
        """Uses a power-up."""
        power_up = random.choice(self.power_ups)
        robot.use_power_up(power_up)

    def trigger_environmental_hazard(self):
        """Triggers an environmental hazard."""
        hazard = random.choice(self.environmental_hazards)
        if hazard == "laser":
            for team in self.teams:
                for robot in team.robots:
                    if robot.is_alive():
                        robot.health -= 10
                        print(f"{robot.name} is hit by laser beam. -10 health.")
        elif hazard == "trap":
            for team in self.teams:
                for robot in team.robots:
                    if robot.is_alive():
                        robot.health -= 20
                        print(f"{robot.name} is caught in trap. -20 health.")

    def update_scores(self):
        """Updates the scores of all teams."""
        for team in self.teams:
            print(f"{team.name}'s score: {team.score}")
            for robot in team.robots:
                print(f"{robot.name}'s score: {robot.score}")


def main():
    # Create teams and robots
    team1 = Team("Team 1")
    team2 = Team("Team 2")

    robot1 = Robot("Robot 1", "Team 1")
    robot2 = Robot("Robot 2", "Team 1")
    robot3 = Robot("Robot 3", "Team 2")
    robot4 = Robot("Robot 4", "Team 2")

    team1.add_robot(robot1)
    team1.add_robot(robot2)
    team2.add_robot(robot3)
    team2.add_robot(robot4)

    # Create CyberArena
    arena = CyberArena()
    arena.add_team(team1)
    arena.add_team(team2)

    # Simulate battles
    for _ in range(5):
        arena.simulate_battle()
        arena.use_power_up(random.choice([robot1, robot2, robot3, robot4]))
        arena.trigger_environmental_hazard()
        time.sleep(1)

    # Update scores
    arena.update_scores()


if __name__ == "__main__":
    main()