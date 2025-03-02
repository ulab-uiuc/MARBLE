# ecosystem.py
class Ecosystem:
    def __init__(self):
        self.species = []
        self.environmental_factors = []
        self.challenges = []

    def add_species(self, species):
        self.species.append(species)

    def add_environmental_factor(self, environmental_factor):
        self.environmental_factors.append(environmental_factor)

    def add_challenge(self, challenge):
        self.challenges.append(challenge)

    def update(self):
        for species in self.species:
            species.update(self.environmental_factors)
        for environmental_factor in self.environmental_factors:
            environmental_factor.update(self.species)
        for challenge in self.challenges:
            challenge.update(self.species, self.environmental_factors)


# species.py
class Species:
    def __init__(self, name, population, food_source, habitat):
        self.name = name
        self.population = population
        self.food_source = food_source
        self.habitat = habitat

    def update(self, environmental_factors):for factor in environmental_factors:
            if factor.value < 0.5:  # If the environmental factor's value is below 0.5
                self.population *= 0.9  # Reduce the population by 10%
            elif factor.value > 1.5:  # If the environmental factor's value is above 1.5
                self.population *= 1.1  # Increase the population by 10%class Game:
    def __init__(self):
        self.ecosystem = Ecosystem()
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def update(self):
        self.ecosystem.update()
        for player in self.players:
            player.update(self.ecosystem)

    def display(self):
        print("Ecosystem Status:")
        for species in self.ecosystem.species:
            print(f"{species.name}: {species.population}")
        for environmental_factor in self.ecosystem.environmental_factors:
            print(f"{environmental_factor.name}: {environmental_factor.value}")
        for challenge in self.ecosystem.challenges:
            print(f"{challenge.name}: {challenge.description}")


# main.py
def main():
    game = Game()

    # Create players
    player1 = Player("Player 1")
    player2 = Player("Player 2")

    # Create species
    species1 = Species("Species 1", 100, "Food Source 1", "Habitat 1")
    species2 = Species("Species 2", 50, "Food Source 2", "Habitat 2")

    # Create environmental factors
    climate = EnvironmentalFactor("Climate", 1.0)
    pollution = EnvironmentalFactor("Pollution", 0.0)

    # Create challenges
    invasive_species = Challenge("Invasive Species", "An invasive species has been introduced to the ecosystem.")

    # Add species, environmental factors, and challenges to the ecosystem
    game.ecosystem.add_species(species1)
    game.ecosystem.add_species(species2)
    game.ecosystem.add_environmental_factor(climate)
    game.ecosystem.add_environmental_factor(pollution)
    game.ecosystem.add_challenge(invasive_species)

    # Add players to the game
    game.add_player(player1)
    game.add_player(player2)

    # Update and display the game state
    game.update()
    game.display()

if __name__ == "__main__":
    main()