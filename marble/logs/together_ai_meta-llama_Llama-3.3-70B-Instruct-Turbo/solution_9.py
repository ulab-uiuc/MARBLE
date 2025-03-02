# solution.py
from datetime import datetime
from typing import List, Dict

class Project:
    """Represents a project with name, start and end dates, and description."""
    def __init__(self, name: str, start_date: str, end_date: str, description: str):
        # Initialize project attributes
        self.name = name
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d")
        self.description = description
        self.tasks = []

    def add_task(self, task):
        # Add a task to the project
        self.tasks.append(task)

    def __str__(self):
        # Return a string representation of the project
        return f"Project: {self.name}, Start Date: {self.start_date.date()}, End Date: {self.end_date.date()}, Description: {self.description}"


class Task:
    """Represents a task with name, description, deadline, and status."""
    def __init__(self, name: str, description: str, deadline: str):
        # Initialize task attributes
        self.name = name
        self.description = description
        self.deadline = datetime.strptime(deadline, "%Y-%m-%d")
        self.status = "Not Started"
        self.assignee = None

    def assign(self, assignee):
        # Assign the task to a team member
        self.assignee = assignee

    def update_status(self, status):
        # Update the status of the task
        self.status = status

    def __str__(self):
        # Return a string representation of the task
        return f"Task: {self.name}, Description: {self.description}, Deadline: {self.deadline.date()}, Status: {self.status}, Assignee: {self.assignee}"


class TeamMember:
    """Represents a team member with name and email."""
    def __init__(self, name: str, email: str):
        # Initialize team member attributes
        self.name = name
        self.email = email
        self.tasks = []
        self.performance = {"completion_rate": 0, "average_time": 0, "feedback": []}

    def add_task(self, task):
        # Add a task to the team member's tasks
        self.tasks.append(task)

    def update_performance(self, completion_rate, average_time, feedback):
        # Update the team member's performance metrics
        self.performance["completion_rate"] = completion_rate
        self.performance["average_time"] = average_time
        self.performance["feedback"].append(feedback)

    def __str__(self):
        # Return a string representation of the team member
        return f"Team Member: {self.name}, Email: {self.email}"


class MessagingSystem:
    """Represents a messaging system for team members to communicate."""
    def __init__(self):
        # Initialize messaging system attributes
        self.messages = []

    def send_message(self, sender, recipient, message):
        # Send a message from one team member to another
        self.messages.append({"sender": sender, "recipient": recipient, "message": message})

    def __str__(self):
        # Return a string representation of the messaging system
        return "Messaging System"


class ReportGenerator:
    """Represents a report generator for project progress, team performance, and individual performance metrics."""
    def __init__(self):
        # Initialize report generator attributes
        self.reports = []

    def generate_report(self, project, team_members):
        # Generate a report on project progress, team performance, and individual performance metrics
        report = {"project": project, "team_members": team_members}
        self.reports.append(report)

    def export_report(self, report, format):
        # Export the report in a specified format (e.g., PDF, CSV)
        if format == "PDF":
            # Export report as PDF
            print("Exporting report as PDF...")
        elif format == "CSV":
            # Export report as CSV
            print("Exporting report as CSV...")
        else:
            print("Invalid format. Please choose PDF or CSV.")

    def __str__(self):
        # Return a string representation of the report generator
        return "Report Generator"


class TeamCollaborationManager:def create_project(self, name, start_date, end_date, description):
def add_team_member(self, name, email):
    team_member = TeamMember(name, email)
    self.team_members.append(team_member)
    project = Project(name, start_date, end_date, description)
    self.projects.append(project)def send_message(self, sender, recipient, message):
        # Send a message from one team member to another
        self.messaging_system.send_message(sender, recipient, message)

    def generate_report(self, project, team_members):
        # Generate a report on project progress, team performance, and individual performance metrics
        self.report_generator.generate_report(project, team_members)

    def export_report(self, report, format):
        # Export the report in a specified format (e.g., PDF, CSV)
        self.report_generator.export_report(report, format)

    def __str__(self):
        # Return a string representation of the team collaboration manager
        return "Team Collaboration Manager"


# Test cases
def test_team_collaboration_manager():
    # Create a team collaboration manager
    manager = TeamCollaborationManager()

    # Create a project
    manager.create_project("Project 1", "2024-01-01", "2024-01-31", "This is a test project.")

    # Add team members
    manager.add_team_member("John Doe", "john.doe@example.com")
    manager.add_team_member("Jane Doe", "jane.doe@example.com")

    # Assign tasks
    project = manager.projects[0]
    task1 = Task("Task 1", "This is a test task.", "2024-01-15")
    task2 = Task("Task 2", "This is another test task.", "2024-01-20")
    manager.assign_task(project, task1, manager.team_members[0])
    manager.assign_task(project, task2, manager.team_members[1])

    # Send messages
    manager.send_message(manager.team_members[0], manager.team_members[1], "Hello, Jane!")
    manager.send_message(manager.team_members[1], manager.team_members[0], "Hi, John!")

    # Generate report
    manager.generate_report(project, manager.team_members)

    # Export report
    manager.export_report(manager.report_generator.reports[0], "PDF")

    # Print team collaboration manager
    print(manager)

    # Print projects
    for project in manager.projects:
        print(project)

    # Print team members
    for team_member in manager.team_members:
        print(team_member)

    # Print tasks
    for task in project.tasks:
        print(task)

    # Print messaging system
    print(manager.messaging_system)

    # Print report generator
    print(manager.report_generator)


if __name__ == "__main__":
    test_team_collaboration_manager()