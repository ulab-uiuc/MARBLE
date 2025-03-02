# office_task_collaborator.py
# This is the main implementation of the Office_Task_Collaborator system.

import datetime
import calendar
import os
import json
from calendar import monthrange
from datetime import date

class Task:
    """Represents a task with its attributes."""
    
    def __init__(self, title, description, deadline, priority, assigned_to=None):
        """
        Initializes a Task object.

        Args:
            title (str): The title of the task.
            description (str): The description of the task.
            deadline (date): The deadline of the task.
            priority (str): The priority level of the task (e.g., high, medium, low).
            assigned_to (str, optional): The name of the user assigned to the task. Defaults to None.
        """
        self.title = title
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.assigned_to = assigned_to
        self.status = "Not Started"
        self.comments = []

    def update_status(self, status):
        """
        Updates the status of the task.

        Args:
            status (str): The new status of the task (e.g., in progress, completed).
        """
        self.status = status

    def add_comment(self, comment):
        """
        Adds a comment to the task.

        Args:
            comment (str): The comment to be added.
        """
        self.comments.append(comment)


class User:
    """Represents a user with their attributes."""
    
    def __init__(self, name):
        """
        Initializes a User object.

        Args:
            name (str): The name of the user.
        """
        self.name = name
        self.tasks = []

    def assign_task(self, task):
        """
        Assigns a task to the user.

        Args:
            task (Task): The task to be assigned.
        """
        self.tasks.append(task)


class Office_Task_Collaborator:
    """Represents the Office_Task_Collaborator system."""
    
    def __init__(self):
        """
        Initializes the Office_Task_Collaborator system.
        """
        self.users = {}
        self.tasks = {}

    def create_task(self, title, description, deadline, priority, assigned_to=None):
        """
        Creates a new task.

        Args:
            title (str): The title of the task.
            description (str): The description of the task.
            deadline (date): The deadline of the task.
            priority (str): The priority level of the task (e.g., high, medium, low).
            assigned_to (str, optional): The name of the user assigned to the task. Defaults to None.

        Returns:
            Task: The created task.
        """
        task = Task(title, description, deadline, priority, assigned_to)
        self.tasks[title] = task
        return task

    def assign_task(self, task_title, user_name):
        """
        Assigns a task to a user.

        Args:
            task_title (str): The title of the task to be assigned.
            user_name (str): The name of the user to be assigned.
        """
        task = self.tasks[task_title]
        user = self.users[user_name]
        user.assign_task(task)

    def update_task_status(self, task_title, status):
        """
        Updates the status of a task.

        Args:
            task_title (str): The title of the task to be updated.
            status (str): The new status of the task (e.g., in progress, completed).
        """
        task = self.tasks[task_title]
        task.update_status(status)

    def add_comment(self, task_title, comment):
        """
        Adds a comment to a task.

        Args:
            task_title (str): The title of the task to be commented.
            comment (str): The comment to be added.
        """
        task = self.tasks[task_title]
        task.add_comment(comment)

    def get_user_tasks(self, user_name):
        """
        Retrieves the tasks assigned to a user.

        Args:
            user_name (str): The name of the user.

        Returns:
            list: A list of tasks assigned to the user.
        """
        user = self.users[user_name]
        return user.tasks

    def get_upcoming_deadlines(self, user_name):
        """
        Retrieves the upcoming deadlines for a user.

        Args:
            user_name (str): The name of the user.

        Returns:
            list: A list of upcoming deadlines for the user.
        """
        user = self.users[user_name]
        upcoming_deadlines = []
        for task in user.tasks:
            if task.deadline > date.today():
                upcoming_deadlines.append(task.deadline)
        return upcoming_deadlines

    def get_completed_tasks(self, user_name):
        """
        Retrieves the completed tasks for a user.

        Args:
            user_name (str): The name of the user.

        Returns:
            list: A list of completed tasks for the user.
        """
        user = self.users[user_name]
        completed_tasks = []
        for task in user.tasks:
            if task.status == "Completed":
                completed_tasks.append(task)
        return completed_tasks

    def generate_report(self, user_name):
        """
        Generates a report for a user.

        Args:
            user_name (str): The name of the user.

        Returns:
            dict: A dictionary containing the report for the user.
        """
        user = self.users[user_name]
        report = {
            "tasks": len(user.tasks),
            "upcoming_deadlines": self.get_upcoming_deadlines(user_name),
            "completed_tasks": self.get_completed_tasks(user_name)
        }
        return report


# Example usage:
if __name__ == "__main__":
    # Create an instance of the Office_Task_Collaborator system
    office_task_collaborator = Office_Task_Collaborator()

    # Create users
    user1 = User("John Doe")
    user2 = User("Jane Doe")
    office_task_collaborator.users["John Doe"] = user1
    office_task_collaborator.users["Jane Doe"] = user2

    # Create tasks
    task1 = office_task_collaborator.create_task("Task 1", "This is task 1", date(2024, 7, 31), "High")
    task2 = office_task_collaborator.create_task("Task 2", "This is task 2", date(2024, 8, 15), "Medium")
    task3 = office_task_collaborator.create_task("Task 3", "This is task 3", date(2024, 9, 1), "Low")

    # Assign tasks to users
    office_task_collaborator.assign_task("Task 1", "John Doe")
    office_task_collaborator.assign_task("Task 2", "Jane Doe")
    office_task_collaborator.assign_task("Task 3", "John Doe")

    # Update task status
    office_task_collaborator.update_task_status("Task 1", "In Progress")

    # Add comment to task
    office_task_collaborator.add_comment("Task 1", "This is a comment")

    # Get user tasks
    tasks = office_task_collaborator.get_user_tasks("John Doe")
    for task in tasks:
        print(task.title)

    # Get upcoming deadlines
    deadlines = office_task_collaborator.get_upcoming_deadlines("John Doe")
    for deadline in deadlines:
        print(deadline)

    # Get completed tasks
    completed_tasks = office_task_collaborator.get_completed_tasks("John Doe")
    for task in completed_tasks:
        print(task.title)

    # Generate report
    report = office_task_collaborator.generate_report("John Doe")
    print(report)