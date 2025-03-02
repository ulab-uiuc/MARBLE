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
            health (int): The initial health of the robot. Defaults to 100.
            damage (int): The initial damage of the robot. Defaults to 10.
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
        else:
            print(f"{self.name} is dead and cannot attack.")

    def use_power_up(self, power_up):
        """Uses a power-up."""
        if power_up == "health":
            self.health += 20
            print(f"{self.name} uses health power-up and gains 20 health.")
        elif power_up == "damage":
            self.damage += 10
            print(f"{self.name} uses damage power-up and gains 10 damage.")

    def learn_from_battle(self):
        """Learns from a previous battle."""
        self.score += 1
        print(f"{self.name} learns from battle and gains 1 score.")


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

    def is_alive(self):
        """Checks if the team is alive."""
        return any(robot.is_alive() for robot in self.robots)

    def capture_flag(self):
        """Captures a flag."""
        if self.is_alive():
            self.score += 10
            print(f"{self.name} captures flag and gains 10 score.")
        else:
            print(f"{self.name} is dead and cannot capture flag.")

    def defend_base(self):
        """Defends a base."""
        if self.is_alive():
            self.score += 5
            print(f"{self.name} defends base and gains 5 score.")
        else:
            print(f"{self.name} is dead and cannot defend base.")

    def escort_payload(self):
        """Escorts a payload."""
        if self.is_alive():
            self.score += 15
            print(f"{self.name} escorts payload and gains 15 score.")
        else:
            print(f"{self.name} is dead and cannot escort payload.")


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

    def simulate_battle(self):for team1 in self.teams:for team2 in self.teams:if team1 != team2 and team1.is_alive() and team2.is_alive():for robot1 in team1.robots:for robot2 in team2.robots:if robot1.is_alive() and robot2.is_alive():robot1.attack(robot2)if not robot2.is_alive():team2.robots.remove(robot2)if random.random() < 0.2:robot1.use_power_up(random.choice(self.power_ups))if random.random() < 0.1:print(f"{robot1.name} triggers {random.choice(self.environmental_hazards)}")for team in self.teams:if team.is_alive() and team.robots:if random.random() < 0.3:team.capture_flag()elif random.random() < 0.2:team.defend_base()elif random.random() < 0.1:team.escort_payload()for team in self.teams:for robot in team.robots:if robot.is_alive():robot.learn_from_battle()for team in self.teams:print(f"{team.name} score: {team.score}")for robot in team.robots:print(f"{robot.name} score: {robot.score}")for team in self.teams:if team.robots:for robot in team.robots[:]:for team in self.teams:if team.robots and team.is_alive():if random.random() < 0.3:
                    team.capture_flag()
                elif random.random() < 0.2:
                    team.defend_base()
                elif random.random() < 0.1:
                    team.escort_payload()
        for team in self.teams:
            for robot in team.robots:
                if robot.is_alive():
                    robot.learn_from_battle()for team in self.teams:
            if team.is_alive() and team.robots:
                if random.random() < 0.3:
                    team.capture_flag()
                elif random.random() < 0.2:
                    team.defend_base()
                elif random.random() < 0.1:
                    team.escort_payload()for team in self.teams:
            print(f"{team.name} score: {team.score}")
            for robot in team.robots:
                print(f"{robot.name} score: {robot.score}")


# Create robots
robot1 = Robot("Robot 1", "Team A")
robot2 = Robot("Robot 2", "Team A")
robot3 = Robot("Robot 3", "Team B")
robot4 = Robot("Robot 4", "Team B")

# Create teams
team_a = Team("Team A")
team_b = Team("Team B")

# Add robots to teams
team_a.add_robot(robot1)
team_a.add_robot(robot2)
team_b.add_robot(robot3)
team_b.add_robot(robot4)

# Create CyberArena
cyber_arena = CyberArena()

# Add teams to CyberArena
cyber_arena.add_team(team_a)
cyber_arena.add_team(team_b)

# Simulate battles
for i in range(10):
    print(f"Battle {i+1}:")
    cyber_arena.simulate_battle()
    time.sleep(1)

# Display scores
cyber_arena.display_scores()