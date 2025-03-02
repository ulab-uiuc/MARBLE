# solution.py

from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json

# User class to represent a user in the system
class User:
    def __init__(self, username: str, role: str):
        self.username = username
        self.role = role

# Task class to represent a task in the system
class Task:
    def __init__(self, title: str, description: str, assignee: User, deadline: datetime, priority: str):
        self.title = title
        self.description = description
        self.assignee = assignee
        self.deadline = deadline
        self.priority = priority
        self.status = "Not Started"  # Initial status
        self.comments = []  # List to hold comments
        self.attachments = []  # List to hold file attachments

    def update_status(self, new_status: str):
        self.status = new_status

    def add_comment(self, comment: str):
        self.comments.append(comment)

    def add_attachment(self, attachment: str):
        self.attachments.append(attachment)

# TaskManager class to manage tasks and users
class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []  # List to hold all tasks
        self.users: Dict[str, User] = {}  # Dictionary to hold users by username

    def add_user(self, username: str, role: str):
        """Add a new user to the system."""
        self.users[username] = User(username, role)def create_task(self, title: str, description: str, assignee_username: str, deadline: datetime, priority: str) -> Optional[Task]:
        """Create a new task and assign it to a user."""
        if assignee_username not in self.users:
            print(f"User {assignee_username} does not exist.")
            return None
        if deadline <= datetime.now():
            print("Deadline must be a future date.")
            return None
        if priority not in ["Low", "Medium", "High"]:
            print("Priority must be one of: Low, Medium, High.")
            return None
        assignee = self.users[assignee_username]
        new_task = Task(title, description, assignee, deadline, priority)
        self.tasks.append(new_task)
        self.notify_user(assignee, f"New task assigned: {title}")
        return new_task        assignee = self.users[assignee_username]
        new_task = Task(title, description, assignee, deadline, priority)
        self.tasks.append(new_task)
        self.notify_user(assignee, f"New task assigned: {title}")
        return new_task

    def update_task_status(self, task: Task, new_status: str):
        """Update the status of a task."""
        task.update_status(new_status)
        self.notify_user(task.assignee, f"Task '{task.title}' status updated to {new_status}")

    def add_comment_to_task(self, task: Task, comment: str):
        """Add a comment to a task."""
        task.add_comment(comment)
        self.notify_user(task.assignee, f"New comment on task '{task.title}': {comment}")

    def add_attachment_to_task(self, task: Task, attachment: str):
        """Add an attachment to a task."""
        task.add_attachment(attachment)
        self.notify_user(task.assignee, f"New attachment added to task '{task.title}'")

    def notify_user(self, user: User, message: str):
        """Simulate sending a notification to a user."""
        print(f"Notification to {user.username}: {message}")

    def generate_report(self) -> Dict[str, List[str]]:
        """Generate a report of task progress."""
        report = {
            "completed": [],
            "pending": [],
            "overdue": []
        }
        current_time = datetime.now()
        for task in self.tasks:
            if task.status == "Completed":
                report["completed"].append(task.title)
            elif task.deadline < current_time and task.status != "Completed":
                report["overdue"].append(task.title)
            else:
                report["pending"].append(task.title)
        return report

# Example usage
if __name__ == "__main__":
    manager = TaskManager()
    manager.add_user("alice", "developer")
    manager.add_user("bob", "manager")

    # Create a task
    task1 = manager.create_task("Implement feature X", "Details about feature X", "alice", datetime.now() + timedelta(days=5), "High")
    
    # Update task status
    if task1:
        manager.update_task_status(task1, "In Progress")
        manager.add_comment_to_task(task1, "Started working on this.")
        manager.add_attachment_to_task(task1, "design_document.pdf")

    # Generate report
    report = manager.generate_report()
    print(json.dumps(report, indent=2))