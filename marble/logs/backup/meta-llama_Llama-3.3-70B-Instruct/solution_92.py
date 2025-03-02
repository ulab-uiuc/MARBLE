# solution.py
from enum import Enum
from datetime import datetime
from typing import List, Dictfrom enum import Enum

class TaskStatus(Enum):
    PENDING = 1
    IN_PROGRESS = 2
    COMPLETED = 3

class Task:def assign_to(self, user: str, project: Project):self.assigned_to = user
        self.history.append((f"Assigned to {user}", datetime.now()))
        if not project.check_dependencies(self.name):
            print("Cannot assign task: dependencies not met")
            return        self.assigned_to = user
        self.history.append((f"Assigned to {user}", datetime.now()))

# Define a class for projects
class Project:
    def __init__(self, name: str):
    def check_dependencies(self, task_name: str) -> bool:
        task = self.tasks.get(task_name)
        if task:
            for dependency in task.dependencies:
                dependency_task = self.tasks.get(dependency)
                if dependency_task and dependency_task.status != TaskStatus.COMPLETED:
                    return False
            return True
        return False
        # Initialize project attributes
        self.name = name
        self.tasks = {}
        self.users = {}

    def add_task(self, task: Task):
        # Add a task to the project
        self.tasks[task.name] = task

    def add_user(self, user: str, role: UserRole):
        # Add a user to the project
        self.users[user] = role

    def get_task_status(self, task_name: str):
        # Get the status of a task
        task = self.tasks.get(task_name)
        if task:
            return task.status
        return None

    def get_user_role(self, user: str):
        # Get the role of a user
        return self.users.get(user)

# Define a class for the project manager
class ProjectManager:
    def __init__(self):
        # Initialize project manager attributes
        self.projects = {}

    def create_project(self, project_name: str):    def add_task_to_project(self, project_name: str, task: Task):
        project = self.projects.get(project_name)
        if project and not project.check_dependencies(task.name):
            print("Cannot add task to project: dependencies not met")
            return
        project.add_task(task)        project.add_task(task)

    def add_user_to_project(self, project_name: str, user: str, role: UserRole):
        # Add a user to a project
        project = self.projects.get(project_name)
        if project:
            project.add_user(user, role)

    def get_project_status(self, project_name: str):
        # Get the status of a project
        project = self.projects.get(project_name)
        if project:
            task_status = {}
            for task_name, task in project.tasks.items():
                task_status[task_name] = task.status
            return task_status
        return None

    def send_notification(self, project_name: str, task_name: str, notification: str):
        # Send a notification to users
        project = self.projects.get(project_name)
        if project:
            task = project.tasks.get(task_name)
            if task:
                # Send notification to assigned user
                if task.assigned_to:
                    print(f"Notification sent to {task.assigned_to}: {notification}")
                # Send notification to project users
                for user, role in project.users.items():
                    print(f"Notification sent to {user}: {notification}")

# Define a class for the dashboard
class Dashboard:
    def __init__(self, project_manager: ProjectManager):
        # Initialize dashboard attributes
        self.project_manager = project_manager

    def display_project_status(self, project_name: str):
        # Display the status of a project
        project_status = self.project_manager.get_project_status(project_name)
        if project_status:
            print(f"Project {project_name} Status:")
            for task_name, status in project_status.items():
                print(f"Task {task_name}: {status.name}")
        else:
            print(f"Project {project_name} not found")

# Usage example
project_manager = ProjectManager()
project_manager.create_project("My Project")

task1 = Task("Task 1", "Description 1", datetime(2024, 12, 31))
task2 = Task("Task 2", "Description 2", datetime(2024, 12, 31), dependencies=["Task 1"])

project_manager.add_task_to_project("My Project", task1)
project_manager.add_task_to_project("My Project", task2)

project_manager.add_user_to_project("My Project", "John Doe", UserRole.TEAM_MEMBER)
project_manager.add_user_to_project("My Project", "Jane Doe", UserRole.PROJECT_MANAGER)

dashboard = Dashboard(project_manager)
dashboard.display_project_status("My Project")

project_manager.send_notification("My Project", "Task 1", "Task assigned to John Doe")