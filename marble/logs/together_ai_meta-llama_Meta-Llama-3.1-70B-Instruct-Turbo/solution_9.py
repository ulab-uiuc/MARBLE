# project.py
class Project:
    def __init__(self, name, start_date, end_date, description):
        """
        Initialize a Project object.

        Args:
            name (str): The name of the project.
            start_date (str): The start date of the project.
            end_date (str): The end date of the project.
            description (str): A brief description of the project.
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
            task (Task): The task to be added.
        """
        self.tasks.append(task)

    def __str__(self):
        return f"Project: {self.name}, Start Date: {self.start_date}, End Date: {self.end_date}, Description: {self.description}"


# task.py
class Task:
    def __init__(self, name, description, deadline, assigned_to):
        """
        Initialize a Task object.

        Args:
            name (str): The name of the task.
            description (str): A brief description of the task.
            deadline (str): The deadline for the task.
            assigned_to (str): The team member assigned to the task.
        """
        self.name = name
        self.description = description
        self.deadline = deadline
        self.assigned_to = assigned_to
        self.status = "Not Started"

    def update_status(self, status):
        """
        Update the status of the task.

        Args:
            status (str): The new status of the task.
        """
        self.status = status

    def __str__(self):
        return f"Task: {self.name}, Description: {self.description}, Deadline: {self.deadline}, Assigned To: {self.assigned_to}, Status: {self.status}"


# team_member.py
class TeamMember:
    def __init__(self, name):
        """
        Initialize a TeamMember object.

        Args:
            name (str): The name of the team member.
        """
        self.name = name
        self.tasks = []
        self.performance_dashboard = PerformanceDashboard()

    def add_task(self, task):
        """
        Add a task to the team member's tasks.

        Args:
            task (Task): The task to be added.
        """
        self.tasks.append(task)

    def __str__(self):
        return f"Team Member: {self.name}"


# performance_dashboard.py
class PerformanceDashboard:
    def __init__(self):
        """
        Initialize a PerformanceDashboard object.
        """
        self.task_completion_rate = 0
        self.average_time_taken = 0
        self.feedback = []

    def update_task_completion_rate(self, task_completion_rate):
        """
        Update the task completion rate.

        Args:
            task_completion_rate (float): The new task completion rate.
        """
        self.task_completion_rate = task_completion_rate

    def update_average_time_taken(self, average_time_taken):
        """
        Update the average time taken to complete tasks.

        Args:
            average_time_taken (float): The new average time taken.
        """
        self.average_time_taken = average_time_taken

    def add_feedback(self, feedback):
        """
        Add feedback to the performance dashboard.

        Args:
            feedback (str): The feedback to be added.
        """
        self.feedback.append(feedback)

    def __str__(self):
        return f"Task Completion Rate: {self.task_completion_rate}, Average Time Taken: {self.average_time_taken}, Feedback: {self.feedback}"


# messaging_system.py
class MessagingSystem:
    def __init__(self):
        """
        Initialize a MessagingSystem object.
        """
        self.messages = []

    def send_message(self, message):
        """
        Send a message.

        Args:
            message (str): The message to be sent.
        """
        self.messages.append(message)

    def __str__(self):
        return f"Messages: {self.messages}"


# team_collaboration_manager.py
class TeamCollaborationManager:
    def __init__(self):
        """
        Initialize a TeamCollaborationManager object.
        """
        self.projects = []
        self.team_members = []
        self.messaging_system = MessagingSystem()

    def create_project(self, name, start_date, end_date, description):
        """
        Create a new project.

        Args:
            name (str): The name of the project.
            start_date (str): The start date of the project.
            end_date (str): The end date of the project.
            description (str): A brief description of the project.
        """
        project = Project(name, start_date, end_date, description)
        self.projects.append(project)

    def create_task(self, project_name, task_name, description, deadline, assigned_to):
        """
        Create a new task.

        Args:
            project_name (str): The name of the project.
            task_name (str): The name of the task.
            description (str): A brief description of the task.
            deadline (str): The deadline for the task.
            assigned_to (str): The team member assigned to the task.
        """
        project = next((project for project in self.projects if project.name == project_name), None)
        if project:
            task = Task(task_name, description, deadline, assigned_to)
            project.add_task(task)
            team_member = next((team_member for team_member in self.team_members if team_member.name == assigned_to), None)
            if team_member:
                team_member.add_task(task)

    def send_message(self, message):
        """
        Send a message.

        Args:
            message (str): The message to be sent.
        """
        self.messaging_system.send_message(message)

    def __str__(self):
        return f"Projects: {self.projects}, Team Members: {self.team_members}, Messaging System: {self.messaging_system}"


# solution.py
def main():
    team_collaboration_manager = TeamCollaborationManager()

    # Create team members
    team_member1 = TeamMember("John Doe")
    team_member2 = TeamMember("Jane Doe")
    team_collaboration_manager.team_members.extend([team_member1, team_member2])

    # Create projects
    team_collaboration_manager.create_project("Project 1", "2022-01-01", "2022-01-31", "This is project 1")
    team_collaboration_manager.create_project("Project 2", "2022-02-01", "2022-02-28", "This is project 2")

    # Create tasks
    team_collaboration_manager.create_task("Project 1", "Task 1", "This is task 1", "2022-01-15", "John Doe")
    team_collaboration_manager.create_task("Project 1", "Task 2", "This is task 2", "2022-01-20", "Jane Doe")
    team_collaboration_manager.create_task("Project 2", "Task 3", "This is task 3", "2022-02-10", "John Doe")
    team_collaboration_manager.create_task("Project 2", "Task 4", "This is task 4", "2022-02-15", "Jane Doe")

    # Send messages
    team_collaboration_manager.send_message("Hello, team!")
    team_collaboration_manager.send_message("This is a test message.")

    # Print team collaboration manager
    print(team_collaboration_manager)

if __name__ == "__main__":
    main()