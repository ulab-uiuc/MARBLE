# solution.py

# Import required libraries
from datetime import datetime
from enum import Enum
from typing import List, Dict

# Define a class for TaskStatus
class TaskStatus(Enum):
    NOT_STARTED = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    OVERDUE = 4

# Define a class for TaskPriority
class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

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

    def create_task(self, title: str, description: str, deadline: datetime, priority: TaskPriority, assigned_to: User) -> Task:
        task = Task(len(self.tasks) + 1, title, description, deadline, priority, TaskStatus.NOT_STARTED, assigned_to)
        self.tasks.append(task)
        return task

    def assign_task(self, task: Task, assigned_to: User):
        task.assigned_to = assigned_to

    def update_task_status(self, task: Task, status: TaskStatus):
        task.update_status(status)

    def add_comment_to_task(self, task: Task, comment: str):
        task.add_comment(comment)

    def add_attachment_to_task(self, task: Task, attachment: str):
        task.add_attachment(attachment)

    def generate_report(self) -> Dict[str, List[Task]]:report = {
            "completed": [task for task in self.tasks if task.status == TaskStatus.COMPLETED],
            "pending": [task for task in self.tasks if (task.status == TaskStatus.NOT_STARTED or task.status == TaskStatus.IN_PROGRESS) and task.deadline >= datetime.now()],
            "overdue": [task for task in self.tasks if (task.deadline < datetime.now() and task.status != TaskStatus.COMPLETED)]
        }        return report

    def send_notification(self, task: Task, message: str):
        print(f"Notification sent to {task.assigned_to.name}: {message}")

# Define a class for TestOfficeTaskCollaborationManager
class TestOfficeTaskCollaborationManager:
    def test_create_task(self):
        manager = OfficeTaskCollaborationManager()
        user = User(1, "John Doe", "Admin")
        task = manager.create_task("Test Task", "This is a test task", datetime(2024, 7, 26), TaskPriority.HIGH, user)
        assert task.title == "Test Task"
        assert task.description == "This is a test task"
        assert task.deadline == datetime(2024, 7, 26)
        assert task.priority == TaskPriority.HIGH
        assert task.status == TaskStatus.NOT_STARTED
        assert task.assigned_to == user

    def test_assign_task(self):
        manager = OfficeTaskCollaborationManager()
        user1 = User(1, "John Doe", "Admin")
        user2 = User(2, "Jane Doe", "User")
        task = manager.create_task("Test Task", "This is a test task", datetime(2024, 7, 26), TaskPriority.HIGH, user1)
        manager.assign_task(task, user2)
        assert task.assigned_to == user2

    def test_update_task_status(self):
        manager = OfficeTaskCollaborationManager()
        user = User(1, "John Doe", "Admin")
        task = manager.create_task("Test Task", "This is a test task", datetime(2024, 7, 26), TaskPriority.HIGH, user)
        manager.update_task_status(task, TaskStatus.IN_PROGRESS)
        assert task.status == TaskStatus.IN_PROGRESS

    def test_add_comment_to_task(self):
        manager = OfficeTaskCollaborationManager()
        user = User(1, "John Doe", "Admin")
        task = manager.create_task("Test Task", "This is a test task", datetime(2024, 7, 26), TaskPriority.HIGH, user)
        manager.add_comment_to_task(task, "This is a test comment")
        assert len(task.comments) == 1
        assert task.comments[0] == "This is a test comment"

    def test_add_attachment_to_task(self):
        manager = OfficeTaskCollaborationManager()
        user = User(1, "John Doe", "Admin")
        task = manager.create_task("Test Task", "This is a test task", datetime(2024, 7, 26), TaskPriority.HIGH, user)
        manager.add_attachment_to_task(task, "test_attachment.txt")
        assert len(task.attachments) == 1
        assert task.attachments[0] == "test_attachment.txt"

    def test_generate_report(self):
        manager = OfficeTaskCollaborationManager()
        user = User(1, "John Doe", "Admin")
        task1 = manager.create_task("Test Task 1", "This is a test task", datetime(2024, 7, 26), TaskPriority.HIGH, user)
        task2 = manager.create_task("Test Task 2", "This is a test task", datetime(2024, 7, 26), TaskPriority.HIGH, user)
        task3 = manager.create_task("Test Task 3", "This is a test task", datetime(2024, 7, 26), TaskPriority.HIGH, user)
        manager.update_task_status(task1, TaskStatus.COMPLETED)
        manager.update_task_status(task2, TaskStatus.IN_PROGRESS)
        manager.update_task_status(task3, TaskStatus.OVERDUE)
        report = manager.generate_report()
        assert len(report["completed"]) == 1
        assert len(report["pending"]) == 1
        assert len(report["overdue"]) == 1

    def test_send_notification(self):
        manager = OfficeTaskCollaborationManager()
        user = User(1, "John Doe", "Admin")
        task = manager.create_task("Test Task", "This is a test task", datetime(2024, 7, 26), TaskPriority.HIGH, user)
        manager.send_notification(task, "This is a test notification")

# Run the tests
test_manager = TestOfficeTaskCollaborationManager()
test_manager.test_create_task()
test_manager.test_assign_task()
test_manager.test_update_task_status()
test_manager.test_add_comment_to_task()
test_manager.test_add_attachment_to_task()
test_manager.test_generate_report()
test_manager.test_send_notification()