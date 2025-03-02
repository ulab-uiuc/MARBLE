# office_task_scheduler.py
# This is the main implementation of the OfficeTaskScheduler program.

import datetime
import getpass
import os
import pickle
import random
import time

class User:
    """Represents a user in the office task scheduler system."""
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.tasks = []
        self.notifications = []

class Task:
    """Represents a task in the office task scheduler system."""
    
    def __init__(self, title, deadline, priority, assigned_to=None):
        self.title = title
        self.deadline = deadline
        self.priority = priority
        self.status = "pending"
        self.assigned_to = assigned_to
        self.comments = []

class OfficeTaskScheduler:
    """Represents the office task scheduler system."""
    
    def __init__(self):
self.lock = threading.Lock()
        self.users = {}
        self.tasks = []
        self.load_data()

    def load_data(self):if os.path.exists("users.dat"): with self.lock: with open("users.dat", "rb") as f: self.users = pickle.load(f)def save_data(self):with self.lock: with open("users.dat", "wb") as f: pickle.dump(self.users, f)with self.lock: with open("tasks.dat", "wb") as f: pickle.dump(self.tasks, f)with self.lock: with open("tasks.dat", "wb") as f: pickle.dump(self.tasks, f)with self.lock: with open("users.dat", "wb") as f: pickle.dump(self.users, f)
        """Saves user and task data to files."""
        
        with open("users.dat", "wb") as f:
            pickle.dump(self.users, f)
        with open("tasks.dat", "wb") as f:
            pickle.dump(self.tasks, f)

    def register_user(self):
        """Registers a new user."""
        
        username = input("Enter a username: ")
        password = getpass.getpass("Enter a password: ")
        confirm_password = getpass.getpass("Confirm password: ")
        if password != confirm_password:
            print("Passwords do not match.")
            return
        if username in self.users:
            print("Username already exists.")
            return
        self.users[username] = User(username, password)
        self.save_data()
        print("User registered successfully.")

    def login_user(self):
        """Logs in an existing user."""
        
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")
        if username not in self.users or self.users[username].password != password:
            print("Invalid username or password.")
            return
        return self.users[username]

    def create_task(self, user):
        """Creates a new task for the given user."""
        
        title = input("Enter a title: ")
        deadline = input("Enter a deadline (YYYY-MM-DD): ")
        deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d").date()
        priority = input("Enter a priority (high, medium, low): ")
        assigned_to = input("Enter the username of the user to assign the task to (leave blank for yourself): ")
        if assigned_to == "":
            assigned_to = user.username
        if assigned_to not in self.users:
            print("User does not exist.")
            return
        task = Task(title, deadline, priority, assigned_to)
        self.tasks.append(task)
        self.save_data()
        print("Task created successfully.")

    def view_tasks(self, user):
        """Displays the tasks assigned to the given user."""
        
        print("Tasks:")
        for task in self.tasks:
            if task.assigned_to == user.username:
                print(f"Title: {task.title}, Deadline: {task.deadline}, Priority: {task.priority}, Status: {task.status}")
                for comment in task.comments:
                    print(f"Comment: {comment}")

    def update_task_status(self, user):
        """Updates the status of a task assigned to the given user."""
        
        task_title = input("Enter the title of the task to update: ")
        for task in self.tasks:
            if task.title == task_title and task.assigned_to == user.username:
                task.status = input("Enter the new status (pending, in progress, completed): ")
                self.save_data()
                print("Task status updated successfully.")
                return
        print("Task not found.")

    def add_comment(self, user):
        """Adds a comment to a task assigned to the given user."""
        
        task_title = input("Enter the title of the task to add a comment to: ")
        for task in self.tasks:
            if task.title == task_title and task.assigned_to == user.username:
                comment = input("Enter the comment: ")
                task.comments.append(comment)
                self.save_data()
                print("Comment added successfully.")
                return
        print("Task not found.")

    def generate_report(self):
        """Generates a report on task completion rates, overdue tasks, and task distribution among team members."""
        
        print("Task Completion Rates:")
        for user in self.users.values():
            completed_tasks = sum(1 for task in self.tasks if task.assigned_to == user.username and task.status == "completed")
            total_tasks = sum(1 for task in self.tasks if task.assigned_to == user.username)
            if total_tasks > 0:
                print(f"{user.username}: {completed_tasks / total_tasks * 100}%")
        print("Overdue Tasks:")
        for task in self.tasks:
            if task.deadline < datetime.date.today():
                print(f"Title: {task.title}, Deadline: {task.deadline}, Priority: {task.priority}, Status: {task.status}")
        print("Task Distribution Among Team Members:")
        for user in self.users.values():
            tasks_assigned = sum(1 for task in self.tasks if task.assigned_to == user.username)
            print(f"{user.username}: {tasks_assigned}")

def main():
    scheduler = OfficeTaskScheduler()
    while True:
        print("1. Register User")
        print("2. Login User")
        print("3. Create Task")
        print("4. View Tasks")
        print("5. Update Task Status")
        print("6. Add Comment")
        print("7. Generate Report")
        print("8. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            scheduler.register_user()
        elif choice == "2":
            user = scheduler.login_user()
            if user:
                print("Logged in successfully.")
                while True:
                    print("1. Create Task")
                    print("2. View Tasks")
                    print("3. Update Task Status")
                    print("4. Add Comment")
                    print("5. Generate Report")
                    print("6. Logout")
                    choice = input("Enter your choice: ")
                    if choice == "1":
                        scheduler.create_task(user)
                    elif choice == "2":
                        scheduler.view_tasks(user)
                    elif choice == "3":
                        scheduler.update_task_status(user)
                    elif choice == "4":
                        scheduler.add_comment(user)
                    elif choice == "5":
                        scheduler.generate_report()
                    elif choice == "6":
                        break
        elif choice == "8":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()