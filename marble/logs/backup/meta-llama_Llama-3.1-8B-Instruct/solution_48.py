# office_task_collaboration_manager.py
# This is the main implementation of the Office Task Collaboration Manager

import datetime
import getpass
import os
import pickle
import random
import string
import time
from enum import Enum
from typing import Dict, List

class TaskStatus(Enum):
    """Task status enumeration"""
    NOT_STARTED = 1
    IN_PROGRESS = 2
    COMPLETED = 3

class User:
    """User class"""
    def __init__(self, username: str, password: str, role: str):
        self.username = username
        self.password = password
        self.role = role
        self.tasks = []

class Task:
    """Task class"""
    def __init__(self, title: str, description: str, deadline: datetime.date, priority: int, status: TaskStatus):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.status = status
        self.comments = []
        self.attachments = []
        self.assignee = None

class OfficeTaskCollaborationManager:
    """Office Task Collaboration Manager class"""
    def __init__(self):
        self.users = {}
        self.tasks = []
        self.notifications = {}

    def create_user(self, username: str, password: str, role: str):
        """Create a new user"""
        if username not in self.users:
            self.users[username] = User(username, password, role)
            print(f"User {username} created successfully.")
        else:
            print(f"User {username} already exists.")

    def authenticate_user(self, username: str, password: str):
        """Authenticate a user"""
        if username in self.users and self.users[username].password == password:
            return self.users[username]
        else:
            return None

    def create_task(self, title: str, description: str, deadline: datetime.date, priority: int, status: TaskStatus):
        """Create a new task"""
        task = Task(title, description, deadline, priority, status)
        self.tasks.append(task)
        print(f"Task {title} created successfully.")

    def assign_task(self, task_title: str, assignee: str):
        """Assign a task to a user"""
        for task in self.tasks:
            if task.title == task_title:
                task.assignee = self.users[assignee]
                print(f"Task {task_title} assigned to {assignee} successfully.")
                return
        print(f"Task {task_title} not found.")

    def update_task_status(self, task_title: str, status: TaskStatus):
        """Update the status of a task"""
        for task in self.tasks:
            if task.title == task_title:
                task.status = status
                print(f"Task {task_title} status updated successfully.")
                return
        print(f"Task {task_title} not found.")

    def add_comment(self, task_title: str, comment: str):
        """Add a comment to a task"""
        for task in self.tasks:
            if task.title == task_title:
                task.comments.append(comment)
                print(f"Comment added to task {task_title} successfully.")
                return
        print(f"Task {task_title} not found.")

    def add_attachment(self, task_title: str, attachment: str):
        """Add an attachment to a task"""
        for task in self.tasks:
            if task.title == task_title:
                task.attachments.append(attachment)
                print(f"Attachment added to task {task_title} successfully.")
                return
        print(f"Task {task_title} not found.")

    def generate_report(self):
        """Generate a report on task progress"""
        completed_tasks = [task for task in self.tasks if task.status == TaskStatus.COMPLETED]
        pending_tasks = [task for task in self.tasks if task.status == TaskStatus.NOT_STARTED or task.status == TaskStatus.IN_PROGRESS]
        overdue_tasks = [task for task in self.tasks if task.deadline < datetime.date.today()]
        print("Task Report:")
        print(f"Completed Tasks: {len(completed_tasks)}")
        print(f"Pending Tasks: {len(pending_tasks)}")
        print(f"Overdue Tasks: {len(overdue_tasks)}")

    def send_notification(self, task_title: str, message: str):
        """Send a notification to users"""
        for task in self.tasks:
            if task.title == task_title:
                for user in self.users.values():
                    if user.role == "admin" or user == task.assignee:
                        print(f"Notification sent to {user.username}: {message}")
                        return
        print(f"Task {task_title} not found.")

def main():
    # Initialize the Office Task Collaboration Manager
    manager = OfficeTaskCollaborationManager()

    # Create users
    manager.create_user("admin", "password", "admin")
    manager.create_user("user1", "password", "user")

    # Authenticate user
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    user = manager.authenticate_user(username, password)
    if user:
        print(f"Welcome, {username}!")
    else:
        print("Invalid username or password.")
        return

    # Create tasks
    manager.create_task("Task 1", "This is task 1", datetime.date(2024, 7, 31), 1, TaskStatus.NOT_STARTED)
    manager.create_task("Task 2", "This is task 2", datetime.date(2024, 8, 31), 2, TaskStatus.IN_PROGRESS)

    # Assign tasks
    manager.assign_task("Task 1", "user1")

    # Update task status
    manager.update_task_status("Task 1", TaskStatus.COMPLETED)

    # Add comments and attachments
    manager.add_comment("Task 1", "This is a comment.")
    manager.add_attachment("Task 1", "attachment.txt")

    # Generate report
    manager.generate_report()

    # Send notification
    manager.send_notification("Task 1", "Task completed!")

if __name__ == "__main__":
    main()