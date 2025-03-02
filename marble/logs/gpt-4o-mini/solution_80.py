# solution.py

# Import necessary libraries
import random
import time
from collections import defaultdict

# Define a class to represent a species in the ecosystem
class Species:
    def __init__(self, name, population_limit, food_source, habitat):
        self.name = name  # Name of the species
        self.population = 0  # Current population of the species
        self.population_limit = population_limit  # Maximum population limit
        self.food_source = food_source  # Food source for the species
        self.habitat = habitat  # Habitat of the species

    def add_population(self, amount):
        """Add to the population, ensuring it does not exceed the limit."""
        if self.population + amount <= self.population_limit:
            self.population += amount
        else:
            print(f"{self.name} population limit reached!")

    def remove_population(self, amount):
        """Remove from the population, ensuring it does not go below zero."""
        if self.population - amount >= 0:
            self.population -= amount
        else:
            print(f"{self.name} population cannot go below zero!")

# Define a class to represent the ecosystem
class EcoSphere:
    def __init__(self):
        self.species = {}  # Dictionary to hold species
        self.environmental_factors = {
            'climate': 'normal',
            'pollution': 0,
            'natural_disasters': 0
        }  # Environmental factors affecting the ecosystem
        self.players = []  # List to hold players managing the ecosystem

    def add_player(self, player):
        """Add a player to the shared ecosystem."""
        self.players.append(player)
        player.ecosphere = self  # Assign the shared ecosystem to the player
    def add_species(self, species):
        """Add a new species to the ecosystem."""
        self.species[species.name] = species

    def simulate_environment(self):
        """Simulate environmental changes and their effects on the ecosystem."""
        # Randomly change climate and pollution levels
        self.environmental_factors['climate'] = random.choice(['normal', 'drought', 'flood'])
        self.environmental_factors['pollution'] = random.randint(0, 100)
        self.environmental_factors['natural_disasters'] = random.randint(0, 3)

        # Provide feedback based on environmental factors
        for species in self.species.values():
            if self.environmental_factors['climate'] == 'drought':
                species.remove_population(int(species.population * 0.1))  # 10% population loss
            elif self.environmental_factors['climate'] == 'flood':
                species.remove_population(int(species.population * 0.2))  # 20% population loss

            if self.environmental_factors['pollution'] > 50:
                species.remove_population(int(species.population * 0.15))  # 15% population loss

    def display_status(self):
        """Display the current status of the ecosystem."""
        print("Ecosystem Status:")
        for species in self.species.values():
            print(f"{species.name}: Population = {species.population}/{species.population_limit}")
        print(f"Environmental Factors: {self.environmental_factors}")

# Define a class for player collaboration
class Player:
    def __init__(self, name):
        self.name = name  # Player's name
        self.ecosphere = EcoSphere()  # Each player has their own ecosystem

    def introduce_species(self, species):
        """Introduce a new species to the player's ecosystem."""
        self.ecosphere.add_species(species)

    def manage_ecosphere(self):
        """Manage the ecosystem by simulating environmental changes."""
        self.ecosphere.simulate_environment()
        self.ecosphere.display_status()

# Main function to run the EcoSphere Manager simulation
def main():
    # Create shared ecosystem
    shared_ecosphere = EcoSphere()

    # Create players
    player1 = Player("Alice")
    player2 = Player("Bob")

    # Add players to the shared ecosystem
    shared_ecosphere.add_player(player1)
    shared_ecosphere.add_player(player2)

    # Introduce species
    player1.introduce_species(Species("Deer", 100, "Grass", "Forest"))
    player1.introduce_species(Species("Wolf", 50, "Deer", "Forest"))
    player2.introduce_species(Species("Fish", 200, "Algae", "Lake"))
    player2.introduce_species(Species("Eagle", 30, "Fish", "Sky"))
    # Simulate the ecosystem over time
    for _ in range(5):  # Simulate for 5 time intervals
        print("\n--- Time Interval ---")
        player1.manage_ecosphere()
        player2.manage_ecosphere()
        time.sleep(1)  # Pause for a moment to simulate time passing

if __name__ == "__main__":
    main()