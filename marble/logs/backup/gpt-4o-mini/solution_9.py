# solution.py

from datetime import datetime
from typing import List, Dict, Optional
import csv

# Class to represent a User in the system
class User:
    def __init__(self, username: str):
        self.username = username
        self.tasks = []  # List to hold tasks assigned to the user
        self.feedback = []  # List to hold feedback received by the user

    def add_feedback(self, feedback: str):
        """Add feedback to the user's feedback list."""
        self.feedback.append(feedback)

    def task_completion_rate(self) -> float:
        """Calculate the task completion rate for the user."""
        completed_tasks = sum(1 for task in self.tasks if task.status == 'completed')
        return completed_tasks / len(self.tasks) * 100 if self.tasks else 0

    def average_time_to_complete(self) -> float:
        """Calculate the average time taken to complete tasks."""
        total_time = sum(task.time_taken for task in self.tasks if task.status == 'completed')
        completed_tasks = sum(1 for task in self.tasks if task.status == 'completed')
        return total_time / completed_tasks if completed_tasks else 0

# Class to represent a Task in the system
class Task:
    def __init__(self, title: str, assignee: User, deadline: datetime):
        self.title = title
        self.assignee = assignee
        self.deadline = deadline
        self.status = 'not started'  # Initial status of the task
        self.time_taken = 0  # Time taken to complete the task
        self.assignee.tasks.append(self)  # Add task to the user's task list

    def update_status(self, new_status: str):
        """Update the status of the task."""
        self.status = new_status

    def mark_completed(self, time_taken: float):
        """Mark the task as completed and record the time taken."""
        self.status = 'completed'
        self.time_taken = time_taken

# Class to represent a Project in the system
class Project:
    def __init__(self, name: str, start_date: datetime, end_date: datetime, description: str):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.tasks = []  # List to hold tasks in the project

    def add_task(self, task: Task):
        """Add a task to the project."""
        self.tasks.append(task)

# Class to represent the Team Collaboration Manager
class TeamCollaborationManager:
    def __init__(self):
        self.projects: List[Project] = []  # List to hold all projects
        self.users: Dict[str, User] = {}  # Dictionary to hold users by username

    def add_user(self, username: str):
        """Add a new user to the system."""
        if username not in self.users:
            self.users[username] = User(username)

    def create_project(self, name: str, start_date: str, end_date: str, description: str):
        """Create a new project."""
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        project = Project(name, start_date, end_date, description)
        self.projects.append(project)

    def create_task(self, project_name: str, title: str, assignee_username: str, deadline: str):
        """Create a new task within a project."""
        project = next((p for p in self.projects if p.name == project_name), None)        if not project:
            raise ValueError(f'Project "{project_name}" not found.')
        if assignee_username not in self.users:
            raise ValueError(f'Assignee "{assignee_username}" not found.')            deadline = datetime.strptime(deadline, '%Y-%m-%d')
            task = Task(title, self.users[assignee_username], deadline)
            project.add_task(task)

    def generate_report(self) -> List[Dict[str, str]]:
        """Generate a report of project and user performance."""
        report = []
        for project in self.projects:
            for task in project.tasks:
                report.append({
                    'Project': project.name,
                    'Task': task.title,
                    'Assignee': task.assignee.username,
                    'Status': task.status,
                    'Deadline': task.deadline.strftime('%Y-%m-%d'),
                    'Time Taken': task.time_taken
                })
        return report

    def export_report(self, report: List[Dict[str, str]], filename: str):
        """Export the report to a CSV file."""
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=report[0].keys())
            writer.writeheader()
            writer.writerows(report)

# Example usage
if __name__ == "__main__":
    manager = TeamCollaborationManager()
    manager.add_user("alice")
    manager.add_user("bob")

    manager.create_project("Project Alpha", "2023-01-01", "2023-12-31", "Description of Project Alpha")
    manager.create_task("Project Alpha", "Task 1", "alice", "2023-06-01")
    manager.create_task("Project Alpha", "Task 2", "bob", "2023-07-01")

    report = manager.generate_report()
    manager.export_report(report, "project_report.csv")