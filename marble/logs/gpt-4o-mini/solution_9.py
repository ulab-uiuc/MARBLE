# solution.py

from datetime import datetime
from typing import List, Dict, Optional
import csv

# Class to represent a Task
class Task:
    def __init__(self, name: str, assignee: str, deadline: datetime):
        self.name = name  # Name of the task
        self.assignee = assignee  # User assigned to the task
        self.deadline = deadline  # Deadline for the task
        self.status = 'Not Started'  # Initial status of the task

    def update_status(self, status: str):
        """Update the status of the task."""
        self.status = status

# Class to represent a Project
class Project:
    def __init__(self, name: str, start_date: datetime, end_date: datetime, description: str):
        self.name = name  # Name of the project
        self.start_date = start_date  # Start date of the project
        self.end_date = end_date  # End date of the project
        self.description = description  # Description of the project
        self.tasks: List[Task] = []  # List to hold tasks in the project

    def add_task(self, task: Task):
        """Add a task to the project."""
        self.tasks.append(task)

# Class to represent a User
class User:
    def __init__(self, username: str):
        self.username = username  # Username of the user
        self.tasks_completed = 0  # Count of completed tasks
        self.total_tasks = 0  # Total tasks assigned to the user
        self.feedback = []  # List to hold feedback received

    def complete_task(self):
        """Increment the count of completed tasks."""
        self.tasks_completed += 1
        self.total_tasks += 1

    def add_feedback(self, feedback: str):
        """Add feedback received by the user."""
        self.feedback.append(feedback)

    def performance_dashboard(self) -> Dict[str, float]:
        """Generate performance metrics for the user."""
        completion_rate = (self.tasks_completed / self.total_tasks) * 100 if self.total_tasks > 0 else 0
        return {
            'completion_rate': completion_rate,
            'average_time': None,  # Placeholder for average time calculation
            'feedback': self.feedback
        }

# Class to manage the overall Team Collaboration
class TeamCollaborationManager:
    def __init__(self):
        self.projects: List[Project] = []  # List to hold projects
        self.users: Dict[str, User] = {}  # Dictionary to hold users by username

    def create_project(self, name: str, start_date: datetime, end_date: datetime, description: str):
        """Create a new project."""
        project = Project(name, start_date, end_date, description)def assign_task(self, project_name: str, task_name: str, assignee: str, deadline: datetime):
        """Assign a task to a user within a project."""
        if assignee not in self.users:
            raise ValueError(f'User {assignee} does not exist.')
        project = next((p for p in self.projects if p.name == project_name), None)
        if project:
            task = Task(task_name, assignee, deadline)
            project.add_task(task)
            self.users[assignee].total_tasks += 1

            # Update completed tasks if the task is marked as completed
            if task.status == 'Completed':
                self.users[assignee].complete_task()            task = Task(task_name, assignee, deadline)
            project.add_task(task)
            if assignee in self.users:
                self.users[assignee].total_tasks += 1

    def generate_report(self) -> List[Dict[str, str]]:
        """Generate a report of project progress and user performance."""
        report = []
        for project in self.projects:
            for task in project.tasks:
                report.append({
                    'project_name': project.name,
                    'task_name': task.name,
                    'assignee': task.assignee,
                    'status': task.status,
                    'deadline': task.deadline.strftime('%Y-%m-%d')
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
    manager.add_user("Alice")
    manager.add_user("Bob")

    # Create a project
    manager.create_project("Project Alpha", datetime(2023, 1, 1), datetime(2023, 12, 31), "Description of Project Alpha")

    # Assign tasks
    manager.assign_task("Project Alpha", "Task 1", "Alice", datetime(2023, 6, 1))
    manager.assign_task("Project Alpha", "Task 2", "Bob", datetime(2023, 6, 15))

    # Generate and export report
    report = manager.generate_report()
    manager.export_report(report, "project_report.csv")