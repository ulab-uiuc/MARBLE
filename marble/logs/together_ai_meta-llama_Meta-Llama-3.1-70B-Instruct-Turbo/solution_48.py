# solution.py

# Import required libraries
from datetime import datetime
from enum import Enum
from typing import List, Dict

# Define an Enum for task status
class TaskStatus(Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

# Define an Enum for task priority
class TaskPriority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

# Define a class for User
class User:
    def __init__(self, id: int, name: str, role: str):
        self.id = id
        self.name = name
        self.role = role

# Define a class for Task
class Task:
    def __init__(self, id: int, title: str, description: str, deadline: datetime, priority: TaskPriority, status: TaskStatus, assigned_to: User):
        self.id = id
        self.title = title
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.status = status
        self.assigned_to = assigned_to
        self.comments = []
        self.attachments = []

    def add_comment(self, comment: str):
        self.comments.append(comment)

    def add_attachment(self, attachment: str):
        self.attachments.append(attachment)

    def update_status(self, status: TaskStatus):
        self.status = status

# Define a class for OfficeTaskCollaborationManager
class OfficeTaskCollaborationManager:
    def __init__(self):
        self.tasks = []
        self.users = []

    def create_task(self, title: str, description: str, deadline: datetime, priority: TaskPriority, assigned_to: User):
        task = Task(len(self.tasks) + 1, title, description, deadline, priority, TaskStatus.NOT_STARTED, assigned_to)
        self.tasks.append(task)
        return task

    def assign_task(self, task_id: int, assigned_to: User):
        task = next((task for task in self.tasks if task.id == task_id), None)
        if task:
            task.assigned_to = assigned_to
            print(f"Task {task_id} assigned to {assigned_to.name}")
        else:
            print(f"Task {task_id} not found")

    def update_task_status(self, task_id: int, status: TaskStatus):
        task = next((task for task in self.tasks if task.id == task_id), None)
        if task:
            task.update_status(status)
            print(f"Task {task_id} status updated to {status.value}")
        else:
            print(f"Task {task_id} not found")

    def add_comment_to_task(self, task_id: int, comment: str):
        task = next((task for task in self.tasks if task.id == task_id), None)
        if task:
            task.add_comment(comment)
            print(f"Comment added to task {task_id}")
        else:
            print(f"Task {task_id} not found")

    def add_attachment_to_task(self, task_id: int, attachment: str):
        task = next((task for task in self.tasks if task.id == task_id), None)
        if task:
            task.add_attachment(attachment)
            print(f"Attachment added to task {task_id}")
        else:
            print(f"Task {task_id} not found")

    def generate_report(self):
        completed_tasks = [task for task in self.tasks if task.status == TaskStatus.COMPLETED]pending_tasks = [task for task in self.tasks if task.status in [TaskStatus.NOT_STARTED, TaskStatus.IN_PROGRESS]]overdue_tasks = [task for task in self.tasks if task.deadline < datetime.now()]
        print("Completed Tasks:")
        for task in completed_tasks:
            print(f"Task {task.id}: {task.title}")
        print("Pending Tasks:")
        for task in pending_tasks:
            print(f"Task {task.id}: {task.title}")
        print("Overdue Tasks:")
        for task in overdue_tasks:
            print(f"Task {task.id}: {task.title}")

# Define a class for UserAuthenticator
class UserAuthenticator:
    def __init__(self):
        self.users = []

    def add_user(self, user: User):
        self.users.append(user)

    def authenticate_user(self, user_id: int, role: str):
        user = next((user for user in self.users if user.id == user_id and user.role == role), None)
        if user:
            return user
        else:
            return None

# Test the implementation
if __name__ == "__main__":
    # Create users
    user1 = User(1, "John Doe", "Admin")
    user2 = User(2, "Jane Doe", "User")

    # Create an OfficeTaskCollaborationManager instance
    manager = OfficeTaskCollaborationManager()

    # Create tasks
    task1 = manager.create_task("Task 1", "This is task 1", datetime(2024, 3, 16), TaskPriority.HIGH, user1)
    task2 = manager.create_task("Task 2", "This is task 2", datetime(2024, 3, 17), TaskPriority.MEDIUM, user2)

    # Assign tasks
    manager.assign_task(task1.id, user2)
    manager.assign_task(task2.id, user1)

    # Update task status
    manager.update_task_status(task1.id, TaskStatus.IN_PROGRESS)
    manager.update_task_status(task2.id, TaskStatus.COMPLETED)

    # Add comments and attachments to tasks
    manager.add_comment_to_task(task1.id, "This is a comment")
    manager.add_attachment_to_task(task1.id, "attachment.txt")

    # Generate report
    manager.generate_report()

    # Test user authentication
    authenticator = UserAuthenticator()
    authenticator.add_user(user1)
    authenticated_user = authenticator.authenticate_user(1, "Admin")
    if authenticated_user:
        print(f"User {authenticated_user.name} authenticated successfully")
    else:
        print("User authentication failed")