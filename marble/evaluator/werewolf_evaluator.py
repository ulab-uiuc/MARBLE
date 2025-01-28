import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from marble.environments.werewolf_env import WerewolfEnv

if __name__ == "__main__":
    # Game Initialization
    name_prefix = "werewolf_engine_demo"
    config_path = os.path.join("marble", "configs", "test_config", "werewolf_config.yaml")

    # Ensure the config file exists
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at {config_path}")

    # Statistics Initialization
    total_games = 10
    villager_wins = 0
    werewolf_wins = 0
    villager_scores = []
    werewolf_scores = []
    score_differences = []

    try:
        for game_number in range(1, total_games + 1):
            print(f"Starting game {game_number}/{total_games}: {name_prefix}_{game_number}")
            try:
                # Create a new game environment
                env = WerewolfEnv(name=f"{name_prefix}_{game_number}", config_path=config_path)

                # Run the game
                game_result = env.start()

                # Collect Results
                if game_result["result"] == "Villagers win":
                    villager_wins += 1
                elif game_result["result"] == "Werewolves win":
                    werewolf_wins += 1

                # Extract scores
                villager_score = env.scores["villager"]["total"]
                werewolf_score = env.scores["werewolf"]["total"]
                villager_scores.append(villager_score)
                werewolf_scores.append(werewolf_score)

                # Calculate score difference
                score_difference = abs(villager_score - werewolf_score)
                score_differences.append(score_difference)

                print(f"Game {game_number} complete. Result: {game_result['result']}")

            except Exception as game_error:
                # Log error and continue to the next game
                print(f"An error occurred during game {game_number}: {game_error}")
                continue

        # Final Statistics
        villager_win_rate = villager_wins / total_games
        werewolf_win_rate = werewolf_wins / total_games
        average_villager_score = sum(villager_scores) / total_games if villager_scores else 0
        average_werewolf_score = sum(werewolf_scores) / total_games if werewolf_scores else 0
        average_score_difference = sum(score_differences) / total_games if score_differences else 0

        # Print Statistics
        print("\n=== Werewolf Game Statistics ===")
        print(f"Total Games Played: {total_games}")
        print(f"Villager Win Rate: {villager_win_rate:.2%}")
        print(f"Werewolf Win Rate: {werewolf_win_rate:.2%}")
        print(f"Average Villager Score: {average_villager_score:.2f}")
        print(f"Average Werewolf Score: {average_werewolf_score:.2f}")
        print(f"Average Score Difference: {average_score_difference:.2f}")

    except Exception as e:
        # Handle Initialization or Overall Simulation Errors
        print(f"An error occurred during the simulation: {e}")
