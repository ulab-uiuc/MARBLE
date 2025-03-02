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
    def __init__(self, id, description, deadline, priority_level, assigned_user=None):
        """
        Initialize a task with id, description, deadline, priority level, and assigned user.
        
        Args:
        id (int): Unique task id.
        description (str): Detailed task description.
        deadline (datetime): Task deadline.
        priority_level (PriorityLevel): Task priority level.
        assigned_user (str, optional): Assigned user. Defaults to None.
        """
        self.id = id
        self.description = description
        self.deadline = deadline
        self.priority_level = priority_level
        self.assigned_user = assigned_user
        self.status = TaskStatus.NOT_STARTED
        self.messages = []

    def assign_task(self, user):
        """
        Assign the task to a user.
        
        Args:
        user (str): User to assign the task to.
        """
        self.assigned_user = user

    def update_status(self, status):
        """
        Update the task status.
        
        Args:
        status (TaskStatus): New task status.
        """
        self.status = status

    def add_message(self, message):
        """
        Add a message to the task.
        
        Args:
        message (str): Message to add.
        """
        self.messages.append(message)

# Define a class for the task collaborator system
class OfficeTaskCollaborator:
    def __init__(self):
        """
        Initialize the task collaborator system.
        """
        self.tasks = {}
        self.users = {}
        self.calendar = {}

    def create_task(self, id, description, deadline, priority_level):
        """
        Create a new task.
        
        Args:
        id (int): Unique task id.
        description (str): Detailed task description.
        deadline (datetime): Task deadline.
        priority_level (PriorityLevel): Task priority level.
        
        Returns:
        Task: Created task.
        """
        task = Task(id, description, deadline, priority_level)
        self.tasks[id] = task
        return task

    def assign_task(self, task_id, user):
        """
        Assign a task to a user.
        
        Args:
        task_id (int): Task id to assign.
        user (str): User to assign the task to.
        """
        if task_id in self.tasks:
            self.tasks[task_id].assign_task(user)
            if user not in self.users:
                self.users[user] = []
            self.users[user].append(task_id)

    def update_task_status(self, task_id, status):
        """
        Update the status of a task.
        
        Args:
        task_id (int): Task id to update.
        status (TaskStatus): New task status.
        """
        if task_id in self.tasks:
            self.tasks[task_id].update_status(status)

    def sync_with_calendar(self, task_id):
        """
        Sync a task with the calendar.
        
        Args:
        task_id (int): Task id to sync.
        """
        if task_id in self.tasks:
            deadline = self.tasks[task_id].deadline
            self.calendar[task_id] = deadline

    def generate_report(self):
        """
        Generate a report on task completion rates, team performance, and project progress.
        
        Returns:
        str: Report.
        """
        report = ""
        for task_id, task in self.tasks.items():
            report += f"Task {task_id}: {task.description} - Status: {task.status.name}\n"
        return report

    def add_message(self, task_id, message):
        """
        Add a message to a task.
        
        Args:
        task_id (int): Task id to add the message to.
        message (str): Message to add.
        """
        if task_id in self.tasks:
            self.tasks[task_id].add_message(message)

# Define a function to test the task collaborator system
def test_task_collaborator():
    collaborator = OfficeTaskCollaborator()
    
    # Create tasks
    task1 = collaborator.create_task(1, "Task 1 description", datetime(2024, 9, 16), PriorityLevel.HIGH)
    task2 = collaborator.create_task(2, "Task 2 description", datetime(2024, 9, 17), PriorityLevel.MEDIUM)
    
    # Assign tasks
    collaborator.assign_task(1, "User 1")
    collaborator.assign_task(2, "User 2")
    
    # Update task status
    collaborator.update_task_status(1, TaskStatus.IN_PROGRESS)
    
    # Sync with calendar
    collaborator.sync_with_calendar(1)
    
    # Generate report
    report = collaborator.generate_report()
    print(report)
    
    # Add message
    collaborator.add_message(1, "Message 1")

# Run the test
test_task_collaborator()

# Test cases
class TestTaskCollaborator:
    def test_create_task(self):
        collaborator = OfficeTaskCollaborator()
        task = collaborator.create_task(1, "Task 1 description", datetime(2024, 9, 16), PriorityLevel.HIGH)
        assert task.id == 1
        assert task.description == "Task 1 description"
        assert task.deadline == datetime(2024, 9, 16)
        assert task.priority_level == PriorityLevel.HIGH

    def test_assign_task(self):
        collaborator = OfficeTaskCollaborator()
        task = collaborator.create_task(1, "Task 1 description", datetime(2024, 9, 16), PriorityLevel.HIGH)
        collaborator.assign_task(1, "User 1")
        assert task.assigned_user == "User 1"

    def test_update_task_status(self):
        collaborator = OfficeTaskCollaborator()
        task = collaborator.create_task(1, "Task 1 description", datetime(2024, 9, 16), PriorityLevel.HIGH)
        collaborator.update_task_status(1, TaskStatus.IN_PROGRESS)
        assert task.status == TaskStatus.IN_PROGRESS

    def test_sync_with_calendar(self):
        collaborator = OfficeTaskCollaborator()
        task = collaborator.create_task(1, "Task 1 description", datetime(2024, 9, 16), PriorityLevel.HIGH)
        collaborator.sync_with_calendar(1)
        assert collaborator.calendar[1] == datetime(2024, 9, 16)

    def test_generate_report(self):
        collaborator = OfficeTaskCollaborator()
        task = collaborator.create_task(1, "Task 1 description", datetime(2024, 9, 16), PriorityLevel.HIGH)
        report = collaborator.generate_report()
        assert report == "Task 1: Task 1 description - Status: NOT_STARTED\n"

    def test_add_message(self):
        collaborator = OfficeTaskCollaborator()
        task = collaborator.create_task(1, "Task 1 description", datetime(2024, 9, 16), PriorityLevel.HIGH)
        collaborator.add_message(1, "Message 1")
        assert task.messages == ["Message 1"]

# Run the test cases
test_cases = TestTaskCollaborator()
test_cases.test_create_task()
test_cases.test_assign_task()
test_cases.test_update_task_status()
test_cases.test_sync_with_calendar()
test_cases.test_generate_report()
test_cases.test_add_message()