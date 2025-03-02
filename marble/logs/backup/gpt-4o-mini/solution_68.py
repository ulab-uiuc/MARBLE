# solution.py

# Import necessary libraries
import json
from datetime import datetime, timedelta
from collections import defaultdict
import random

# User class to represent each user in the system
class User:
    def __init__(self, username):
        self.username = username
        self.tasks = []  # List to hold user's tasks

    def add_task(self, task):
        """Add a task to the user's task list."""
        self.tasks.append(task)

# Task class to represent a task
class Task:
    def __init__(self, name, duration, priority, dependencies=None):
        self.name = name
        self.duration = duration  # Duration in hours
        self.priority = priority  # Priority level (1-5)
        self.dependencies = dependencies if dependencies else []  # List of task names

# CollaborativeSchedulePlanner class to manage the scheduling system
class CollaborativeSchedulePlanner:
    def __init__(self):
        self.users = {}  # Dictionary to hold users
        self.schedule = []  # List to hold scheduled tasks
        self.feedback = defaultdict(list)  # Dictionary to hold user feedback

    def add_user(self, username):
        """Add a new user to the system."""
        if username not in self.users:
            self.users[username] = User(username)

    def add_task(self, username, task):
        """Add a task for a specific user."""
        if username in self.users:
            self.users[username].add_task(task)

    def generate_schedule(self):
        """Generate a schedule based on user tasks and priorities."""
        # Sort tasks by priority and duration
        all_tasks = [task for user in self.users.values() for task in user.tasks]
        all_tasks.sort(key=lambda x: (-x.priority, x.duration))

        current_time = datetime.now()
        for task in all_tasks:
            # Check for dependencies
                if all(dep in [t[0] for t in self.schedule] for dep in task.dependencies):                self.schedule.append((task.name, current_time, task.duration))
                current_time += timedelta(hours=task.duration)

    def provide_feedback(self, username, task_name, feedback):
        """Allow users to provide feedback on the schedule."""
        self.feedback[task_name].append((username, feedback))

    def adjust_schedule(self):
        """Adjust the schedule based on user feedback."""
        # Simple adjustment logic based on feedback
        for task_name, feedback_list in self.feedback.items():
            if feedback_list:
                # Randomly adjust task duration based on feedback
                adjustment = random.choice([-1, 1])  # Randomly decrease or increase duration
                for i, (user, feedback) in enumerate(feedback_list):
                    if feedback == "too long":
                        adjustment = -1
                    elif feedback == "too short":
                        adjustment = 1
                # Find the task in the schedule and adjust its duration
                for i, (name, start_time, duration) in enumerate(self.schedule):
                    if name == task_name:
                        new_duration = max(1, duration + adjustment)  # Ensure duration is at least 1 hour
                        self.schedule[i] = (name, start_time, new_duration)

    def generate_report(self):
        """Generate a report of the current schedule."""
        report = {"schedule": self.schedule, "feedback": dict(self.feedback)}
        return json.dumps(report, indent=4)

# Example usage
if __name__ == "__main__":
    planner = CollaborativeSchedulePlanner()
    
    # Adding users
    planner.add_user("Alice")
    planner.add_user("Bob")

    # Adding tasks
    planner.add_task("Alice", Task("Design UI", 4, 5))
    planner.add_task("Bob", Task("Implement API", 3, 4, dependencies=["Design UI"]))
    planner.add_task("Alice", Task("Write Documentation", 2, 3))

    # Generate initial schedule
    planner.generate_schedule()
    print("Initial Schedule:")
    print(planner.generate_report())

    # Users provide feedback
    planner.provide_feedback("Alice", "Implement API", "too long")
    planner.provide_feedback("Bob", "Design UI", "too short")

    # Adjust schedule based on feedback
    planner.adjust_schedule()
    print("\nAdjusted Schedule:")
    print(planner.generate_report())