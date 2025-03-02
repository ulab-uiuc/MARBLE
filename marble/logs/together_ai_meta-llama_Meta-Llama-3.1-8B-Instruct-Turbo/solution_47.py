# office_task_collaborator.py
# This is the main implementation of the Office_Task_Collaborator system.

import datetime
import calendar
import os
import json
from calendar import monthrange
from datetime import date
from datetime import timedelta

class Task:
    """
    Represents a task with a description, deadline, priority, and status.
    """
    def __init__(self, description, deadline, priority, status="not started"):
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.status = status

    def update_status(self, status):
        """
        Updates the status of the task.
        """
        self.status = status

class User:
    """
    Represents a user with a name and a list of assigned tasks.
    """
    def __init__(self, name):
        self.name = name
        self.assigned_tasks = []

    def assign_task(self, task):
        """
        Assigns a task to the user.
        """
        self.assigned_tasks.append(task)

class Project:
    """
    Represents a project with a name and a list of tasks.
    """
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def add_task(self, task):
        """
        Adds a task to the project.
        """
        self.tasks.append(task)

class Office_Task_Collaborator:
    """
    Represents the Office_Task_Collaborator system with a list of users and projects.
    """
    def __init__(self):
        self.users = []
        self.projects = []

    def create_user(self, name):
        """
        Creates a new user.
        """
        self.users.append(User(name))

    def create_project(self, name):
        """
        Creates a new project.
        """
        self.projects.append(Project(name))

    def assign_task(self, user_name, task_description, deadline, priority):
        """
        Assigns a task to a user.
        """
        user = next((user for user in self.users if user.name == user_name), None)
        if user:
            task = Task(task_description, deadline, priority)
            user.assign_task(task)
            return task
        else:
            return None

    def update_task_status(self, user_name, task_description, status):
        """
        Updates the status of a task assigned to a user.
        """
        user = next((user for user in self.users if user.name == user_name), None)
        if user:
            task = next((task for task in user.assigned_tasks if task.description == task_description), None)
            if task:
                task.update_status(status)
                return task
        return None

    def sync_deadlines(self, user_name, calendar_app):
        """
        Syncs task deadlines with a calendar application.
        """
        user = next((user for user in self.users if user.name == user_name), None)
        if user:
            for task in user.assigned_tasks:
                # Simulate syncing deadlines with a calendar application
                print(f"Syncing deadline for task '{task.description}' with {calendar_app}...")
                # Add code to integrate with the calendar application
            return True
        return False

    def generate_report(self):
        """
        Generates a report on task completion rates, team performance, and project progress.
        """
        report = ""
        for user in self.users:
            report += f"User: {user.name}\n"
            report += f"Assigned Tasks: {len(user.assigned_tasks)}\n"
            report += f"Completed Tasks: {len([task for task in user.assigned_tasks if task.status == 'completed'])}\n"
            report += f"Progress: {(len([task for task in user.assigned_tasks if task.status == 'completed']) / len(user.assigned_tasks)) * 100}%\n\n"
        return report

def main():
    # Create an instance of the Office_Task_Collaborator system
    office_task_collaborator = Office_Task_Collaborator()

    # Create users
    office_task_collaborator.create_user("John Doe")
    office_task_collaborator.create_user("Jane Doe")

    # Create projects
    office_task_collaborator.create_project("Project 1")
    office_task_collaborator.create_project("Project 2")

    # Assign tasks to users
    task1 = office_task_collaborator.assign_task("John Doe", "Task 1", datetime.date(2024, 3, 15), "high")
    task2 = office_task_collaborator.assign_task("Jane Doe", "Task 2", datetime.date(2024, 3, 20), "medium")

    # Update task status
    office_task_collaborator.update_task_status("John Doe", "Task 1", "in progress")

    # Sync deadlines with a calendar application
    office_task_collaborator.sync_deadlines("John Doe", "Google Calendar")

    # Generate report
    report = office_task_collaborator.generate_report()
    print(report)

if __name__ == "__main__":
    main()