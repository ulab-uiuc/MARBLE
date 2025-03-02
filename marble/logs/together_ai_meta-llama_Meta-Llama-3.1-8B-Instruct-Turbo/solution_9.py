# team_collaboration_manager.py

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
    
    def __init__(self, name, deadline):
        self.name = name
        self.deadline = deadline
        self.status = "Not Started"
        self.assignee = None
        self.comments = []

    def assign(self, team_member):
        """Assigns the task to a team member."""
        self.assignee = team_member

    def update_status(self, status):
        """Updates the status of the task."""
        self.status = status

    def add_comment(self, comment):
        """Adds a comment to the task."""
        self.comments.append(comment)


class TeamMember:
    """Represents a team member with their name and performance metrics."""
    
    def __init__(self, name):
        self.name = name
        self.task_completion_rate = 0
        self.average_time_taken = 0
        self.feedback = []
        self.tasks_assigned = []

    def add_task(self, task):
        """Adds a task assigned to the team member."""
        self.tasks_assigned.append(task)

    def update_task_completion_rate(self, completion_rate):
        """Updates the task completion rate of the team member."""
        self.task_completion_rate = completion_rate

    def update_average_time_taken(self, average_time):
        """Updates the average time taken by the team member."""
        self.average_time_taken = average_time

    def add_feedback(self, feedback):
        """Adds feedback to the team member."""
        self.feedback.append(feedback)


class Message:
    """Represents a message with its content and sender."""
    
    def __init__(self, content, sender):
        self.content = content
        self.sender = sender


class PerformanceDashboard:
    """Represents a performance dashboard with metrics for a team member."""
    
    def __init__(self, team_member):
        self.team_member = team_member
        self.metrics = {}

    def update_metrics(self, metrics):
        """Updates the metrics of the performance dashboard."""
        self.metrics = metrics


class TeamCollaborationManager:
    """Represents a team collaboration manager with its projects, team members, and performance dashboards."""
    
    def __init__(self):
        self.projects = []
        self.team_members = []
        self.performance_dashboards = []

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

    def create_performance_dashboard(self, team_member):
        """Creates a new performance dashboard."""
        performance_dashboard = PerformanceDashboard(team_member)
        self.performance_dashboards.append(performance_dashboard)
        return performance_dashboard

    def generate_report(self, project):
        """Generates a report for a project."""
        report = {
            "project_name": project.name,
            "project_start_date": project.start_date,
            "project_end_date": project.end_date,
            "project_description": project.description,
            "tasks": [task.name for task in project.tasks],
            "messages": [message.content for message in project.messages],
            "team_members": [team_member.name for team_member in project.team_members]
        }
        return report


# Test cases
if __name__ == "__main__":
    # Create a team collaboration manager
    team_collaboration_manager = TeamCollaborationManager()

    # Create a project
    project = team_collaboration_manager.create_project("Project 1", "2022-01-01", "2022-01-31", "This is a project.")

    # Create team members
    team_member1 = team_collaboration_manager.create_team_member("John Doe")
    team_member2 = team_collaboration_manager.create_team_member("Jane Doe")

    # Create tasks
    task1 = Task("Task 1", "2022-01-15")
    task2 = Task("Task 2", "2022-01-20")

    # Assign tasks to team members
    task1.assign(team_member1)
    task2.assign(team_member2)

    # Add tasks to project
    project.add_task(task1)
    project.add_task(task2)

    # Add team members to project
    project.add_team_member(team_member1)
    project.add_team_member(team_member2)

    # Create performance dashboard
    performance_dashboard = team_collaboration_manager.create_performance_dashboard(team_member1)

    # Update task completion rate
    performance_dashboard.update_metrics({"task_completion_rate": 0.5})

    # Generate report
    report = team_collaboration_manager.generate_report(project)

    # Print report
    print(report)