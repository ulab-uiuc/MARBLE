# solution.py
from datetime import datetime
from enum import Enum
import calendar

# Define an Enum for task status
class TaskStatus(Enum):
    NOT_STARTED = 1
    IN_PROGRESS = 2
    COMPLETED = 3

# Define an Enum for priority levels
class PriorityLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

# Define a class for tasks
class Task:
    def __init__(self, id, description, deadline, priority, assigned_to=None):
        """
        Initialize a task with id, description, deadline, priority, and assigned_to.
        
        Args:
        id (int): Unique task id.
        description (str): Task description.
        deadline (datetime): Task deadline.
        priority (PriorityLevel): Task priority level.
        assigned_to (str, optional): User assigned to the task. Defaults to None.
        """
        self.id = id
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.assigned_to = assigned_to
        self.status = TaskStatus.NOT_STARTED

    def update_status(self, status):
        """
        Update the task status.
        
        Args:
        status (TaskStatus): New task status.
        """
        self.status = status

# Define a class for users
class User:
    def __init__(self, id, name):
        """
        Initialize a user with id and name.
        
        Args:
        id (int): Unique user id.
        name (str): User name.
        """
        self.id = id
        self.name = name
        self.tasks = []

    def assign_task(self, task):
        """
        Assign a task to the user.
        
        Args:
        task (Task): Task to be assigned.
        """
        self.tasks.append(task)
        task.assigned_to = self.name

# Define a class for the task collaborator system
class OfficeTaskCollaborator:class Messaging:
    def __init__(self):
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login('your-email@gmail.com', 'your-password')
    def send_message(self, message):
        self.server.sendmail('your-email@gmail.com', 'recipient-email@gmail.com', message)
        self.server.quit()def test_send_message():
    messaging = Messaging()
    messaging.send_message("Hello, world!")

# Run test cases
test_create_task()
test_assign_task()
test_update_task_status()
test_sync_with_calendar()
test_generate_report()
test_create_user()
test_send_message()

# Example usage
collaborator = OfficeTaskCollaborator()
user = collaborator.create_user("John Doe")
task = collaborator.create_task("Test task", datetime(2024, 9, 16), PriorityLevel.HIGH)
collaborator.assign_task(task, user)
collaborator.update_task_status(task, TaskStatus.IN_PROGRESS)
collaborator.sync_with_calendar(task)
collaborator.generate_report()

messaging = Messaging()
messaging.send_message("Hello, world!")