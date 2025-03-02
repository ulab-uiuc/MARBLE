# family_adventure_quest.py

class Quest:
    """Represents a quest with multiple stages."""
    def __init__(self, name, storylines, puzzles, physical_challenges):
        self.name = name
        self.storylines = storylines
        self.puzzles = puzzles
        self.physical_challenges = physical_challenges
        self.stages = []
        self.current_stage = 0

    def add_stage(self, stage):
        """Adds a stage to the quest."""
        self.stages.append(stage)

    def next_stage(self):
        """Moves to the next stage of the quest."""
        if self.current_stage < len(self.stages) - 1:
            self.current_stage += 1
            return self.stages[self.current_stage]
        else:
            return None

    def get_current_stage(self):
        """Returns the current stage of the quest."""
        return self.stages[self.current_stage]


class Stage:
    """Represents a stage of a quest."""
    def __init__(self, name, task):
        self.name = name
        self.task = task
        self.completed = False

    def complete(self):
        """Marks the stage as completed."""
        self.completed = True


class FamilyMember:
    """Represents a family member."""
    def __init__(self, name):
        self.name = name
        self.quests = []
        self.achievements = []

    def assign_quest(self, quest):
        """Assigns a quest to the family member."""
        self.quests.append(quest)

    def complete_stage(self, quest, stage):
        """Completes a stage of a quest."""
        for q in self.quests:
            if q.name == quest.name:
                for s in q.stages:
                    if s.name == stage.name:
                        s.complete()
                        return

    def add_achievement(self, achievement):
        """Adds an achievement to the family member."""
        self.achievements.append(achievement)


class Achievement:
    """Represents an achievement."""
    def __init__(self, name, description):
        self.name = name
        self.description = description


class FamilyAdventureQuest:def track_progress(self, family_member, quest):
    """Tracks the progress of a family member on a quest."""
    for q in family_member.quests:
        if q.name == quest.name:
            current_stage = q.get_current_stage()
            if current_stage and not current_stage.completed:
                print(f"{family_member.name} is currently on stage {current_stage.name} of quest {q.name}")
            elif current_stage and current_stage.completed:
                next_stage = q.next_stage()
                if next_stage:
                    print(f"{family_member.name} has completed stage {current_stage.name} of quest {q.name}. Next stage is {next_stage.name}.")
                else:
                    print(f"{family_member.name} has completed quest {q.name}.")
            else:
                print(f"{family_member.name} has not started quest {q.name}.")for q in family_member.quests:
            if q.name == quest.name:
                current_stage = q.get_current_stage()
                if current_stage:
                    print(f"{family_member.name} is currently on stage {current_stage.name} of quest {q.name}")
                else:
                    print(f"{family_member.name} has completed quest {q.name}")

    def add_achievement(self, family_member, achievement):
        """Adds an achievement to a family member."""
        family_member.add_achievement(achievement)


# Example usage:

# Create a new Family Adventure Quest system
faq = FamilyAdventureQuest()

# Create a new quest
quest = faq.create_quest("The Lost City", ["storyline1", "storyline2"], ["puzzle1", "puzzle2"], ["physical_challenge1", "physical_challenge2"])

# Create stages for the quest
stage1 = Stage("Stage 1", "Solve a math problem")
stage2 = Stage("Stage 2", "Complete a scavenger hunt")
quest.add_stage(stage1)
quest.add_stage(stage2)

# Create a new family member
family_member = FamilyMember("John")

# Assign the quest to the family member
faq.assign_quest(family_member, quest)

# Track the progress of the family member on the quest
faq.track_progress(family_member, quest)

# Complete a stage of the quest
family_member.complete_stage(quest, stage1)

# Track the progress of the family member on the quest again
faq.track_progress(family_member, quest)

# Add an achievement to the family member
achievement = Achievement("Completed Stage 1", "Congratulations on completing stage 1 of the quest!")
faq.add_achievement(family_member, achievement)

# Print the achievements of the family member
print(f"{family_member.name}'s achievements:")
for achievement in family_member.achievements:
    print(f"{achievement.name}: {achievement.description}")