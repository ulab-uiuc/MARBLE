    def generate_report(self):
        report = {}
        for project in self.projects.values():
            project_report = {}
            for task in project.tasks:
                task_report = {
                    "status": task.status.name,
                    "priority": task.priority.name,
                    "deadline": task.deadline,
                    "assigned_to": task.assigned_to
                }
                project_report[task.id] = task_report
            report[project.name] = project_report
        return report# office_task_collaborator.py

from datetime import datetime
from enum import Enum
from typing import List, Dict

class TaskStatus(Enum):
    """Enum for task status"""
    NOT_STARTED = 1
    IN_PROGRESS = 2
    COMPLETED = 3

class TaskPriority(Enum):
    """Enum for task priority"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class Task:
    """Class representing a task"""
    def __init__(self, id: int, description: str, deadline: datetime, priority: TaskPriority, assigned_to: str = None):
        self.id = id
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.assigned_to = assigned_to
        self.status = TaskStatus.NOT_STARTED

    def update_status(self, status: TaskStatus):
        """Update the status of the task"""
        self.status = status

class User:
    """Class representing a user"""
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.tasks = []

    def assign_task(self, task: Task):
        """Assign a task to the user"""
        self.tasks.append(task)

class Project:
    """Class representing a project"""
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.tasks = []

    def add_task(self, task: Task):
        """Add a task to the project"""
        self.tasks.append(task)

class OfficeTaskCollaborator:
    """Class representing the office task collaborator system"""
    def __init__(self):
        self.users = {}
        self.projects = {}
        self.tasks = {}

    def create_user(self, id: int, name: str):
        """Create a new user"""
        self.users[id] = User(id, name)

    def create_project(self, id: int, name: str):
        """Create a new project"""
        self.projects[id] = Project(id, name)

    def create_task(self, id: int, description: str, deadline: datetime, priority: TaskPriority, project_id: int, assigned_to: str = None):
        """Create a new task"""
        task = Task(id, description, deadline, priority, assigned_to)
        self.tasks[id] = task
        self.projects[project_id].add_task(task)
        if assigned_to:
            self.users[assigned_to].assign_task(task)

    def update_task_status(self, task_id: int, status: TaskStatus):
        """Update the status of a task"""
        self.tasks[task_id].update_status(status)

    def get_user_tasks(self, user_id: int):
        """Get the tasks assigned to a user"""
        return self.users[user_id].tasks

    def get_project_tasks(self, project_id: int):
        """Get the tasks in a project"""
        return self.projects[project_id].tasks

def generate_report(self):
        report = {}
        for project in self.projects.values():
            project_report = {}
            for task in project.tasks:
                task_report = {
                    "status": task.status.name,
                    "priority": task.priority.name,
                    "deadline": task.deadline,
                    "assigned_to": task.assigned_to
                }
                project_report[task.id] = task_report
            report[project.name] = project_report
        return report

# calendar_integration.py

import datetime
import calendar

class CalendarIntegration:
    """Class representing calendar integration"""
    def __init__(self):
        self.calendars = {}

    def add_calendar(self, calendar_name: str):
        """Add a calendar"""
        self.calendars[calendar_name] = []

    def sync_task_deadline(self, task: Task, calendar_name: str):
        """Sync a task deadline with a calendar"""
        self.calendars[calendar_name].append(task.deadline)

    def get_upcoming_deadlines(self, calendar_name: str):
        """Get the upcoming deadlines in a calendar"""
        upcoming_deadlines = []
        for deadline in self.calendars[calendar_name]:
            if deadline > datetime.datetime.now():
                upcoming_deadlines.append(deadline)
        return upcoming_deadlines

# messaging.py

class Messaging:
    """Class representing messaging"""
    def __init__(self):
        self.messages = {}

    def send_message(self, sender: str, recipient: str, message: str):
        """Send a message"""
        if recipient not in self.messages:
            self.messages[recipient] = []
        self.messages[recipient].append((sender, message))

    def get_messages(self, recipient: str):
        """Get the messages for a recipient"""
        return self.messages.get(recipient, [])

# solution.py

def main():
    # Create the office task collaborator system
    office_task_collaborator = OfficeTaskCollaborator()

    # Create users
    office_task_collaborator.create_user(1, "John Doe")
    office_task_collaborator.create_user(2, "Jane Doe")

    # Create projects
    office_task_collaborator.create_project(1, "Project 1")
    office_task_collaborator.create_project(2, "Project 2")

    # Create tasks
    office_task_collaborator.create_task(1, "Task 1", datetime.datetime(2024, 3, 16), TaskPriority.HIGH, 1, 1)
    office_task_collaborator.create_task(2, "Task 2", datetime.datetime(2024, 3, 17), TaskPriority.MEDIUM, 1, 2)
    office_task_collaborator.create_task(3, "Task 3", datetime.datetime(2024, 3, 18), TaskPriority.LOW, 2, 1)

    # Update task status
    office_task_collaborator.update_task_status(1, TaskStatus.IN_PROGRESS)

    # Get user tasks
    user_tasks = office_task_collaborator.get_user_tasks(1)
    for task in user_tasks:
        print(f"Task {task.id}: {task.description}")

    # Get project tasks
    project_tasks = office_task_collaborator.get_project_tasks(1)
    for task in project_tasks:
        print(f"Task {task.id}: {task.description}")

    # Generate report
    report = office_task_collaborator.generate_report()
    for project, tasks in report.items():
        print(f"Project: {project}")
        for task, status in tasks.items():
            print(f"Task {task}: {status}")

    # Integrate with calendar
    calendar_integration = CalendarIntegration()
    calendar_integration.add_calendar("Google Calendar")
    calendar_integration.sync_task_deadline(office_task_collaborator.tasks[1], "Google Calendar")
    upcoming_deadlines = calendar_integration.get_upcoming_deadlines("Google Calendar")
    for deadline in upcoming_deadlines:
        print(f"Upcoming deadline: {deadline}")

    # Send message
    messaging = Messaging()
    messaging.send_message("John Doe", "Jane Doe", "Hello!")
    messages = messaging.get_messages("Jane Doe")
    for sender, message in messages:
        print(f"Message from {sender}: {message}")

if __name__ == "__main__":
    main()