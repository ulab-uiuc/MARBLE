# solution.py
# TeamSyncPro: A Collaborative Schedule Management System

# Import required libraries
import datetime
import threading
from typing import Dict, List

# Define a class for User
class User:
    def __init__(self, username: str, password: str):
        # Initialize user attributes
        self.username = username
        self.password = password
        self.tasks = []
        self.meetings = []
        self.projects = []

# Define a class for Task
class Task:
    def __init__(self, title: str, description: str, priority: str, deadline: datetime.date, time_slot: datetime.time):
        # Initialize task attributes
        self.title = title
        self.description = description
        self.priority = priority
        self.deadline = deadline
        self.time_slot = time_slot
        self.progress = 0
        self.completed = False

# Define a class for Meeting
class Meeting:
    def __init__(self, title: str, description: str, date: datetime.date, time: datetime.time):
        # Initialize meeting attributes
        self.title = title
        self.description = description
        self.date = date
        self.time = time

# Define a class for Project
class Project:
    def __init__(self, title: str, description: str):
        # Initialize project attributes
        self.title = title
        self.description = description
        self.tasks = []
        self.meetings = []

# Define a class for TeamSyncPro
class TeamSyncPro:
    def __init__(self):
        # Initialize TeamSyncPro attributes
        self.users = {}
        self.tasks = {}
        self.meetings = {}
        self.projects = {}
        self.lock = threading.Lock()

    # Method to add a user
    def add_user(self, username: str, password: str):
        # Add a user to the system
        with self.lock:
            if username not in self.users:
                self.users[username] = User(username, password)
                print(f"User {username} added successfully.")
            else:
                print(f"User {username} already exists.")

    # Method to add a taskdef add_task(self, username: str, title: str, description: str, priority: str, deadline: datetime.date, time_slot: datetime.time):
    # Add a task to the system
    with self.lock:
        if username in self.users:
            task = Task(title, description, priority, deadline, time_slot)
            self.users[username].tasks.append(task)
            print(f"Task {title} added successfully for user {username}.")
        else:
            print(f"User {username} does not exist.")with self.lock:
            if username in self.users:if 0 <= progress <= 100: task.progress = progressif progress == 100:
                            task.completed = True
                        print(f"Progress of task {task_title} updated to {progress}.")
                        return
                print(f"Task {task_title} does not exist.")
            else:
                print(f"User {username} does not exist.")

    # Method to generate productivity report
    def generate_productivity_report(self, username: str):
        # Generate a productivity report for a user
        with self.lock:
            if username in self.users:
                print(f"Productivity Report for {username}:")
                for task in self.users[username].tasks:
                    print(f"Task: {task.title}, Progress: {task.progress}%")
                for meeting in self.users[username].meetings:
                    print(f"Meeting: {meeting.title}, Date: {meeting.date}, Time: {meeting.time}")
                for project in self.users[username].projects:
                    print(f"Project: {project.title}, Description: {project.description}")
            else:
                print(f"User {username} does not exist.")

    # Method to send reminders and notifications
    def send_reminders_and_notifications(self, username: str):
        # Send reminders and notifications to a user
        with self.lock:
            if username in self.users:
                for task in self.users[username].tasks:
                    if task.deadline == datetime.date.today():
                        print(f"Reminder: Task {task.title} is due today.")
                for meeting in self.users[username].meetings:
                    if meeting.date == datetime.date.today():
                        print(f"Notification: Meeting {meeting.title} is today.")
            else:
                print(f"User {username} does not exist.")

# Create an instance of TeamSyncPro
team_sync_pro = TeamSyncPro()

# Add users
team_sync_pro.add_user("john", "password123")
team_sync_pro.add_user("jane", "password123")

# Add tasks
team_sync_pro.add_task("john", "Task 1", "Description 1", "High", datetime.date(2024, 9, 20), datetime.time(10, 0, 0))
team_sync_pro.add_task("jane", "Task 2", "Description 2", "Low", datetime.date(2024, 9, 25), datetime.time(11, 0, 0))

# Add meetings
team_sync_pro.add_meeting("john", "Meeting 1", "Description 1", datetime.date(2024, 9, 22), datetime.time(12, 0, 0))
team_sync_pro.add_meeting("jane", "Meeting 2", "Description 2", datetime.date(2024, 9, 28), datetime.time(13, 0, 0))

# Add projects
team_sync_pro.add_project("john", "Project 1", "Description 1")
team_sync_pro.add_project("jane", "Project 2", "Description 2")

# Set task priority
team_sync_pro.set_task_priority("john", "Task 1", "Medium")

# Allocate time slot
team_sync_pro.allocate_time_slot("jane", "Task 2", datetime.time(14, 0, 0))

# Track progress
team_sync_pro.track_progress("john", "Task 1", 50)

# Generate productivity report
team_sync_pro.generate_productivity_report("john")

# Send reminders and notifications
team_sync_pro.send_reminders_and_notifications("jane")