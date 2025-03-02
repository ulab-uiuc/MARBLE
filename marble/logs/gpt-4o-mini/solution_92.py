# solution.py

from datetime import datetime
from typing import List, Dict, Optional

# Define user roles as constants
class UserRole:
    PROJECT_MANAGER = "Project Manager"
    TEAM_LEAD = "Team Lead"
    TEAM_MEMBER = "Team Member"

# Task class to represent a task in the project
class Task:
    def __init__(self, name: str, description: str, deadline: datetime, dependencies: List[str] = None):
        self.name = name
        self.description = description
        self.deadline = deadline
        self.dependencies = dependencies if dependencies else []
        self.status = "Pending"  # Task status can be Pending, In Progress, or Completed
        self.history = []  # History log for tracking changes

    def update_status(self, new_status: str):
        """Update the status of the task and log the change."""
self.assignee = None  # Store the assignee of the task
        self.history.append((self.status, new_status, datetime.now()))
        self.status = new_status

# Project class to represent a project containing multiple tasks
class Project:
    def __init__(self, name: str):
        self.name = name
        self.tasks: Dict[str, Task] = {}  # Dictionary to hold tasks by name

    def add_task(self, task: Task):
        """Add a task to the project."""
        self.tasks[task.name] = task

    def get_dashboard(self) -> Dict[str, List[str]]:
        """Generate a dashboard of task statuses."""
        dashboard = {
            "Pending": [],
            "In Progress": [],
            "Completed": [],
            "Delayed": []
        }
        for task in self.tasks.values():
            if task.status == "Pending":
                dashboard["Pending"].append(task.name)
            elif task.status == "In Progress":
                dashboard["In Progress"].append(task.name)
            elif task.status == "Completed":
                dashboard["Completed"].append(task.name)
            # Check for delays
            if task.status != "Completed" and task.deadline < datetime.now():
                dashboard["Delayed"].append(task.name)
        return dashboard

# User class to represent a user in the system
class User:
    def __init__(self, username: str, role: str):
        self.username = username
        self.role = role

    def notify(self, message: str):
        """Send a notification to the user."""
        print(f"Notification to {self.username}: {message}")

# MultiAgentProjectManager class to manage projects and users
class MultiAgentProjectManager:
    def __init__(self):
        self.projects: Dict[str, Project] = {}  # Dictionary to hold projects by name
        self.users: Dict[str, User] = {}  # Dictionary to hold users by username

    def create_project(self, project_name: str):
        """Create a new project."""
        self.projects[project_name] = Project(project_name)

    def add_user(self, username: str, role: str):
        """Add a new user to the system."""
        self.users[username] = User(username, role)

    def assign_task(self, project_name: str, task: Task, assignee: str):
        """Assign a task to a user and add it to the project."""
        if project_name in self.projects:
            project = self.projects[project_name]
            project.add_task(task)
            self.users[assignee].notify(f"Task '{task.name}' has been assigned to you.")
task.assignee = assignee  # Store the assignee in the task
        else:
            print(f"Project '{project_name}' does not exist.")

    def update_task_status(self, project_name: str, task_name: str, new_status: str):
        """Update the status of a task in a project."""
        if project_name in self.projects:
            project = self.projects[project_name]
            if task_name in project.tasks:
                task = project.tasks[task_name]
                task.update_status(new_status)
                if new_status == "Completed":
                    self.notify_dependencies(project, task_name)
            else:
                print(f"Task '{task_name}' does not exist in project '{project_name}'.")
        else:
            print(f"Project '{project_name}' does not exist.")

    def notify_dependencies(self, project: Project, completed_task_name: str):
        """Notify users of tasks that are dependent on the completed task."""
        for task in project.tasks.values():
            if completed_task_name in task.dependencies:
                task.dependencies.remove(completed_task_name)
                if not task.dependencies:  # If no more dependencies, notify user
                    self.users[task.name].notify(f"Task '{task.name}' can now be started.")

# Example usage
if __name__ == "__main__":
    manager = MultiAgentProjectManager()
    
    # Create users
    manager.add_user("alice", UserRole.PROJECT_MANAGER)
    manager.add_user("bob", UserRole.TEAM_MEMBER)
    
    # Create a project
    manager.create_project("Project Alpha")
    
    # Create tasks
    task1 = Task("Task A", "Description for Task A", datetime(2023, 12, 1))
    task2 = Task("Task B", "Description for Task B", datetime(2023, 12, 2))
    task3 = Task("Task C", "Description for Task C", datetime(2023, 12, 3), dependencies=["Task A", "Task B"])
    
    # Assign tasks
    manager.assign_task("Project Alpha", task1, "bob")
    manager.assign_task("Project Alpha", task2, "bob")
    manager.assign_task("Project Alpha", task3, "bob")
    
    # Update task statuses
    manager.update_task_status("Project Alpha", "Task A", "Completed")
    manager.update_task_status("Project Alpha", "Task B", "Completed")
    manager.update_task_status("Project Alpha", "Task C", "In Progress")
    
    # Print dashboard
    dashboard = manager.projects["Project Alpha"].get_dashboard()
    print(dashboard)