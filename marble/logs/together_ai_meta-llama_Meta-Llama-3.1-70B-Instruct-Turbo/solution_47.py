# office_task_collaborator.py

from datetime import datetime
from enum import Enum
from typing import List, Dict

# Define an Enum for task status
class TaskStatus(Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

# Define an Enum for task priority
class TaskPriority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

# Define a class for User
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.tasks = []

    def assign_task(self, task):
        self.tasks.append(task)

# Define a class for Task
class Task:
    def __init__(self, title: str, description: str, deadline: datetime, priority: TaskPriority, assigned_to: User):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.assigned_to = assigned_to
        self.status = TaskStatus.NOT_STARTED
        self.messages = []

    def update_status(self, status: TaskStatus):
        self.status = status

    def add_message(self, message: str):
        self.messages.append(message)

# Define a class for Project
class Project:
    def __init__(self, name: str):
        self.name = name
        self.tasks = []

    def add_task(self, task: Task):
        self.tasks.append(task)

# Define a class for OfficeTaskCollaborator
class OfficeTaskCollaborator:
    def __init__(self):
        self.users = []
        self.projects = []

    def add_user(self, user: User):
        self.users.append(user)

    def add_project(self, project: Project):
        self.projects.append(project)

    def create_task(self, title: str, description: str, deadline: datetime, priority: TaskPriority, assigned_to: User, project: Project):
        task = Task(title, description, deadline, priority, assigned_to)
        project.add_task(task)
        assigned_to.assign_task(task)

    def generate_report(self, project: Project):
        report = {
            "project_name": project.name,
            "tasks": []
        }
        for task in project.tasks:
            task_report = {
                "title": task.title,
                "status": task.status.value,
                "deadline": task.deadline.strftime("%Y-%m-%d"),
                "priority": task.priority.value,
                "assigned_to": task.assigned_to.name
            }
            report["tasks"].append(task_report)
        return report

    def sync_with_calendar(self, project: Project):
        # This method should be implemented to sync with calendar applications
        # For simplicity, it's not implemented here
        pass

# Define a class for Calendar
class Calendar:
    def __init__(self):
        self.events = []

    def add_event(self, event: str):
        self.events.append(event)

    def sync_with_office_task_collaborator(self, office_task_collaborator: OfficeTaskCollaborator):
        # This method should be implemented to sync with OfficeTaskCollaborator
        # For simplicity, it's not implemented here
        pass

# Test cases
def test_create_task():
    office_task_collaborator = OfficeTaskCollaborator()
    user = User("John Doe", "john@example.com")
    project = Project("Test Project")
    office_task_collaborator.add_user(user)
    office_task_collaborator.add_project(project)
    deadline = datetime(2024, 3, 16)
    office_task_collaborator.create_task("Test Task", "This is a test task", deadline, TaskPriority.HIGH, user, project)
    assert len(project.tasks) == 1
    assert len(user.tasks) == 1

def test_assign_task():
    office_task_collaborator = OfficeTaskCollaborator()
    user1 = User("John Doe", "john@example.com")
    user2 = User("Jane Doe", "jane@example.com")
    project = Project("Test Project")
    office_task_collaborator.add_user(user1)
    office_task_collaborator.add_user(user2)
    office_task_collaborator.add_project(project)
    deadline = datetime(2024, 3, 16)
    office_task_collaborator.create_task("Test Task", "This is a test task", deadline, TaskPriority.HIGH, user1, project)
    assert len(user1.tasks) == 1
    assert len(user2.tasks) == 0

def test_update_task_status():
    office_task_collaborator = OfficeTaskCollaborator()
    user = User("John Doe", "john@example.com")
    project = Project("Test Project")
    office_task_collaborator.add_user(user)
    office_task_collaborator.add_project(project)
    deadline = datetime(2024, 3, 16)
    office_task_collaborator.create_task("Test Task", "This is a test task", deadline, TaskPriority.HIGH, user, project)
    task = project.tasks[0]
    task.update_status(TaskStatus.IN_PROGRESS)
    assert task.status == TaskStatus.IN_PROGRESS

def test_generate_report():
    office_task_collaborator = OfficeTaskCollaborator()
    user = User("John Doe", "john@example.com")
    project = Project("Test Project")
    office_task_collaborator.add_user(user)
    office_task_collaborator.add_project(project)
    deadline = datetime(2024, 3, 16)
    office_task_collaborator.create_task("Test Task", "This is a test task", deadline, TaskPriority.HIGH, user, project)
    report = office_task_collaborator.generate_report(project)
    assert report["project_name"] == project.name
    assert len(report["tasks"]) == 1

def test_sync_with_calendar():
    # This test case should be implemented to test the sync_with_calendar method
    # For simplicity, it's not implemented here
    pass

# Run test cases
test_create_task()
test_assign_task()
test_update_task_status()
test_generate_report()
test_sync_with_calendar()