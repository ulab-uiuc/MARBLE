# project_manager.py

from enum import Enum
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserRole(Enum):
    """User roles with different levels of access and responsibilities."""
    PROJECT_MANAGER = 1
    TEAM_LEAD = 2
    TEAM_MEMBER = 3

class TaskStatus(Enum):
    """Task status."""
    PENDING = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    DELAYED = 4

class Task:def update_status(self, status):
    if status == TaskStatus.COMPLETED:
        for dependency in self.dependencies:
            dependency_task = next((task for task in self.project.tasks if task.name == dependency), None)
            if dependency_task and dependency_task.status != TaskStatus.COMPLETED:
                raise ValueError(f"Cannot complete task {self.name} because dependency {dependency} has not been completed")self.status = status
        self.history_log.append(f"Task status updated to {status} on {datetime.now()}")
        logger.info(f"Task {self.name} status updated to {status}")

    def send_notification(self, message):
        """Send notification to assigned user."""
        if self.assigned_to:
            logger.info(f"Notification sent to {self.assigned_to}: {message}")

class Project:def add_task(self, task):
    task.project = self
    self.tasks.append(task)self.tasks.append(task)
        logger.info(f"Task {task.name} added to project {self.name}")

    def add_user(self, user):
        """Add user to project."""
        self.users.append(user)
        logger.info(f"User {user} added to project {self.name}")

    def get_task(self, task_name):
        """Get task by name."""
        for task in self.tasks:
            if task.name == task_name:
                return task
        return None

class User:
    """User with role and assigned tasks."""
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.assigned_tasks = []

    def assign_task(self, task):
        """Assign task to user."""
        self.assigned_tasks.append(task)
        task.assign(self.name)
        logger.info(f"Task {task.name} assigned to user {self.name}")

class MultiAgentProjectManager:def update_task_status(self, project, task_name, status):
    task = project.get_task(task_name)
    if task:
        try:
            task.update_status(status)
        except ValueError as e:
            logger.error(f"Error updating task status: {e}")task.update_status(status)
        else:
            logger.error(f"Task {task_name} not found in project {project.name}")

    def send_notification(self, project, task_name, message):
        """Send notification."""
        task = project.get_task(task_name)
        if task:
            task.send_notification(message)
        else:
            logger.error(f"Task {task_name} not found in project {project.name}")

# Example usage
if __name__ == "__main__":
    project_manager = MultiAgentProjectManager()

    # Create project
    project = project_manager.create_project("My Project")

    # Create tasks
    task1 = project_manager.create_task(project, "Task 1", "Description 1", datetime(2024, 3, 16))
    task2 = project_manager.create_task(project, "Task 2", "Description 2", datetime(2024, 3, 17), dependencies=["Task 1"])

    # Create users
    user1 = project_manager.create_user("John Doe", UserRole.TEAM_MEMBER)
    user2 = project_manager.create_user("Jane Doe", UserRole.TEAM_LEAD)

    # Assign tasks to users
    project_manager.assign_task_to_user(project, "Task 1", user1)
    project_manager.assign_task_to_user(project, "Task 2", user2)

    # Update task status
    project_manager.update_task_status(project, "Task 1", TaskStatus.COMPLETED)

    # Send notification
    project_manager.send_notification(project, "Task 1", "Task completed")