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
        if assignee_username not in self.users:        if deadline <= datetime.now():
            raise ValueError("Deadline must be a future date.")
        if assignee_username not in self.users:
            raise ValueError("Assignee does not exist.")
        task = Task(title, assignee_username, deadline, priority)        self.tasks.append(task)
        self.users[assignee_username].tasks.append(task)
        self.notifications[assignee_username].append(f"New task assigned: {title}")

    def update_task_status(self, task_title, new_status, username):
        """Update the status of a task."""
        task = self.find_task(task_title)
        if task.assignee != username:
            raise PermissionError("You do not have permission to update this task.")
        task.update_status(new_status)

    def add_task_comment(self, task_title, comment, username):
        """Add a comment to a task."""
        task = self.find_task(task_title)
        if task.assignee != username:
            raise PermissionError("You do not have permission to comment on this task.")
        task.add_comment(comment)

    def find_task(self, title):
        """Find a task by its title."""
        for task in self.tasks:
            if task.title == title:
                return task
        raise ValueError("Task not found.")

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

# Example usage
if __name__ == "__main__":
    scheduler = OfficeTaskScheduler()
    
    # Adding users
    scheduler.add_user("alice")
    scheduler.add_user("bob")
    
    # Creating tasks
    scheduler.create_task("Complete report", "alice", datetime.now() + timedelta(days=2), "high")
    scheduler.create_task("Prepare presentation", "bob", datetime.now() + timedelta(days=1), "medium")
    
    # Updating task status
    scheduler.update_task_status("Complete report", "in progress", "alice")
    
    # Adding comments
    scheduler.add_task_comment("Complete report", "Started working on it.", "alice")
    
    # Generating report
    report = scheduler.generate_report()
    print(report)
    
    # User dashboard
    alice_tasks = scheduler.get_user_dashboard("alice")
    print(alice_tasks)