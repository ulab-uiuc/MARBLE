# CyberArena.py

class Robot:
    def __init__(self, name, team):
        self.name = name
        self.team = team
        self.health = 100
        self.weapon = None

    def equip_weapon(self, weapon):
        self.weapon = weapon

    def attack(self, target):
        if self.weapon:
            damage = self.weapon.damage
            print(f"{self.name} attacks {target.name} with {self.weapon.name} causing {damage} damage.")
            target.receive_damage(damage)
        else:
            print(f"{self.name} has no weapon equipped.")

    def receive_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            print(f"{self.name} has been defeated.")
        else:
            print(f"{self.name} has {self.health} health remaining.")


class Weapon:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage


class Team:
    def __init__(self, name):
        self.name = name
        self.members = []self.roles = []
]def add_member(self, robot):
        self.members.append(robot)

    def team_attack(self, target):

self.roles = roles
self.objective = objective        for robot in self.members:
            robot.attack(target)


# Create robots
robot1 = Robot("R1", "Team A")
robot2 = Robot("R2", "Team A")
robot3 = Robot("R3", "Team B")
robot4 = Robot("R4", "Team B")

# Equip weapons
weapon1 = Weapon("Laser Gun", 20)
weapon2 = Weapon("Sword", 15)

robot1.equip_weapon(weapon1)
robot2.equip_weapon(weapon2)
robot3.equip_weapon(weapon1)
robot4.equip_weapon(weapon2)

# Create teams
team_a = Team("Team A")
team_a.add_member(robot1)
team_a.add_member(robot2)

team_b = Team("Team B")
team_b.add_member(robot3)
team_b.add_member(robot4)

# Team A attacks Team B
team_a.team_attack(robot3)
team_a.team_attack(robot4)

# Team B attacks Team A
team_b.team_attack(robot1)
team_b.team_attack(robot2)