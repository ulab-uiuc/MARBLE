# EcoSphere Manager

class Species:
    def __init__(self, name, population_limit, food_sources, habitat):
        self.name = name
        self.population_limit = population_limit
        self.food_sources = food_sources
        self.habitat = habitat
        self.population = 0

    def __str__(self):
        return f"{self.name} - Population: {self.population}/{self.population_limit}, Food Sources: {self.food_sources}, Habitat: {self.habitat}"

class Ecosystem:
    def __init__(self):
        self.species = []

    def add_species(self, species):
        self.species.append(species)

    def show_species(self):
        for specie in self.species:
            print(specie)

# Creating species
lion = Species("Lion", 10, ["Zebra", "Antelope"], "Grasslands")
        # Simulate dynamic responses to player actions and environmental changes
        for specie in self.species:
            # Adjust population based on food availability, habitat conditions, and external factors
            if specie.food_sources and specie.habitat:
                specie.population = min(specie.population_limit, specie.population + len(specie.food_sources) - 1)
            # Additional logic for climate variations, pollution levels, etc. can be added here

zebra = Species("Zebra", 20, ["Grass"], "Grasslands")
shark = Species("Shark", 5, ["Fish", "Seals"], "Ocean")

# Creating ecosystem
ecosystem = Ecosystem()
ecosystem.add_species(lion)
ecosystem.add_species(zebra)
ecosystem.add_species(shark)

# Displaying species in the ecosystem
ecosystem.show_species()