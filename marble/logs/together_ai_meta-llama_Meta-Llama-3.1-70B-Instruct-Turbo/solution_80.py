def main():
    game = Game()
    game.start_simulation(1)  # Start the simulation mechanism with a time interval of 1 unit    game = Game()
    ui = UI(game)

    # Create players
    player1 = Player("Player 1")
    player2 = Player("Player 2")

    # Add players to the game
    game.add_player(player1)
    game.add_player(player2)

    # Start the game
    game.start_game()

    # Create ecosystem
    game.update_game_state()  # Update the game state based on the current state of the ecosystem
    ecosystem = game.ecosystem

    # Add species to the ecosystem
    ecosystem.add_species("Lion", 100, "Meat", "Savannah")
    ecosystem.add_species("Giraffe", 50, "Leaves", "Savannah")

    # Add environmental factors to the ecosystem
    ecosystem.add_environmental_factor("Temperature", 25)
    ecosystem.add_environmental_factor("Pollution", 10)

    # Manage species and environmental factors
    player1.manage_species(ecosystem, "Lion")
    player1.manage_environmental_factor(ecosystem, "Temperature")
    player2.manage_species(ecosystem, "Giraffe")
    player2.manage_environmental_factor(ecosystem, "Pollution")

    # Display ecosystem status
    ui.display_ecosystem_status()

    # Display player status
    ui.display_player_status("Player 1")
    ui.display_player_status("Player 2")

    # Display game status
    ui.display_game_status()

    # End the game
    game.end_game()


if __name__ == "__main__":
    main()