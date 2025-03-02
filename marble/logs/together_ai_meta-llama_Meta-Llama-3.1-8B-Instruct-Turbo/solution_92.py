# solution.py

# Importing required libraries
import datetime
import logging
from enum import Enum
from typing import List, Dict

# Setting up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    def __init__(self, name: str, description: str, deadline: datetime.date, dependencies: List[str] = None):
        self.name = name
        self.description = description
        self.deadline = deadline
        self.dependencies = dependencies if dependencies else []
        self.status = TaskStatus.PENDING
        self.history = []

    def update_status(self, status: TaskStatus):
        self.status = statusself.history.append(f"Task {self.name} completed")
if not self.dependencies:
    project.remove_task(self.name)
    project.history.append(f"Task {self.name} removed")
        self.history.append(f"Status updated to {status.name}")

    def add_dependency(self, task_name: str):
        self.dependencies.append(task_name)

    def remove_dependency(self, task_name: str):
        self.dependencies.remove(task_name)

# Defining project class
class Project:
    def __init__(self, name: str):
        self.name = name
        self.tasks = {}
        self.history = []

    def add_task(self, task: Task):
        self.tasks[task.name] = task
        self.history.append(f"Task {task.name} added")

    def remove_task(self, task_name: str):
        if task_name in self.tasks:
            del self.tasks[task_name]
            self.history.append(f"Task {task_name} removed")

    def update_task_status(self, task_name: str, status: TaskStatus):
        if task_name in self.tasks:
            self.tasks[task_name].update_status(status)
            self.history.append(f"Task {task_name} status updated to {status.name}")

# Defining user class
class User:
    def __init__(self, name: str, role: UserRole):
        self.name = name
        self.role = role
        self.tasks = {}

    def assign_task(self, task: Task):
        self.tasks[task.name] = task
        logger.info(f"Task {task.name} assigned to {self.name}")

    def update_task_status(self, task_name: str, status: TaskStatus):
        if task_name in self.tasks:
            self.tasks[task_name].update_status(status)
            logger.info(f"Task {task_name} status updated to {status.name}")

# Defining notification class
class Notification:
    def __init__(self, subject: str, message: str, recipient: User):
        self.subject = subject
        self.message = message
        self.recipient = recipient

    def send(self):
        logger.info(f"Notification sent to {self.recipient.name}: {self.subject} - {self.message}")

# Defining project manager class
class ProjectManager(User):
    def __init__(self, name: str):
        super().__init__(name, UserRole.PROJECT_MANAGER)

    def create_project(self, project_name: str):
        project = Project(project_name)
        logger.info(f"Project {project_name} created")
        return project

    def assign_task(self, project: Project, task: Task):
        project.add_task(task)
        self.assign_task(task)

# Defining team lead class
class TeamLead(User):
    def __init__(self, name: str):
        super().__init__(name, UserRole.TEAM_LEAD)

    def assign_task(self, project: Project, task: Task):
        project.add_task(task)
        self.assign_task(task)

# Defining team member class
class TeamMember(User):
    def __init__(self, name: str):
        super().__init__(name, UserRole.TEAM_MEMBER)

    def update_task_status(self, project: Project, task_name: str, status: TaskStatus):
        project.update_task_status(task_name, status)
        self.update_task_status(task_name, status)

# Defining main function
def main():
    # Creating project manager
    project_manager = ProjectManager("John Doe")

    # Creating project
    project = project_manager.create_project("My Project")

    # Creating tasks
    task1 = Task("Task 1", "This is task 1", datetime.date(2024, 3, 16))
    task2 = Task("Task 2", "This is task 2", datetime.date(2024, 3, 17), ["Task 1"])
    task3 = Task("Task 3", "This is task 3", datetime.date(2024, 3, 18), ["Task 2"])

    # Adding tasks to project
    project.add_task(task1)
    project.add_task(task2)
    project.add_task(task3)

    # Assigning tasks to team members
    team_member1 = TeamMember("Jane Doe")
    team_member2 = TeamMember("Bob Smith")
    team_member3 = TeamMember("Alice Johnson")

    project_manager.assign_task(project, task1)
    project_manager.assign_task(project, task2)
    project_manager.assign_task(project, task3)

    team_member1.assign_task(project, task1)
    team_member2.assign_task(project, task2)
    team_member3.assign_task(project, task3)

    # Updating task status
    team_member1.update_task_status(project, "Task 1", TaskStatus.IN_PROGRESS)
    team_member2.update_task_status(project, "Task 2", TaskStatus.IN_PROGRESS)
    team_member3.update_task_status(project, "Task 3", TaskStatus.IN_PROGRESS)

    # Sending notifications
    notification1 = Notification("Task 1 updated", "Task 1 is in progress", team_member1)
    notification2 = Notification("Task 2 updated", "Task 2 is in progress", team_member2)
    notification3 = Notification("Task 3 updated", "Task 3 is in progress", team_member3)

    notification1.send()
    notification2.send()
    notification3.send()

    # Printing project history
    logger.info("Project History:")
    for entry in project.history:
        logger.info(entry)

# Running main function
if __name__ == "__main__":
    main()