# solution.py
# TeamSyncPro: A Collaborative Schedule Management System

# Import required libraries
import datetime
import threading
from typing import Dict, List

# Define a class for User
class User:
    def __init__(self, name: str, email: str):
        # Initialize user attributes
        self.name = name
        self.email = email
        self.tasks = []
        self.meetings = []

# Define a class for Task
class Task:
    def __init__(self, title: str, description: str, priority: str, deadline: datetime.date):
    def __init__(self, task_id: int, title: str, description: str, priority: str, deadline: datetime.date):
        # Initialize task attributes
        self.title = title
        self.description = description
        self.priority = priority
        self.deadline = deadline
        self.status = "Not Started"

# Define a class for Meeting
class Meeting:
    def __init__(self, title: str, description: str, date: datetime.date, time: datetime.time):
    def __init__(self, meeting_id: int, title: str, description: str, date: datetime.date, time: datetime.time):
        # Initialize meeting attributes
        self.title = title
        self.description = description
        self.date = date
        self.time = time

# Define a class for TeamSyncPro
class TeamSyncPro:def add_task(self, title: str, description: str, priority: str, deadline: datetime.date, assigned_to: str) -> int:    def add_user(self, name: str, email: str):
        self.users[email] = User(name, email)
    def __init__(self):
        self.users = {}
        self.tasks = {}
        self.meetings = {}
        if assigned_to not in self.users:
            raise ValueError(f"User {assigned_to} not found")if title in self.tasks:
            raise ValueError(f"Task with title '{title}' already exists")
        self.tasks[title] = Task(title, description, priority, deadline)# Assign the task to the user
        self.users[assigned_to].tasks.append(title)# Method to add a meetingdef add_meeting(self, title: str, description: str, date: datetime.date, time: datetime.time, attendees: List[str]):
    for attendee in attendees:
        if attendee not in self.users:
            raise ValueError(f"User {attendee} not found")# Create a new meeting and add to the meetings dictionary
        self.meetings[title] = Meeting(title, description, date, time)
        # Add the meeting to each attendee's meetings list
        for attendee in attendees:
            self.users[attendee].meetings.append(title)

    # Method to update a task status
    def update_task_status(self, title: str, status: str):
        # Update the task status
        self.tasks[title].status = status

    # Method to generate productivity reports
    def generate_productivity_reports(self):
        # Generate reports for each user
        for user in self.users.values():
            print(f"User: {user.name}")
            print("Tasks:")
            for task_title in user.tasks:
                task = self.tasks[task_title]
                print(f"  - {task.title}: {task.status}")
            print("Meetings:")
            for meeting_title in user.meetings:
                meeting = self.meetings[meeting_title]
                print(f"  - {meeting.title}: {meeting.date} {meeting.time}")

    # Method to send reminders and notifications
    def send_reminders_and_notifications(self):
        # Send reminders for upcoming tasks and meetings
        for task in self.tasks.values():
            if task.deadline == datetime.date.today():
                print(f"Reminder: {task.title} is due today")
        for meeting in self.meetings.values():
            if meeting.date == datetime.date.today():
                print(f"Reminder: {meeting.title} is today at {meeting.time}")

# Create a TeamSyncPro instance
team_sync_pro = TeamSyncPro()

# Add users
team_sync_pro.add_user("John Doe", "john.doe@example.com")
team_sync_pro.add_user("Jane Doe", "jane.doe@example.com")

# Add tasks
team_sync_pro.add_task("Task 1", "Description 1", "High", datetime.date(2024, 9, 20), "john.doe@example.com")
team_sync_pro.add_task("Task 2", "Description 2", "Low", datetime.date(2024, 9, 25), "jane.doe@example.com")

# Add meetings
team_sync_pro.add_meeting("Meeting 1", "Description 1", datetime.date(2024, 9, 22), datetime.time(10, 0), ["john.doe@example.com", "jane.doe@example.com"])

# Update task status
team_sync_pro.update_task_status("Task 1", "In Progress")

# Generate productivity reports
team_sync_pro.generate_productivity_reports()

# Send reminders and notifications
team_sync_pro.send_reminders_and_notifications()

# Define a function to simulate real-time updates and synchronization
def simulate_real_time_updates(team_sync_pro: TeamSyncPro):
    while True:
        # Simulate real-time updates and synchronization
        print("Simulating real-time updates and synchronization...")
        team_sync_pro.generate_productivity_reports()
        team_sync_pro.send_reminders_and_notifications()
        # Wait for 1 minute before simulating again
        threading.sleep(60)

# Create a thread to simulate real-time updates and synchronization
thread = threading.Thread(target=simulate_real_time_updates, args=(team_sync_pro,))
thread.start()

# Define a function to handle user input
def handle_user_input(team_sync_pro: TeamSyncPro):
    while True:
        # Display menu options
        print("Menu:")
        print("1. Add user")
        print("2. Add task")
        print("3. Add meeting")
        print("4. Update task status")
        print("5. Generate productivity reports")
        print("6. Send reminders and notifications")
        print("7. Exit")
        # Get user input
        choice = input("Enter your choice: ")
        # Handle user input
        if choice == "1":
            name = input("Enter user name: ")
            email = input("Enter user email: ")
            team_sync_pro.add_user(name, email)
        elif choice == "2":
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            priority = input("Enter task priority: ")
            deadline = datetime.datetime.strptime(input("Enter task deadline (YYYY-MM-DD): "), "%Y-%m-%d").date()
            assigned_to = input("Enter user email to assign task to: ")
            team_sync_pro.add_task(title, description, priority, deadline, assigned_to)
        elif choice == "3":
            title = input("Enter meeting title: ")
            description = input("Enter meeting description: ")
            date = datetime.datetime.strptime(input("Enter meeting date (YYYY-MM-DD): "), "%Y-%m-%d").date()
            time = datetime.datetime.strptime(input("Enter meeting time (HH:MM): "), "%H:%M").time()
            attendees = input("Enter user emails to invite to meeting (separated by commas): ").split(",")
            team_sync_pro.add_meeting(title, description, date, time, attendees)
        elif choice == "4":
            title = input("Enter task title: ")
            status = input("Enter new task status: ")
            team_sync_pro.update_task_status(title, status)
        elif choice == "5":
            team_sync_pro.generate_productivity_reports()
        elif choice == "6":
            team_sync_pro.send_reminders_and_notifications()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")

# Handle user input
handle_user_input(team_sync_pro)