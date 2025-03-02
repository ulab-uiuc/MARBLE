# FamilyAdventureQuest.py

class QuestCreationModule:
    def __init__(self):
        self.quests = []

    def create_quest(self, quest_details):
        # Create a new quest with the provided details
        new_quest = {
            "name": quest_details.get("name"),
            "storyline": quest_details.get("storyline"),
            "puzzles": quest_details.get("puzzles"),
            "challenges": quest_details.get("challenges")
        }
        self.quests.append(new_quest)
        return new_quest

class QuestAssignmentModule:
    def __init__(self, quest_creation_module):
        self.quest_creation_module = quest_creation_module
        self.assigned_quests = {}

    def assign_quest(self, family_member, quest):
        # Assign a quest to a family memberif quest.get('name') not in [q.get('name') for q in self.quest_creation_module.quests]:
            self.assigned_quests[family_member] = quest
            return True
        else:
            return False            self.assigned_quests[family_member] = quest
            return True
        return False            self.assigned_quests[family_member] = quest
            return True
        return False

    def track_progress(self, family_member, stage_completed):
        # Track the progress of a family member in a quest
        if family_member in self.assigned_quests:
            # Update progress and unlock next stage if current stage is completed
            current_quest = self.assigned_quests[family_member]
            if stage_completed < len(current_quest.get("puzzles")):
                # Update progress
                current_quest["progress"] = stage_completed
                # Check if the next stage should be unlocked
                if stage_completed + 1 < len(current_quest.get("puzzles")):
                    current_quest["next_stage_unlocked"] = True
                return True
        return False

class InteractiveStorytelling:
    def __init__(self, quest_assignment_module):
        self.quest_assignment_module = quest_assignment_module

    def update_story(self, family_member):
        # Update the story based on the family member's progress
        if family_member in self.quest_assignment_module.assigned_quests:
            current_quest = self.quest_assignment_module.assigned_quests[family_member]
            progress = current_quest.get("progress", 0)
            if progress < len(current_quest.get("storyline")):
                return current_quest.get("storyline")[progress]
        return "No more story available."

class AchievementsAndRewardsSystem:
    def __init__(self, quest_assignment_module):
        self.quest_assignment_module = quest_assignment_module
        self.achievements = {}

    def award_achievement(self, family_member, achievement):
        # Award an achievement to a family member
        if family_member in self.quest_assignment_module.assigned_quests:
            if family_member not in self.achievements:
                self.achievements[family_member] = []
            self.achievements[family_member].append(achievement)
            return True
        return False

class FamilyCollaborationTools:
    def __init__(self, quest_assignment_module):
        self.quest_assignment_module = quest_assignment_module

    def collaborate(self, sender, receiver, message):
        # Send a message to another family member
        if sender in self.quest_assignment_module.assigned_quests and receiver in self.quest_assignment_module.assigned_quests:
            return f"{sender} sent a message to {receiver}: {message}"
        return "Message not sent. Check family members."

# Main program
if __name__ == "__main__":
    # Initialize modules
    quest_creation_module = QuestCreationModule()
    quest_assignment_module = QuestAssignmentModule(quest_creation_module)
    interactive_storytelling = InteractiveStorytelling(quest_assignment_module)
    achievements_system = AchievementsAndRewardsSystem(quest_assignment_module)
    family_collaboration_tools = FamilyCollaborationTools(quest_assignment_module)

    # Example of creating a quest
    quest_details = {
        "name": "Quest 1",
        "storyline": ["Once upon a time...", "The end."],
        "puzzles": ["Puzzle 1", "Puzzle 2", "Puzzle 3"],
        "challenges": ["Challenge 1", "Challenge 2"]
    }
    quest = quest_creation_module.create_quest(quest_details)

    # Example of assigning a quest to a family member
    assigned = quest_assignment_module.assign_quest("Family Member 1", quest)
    if assigned:
        print("Quest assigned successfully.")
    else:
        print("Quest assignment failed.")

    # Example of tracking progress
    progress_tracked = quest_assignment_module.track_progress("Family Member 1", 1)
    if progress_tracked:
        print("Progress tracked successfully.")
    else:
        print("Progress tracking failed.")

    # Example of updating the story
    story_update = interactive_storytelling.update_story("Family Member 1")
    print(story_update)

    # Example of awarding an achievement
    achievement_awarded = achievements_system.award_achievement("Family Member 1", "Completed Quest 1")
    if achievement_awarded:
        print("Achievement awarded successfully.")
    else:
        print("Achievement awarding failed.")

    # Example of family collaboration
    collaboration_result = family_collaboration_tools.collaborate("Family Member 1", "Family Member 2", "Hello!")
    print(collaboration_result)