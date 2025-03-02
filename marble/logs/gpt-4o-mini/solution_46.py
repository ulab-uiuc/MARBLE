# solution.py

from datetime import datetime, timedelta
from collections import defaultdict

class User:
    """Class representing a user in the task management system."""
    
    def __init__(self, username):
        self.username = username
        self.tasks = []  # List to hold tasks assigned to the user

class Task:
    """Class representing a task in the task management system."""
    
    def __init__(self, title, assignee, deadline, priority):
        self.title = title
        self.assignee = assignee
        self.deadline = deadline
        self.priority = priority
        self.status = 'pending'  # Initial status of the task
        self.comments = []  # List to hold comments for the task

    def update_status(self, new_status):
        """Update the status of the task."""
        self.status = new_status

    def add_comment(self, comment):
        """Add a comment to the task."""
        self.comments.append(comment)

class OfficeTaskScheduler:
    """Main class for managing the task scheduling system."""
    
    def __init__(self):
        self.users = {}  # Dictionary to hold users
        self.tasks = []  # List to hold all tasks
        self.notifications = defaultdict(list)  # Notifications for users

    def add_user(self, username):
        """Add a new user to the system."""
        if username not in self.users:
            self.users[username] = User(username)

    def create_task(self, title, assignee_username, deadline, priority):
        """Create a new task and assign it to a user."""
        if assignee_username not in self.users:if deadline <= datetime.now():
            raise ValueError("Deadline must be a future date.")
        if assignee_username not in self.users:        self.tasks.append(task)
        self.users[assignee_username].tasks.append(task)
        self.notifications[assignee_username].append(f"New task assigned: {title}")

    def update_task_status(self, task_title, new_status, username):
        """Update the status of a task."""
        for task in self.tasks:
            if task.title == task_title and task.assignee == username:
                task.update_status(new_status)
                return
        raise ValueError("Task not found or user not authorized.")

    def add_task_comment(self, task_title, comment, username):
        """Add a comment to a task."""
        for task in self.tasks:
            if task.title == task_title and task.assignee == username:
                task.add_comment(comment)
                return
        raise ValueError("Task not found or user not authorized.")

    def generate_report(self):
        """Generate a report of task completion rates and overdue tasks."""
        report = {
            'total_tasks': len(self.tasks),
            'completed_tasks': sum(1 for task in self.tasks if task.status == 'completed'),
            'overdue_tasks': [task for task in self.tasks if task.deadline < datetime.now() and task.status != 'completed'],
            'task_distribution': defaultdict(int)
        }
        for task in self.tasks:
            report['task_distribution'][task.assignee] += 1
        return report

    def get_user_dashboard(self, username):
        """Get the dashboard for a specific user."""
        if username not in self.users:
            raise ValueError("User does not exist.")
        return self.users[username].tasks

    def notify_users(self):
        """Notify users about upcoming deadlines."""
        for user, notifications in self.notifications.items():
            for task in self.users[user].tasks:
                if task.deadline < datetime.now() + timedelta(days=2) and task.status != 'completed':
                    notifications.append(f"Reminder: Task '{task.title}' is due soon.")
        return self.notifications

# Example usage
if __name__ == "__main__":
    scheduler = OfficeTaskScheduler()
    scheduler.add_user("alice")
    scheduler.add_user("bob")

    # Create tasks
    scheduler.create_task("Finish report", "alice", datetime.now() + timedelta(days=3), "high")
    scheduler.create_task("Prepare presentation", "bob", datetime.now() + timedelta(days=1), "medium")

    # Update task status
    scheduler.update_task_status("Finish report", "in progress", "alice")

    # Add comments
    scheduler.add_task_comment("Finish report", "Started working on it.", "alice")

    # Generate report
    report = scheduler.generate_report()
    print(report)

    # Get user dashboard
    alice_tasks = scheduler.get_user_dashboard("alice")
    print(alice_tasks)

    # Notify users
    notifications = scheduler.notify_users()
    print(notifications)