# solution.py
from datetime import datetime
from enum import Enum
from typing import List, Dict

# Define user roles
class UserRole(Enum):
    PROJECT_MANAGER = 1
    TEAM_LEAD = 2
    TEAM_MEMBER = 3

# Define task status
class TaskStatus(Enum):
    PENDING = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    DELAYED = 4

# Define notification types
class NotificationType(Enum):
    TASK_ASSIGNED = 1
    DEPENDENCY_MET = 2
    TASK_COMPLETED = 3

# Define notification channels
class NotificationChannel(Enum):
    EMAIL = 1
    IN_APP = 2

# User class
class User:
    def __init__(self, id: int, name: str, role: UserRole):
        self.id = id
        self.name = name
        self.role = role

# Task class
class Task:
    def __init__(self, id: int, name: str, description: str, deadline: datetime, dependencies: List[int]):
        self.id = id
        self.name = name
        self.description = description
        self.deadline = deadline
        self.dependencies = dependencies
        self.status = TaskStatus.PENDING
        self.assigned_to = None

    def update_status(self, status: TaskStatus):
        self.status = status

    def assign_to(self, user: User):
        self.assigned_to = user

# Project class
class Project:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.tasks = {}

    def add_task(self, task: Task):
        self.tasks[task.id] = task

    def get_task(self, task_id: int):
        return self.tasks.get(task_id)

# Notification class
class Notification:
    def __init__(self, type: NotificationType, user: User, task: Task, channel: NotificationChannel):
        self.type = type
        self.user = user
        self.task = task
        self.channel = channel

    def send(self):
        # Send notification logic here
        print(f"Notification sent to {self.user.name} via {self.channel.name}")

# History log class
class HistoryLog:
    def __init__(self):
        self.log = []

    def add_entry(self, task: Task, user: User, action: str):
        self.log.append((task, user, action))

    def get_log(self):
        return self.log

# MultiAgent Project Manager class
class MultiAgentProjectManager:
    def __init__(self):
        self.projects = {}
        self.users = {}
        self.notifications = []
        self.history_log = HistoryLog()

    def create_project(self, project_name: str):
        project_id = len(self.projects) + 1
        project = Project(project_id, project_name)
        self.projects[project_id] = project

    def create_task(self, project_id: int, task_name: str, task_description: str, deadline: datetime, dependencies: List[int]):def assign_task(self, project_id: int, task_id: int, user_id: int):
    task = self.projects[project_id].get_task(task_id)
    user = self.users.get(user_id)
    if task and user:
        task.assign_to(user)
        self.history_log.add_entry(task, user, "assigned")
    else:
        raise Exception("Task or user not found")def update_task_status(self, project_id: int, task_id: int, status: TaskStatus):
        task = self.projects[project_id].get_task(task_id)
        if task:
            dependencies_completed = all(self.projects[project_id].get_task(dependency).status == TaskStatus.COMPLETED for dependency in task.dependencies)
            if status == TaskStatus.IN_PROGRESS and not dependencies_completed:
                raise Exception("Cannot start task until all dependencies are completed")
            if status == TaskStatus.COMPLETED and not dependencies_completed:
                raise Exception("Cannot complete task until all dependencies are completed")
            task.update_status(status)
            if status == TaskStatus.COMPLETED:
                notification = Notification(NotificationType.TASK_COMPLETED, task.assigned_to, task, NotificationChannel.EMAIL)
                self.notifications.append(notification)
            self.history_log.add_entry(task, task.assigned_to, "status updated")def get_project_dashboard(self, project_id: int):
        project = self.projects.get(project_id)
        if project:
            pending_tasks = [task for task in project.tasks.values() if task.status == TaskStatus.PENDING]
            in_progress_tasks = [task for task in project.tasks.values() if task.status == TaskStatus.IN_PROGRESS]
            completed_tasks = [task for task in project.tasks.values() if task.status == TaskStatus.COMPLETED]
            return pending_tasks, in_progress_tasks, completed_tasks

    def send_notifications(self):
        for notification in self.notifications:
            notification.send()

    def get_history_log(self):
        return self.history_log.get_log()

# Create a MultiAgent Project Manager instance
project_manager = MultiAgentProjectManager()

# Create users
user1 = User(1, "John Doe", UserRole.PROJECT_MANAGER)
user2 = User(2, "Jane Doe", UserRole.TEAM_MEMBER)
project_manager.users[user1.id] = user1
project_manager.users[user2.id] = user2

# Create a project
project_manager.create_project("Sample Project")

# Create tasks
project_manager.create_task(1, "Task 1", "Task 1 description", datetime(2024, 12, 31), [])
project_manager.create_task(1, "Task 2", "Task 2 description", datetime(2024, 12, 31), [1])

# Assign tasks
project_manager.assign_task(1, 1, 2)
project_manager.assign_task(1, 2, 2)

# Update task status
project_manager.update_task_status(1, 1, TaskStatus.COMPLETED)

# Get project dashboard
pending_tasks, in_progress_tasks, completed_tasks = project_manager.get_project_dashboard(1)
print("Pending tasks:")
for task in pending_tasks:
    print(task.name)
print("In progress tasks:")
for task in in_progress_tasks:
    print(task.name)
print("Completed tasks:")
for task in completed_tasks:
    print(task.name)

# Send notifications
project_manager.send_notifications()

# Get history log
history_log = project_manager.get_history_log()
for entry in history_log:
    print(f"Task {entry[0].name} was {entry[2]} by {entry[1].name}")