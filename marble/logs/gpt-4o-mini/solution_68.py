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

# Task class to represent a task with its properties
class Task:
    def __init__(self, name, duration, priority, dependencies=None):
        self.name = name
        self.duration = duration  # Duration in hours
        self.priority = priority  # Priority level (1-5)
        self.dependencies = dependencies if dependencies else []  # List of task names

# CollaborativeSchedulePlanner class to manage users and tasks
class CollaborativeSchedulePlanner:
    def __init__(self):
        self.users = {}  # Dictionary to hold users
        self.schedule = []  # List to hold all tasks in the schedule
        self.feedback = defaultdict(list)  # Dictionary to hold user feedback

    def add_user(self, username):
        """Add a new user to the system."""
        if username not in self.users:
            self.users[username] = User(username)
            print(f"User {username} added.")
        else:
            print(f"User {username} already exists.")

    def add_task(self, username, task_name, duration, priority, dependencies=None):
        """Add a new task for a user."""
        if username in self.users:
            task = Task(task_name, duration, priority, dependencies)
            self.users[username].tasks.append(task)
            self.schedule.append(task)
            print(f"Task '{task_name}' added for user {username}.")
        else:
            print(f"User {username} not found.")

    def view_schedule(self):
        """View the current schedule."""
        print("Current Schedule:")
        for task in self.schedule:
            print(f"Task: {task.name}, Duration: {task.duration}h, Priority: {task.priority}, Dependencies: {task.dependencies}")

    def provide_feedback(self, username, task_name, feedback):
        """Allow users to provide feedback on tasks."""def adjust_schedule(self):
        """Adjust the schedule based on user feedback and preferences."""
        for task_name, feedback_list in self.feedback.items():
            if feedback_list:
                task_exists = any(task.name == task_name for task in self.schedule)
                if not task_exists:
                    print(f"Task '{task_name}' does not exist in the schedule. Feedback cannot be applied.")
                    continue
                for username, feedback in feedback_list:
                    if 'more time' in feedback.lower():
                        for task in self.schedule:
                            if task.name == task_name:
                                task.duration += 1  # Increase duration by 1 hour
                                task.priority = min(task.priority + 1, 5)  # Increase priority, max 5
                                print(f"Task '{task_name}' duration increased and priority adjusted based on feedback from {username}.")
                    elif 'less time' in feedback.lower():
                        for task in self.schedule:
                            if task.name == task_name:
                                task.duration = max(task.duration - 1, 1)  # Decrease duration, min 1 hour
                                task.priority = max(task.priority - 1, 1)  # Decrease priority, min 1
                                print(f"Task '{task_name}' duration decreased and priority adjusted based on feedback from {username}.")        for task_name, feedback_list in self.feedback.items():
            if feedback_list:
                for username, feedback in feedback_list:
                    if 'more time' in feedback.lower():
                        for task in self.schedule:
                            if task.name == task_name:
                                task.duration += 1  # Increase duration by 1 hour
                                task.priority = min(task.priority + 1, 5)  # Increase priority, max 5
                                print(f"Task '{task_name}' duration increased and priority adjusted based on feedback from {username}.")
                    elif 'less time' in feedback.lower():
                        for task in self.schedule:
                            if task.name == task_name:
                                task.duration = max(task.duration - 1, 1)  # Decrease duration, min 1 hour
                                task.priority = max(task.priority - 1, 1)  # Decrease priority, min 1
                                print(f"Task '{task_name}' duration decreased and priority adjusted based on feedback from {username}.")                for task in self.schedule:
                    if task.name == task_name:
                        task.priority = new_priority
                        print(f"Task '{task_name}' priority adjusted to {new_priority} based on feedback.")

    def generate_report(self):
        """Generate a simple report of the current schedule."""
        report = {"schedule": [], "total_duration": 0}
        for task in self.schedule:
            report["schedule"].append({
                "name": task.name,
                "duration": task.duration,
                "priority": task.priority
            })
            report["total_duration"] += task.duration
        print(json.dumps(report, indent=4))

# Example usage
if __name__ == "__main__":
    planner = CollaborativeSchedulePlanner()
    planner.add_user("Alice")
    planner.add_user("Bob")
    planner.add_task("Alice", "Design", 5, 3)
    planner.add_task("Bob", "Development", 8, 4)
    planner.view_schedule()
    planner.provide_feedback("Alice", "Development", "Needs more time")
    planner.adjust_schedule()
    planner.generate_report()