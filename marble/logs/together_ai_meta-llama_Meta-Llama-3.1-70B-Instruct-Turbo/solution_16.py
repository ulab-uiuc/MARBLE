# codesquad.py

import os
import threading
from datetime import datetime
from typing import Dict, List

# User class to store user information
class User:
    def __init__(self, username: str, password: str, role: str):
        self.username = username
        self.password = password
        self.role = role

# Task class to store task information
class Task:
    def __init__(self, task_id: int, title: str, description: str, status: str):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.status = status
        self.comments = []

    def add_comment(self, comment: str):
        self.comments.append(comment)

# CodeSquad class to manage the collaborative system
class CodeSquad:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.tasks: Dict[int, Task] = {}
        self.task_id_counter = 1
        self.lock = threading.Lock()

    def register_user(self, username: str, password: str, role: str):
        with self.lock:
            if username in self.users:
                print("Username already exists.")
                return
            self.users[username] = User(username, password, role)
            print("User registered successfully.")

    def login_user(self, username: str, password: str):
        with self.lock:
            if username not in self.users:
                print("Username does not exist.")
                return
            if self.users[username].password != password:
                print("Incorrect password.")
                return
            print("User logged in successfully.")

    def create_task(self, title: str, description: str):
        with self.lock:
            task = Task(self.task_id_counter, title, description, "Open")
            self.tasks[self.task_id_counter] = task
            self.task_id_counter += 1
            print("Task created successfully.")

    def view_tasks(self):
        with self.lock:
            for task in self.tasks.values():
                print(f"Task ID: {task.task_id}, Title: {task.title}, Status: {task.status}")

    def update_task_status(self, task_id: int, status: str):
        with self.lock:
            if task_id not in self.tasks:
                print("Task does not exist.")
                return
            self.tasks[task_id].status = status
            print("Task status updated successfully.")

    def add_comment_to_task(self, task_id: int, comment: str):
        with self.lock:
            if task_id not in self.tasks:
                print("Task does not exist.")
                return
            self.tasks[task_id].add_comment(comment)
            print("Comment added to task successfully.")

    def view_task_comments(self, task_id: int):
        with self.lock:
            if task_id not in self.tasks:
                print("Task does not exist.")
                return
            for comment in self.tasks[task_id].comments:
                print(comment)

# Chat class to manage real-time communication
class Chat:
    def __init__(self):
        self.messages: List[str] = []
        self.lock = threading.Lock()

    def send_message(self, message: str):
        with self.lock:
            self.messages.append(message)
            print("Message sent successfully.")

    def view_messages(self):
        with self.lock:
            for message in self.messages:
                print(message)

# VersionControl class to manage version control
class VersionControl:class Chat:
    def __init__(self, codesquad):
    def send_message_to_task(self, task_id, message):
        self.codesquad.add_comment_to_task(task_id, message)
        self.codesquad = codesquad
        self.messages: List[str] = []    def __init__(self):
        self.commits: List[str] = []
        self.lock = threading.Lock()

    def commit_changes(self, commit_message: str):
        with self.lock:
            self.commits.append(commit_message)
            print("Changes committed successfully.")

    def view_commits(self):
        with self.lock:
            for commit in self.commits:
                print(commit)

# Dashboard class to manage the dashboard
class Dashboard:
    def __init__(self):
        self.tasks: Dict[int, Task] = {}
        self.lock = threading.Lock()

    def view_tasks(self):
        with self.lock:
            for task in self.tasks.values():
                print(f"Task ID: {task.task_id}, Title: {task.title}, Status: {task.status}")

    def filter_tasks(self, status: str):
        with self.lock:
            for task in self.tasks.values():
                if task.status == status:
                    print(f"Task ID: {task.task_id}, Title: {task.title}, Status: {task.status}")

# Main function to run the CodeSquad system
def main():
    codesquad = CodeSquad()
    chat = Chat()
    version_control = VersionControl()
    dashboard = Dashboard()

    while True:
        print("1. Register User")
        print("2. Login User")
        print("3. Create Task")
        print("4. View Tasks")
        print("5. Update Task Status")
        print("6. Add Comment to Task")
        print("7. View Task Comments")
        print("8. Send Message")
        print("9. View Messages")
        print("10. Commit Changes")
        print("11. View Commits")
        print("12. View Dashboard")
        print("13. Filter Tasks")
        print("14. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            role = input("Enter role: ")
            codesquad.register_user(username, password, role)
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            codesquad.login_user(username, password)
        elif choice == "3":
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            codesquad.create_task(title, description)
        elif choice == "4":
            codesquad.view_tasks()
        elif choice == "5":
            task_id = int(input("Enter task ID: "))
            status = input("Enter task status: ")
            codesquad.update_task_status(task_id, status)
        elif choice == "6":
            task_id = int(input("Enter task ID: "))
            comment = input("Enter comment: ")
            codesquad.add_comment_to_task(task_id, comment)
        elif choice == "7":
            task_id = int(input("Enter task ID: "))
            codesquad.view_task_comments(task_id)
        elif choice == "8":
            message = input("Enter message: ")
            chat.send_message(message)
        elif choice == "9":
            chat.view_messages()
        elif choice == "10":
            commit_message = input("Enter commit message: ")
            version_control.commit_changes(commit_message)
        elif choice == "11":
            version_control.view_commits()
        elif choice == "12":
            dashboard.view_tasks()
        elif choice == "13":
            status = input("Enter task status: ")
            dashboard.filter_tasks(status)
        elif choice == "14":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()