# solution.py

# Importing required libraries
import random
import time
import threading

# Class to represent a species in the ecosystem
class Species:
    def __init__(self, name, population_limit, food_source, habitat):
        self.name = name
        self.population = 0
        self.population_limit = population_limit
        self.food_source = food_source
        self.habitat = habitat

    def update_population(self):
        # Simulate population growth based on food availability
        if self.food_source > 0:
            self.population += 1
            self.food_source -= 1
        else:
            self.population -= 1

# Class to represent the ecosystem
class Ecosystem:
    def __init__(self):
        self.species = []
        self.water_resources = 100
        self.land_resources = 100
        self.pollution_level = 0
        self.climate = "normal"

    def add_species(self, species):
        self.species.append(species)

    def update_ecosystem(self):
        # Simulate environmental changes
        self.water_resources -= 1
        self.land_resources -= 1
        self.pollution_level += 1
        self.climate = "normal" if random.random() < 0.5 else "extreme"

        # Update species populations
        for species in self.species:
            species.update_population()

    def get_status(self):
        status = f"Ecosystem Status:\n"
        status += f"Water Resources: {self.water_resources}\n"
        status += f"Land Resources: {self.land_resources}\n"
        status += f"Pollution Level: {self.pollution_level}\n"
        status += f"Climate: {self.climate}\n"
        for species in self.species:
            status += f"{species.name}: {species.population}/{species.population_limit}\n"
        return status

# Class to represent a player
class Player:
    def __init__(self, name):
        self.name = name
        self.species = []

    def add_species(self, species):
        self.species.append(species)

    def get_status(self):
        status = f"Player {self.name} Status:\n"
        for species in self.species:
            status += f"{species.name}: {species.population}/{species.population_limit}\n"
        return status

# Class to represent the EcoSphere Manager game
class EcoSphereManager:
    def __init__(self):
        self.ecosystem = Ecosystem()
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def start_game(self):
        # Simulate game loop
        while True:
            self.ecosystem.update_ecosystem()
            for player in self.players:
                player.add_species(Species("Test Species", 10, 10, "Forest"))
            print(self.ecosystem.get_status())
            time.sleep(1)

    def run(self):
        # Create players and add them to the game
        player1 = Player("Player 1")
        player2 = Player("Player 2")
        self.add_player(player1)
        self.add_player(player2)

        # Start the game
        threading.Thread(target=self.start_game).start()

# Create an instance of the EcoSphere Manager game
game = EcoSphereManager()

# Run the game
game.run()