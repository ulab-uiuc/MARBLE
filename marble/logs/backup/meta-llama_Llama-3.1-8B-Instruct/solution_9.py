# team_collaboration_manager.py
# This is the main implementation of the Team Collaboration Manager.

class Project:
    """Represents a project with its name, start date, end date, and description."""
    
    def __init__(self, name, start_date, end_date, description):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.tasks = []
        self.messages = []
        self.team_members = []

    def add_task(self, task):
        """Adds a task to the project."""
        self.tasks.append(task)

    def add_message(self, message):
        """Adds a message to the project."""
        self.messages.append(message)

    def add_team_member(self, team_member):
        """Adds a team member to the project."""
        self.team_members.append(team_member)


class Task:
    """Represents a task with its name, deadline, and status."""
    
    def __init__(self, name, deadline, status="not started"):
        self.name = name
        self.deadline = deadline
        self.status = status
        self.assignee = None

    def assign(self, team_member):
        """Assigns the task to a team member."""
        self.assignee = team_member

    def update_status(self, status):
        """Updates the status of the task."""
        self.status = status


class TeamMember:
    """Represents a team member with their name and tasks assigned."""
    
    def __init__(self, name):def update_performance_metrics(self, task_completion_rate, average_time_taken, feedback):
    if not (0 <= task_completion_rate <= 1):
        raise ValueError("Task completion rate must be between 0 and 1")
    if average_time_taken <= 0:
        raise ValueError("Average time taken must be a positive number")
    if not isinstance(feedback, list) or not all(isinstance(item, str) for item in feedback):
        raise ValueError("Feedback must be a list of strings")
    self.performance_metrics["task_completion_rate"] = task_completion_rate
    self.performance_metrics["average_time_taken"] = average_time_taken
    self.performance_metrics["feedback"] = feedback    self.tasks = []
        self.performance_metrics = {
            "task_completion_rate": 0,
            "average_time_taken": 0,
            "feedback": []
        }

    def assign_task(self, task):
        """Assigns a task to the team member."""
        self.tasks.append(task)
        task.assign(self)

    def update_performance_metrics(self, task_completion_rate, average_time_taken, feedback):
        """Updates the performance metrics of the team member."""
        self.performance_metrics["task_completion_rate"] = task_completion_rate
        self.performance_metrics["average_time_taken"] = average_time_taken
        self.performance_metrics["feedback"] = feedback


class Message:
    """Represents a message with its content and sender."""
    
    def __init__(self, content, sender):
        self.content = content
        self.sender = sender


class TeamCollaborationManager:
    """Represents the team collaboration manager with its projects and team members."""
    
    def __init__(self):
        self.projects = []
        self.team_members = []

    def create_project(self, name, start_date, end_date, description):
        """Creates a new project."""
        project = Project(name, start_date, end_date, description)
        self.projects.append(project)
        return project

    def create_team_member(self, name):
        """Creates a new team member."""
        team_member = TeamMember(name)
        self.team_members.append(team_member)
        return team_member

    def add_task_to_project(self, project, task):
        """Adds a task to a project."""
        project.add_task(task)

    def add_message_to_project(self, project, message):
        """Adds a message to a project."""
        project.add_message(message)

    def add_team_member_to_project(self, project, team_member):
        """Adds a team member to a project."""
        project.add_team_member(team_member)

    def generate_report(self, project):
        """Generates a report for a project."""
        report = {
            "project_name": project.name,
            "project_description": project.description,
            "project_start_date": project.start_date,
            "project_end_date": project.end_date,
            "task_status": [task.status for task in project.tasks],
            "team_member_tasks": {team_member.name: [task.name for task in team_member.tasks] for team_member in project.team_members},
            "messages": [message.content for message in project.messages]
        }
        return report


# Test cases
if __name__ == "__main__":
    manager = TeamCollaborationManager()

    project = manager.create_project("Project 1", "2022-01-01", "2022-01-31", "This is a project.")
    team_member1 = manager.create_team_member("John Doe")
    team_member2 = manager.create_team_member("Jane Doe")

    task1 = Task("Task 1", "2022-01-15")
    task2 = Task("Task 2", "2022-01-20")

    project.add_task_to_project(project, task1)
    project.add_task_to_project(project, task2)

    team_member1.assign_task(task1)
    team_member2.assign_task(task2)

    message1 = Message("Hello, team!", team_member1)
    message2 = Message("Hi, John!", team_member2)

    project.add_message_to_project(project, message1)
    project.add_message_to_project(project, message2)

    manager.add_team_member_to_project(project, team_member1)
    manager.add_team_member_to_project(project, team_member2)

    report = manager.generate_report(project)
    print(report)

    # Print team member performance metrics
    print(team_member1.performance_metrics)
    print(team_member2.performance_metrics)