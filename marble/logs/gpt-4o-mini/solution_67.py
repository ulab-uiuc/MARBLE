# solution.py

# Import necessary libraries
from datetime import datetime, timedelta
from collections import defaultdict
import json

# User class to represent each team member
class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.tasks = []  # List to hold tasks assigned to the user

# Task class to represent a task in the system
class Task:
    def __init__(self, title, description, priority, deadline, assigned_to):
        self.title = title
        self.description = description
        self.priority = priority
        self.deadline = deadline
        self.assigned_to = assigned_to
        self.status = 'Pending'  # Initial status of the task
        self.created_at = datetime.now()  # Timestamp of task creation

# TeamSyncPro class to manage the application logic
class TeamSyncPro:
    def __init__(self):
        self.users = {}  # Dictionary to hold users
        self.tasks = []  # List to hold all tasks
        self.notifications = defaultdict(list)  # Notifications for users

    def register_user(self, username, email):
        if username not in self.users:
            self.users[username] = User(username, email)
            print(f"User {username} registered successfully.")
        else:
            print("Username already exists.")        print(f"User {username} registered successfully.")
        else:
            print("Username already exists.")

    def create_task(self, title, description, priority, deadline, assigned_to):
        """Create a new task and assign it to a user."""
        if assigned_to in self.users:
            task = Task(title, description, priority, deadline, assigned_to)
            self.tasks.append(task)
            self.users[assigned_to].tasks.append(task)
            self.send_notification(assigned_to, f"New task '{title}' assigned.")
            print(f"Task '{title}' created and assigned to {assigned_to}.")
        else:
            print("User not found.")

    def send_notification(self, username, message):
        """Send a notification to a user."""
        self.notifications[username].append(message)

    def update_task_status(self, task_title, new_status):
        """Update the status of a task."""
        for task in self.tasks:
            if task.title == task_title:
                task.status = new_status
                self.send_notification(task.assigned_to, f"Task '{task_title}' status updated to {new_status}.")
                print(f"Task '{task_title}' status updated to {new_status}.")
                return
        print("Task not found.")

    def generate_productivity_report(self):
        """Generate a report of tasks and their statuses."""
        report = {}
        for user in self.users.values():
            report[user.username] = {
                'total_tasks': len(user.tasks),
                'completed_tasks': sum(1 for task in user.tasks if task.status == 'Completed'),
                'pending_tasks': sum(1 for task in user.tasks if task.status == 'Pending'),
            }
        return json.dumps(report, indent=4)

    def get_notifications(self, username):
        """Retrieve notifications for a user."""
        return self.notifications[username]

# Example usage of the TeamSyncPro application
if __name__ == "__main__":
    app = TeamSyncPro()
    
    # Register users
    app.register_user("alice", "alice@example.com")
    app.register_user("bob", "bob@example.com")
    
    # Create tasks
    app.create_task("Design Homepage", "Create a design for the homepage.", "High", datetime.now() + timedelta(days=7), "alice")
    app.create_task("Develop API", "Develop the backend API.", "Medium", datetime.now() + timedelta(days=14), "bob")
    
    # Update task status
    app.update_task_status("Design Homepage", "Completed")
    
    # Generate productivity report
    report = app.generate_productivity_report()
    print("Productivity Report:")
    print(report)
    
    # Get notifications for a user
    notifications = app.get_notifications("alice")
    print("Notifications for Alice:")
    print(notifications)