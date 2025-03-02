# solution.py

class Player:
    """Class representing a player in the quest creation system."""
    
    def __init__(self, username):
        self.username = username
        self.skills = {}  # Dictionary to hold player skills

    def set_skill(self, skill_name, skill_value):
        """Set a skill for the player."""
        self.skills[skill_name] = skill_value


class Quest:
    """Class representing a quest in the game."""
    
    def __init__(self, title):
        self.title = title
        self.objectives = []
        self.enemies = []
        self.rewards = []
        self.difficulty = 1  # Default difficulty level
        self.history = []  # To track changes made to the quest

    def add_objective(self, objective):
        """Add an objective to the quest."""
        self.objectives.append(objective)
        self.history.append(f"Added objective: {objective}")

    def add_enemy(self, enemy):
        """Add an enemy to the quest."""
        self.enemies.append(enemy)
        self.history.append(f"Added enemy: {enemy}")

    def add_reward(self, reward):
        """Add a reward to the quest."""
        self.rewards.append(reward)
        self.history.append(f"Added reward: {reward}")

    def set_difficulty(self, difficulty):
        """Set the difficulty level of the quest."""def get_balance_feedback(self, players):
        """Provide feedback on the balance of the quest based on player skills, objectives, and enemy types."""
        total_skill = sum(sum(player.skills.values()) for player in players)
        enemy_strength = sum(enemy['strength'] for enemy in self.enemies)
        objective_weight = sum(1 for objective in self.objectives)  # Simple weight for each objective
        balance_score = (total_skill + objective_weight) / (enemy_strength + 1)  # Adjusted balance score
        return balance_score    def revert_history(self):
        """Revert to the last change made to the quest."""
        if self.history:
            last_change = self.history.pop()
            return f"Reverted: {last_change}"
        return "No history to revert."


class QuestCreator:
    """Class to manage the quest creation process."""
    
    def __init__(self):
        self.players = []
        self.quests = []

    def add_player(self, player):
        """Add a player to the quest creator system."""
        self.players.append(player)

    def create_quest(self, title):
        """Create a new quest."""
        quest = Quest(title)
        self.quests.append(quest)
        return quest

    def simulate_quest(self, quest):
        """Simulate the quest to see how it plays out."""
        # Placeholder for simulation logic
        return f"Simulating quest: {quest.title} with difficulty {quest.difficulty}"


# Example usage
if __name__ == "__main__":
    # Create a quest creator instance
    quest_creator = QuestCreator()

    # Create players
    player1 = Player("Hero1")
    player1.set_skill("Combat", 5)
    player1.set_skill("Magic", 3)

    player2 = Player("Hero2")
    player2.set_skill("Combat", 4)
    player2.set_skill("Stealth", 2)

    # Add players to the quest creator
    quest_creator.add_player(player1)
    quest_creator.add_player(player2)

    # Create a new quest
    quest = quest_creator.create_quest("Dragon's Lair")

    # Add objectives, enemies, and rewards
    quest.add_objective("Defeat the Dragon")
    quest.add_enemy({"name": "Dragon", "strength": 10})
    quest.add_reward("Gold Treasure")

    # Set difficulty
    quest.set_difficulty(5)

    # Get balance feedback
    balance_feedback = quest.get_balance_feedback(quest_creator.players)
    print(f"Balance Feedback: {balance_feedback}")

    # Simulate the quest
    simulation_result = quest_creator.simulate_quest(quest)
    print(simulation_result)

    # Revert last change
    revert_message = quest.revert_history()
    print(revert_message)