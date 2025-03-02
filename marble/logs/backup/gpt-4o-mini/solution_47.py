# solution.py

from datetime import datetime
from typing import List, Dict, Optional
import json

# Task class to represent a single task in the system
class Task:
    def __init__(self, title: str, description: str, deadline: datetime, priority: int):
        self.title = title  # Title of the task
        self.description = description  # Detailed description of the task
        self.deadline = deadline  # Deadline for the task
        self.priority = priority  # Priority level of the task (1-5)
        self.assigned_to: Optional[str] = None  # User assigned to the task
        self.status = 'Not Started'  # Status of the task

    def assign(self, user: str):
        """Assign the task to a user."""
        self.assigned_to = user

    def update_status(self, status: str):
        """Update the status of the task."""
        self.status = status

# User class to represent a user in the system
class User:
    def __init__(self, username: str):
        self.username = username  # Username of the user
        self.tasks: List[Task] = []  # List of tasks assigned to the user

    def add_task(self, task: Task):
        """Add a task to the user's task list."""
        self.tasks.append(task)

    def get_dashboard(self) -> Dict[str, List[Task]]:
        """Get a dashboard view of the user's tasks."""
        upcoming_tasks = [task for task in self.tasks if task.status != 'Completed']
        completed_tasks = [task for task in self.tasks if task.status == 'Completed']
        return {
            'upcoming_tasks': upcoming_tasks,
            'completed_tasks': completed_tasks
        }

# OfficeTaskCollaborator class to manage the overall system
class OfficeTaskCollaborator:
    def __init__(self):
        self.users: Dict[str, User] = {}  # Dictionary to hold users
        self.tasks: List[Task] = []  # List to hold all tasks

    def add_user(self, username: str):
        """Add a new user to the system."""
        if username not in self.users:
            self.users[username] = User(username)

    def create_task(self, title: str, description: str, deadline: datetime, priority: int, assigned_to: Optional[str] = None):
        """Create a new task and add it to the system."""
        task = Task(title, description, deadline, priority)
        if assigned_to and assigned_to in self.users:
            task.assign(assigned_to)
            self.users[assigned_to].add_task(task)
        self.tasks.append(task)

    def update_task_status(self, task: Task, status: str):
        """Update the status of a given task."""
        task.update_status(status)

    def generate_report(self) -> Dict[str, int]:
        """Generate a report on task completion rates."""def sync_with_calendar(self):
        """Sync task deadlines with calendar applications."""
        for task in self.tasks:
            if task.deadline:
                # Logic to integrate with Google Calendar or Outlook API
                # Example: create_event_in_google_calendar(task)
                pass        pass

# Example usage of the OfficeTaskCollaborator system
if __name__ == "__main__":
    # Create an instance of the task collaborator system
    office_task_collaborator = OfficeTaskCollaborator()

    # Add users to the system
    office_task_collaborator.add_user("Alice")
    office_task_collaborator.add_user("Bob")

    # Create tasks
    office_task_collaborator.create_task("Design Logo", "Create a new logo for the project", datetime(2023, 10, 15), 1, "Alice")
    office_task_collaborator.create_task("Write Documentation", "Document the API endpoints", datetime(2023, 10, 20), 2, "Bob")

    # Update task status
    task_to_update = office_task_collaborator.tasks[0]
    office_task_collaborator.update_task_status(task_to_update, "In Progress")

    # Generate report
    report = office_task_collaborator.generate_report()
    print(json.dumps(report, indent=4))  # Print the report in a readable format