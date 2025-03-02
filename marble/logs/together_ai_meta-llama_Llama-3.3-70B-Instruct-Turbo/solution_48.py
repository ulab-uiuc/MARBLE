# solution.py
import datetime
import unittest
from typing import List, Dict

# User class to represent users in the system
class User:
    def __init__(self, id: int, name: str, role: str):
        # Initialize user with id, name, and role
        self.id = id
        self.name = name
        self.role = role

# Task class to represent tasks in the system
class Task:def __init__(self, id: int, title: str, description: str, deadline: datetime.date, priority: str, status: str, assigned_to: User, manager: OfficeTaskCollaborationManager):
        if assigned_to not in manager.users:
            raise ValueError("User not found in the system")        self.id = id
        self.title = title
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.status = status
        self.assigned_to = assigned_to
        self.comments = []
        self.attachments = []

    def add_comment(self, comment: str):
        # Add a comment to the task
        self.comments.append(comment)

    def add_attachment(self, attachment: str):
        # Add an attachment to the task
        self.attachments.append(attachment)

    def update_status(self, status: str):
        # Update the status of the task
        self.status = status

# OfficeTaskCollaborationManager class to manage tasks and users
class OfficeTaskCollaborationManager:
        manager = OfficeTaskCollaborationManager()
        manager.notification_queue.append((self, 'Task status updated'))
    def __init__(self):
    def process_notifications(self):
        while True:
            if self.notification_queue:
                task, message = self.notification_queue.pop(0)
                self.send_notification(task, message)
            else:
                time.sleep(1)
    def __init__(self):
        self.tasks: List[Task] = []
threading.Thread(target=self.process_notifications).start()
        self.users: List[User] = []
        self.notification_queue = []
        # Initialize the system with an empty list of users and tasks
        self.users: List[User] = []
        self.tasks: List[Task] = []

    def create_user(self, id: int, name: str, role: str):
        # Create a new user and add it to the system
        user = User(id, name, role)
        self.users.append(user)
        return user

    def create_task(self, id: int, title: str, description: str, deadline: datetime.date, priority: str, status: str, assigned_to: User):def assign_task(self, task: Task, user: User):
        if user in self.users:
            task.assigned_to = user
            self.notification_queue.append((task, 'Task assigned to you'))
        else:
            raise ValueError("User not found in the system")        self.notification_queue.append((task, 'Task assigned to you'))import threading

def generate_report(self):
    report = {
        "completed": [],
        "pending": [],
        "overdue": []
    }
    lock = threading.Lock()
    with lock:
        for task in self.tasks:
            if task.status == "Completed":
                report["completed"].append(task)
            elif task.status == "Not Started" or task.status == "In Progress":
                report["pending"].append(task)
            elif task.deadline < datetime.date.today():
                report["overdue"].append(task)
    return report    def send_notification(self, task: Task, message: str):
        # Send a notification to the assigned user
        print(f"Notification to {task.assigned_to.name}: {message}")

# Test cases for the system
class TestOfficeTaskCollaborationManager(unittest.TestCase):
    def test_create_user(self):
        # Test creating a new user
        manager = OfficeTaskCollaborationManager()
        user = manager.create_user(1, "John Doe", "Admin")
        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.role, "Admin")

    def test_create_task(self):
        # Test creating a new task
        manager = OfficeTaskCollaborationManager()
        user = manager.create_user(1, "John Doe", "Admin")
        task = manager.create_task(1, "Task 1", "Description 1", datetime.date(2024, 9, 16), "High", "Not Started", user)
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Task 1")
        self.assertEqual(task.description, "Description 1")
        self.assertEqual(task.deadline, datetime.date(2024, 9, 16))
        self.assertEqual(task.priority, "High")
        self.assertEqual(task.status, "Not Started")
        self.assertEqual(task.assigned_to, user)

    def test_assign_task(self):
        # Test assigning a task to a user
        manager = OfficeTaskCollaborationManager()
        user1 = manager.create_user(1, "John Doe", "Admin")
        user2 = manager.create_user(2, "Jane Doe", "User")
        task = manager.create_task(1, "Task 1", "Description 1", datetime.date(2024, 9, 16), "High", "Not Started", user1)
        manager.assign_task(task, user2)
        self.assertEqual(task.assigned_to, user2)

    def test_generate_report(self):
        # Test generating a report on task progress
        manager = OfficeTaskCollaborationManager()
        user = manager.create_user(1, "John Doe", "Admin")
        task1 = manager.create_task(1, "Task 1", "Description 1", datetime.date(2024, 9, 16), "High", "Completed", user)
        task2 = manager.create_task(2, "Task 2", "Description 2", datetime.date(2024, 9, 16), "High", "Not Started", user)
        task3 = manager.create_task(3, "Task 3", "Description 3", datetime.date(2023, 9, 16), "High", "Not Started", user)
        report = manager.generate_report()
        self.assertEqual(len(report["completed"]), 1)
        self.assertEqual(len(report["pending"]), 1)
        self.assertEqual(len(report["overdue"]), 1)

    def test_send_notification(self):
        # Test sending a notification to the assigned user
        manager = OfficeTaskCollaborationManager()
        user = manager.create_user(1, "John Doe", "Admin")
        task = manager.create_task(1, "Task 1", "Description 1", datetime.date(2024, 9, 16), "High", "Not Started", user)
        manager.send_notification(task, "Task assigned to you")

if __name__ == "__main__":
    unittest.main()