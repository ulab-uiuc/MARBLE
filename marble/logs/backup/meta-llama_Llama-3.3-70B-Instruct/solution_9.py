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
        # Add a task to the team member's task list
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
    def __init__(self):
        # ... existing code ...
        self.error_messages = []
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

    def generate_report(self, report_type, data):
        # Generate a report based on the report type and data
        self.reports.append({"report_type": report_type, "data": data})

    def export_report(self, report_type, format):
        # Export a report in a specific format
        for report in self.reports:
            if report["report_type"] == report_type:
                if format == "PDF":
                    # Export report as PDF
                    print("Exporting report as PDF")
                elif format == "CSV":
                    # Export report as CSV
                    print("Exporting report as CSV")
                else:
                    print("Invalid format")

    def __str__(self):
        # Return a string representation of the report generator
        return "Report Generator"


class TeamCollaborationManager:def create_project(self, name, start_date, end_date, description):
    project = Project(name, start_date, end_date, description)
    self.projects.append(project)def assign_task(self, project_name, task_name, team_member_name):
        try:
            # Assign a task to a team member
            for project in self.projects:
                if project.name == project_name:
                    for task in project.tasks:
                        if task.name == task_name:
                            for team_member in self.team_members:
                                if team_member.name == team_member_name:
                                    task.assign(team_member)
                                    team_member.add_task(task)
                                    return
                            raise ValueError(f"Team member '{team_member_name}' not found")
                    raise ValueError(f"Task '{task_name}' not found in project '{project_name}'")
            raise ValueError(f"Project '{project_name}' not found")
        except ValueError as e:
            self.error_messages.append(str(e))def send_message(self, sender_name, recipient_name, message):
        # Send a message from one team member to another
        for team_member in self.team_members:
            if team_member.name == sender_name:
                sender = team_member
                break
        for team_member in self.team_members:
            if team_member.name == recipient_name:
                recipient = team_member
                break
        self.messaging_system.send_message(sender, recipient, message)

    def generate_report(self, report_type, data):
        # Generate a report based on the report type and data
        self.report_generator.generate_report(report_type, data)

    def export_report(self, report_type, format):
        # Export a report in a specific format
        self.report_generator.export_report(report_type, format)

    def __str__(self):
        # Return a string representation of the team collaboration manager
        return "Team Collaboration Manager"


# Test cases
def test_team_collaboration_manager():
    # Create a team collaboration manager
    team_collaboration_manager = TeamCollaborationManager()

    # Create projects
    team_collaboration_manager.create_project("Project 1", "2022-01-01", "2022-01-31", "Project 1 description")
    team_collaboration_manager.create_project("Project 2", "2022-02-01", "2022-02-28", "Project 2 description")

    # Add team members
    team_collaboration_manager.add_team_member("John Doe", "john.doe@example.com")
    team_collaboration_manager.add_team_member("Jane Doe", "jane.doe@example.com")

    # Create tasks
    project1 = team_collaboration_manager.projects[0]
    project1.add_task(Task("Task 1", "Task 1 description", "2022-01-15"))
    project1.add_task(Task("Task 2", "Task 2 description", "2022-01-20"))

    # Assign tasks
    team_collaboration_manager.assign_task("Project 1", "Task 1", "John Doe")
    team_collaboration_manager.assign_task("Project 1", "Task 2", "Jane Doe")

    # Send messages
    team_collaboration_manager.send_message("John Doe", "Jane Doe", "Hello, Jane!")
    team_collaboration_manager.send_message("Jane Doe", "John Doe", "Hi, John!")

    # Generate reports
    team_collaboration_manager.generate_report("Project Progress", {"project_name": "Project 1", "progress": 50})
    team_collaboration_manager.generate_report("Team Performance", {"team_name": "Team 1", "performance": 80})

    # Export reports
    team_collaboration_manager.export_report("Project Progress", "PDF")
    team_collaboration_manager.export_report("Team Performance", "CSV")

    # Print team collaboration manager
    print(team_collaboration_manager)

    # Print projects
    for project in team_collaboration_manager.projects:
        print(project)

    # Print team members
    for team_member in team_collaboration_manager.team_members:
        print(team_member)

    # Print messaging system
    print(team_collaboration_manager.messaging_system)

    # Print report generator
    print(team_collaboration_manager.report_generator)


if __name__ == "__main__":
    test_team_collaboration_manager()