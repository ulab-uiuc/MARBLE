# solution.py

class Quest:
    """Class representing a quest with multiple stages."""
    
    def __init__(self, title, story, stages):
        self.title = title  # Title of the quest
        self.story = story  # Storyline of the quest
        self.stages = stages  # List of stages in the quest
        self.current_stage = 0  # Track the current stage of the quest

    def complete_stage(self):
        """Mark the current stage as complete and unlock the next stage."""
        if self.current_stage < len(self.stages) - 1:
            self.current_stage += 1  # Move to the next stage
            return True
        return False

    def get_current_stage(self):
        """Return the current stage details."""
        return self.stages[self.current_stage]


class QuestCreationModule:
    """Module for creating custom quests."""
    
    def __init__(self):
        self.quest_library = []  # List to store created quests

    def create_quest(self, title, story, stages):
        """Create a new quest and add it to the library."""
        new_quest = Quest(title, story, stages)
        self.quest_library.append(new_quest)
        return new_quest


class QuestAssignmentModule:
    """Module for assigning quests and tracking progress."""
    
    def __init__(self):
        self.assigned_quests = {}  # Dictionary to track assigned quests

    def assign_quest(self, family_member, quest):
        """Assign a quest to a family member."""
        self.assigned_quests[family_member] = quest

    def track_progress(self, family_member):
        """Return the current stage of the assigned quest for a family member."""
        quest = self.assigned_quests.get(family_member)
        if quest:
            return quest.get_current_stage()
        return None


class InteractiveStorytelling:
    """Module for interactive storytelling based on quest progress."""
    
    def __init__(self):
        pass

    def provide_feedback(self, quest):
        """Provide feedback based on the current stage of the quest."""
        current_stage = quest.get_current_stage()
        return f"You're currently at: {current_stage}. Keep going!"


class AchievementsAndRewards:
    """Module for managing achievements and rewards."""
    
    def __init__(self):
        self.achievements = {}  # Dictionary to store achievements for family members

    def award_achievement(self, family_member, achievement):
        """Award an achievement to a family member."""
        if family_member not in self.achievements:
            self.achievements[family_member] = []
        self.achievements[family_member].append(achievement)

    def get_achievements(self, family_member):
        """Return the achievements of a family member."""
        return self.achievements.get(family_member, [])


class FamilyCollaborationTools:
    """Module for collaboration tools among family members."""
    
    def __init__(self):
        self.chat = {}  # Dictionary to store chat messages
        self.shared_notes = {}  # Dictionary to store shared notes

    def send_message(self, sender, receiver, message):
        """Send a message from one family member to another."""
        if receiver not in self.chat:
            self.chat[receiver] = []
        self.chat[receiver].append((sender, message))

    def add_shared_note(self, family_member, note):
        """Add a shared note accessible to all family members."""
        if family_member not in self.shared_notes:
            self.shared_notes[family_member] = []
        self.shared_notes[family_member].append(note)

    def get_chat(self, family_member):
        """Return chat messages for a family member."""
        return self.chat.get(family_member, [])

    def get_shared_notes(self, family_member):
        """Return shared notes for a family member."""
        return self.shared_notes.get(family_member, [])


# Example usage
if __name__ == "__main__":
    # Create a quest creation module
    quest_creator = QuestCreationModule()
    quest = quest_creator.create_quest("Family Adventure", "A thrilling journey awaits!", ["Solve a riddle", "Find hidden treasures", "Complete a physical challenge"])

    # Assign the quest to a family member
    quest_assigner = QuestAssignmentModule()
    quest_assigner.assign_quest("Alice", quest)

    # Track progress
    print(quest_assigner.track_progress("Alice"))  # Output: Solve a riddle

    # Complete a stage
    quest.complete_stage()
    print(quest_assigner.track_progress("Alice"))  # Output: Find hidden treasures

    # Interactive storytelling
    storyteller = InteractiveStorytelling()
    print(storyteller.provide_feedback(quest))  # Output: You're currently at: Find hidden treasures. Keep going!

    # Achievements and rewards
    rewards_system = AchievementsAndRewards()
    rewards_system.award_achievement("Alice", "First Stage Completed")
    print(rewards_system.get_achievements("Alice"))  # Output: ['First Stage Completed']

    # Family collaboration tools
    collaboration_tools = FamilyCollaborationTools()
    collaboration_tools.send_message("Alice", "Bob", "Let's work together on the next stage!")
    print(collaboration_tools.get_chat("Bob"))  # Output: [('Alice', "Let's work together on the next stage!")]