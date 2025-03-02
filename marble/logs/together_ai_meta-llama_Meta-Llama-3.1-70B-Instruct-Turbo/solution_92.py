
for dependent_task in self.tasks.values():
            if task.name in dependent_task.dependencies:
                if all(dependency_task.status == TaskStatus.COMPLETED for dependency_task in self.tasks.values() if dependency_task.name in dependent_task.dependencies):
                    dependent_task.update_status(TaskStatus.IN_PROGRESS, self)
if self.can_update_status(status, project):
            self.status = status
        else:
            raise ValueError("Cannot update task status due to uncompleted dependencies")# project_manager.py

from datetime import datetime
from enum import Enum
from typing import List, Dict

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

class Task:
    """Task with name, description, deadline, dependencies, and status."""
    def __init__(self, name: str, description: str, deadline: datetime, dependencies: List[str] = None):
    def can_update_status(self, status: TaskStatus, project: Project) -> bool:def update_status(self, status: TaskStatus, project: Project):def assign_task(self, user: str):
        """Assign task to a user."""
        self.assigned_to = user

class Project:
    """Project with tasks and users."""
    def __init__(self, name: str):
        self.name = name
        self.tasks = {}
        self.users = {}

    def add_task(self, task: Task):
    def update_dependent_tasks(self, task: Task):
        """Update status of dependent tasks when a task is completed."""
        for dependent_task in self.tasks.values():
            if task.name in dependent_task.dependencies:
                dependent_task.update_status(TaskStatus.IN_PROGRESS, self)
        """Add task to project."""
        self.tasks[task.name] = task

    def add_user(self, user: str, role: UserRole):def update_dependent_tasks(self, task: Task):def get_task(self, task_name: str):
        """Get task by name."""
        return self.tasks.get(task_name)

    def get_user(self, user: str):
        """Get user by name."""
        return self.users.get(user)

class ProjectManager:
    """Project manager with projects and notification system."""
    def __init__(self):
        self.projects = {}
        self.notifications = []

    def add_project(self, project: Project):
        """Add project to project manager."""
        self.projects[project.name] = project

    def get_project(self, project_name: str):
        """Get project by name."""
        return self.projects.get(project_name)

    def send_notification(self, notification: str):
        """Send notification to users."""
        self.notifications.append(notification)

    def get_notifications(self):
        """Get all notifications."""
        return self.notifications

class HistoryLog:
    """History log with task changes."""
    def __init__(self):
        self.log = []

    def add_log(self, log: str):
        """Add log to history log."""
        self.log.append(log)

    def get_log(self):
        """Get all logs."""
        return self.log

def main():
    # Create project manager
    project_manager = ProjectManager()

    # Create project
    project = Project("My Project")
    project_manager.add_project(project)

    # Create tasks
    task1 = Task("Task 1", "Description 1", datetime(2024, 3, 16))
    task2 = Task("Task 2", "Description 2", datetime(2024, 3, 17), dependencies=["Task 1"])
    task3 = Task("Task 3", "Description 3", datetime(2024, 3, 18), dependencies=["Task 1", "Task 2"])

    # Add tasks to project
    project.add_task(task1)
    project.add_task(task2)
    project.add_task(task3)

    # Create users
    project.add_user("John Doe", UserRole.PROJECT_MANAGER)
    project.add_user("Jane Doe", UserRole.TEAM_LEAD)
    project.add_user("Bob Smith", UserRole.TEAM_MEMBER)

    # Assign tasks to users
    task1.assign_task("John Doe")
    task2.assign_task("Jane Doe")
    task3.assign_task("Bob Smith")

    # Update task status
    task1.update_status(TaskStatus.IN_PROGRESS)
    task2.update_status(TaskStatus.PENDING)
    task3.update_status(TaskStatus.DELAYED)

    # Send notifications
    project_manager.send_notification("Task 1 assigned to John Doe")
    project_manager.send_notification("Task 2 assigned to Jane Doe")
    project_manager.send_notification("Task 3 assigned to Bob Smith")

    # Create history log
    history_log = HistoryLog()
    history_log.add_log("Task 1 created")
    history_log.add_log("Task 2 created")
    history_log.add_log("Task 3 created")
    history_log.add_log("Task 1 assigned to John Doe")
    history_log.add_log("Task 2 assigned to Jane Doe")
    history_log.add_log("Task 3 assigned to Bob Smith")

    # Print project information
    print("Project Name:", project.name)
    print("Tasks:")
    for task in project.tasks.values():
        print("Task Name:", task.name)
        print("Task Description:", task.description)
        print("Task Deadline:", task.deadline)
        print("Task Dependencies:", task.dependencies)
        print("Task Status:", task.status)
        print("Task Assigned To:", task.assigned_to)
    print("Users:")
    for user, role in project.users.items():
        print("User Name:", user)
        print("User Role:", role)
    print("Notifications:")
    for notification in project_manager.get_notifications():
        print(notification)
    print("History Log:")
    for log in history_log.get_log():
        print(log)

if __name__ == "__main__":
    main()