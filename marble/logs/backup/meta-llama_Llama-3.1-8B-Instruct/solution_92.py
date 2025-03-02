# solution.py

# Importing required libraries
import datetime
import threading
import time
from enum import Enum
from typing import List

# Defining user roles
class UserRole(Enum):
    PROJECT_MANAGER = 1
    TEAM_LEAD = 2
    TEAM_MEMBER = 3

# Defining task status
class TaskStatus(Enum):
    PENDING = 1
    IN_PROGRESS = 2
    COMPLETED = 3

# Defining task class
class Task:
    def __init__(self, name: str, description: str, deadline: datetime.date, dependencies: List['Task'] = None):
        self.name = name
        self.description = description
        self.deadline = deadline
        self.dependencies = dependencies if dependencies else []
        self.status = TaskStatus.PENDING
        self.assigned_to = None
        self.history = []

    def assign(self, user):
        if self.status == TaskStatus.PENDING:
            self.assigned_to = user
            self.history.append(f"Task {self.name} assigned to {user.name}")
            threading.Thread(target=self.send_notification).start()
        else:
            raise Exception(f"Task {self.name} is not pending")

    def update_status(self, status: TaskStatus):
        if self.status != status:
            self.status = status
            self.history.append(f"Task {self.name} status updated to {status.name}")
            threading.Thread(target=self.send_notification).start()

    def complete(self):
        if self.status == TaskStatus.IN_PROGRESS:
            self.status = TaskStatus.COMPLETED
            self.history.append(f"Task {self.name} completed")
            threading.Thread(target=self.send_notification).start()

    def send_notification(self):
        # Simulating notification sending
        print(f"Notification sent to {self.assigned_to.name} for task {self.name}")

# Defining user class
class User:
    def __init__(self, name: str, role: UserRole):
        self.name = name
        self.role = role

# Defining project class
class Project:
    def __init__(self, name: str):
        self.name = name
        self.tasks = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def get_task_status(self):
        status = {}
        for task in self.tasks:
            status[task.name] = task.status.name
        return status

# Defining project manager class
class ProjectManager:
    def __init__(self):
        self.projects = {}
        self.users = {}

    def create_project(self, project_name: str):
        self.projects[project_name] = Project(project_name)

    def create_user(self, user_name: str, role: UserRole):
        self.users[user_name] = User(user_name, role)

    def assign_task(self, project_name: str, task_name: str, user_name: str):
        project = self.projects[project_name]
        task = next((t for t in project.tasks if t.name == task_name), None)
        if task:
            user = self.users[user_name]
            task.assign(user)
        else:
            raise Exception(f"Task {task_name} not found in project {project_name}")

    def update_task_status(self, project_name: str, task_name: str, status: TaskStatus):
        project = self.projects[project_name]
        task = next((t for t in project.tasks if t.name == task_name), None)
        if task:
            task.update_status(status)
        else:
            raise Exception(f"Task {task_name} not found in project {project_name}")

    def complete_task(self, project_name: str, task_name: str):
        project = self.projects[project_name]
        task = next((t for t in project.tasks if t.name == task_name), None)
        if task:
            task.complete()
        else:
            raise Exception(f"Task {task_name} not found in project {project_name}")

    def get_project_status(self, project_name: str):
        project = self.projects[project_name]
        return project.get_task_status()

# Creating a project manager instance
project_manager = ProjectManager()

# Creating a project
project_manager.create_project("My Project")

# Creating users
project_manager.create_user("John Doe", UserRole.PROJECT_MANAGER)
project_manager.create_user("Jane Doe", UserRole.TEAM_MEMBER)

# Creating tasks
task1 = Task("Task 1", "This is task 1", datetime.date(2024, 7, 31))
task2 = Task("Task 2", "This is task 2", datetime.date(2024, 8, 31), [task1])
task3 = Task("Task 3", "This is task 3", datetime.date(2024, 9, 31), [task2])

# Adding tasks to the project
project_manager.projects["My Project"].add_task(task1)
project_manager.projects["My Project"].add_task(task2)
project_manager.projects["My Project"].add_task(task3)

# Assigning tasks to users
project_manager.assign_task("My Project", "Task 1", "John Doe")
project_manager.assign_task("My Project", "Task 2", "Jane Doe")

# Updating task status
project_manager.update_task_status("My Project", "Task 1", TaskStatus.IN_PROGRESS)

# Completing tasks
project_manager.complete_task("My Project", "Task 1")

# Getting project status
print(project_manager.get_project_status("My Project"))