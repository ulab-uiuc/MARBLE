# project.py
class Project:
    def __init__(self, name, start_date, end_date, description):
        """
        Initialize a Project object.

        Args:
            name (str): Project name.
            start_date (str): Project start date.
            end_date (str): Project end date.
            description (str): Project description.
        """
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.tasks = []

    def add_task(self, task):
        """
        Add a task to the project.

        Args:
            task (Task): Task object to add.
        """
        self.tasks.append(task)

    def get_project_progress(self):
        """
        Calculate project progress.

        Returns:
            float: Project progress as a percentage.
        """
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for task in self.tasks if task.status == "completed")
        return (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0


# task.py
class Task:
    def __init__(self, name, description, deadline, assigned_to):
        """
        Initialize a Task object.

        Args:
            name (str): Task name.
            description (str): Task description.
            deadline (str): Task deadline.
            assigned_to (str): Task assignee.
        """
        self.name = name
        self.description = description
        self.deadline = deadline
        self.assigned_to = assigned_to
        self.status = "not started"

    def update_status(self, status):
        """
        Update task status.

        Args:
            status (str): New task status.
        """
        self.status = status


# user.py
class User:
    def __init__(self, name):
        """
        Initialize a User object.

        Args:
            name (str): User name.
        """
        self.name = name
        self.tasks = []
        self.performance_dashboard = {"task_completion_rate": 0, "average_time_taken": 0, "feedback": []}

    def add_task(self, task):
        """
        Add a task to the user.

        Args:
            task (Task): Task object to add.
        """
        self.tasks.append(task)

    def update_performance_dashboard(self):
        """
        Update user performance dashboard.
        """
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for task in self.tasks if task.status == "completed")
        self.performance_dashboard["task_completion_rate"] = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        # Calculate average time taken to complete tasks
        # This is a simplified example and actual implementation may vary
        self.performance_dashboard["average_time_taken"] = sum(task.deadline for task in self.tasks if task.status == "completed") / completed_tasks if completed_tasks > 0 else 0


# message.py
class Message:
    def __init__(self, content, sender, receiver):
        """
        Initialize a Message object.

        Args:
            content (str): Message content.
            sender (str): Message sender.
            receiver (str): Message receiver.
        """
        self.content = content
        self.sender = sender
        self.receiver = receiver
        self.attachments = []

    def add_attachment(self, attachment):
        """
        Add an attachment to the message.

        Args:
            attachment (str): Attachment to add.
        """
        self.attachments.append(attachment)


# team_collaboration_manager.py
class TeamCollaborationManager:def create_task(self, project_name, user_name, task_name, description, deadline, assigned_to):task = Task(name, description, deadline, assigned_to)
        return task
raise ValueError("Project or user not found")
project = next((project for project in self.projects if project.name == project_name), None)
user = next((user for user in self.users if user.name == user_name), None)
if project and user:
    project.add_task(task)
    user.add_task(task)

    def create_user(self, name):
        """
        Create a new user.

        Args:
            name (str): User name.
        """
        user = User(name)
        self.users.append(user)
        return user

    def send_message(self, content, sender, receiver):
        """
        Send a message.

        Args:
            content (str): Message content.
            sender (str): Message sender.
            receiver (str): Message receiver.
        """
        message = Message(content, sender, receiver)
        self.messages.append(message)
        return message

    def generate_report(self, project_name):
        """
        Generate a report for a project.

        Args:
            project_name (str): Project name.

        Returns:
            str: Project report.
        """
        project = next((project for project in self.projects if project.name == project_name), None)
        if project:
            report = f"Project: {project.name}\n"
            report += f"Start Date: {project.start_date}\n"
            report += f"End Date: {project.end_date}\n"
            report += f"Description: {project.description}\n"
            report += f"Progress: {project.get_project_progress()}%\n"
            return report
        else:
            return "Project not found"


# test_team_collaboration_manager.py
import unittest
from team_collaboration_manager import TeamCollaborationManager

class TestTeamCollaborationManager(unittest.TestCase):
    def test_create_project(self):
        manager = TeamCollaborationManager()
        project = manager.create_project("Test Project", "2022-01-01", "2022-01-31", "This is a test project")
        self.assertEqual(project.name, "Test Project")
        self.assertEqual(project.start_date, "2022-01-01")
        self.assertEqual(project.end_date, "2022-01-31")
        self.assertEqual(project.description, "This is a test project")

    def test_create_task(self):
        manager = TeamCollaborationManager()
        task = manager.create_task("Test Task", "This is a test task", "2022-01-15", "John Doe")
        self.assertEqual(task.name, "Test Task")
        self.assertEqual(task.description, "This is a test task")
        self.assertEqual(task.deadline, "2022-01-15")
        self.assertEqual(task.assigned_to, "John Doe")

    def test_create_user(self):
        manager = TeamCollaborationManager()
        user = manager.create_user("John Doe")
        self.assertEqual(user.name, "John Doe")

    def test_send_message(self):
        manager = TeamCollaborationManager()
        message = manager.send_message("Hello, world!", "John Doe", "Jane Doe")
        self.assertEqual(message.content, "Hello, world!")
        self.assertEqual(message.sender, "John Doe")
        self.assertEqual(message.receiver, "Jane Doe")

    def test_generate_report(self):
        manager = TeamCollaborationManager()
        project = manager.create_project("Test Project", "2022-01-01", "2022-01-31", "This is a test project")
        report = manager.generate_report("Test Project")
        self.assertIn("Project: Test Project", report)
        self.assertIn("Start Date: 2022-01-01", report)
        self.assertIn("End Date: 2022-01-31", report)
        self.assertIn("Description: This is a test project", report)
        self.assertIn("Progress: 0.0%", report)

if __name__ == "__main__":
    unittest.main()