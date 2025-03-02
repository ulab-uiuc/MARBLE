# solution.py

# Importing required libraries
import datetime
import random
import string
import os

# Defining a class for User
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.tasks = []

# Defining a class for Task
class Task:
    def __init__(self, title, deadline, priority, status="pending"):
        self.title = title
        self.deadline = deadline
        self.priority = priority
        self.status = status
        self.comments = []

# Defining a class for OfficeTaskScheduler
class OfficeTaskScheduler:
    def __init__(self):
        self.users = {}
        self.tasks = {}

    # Method to create a new user
    def create_user(self, username, password):
        if username not in self.users:
            self.users[username] = User(username, password)
            print(f"User {username} created successfully.")
        else:
            print(f"User {username} already exists.")

    # Method to login a user
    def login_user(self, username, password):
        if username in self.users and self.users[username].password == password:
            return self.users[username]
        else:
            print("Invalid username or password.")
            return None

    # Method to create a new task
    def create_task(self, title, deadline, priority, assignee):
        if assignee in self.users:
            task = Task(title, deadline, priority)
            self.tasks[title] = task
            self.users[assignee].tasks.append(title)
            print(f"Task {title} created successfully.")
        else:
            print(f"User {assignee} does not exist.")

    # Method to view tasks for a user
    def view_tasks(self, user):
        if user:
            print(f"Tasks for {user.username}:")
            for task in user.tasks:
                print(f"Title: {self.tasks[task].title}, Deadline: {self.tasks[task].deadline}, Priority: {self.tasks[task].priority}, Status: {self.tasks[task].status}")
        else:
            print("Invalid user.")

    # Method to update task status
    def update_task_status(self, title, status):
        if title in self.tasks:
            self.tasks[title].status = status
            print(f"Task {title} status updated to {status}.")
        else:
            print(f"Task {title} does not exist.")

    # Method to add comment to a task
    def add_comment(self, title, comment):
        if title in self.tasks:
            self.tasks[title].comments.append(comment)
            print(f"Comment added to task {title}.")
        else:
            print(f"Task {title} does not exist.")

    # Method to generate report
    def generate_report(self):
        print("Task Completion Rates:")
        for user in self.users.values():
            completed_tasks = sum(1 for task in user.tasks if self.tasks[task].status == "completed")
            total_tasks = len(user.tasks)
            if total_tasks > 0:
                print(f"{user.username}: {completed_tasks / total_tasks * 100}%")
        print("\nOverdue Tasks:")
        for task in self.tasks.values():
            if task.deadline < datetime.date.today():
                print(f"{task.title}: {task.deadline}")
        print("\nTask Distribution:")
        for user in self.users.values():
            print(f"{user.username}: {len(user.tasks)} tasks")

# Defining a class for NotificationSystem
class NotificationSystem:
    def __init__(self):
        self.notifications = {}

    # Method to send notification
    def send_notification(self, user, message):
        if user in self.notifications:
            self.notifications[user].append(message)
        else:
            self.notifications[user] = [message]

    # Method to view notifications
    def view_notifications(self, user):
        if user in self.notifications:
            print(f"Notifications for {user}:")
            for notification in self.notifications[user]:
                print(notification)
        else:
            print("No notifications.")

# Creating an instance of OfficeTaskScheduler
scheduler = OfficeTaskScheduler()

# Creating an instance of NotificationSystem
notification_system = NotificationSystem()

# Test cases
while True:
    print("\n1. Create user")
    print("2. Login user")
    print("3. Create task")
    print("4. View tasks")
    print("5. Update task status")
    print("6. Add comment")
    print("7. Generate report")
    print("8. Send notification")
    print("9. View notifications")
    print("10. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        username = input("Enter username: ")
        password = input("Enter password: ")
        scheduler.create_user(username, password)
    elif choice == "2":
        username = input("Enter username: ")
        password = input("Enter password: ")
        user = scheduler.login_user(username, password)
    elif choice == "3":
        title = input("Enter task title: ")
        deadline = input("Enter deadline (YYYY-MM-DD): ")
        deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d").date()
        priority = input("Enter priority: ")
        assignee = input("Enter assignee: ")
        scheduler.create_task(title, deadline, priority, assignee)
    elif choice == "4":
        if scheduler.login_user(input("Enter username: "), input("Enter password: ")):
            scheduler.view_tasks(scheduler.login_user(input("Enter username: "), input("Enter password ")))
    elif choice == "5":
        title = input("Enter task title: ")
        status = input("Enter status: ")
        scheduler.update_task_status(title, status)
    elif choice == "6":
        title = input("Enter task title: ")
        comment = input("Enter comment: ")
        scheduler.add_comment(title, comment)
    elif choice == "7":
        scheduler.generate_report()
    elif choice == "8":
        user = scheduler.login_user(input("Enter username: "), input("Enter password: "))
        message = input("Enter message: ")
        notification_system.send_notification(user.username, message)
    elif choice == "9":
        user = scheduler.login_user(input("Enter username: "), input("Enter password: "))
        notification_system.view_notifications(user.username)
    elif choice == "10":
        break
    else:
        print("Invalid choice.")