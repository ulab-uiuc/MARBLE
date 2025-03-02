# office_task_collaboration_manager.py
# This is the main implementation of the Office Task Collaboration Manager

import datetime
import os
import pickle
import random
import string
import threading
from enum import Enum
from typing import Dict, List

# Define a class for User
class User:
    def __init__(self, username: str, password: str, role: str):
        self.username = username
        self.password = password
        self.role = role
        self.tasks = []

# Define a class for Task
class Task:
    def __init__(self, title: str, description: str, deadline: datetime.date, priority: str, status: str):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.status = status
        self.comments = []
        self.attachments = []

# Define a class for Comment
class Comment:
    def __init__(self, text: str, user: User):
        self.text = text
        self.user = user

# Define a class for Attachment
class Attachment:
    def __init__(self, filename: str, user: User):
        self.filename = filename
        self.user = user

# Define a class for Notification
class Notification:
    def __init__(self, message: str, user: User):
        self.message = message
        self.user = user

# Define a class for TaskManager
class TaskManager:
    def __init__(self):
        self.users = {}
        self.tasks = {}
        self.notifications = []

    def create_user(self, username: str, password: str, role: str):
        if username not in self.users:
            self.users[username] = User(username, password, role)
            return True
        return False

    def assign_task(self, task_id: str, user: User):
        if task_id in self.tasks:
            self.tasks[task_id].assignee = user
            self.notifications.append(Notification(f"Task {task_id} assigned to {user.username}", user))
            return True
        return False

    def update_task_status(self, task_id: str, status: str):
        if task_id in self.tasks:
            self.tasks[task_id].status = status
            self.notifications.append(Notification(f"Task {task_id} status updated to {status}", self.tasks[task_id].assignee))
            return True
        return False

    def add_comment(self, task_id: str, text: str, user: User):
        if task_id in self.tasks:
            self.tasks[task_id].comments.append(Comment(text, user))
            self.notifications.append(Notification(f"Comment added to task {task_id} by {user.username}", user))
            return True
        return False

    def add_attachment(self, task_id: str, filename: str, user: User):
        if task_id in self.tasks:
            self.tasks[task_id].attachments.append(Attachment(filename, user))
            self.notifications.append(Notification(f"Attachment added to task {task_id} by {user.username}", user))
            return True
        return False

    def generate_report(self):
        report = ""
        for task_id, task in self.tasks.items():
            report += f"Task {task_id}: {task.title}\n"
            report += f"Status: {task.status}\n"
            report += f"Assignee: {task.assignee.username}\n"
            report += f"Deadline: {task.deadline}\n"
            report += f"Priority: {task.priority}\n"
            report += f"Comments:\n"
            for comment in task.comments:
                report += f"- {comment.text} by {comment.user.username}\n"
            report += f"Attachments:\n"
            for attachment in task.attachments:
                report += f"- {attachment.filename} by {attachment.user.username}\n"
            report += "\n"
        return report

    def send_notification(self, notification: Notification):
        print(f"Notification sent to {notification.user.username}: {notification.message}")

# Define a class for OfficeTaskCollaborationManager
class OfficeTaskCollaborationManager:
    def __init__(self):
        self.task_manager = TaskManager()

    def run(self):
        while True:
            print("1. Create user")
            print("2. Assign task")
            print("3. Update task status")
            print("4. Add comment")
            print("5. Add attachment")
            print("6. Generate report")
            print("7. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                username = input("Enter username: ")
                password = input("Enter password: ")
                role = input("Enter role: ")
                self.task_manager.create_user(username, password, role)
            elif choice == "2":
                task_id = input("Enter task ID: ")
                username = input("Enter assignee's username: ")
                if username in self.task_manager.users:
                    self.task_manager.assign_task(task_id, self.task_manager.users[username])
                else:
                    print("User not found")
            elif choice == "3":
                task_id = input("Enter task ID: ")
                status = input("Enter new status: ")
                self.task_manager.update_task_status(task_id, status)
            elif choice == "4":
                task_id = input("Enter task ID: ")
                text = input("Enter comment text: ")
                username = input("Enter user's username: ")
                if username in self.task_manager.users:
                    self.task_manager.add_comment(task_id, text, self.task_manager.users[username])
                else:
                    print("User not found")
            elif choice == "5":
                task_id = input("Enter task ID: ")
                filename = input("Enter attachment filename: ")
                username = input("Enter user's username: ")
                if username in self.task_manager.users:
                    self.task_manager.add_attachment(task_id, filename, self.task_manager.users[username])
                else:
                    print("User not found")
            elif choice == "6":
                print(self.task_manager.generate_report())
            elif choice == "7":
                break
            else:
                print("Invalid choice")

# Create an instance of OfficeTaskCollaborationManager
office_task_collaboration_manager = OfficeTaskCollaborationManager()

# Run the office task collaboration manager
office_task_collaboration_manager.run()