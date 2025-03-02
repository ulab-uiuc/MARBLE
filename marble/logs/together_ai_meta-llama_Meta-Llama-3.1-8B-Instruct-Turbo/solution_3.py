# solution.py

import random
import time
import pygame
import sys

# Initialize Pygame
pygame.init()

# Define some colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up some constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Set up the display
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

class Robot:
    def __init__(self, x, y, team):
        self.x = x
        self.y = y
        self.team = team
        self.health = 100
        self.score = 0
        self.weapon = random.choice(['ranged', 'melee'])

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def attack(self, other_robot):
        if self.weapon == 'ranged':
            # Ranged attack
            other_robot.health -= 20
            print(f"{self.team} robot attacks {other_robot.team} robot!")
        elif self.weapon == 'melee':
            # Melee attack
            other_robot.health -= 30
            print(f"{self.team} robot attacks {other_robot.team} robot!")

    def is_alive(self):
        return self.health > 0

class Team:
    def __init__(self, name):
        self.name = name
        self.robots = []

    def add_robot(self, robot):
        self.robots.append(robot)

    def remove_robot(self, robot):
        self.robots.remove(robot)

class Game:
    def __init__(self):
        self.teams = [Team('Red'), Team('Blue')]
        self.robots = []
        self.scoreboard = {'Red': 0, 'Blue': 0}

        # Create robots
        for i in range(5):
            self.teams[0].add_robot(Robot(100, 100, 'Red'))
            self.teams[1].add_robot(Robot(700, 100, 'Blue'))

        # Randomly assign roles
        for team in self.teams:
            for robot in team.robots:
                if random.random() < 0.5:
                    robot.weapon = 'ranged'
                else:
                    robot.weapon = 'melee'

    def update(self):
        # Update robot positions
        for team in self.teams:
            for robot in team.robots:
                robot.move(0, 2)

        # Check for collisions
        for team in self.teams:
            for robot in team.robots:
                for other_team in self.teams:
                    if other_team != team:
                        for other_robot in other_team.robots:
                            if robot.x - 20 < other_robot.x + 20 and robot.x + 20 > other_robot.x - 20 and robot.y - 20 < other_robot.y + 20 and robot.y + 20 > other_robot.y - 20:
                                robot.attack(other_robot)

        # Update scores
        for team in self.teams:
            for robot in team.robots:
                if robot.is_alive():
                    self.scoreboard[team.name] += 1

    def draw(self):
        # Draw background
        SCREEN.fill(WHITE)

        # Draw robots
        for team in self.teams:
            for robot in team.robots:
                if robot.team == 'Red':
                    pygame.draw.rect(SCREEN, RED, (robot.x, robot.y, 20, 20))
                else:
                    pygame.draw.rect(SCREEN, BLUE, (robot.x, robot.y, 20, 20))

        # Draw scoreboard
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.scoreboard['Red']} - {self.scoreboard['Blue']}", True, (0, 0, 0))
        SCREEN.blit(text, (10, 10))

        # Update display
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.update()
            self.draw()
            clock.tick(FPS)

        pygame.quit()
        sys.exit()

game = Game()
game.run()