# solution.py

# Import necessary libraries
from datetime import datetime, timedelta
from collections import defaultdict
import json

# User class to manage user information and tasks
class User:
    def __init__(self, username):
        self.username = username
        self.tasks = []  # List to hold user's tasks
        self.messages = []  # List to hold messages

    def add_task(self, task):
        self.tasks.append(task)

    def send_message(self, message):
        self.messages.append(message)

# Task class to manage individual tasks
class Task:
    def __init__(self, title, priority, deadline):
        self.title = title
        self.priority = priority
        self.deadline = deadline
        self.completed = False

    def mark_completed(self):
        self.completed = True

# TeamSyncPro class to manage the overall application
class TeamSyncPro:
    def __init__(self):
        self.users = {}  # Dictionary to hold users
        self.tasks = []  # List to hold all tasks
        self.notifications = []  # List to hold notifications

    def add_user(self, username):
        if username not in self.users:
            self.users[username] = User(username)

    def add_task(self, username, title, priority, deadline):
        if username in self.users:
            task = Task(title, priority, deadline)if not self.check_task_conflict(username, task):
                self.users[username].add_task(task)
    def check_task_conflict(self, username, new_task):
        for task in self.users[username].tasks:
            if task.deadline == new_task.deadline and task.priority == new_task.priority:
                return True
        return False
                self.tasks.append(task)
                self.notifications.append(f"Task '{title}' added for user '{username}'.")self.tasks.append(task)
            self.notifications.append(f"Task '{title}' added for user '{username}'.")

    def mark_task_completed(self, username, task_title):
        if username in self.users:
            for task in self.users[username].tasks:
                if task.title == task_title:
                    task.mark_completed()
                    self.notifications.append(f"Task '{task_title}' marked as completed for user '{username}'.")

    def generate_productivity_report(self):
        report = {
            "total_tasks": len(self.tasks),
            "completed_tasks": sum(task.completed for task in self.tasks),
            "user_contributions": {user: len(self.users[user].tasks) for user in self.users}
        }
        return json.dumps(report, indent=4)

    def send_notification(self, message):
        self.notifications.append(message)

    def get_notifications(self):
        return self.notifications

# Example usage of the TeamSyncPro application
if __name__ == "__main__":
    app = TeamSyncPro()

    # Adding users
    app.add_user("alice")
    app.add_user("bob")

    # Adding tasks
    app.add_task("alice", "Complete project report", "High", datetime.now() + timedelta(days=2))
    app.add_task("bob", "Prepare presentation", "Medium", datetime.now() + timedelta(days=1))

    # Marking a task as completed
    app.mark_task_completed("alice", "Complete project report")

    # Generating productivity report
    report = app.generate_productivity_report()
    print("Productivity Report:")
    print(report)

    # Display notifications
    print("Notifications:")
    print(app.get_notifications())