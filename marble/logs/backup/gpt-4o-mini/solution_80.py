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
            print(f"Cannot add {amount} to {self.name}. Population limit reached.")

    def remove_population(self, amount):
        """Remove from the population, ensuring it does not go below zero."""
        if self.population - amount >= 0:
            self.population -= amount
        else:
            print(f"Cannot remove {amount} from {self.name}. Population cannot be negative.")

# Define a class to represent the ecosystem
class EcoSphere:
    def __init__(self):
        self.species = {}  # Dictionary to hold species
        self.environmental_factors = {
            'climate': 'stable',
            'pollution': 0,
            'natural_disasters': 0
        }  # Environmental factors affecting the ecosystem

    def add_species(self, species):
        """Add a new species to the ecosystem."""
        self.species[species.name] = species

    def simulate_environment(self):
        """Simulate environmental changes and their effects on the ecosystem."""
        # Randomly change climate and pollution levels
        self.environmental_factors['climate'] = random.choice(['stable', 'drought', 'flood'])
        self.environmental_factors['pollution'] = random.randint(0, 100)
        self.environmental_factors['natural_disasters'] = random.randint(0, 2)

        # Provide feedback based on environmental factors
        self.evaluate_ecosystem_health()

    def evaluate_ecosystem_health(self):
        """Evaluate the health of the ecosystem based on species populations and environmental factors."""
        print("Evaluating ecosystem health...")
        for species in self.species.values():
            if self.environmental_factors['climate'] == 'drought':
                species.remove_population(int(species.population * 0.1))  # 10% population loss
            elif self.environmental_factors['climate'] == 'flood':
                species.add_population(int(species.population * 0.05))  # 5% population increase

            # Check pollution effects
            if self.environmental_factors['pollution'] > 50:
                species.remove_population(int(species.population * 0.2))  # 20% population loss due to pollution

        # Print current populations
        for species in self.species.values():
            print(f"{species.name} population: {species.population}")

# Define a class for player collaboration
class Player:
    def __init__(self, name, eco_sphere):
        self.name = name  # Player's name
        self.eco_sphere = eco_sphere  # Shared EcoSphere instance

    def introduce_species(self, species):
        """Introduce a new species to the shared EcoSphere."""
        self.eco_sphere.add_species(species)    def introduce_species(self, species):
        """Introduce a new species to the player's EcoSphere."""
        self.eco_sphere.add_species(species)

    def manage_ecosystem(self):
        """Manage the ecosystem by simulating environmental changes."""
        while True:
            self.eco_sphere.simulate_environment()
            time.sleep(5)  # Simulate time passing in the ecosystem

# Example usage
if __name__ == "__main__":
    # Create players
    player1 = Player("Alice")
    player2 = Player("Bob")

    # Create species
    deer = Species("Deer", population_limit=100, food_source="Grass", habitat="Forest")
    wolf = Species("Wolf", population_limit=50, food_source="Deer", habitat="Forest")

    # Introduce species to players
    player1.introduce_species(deer)
    player2.introduce_species(wolf)

    # Set initial populations
    deer.add_population(30)
    wolf.add_population(10)

    # Start managing the ecosystem (this will run indefinitely in a real scenario)
    player1.manage_ecosystem()