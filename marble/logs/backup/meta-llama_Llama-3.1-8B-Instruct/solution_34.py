# project.py
class Project:
    def __init__(self, name, scope, budget, timeline):
        """
        Initialize a new project.

        Args:
            name (str): The name of the project.
            scope (str): The scope of the project.
            budget (float): The budget of the project.
            timeline (str): The timeline of the project.
        """
        self.name = name
        self.scope = scope
        self.budget = budget
        self.timeline = timeline
        self.tasks = []
        self.team_members = []
        self.project_plan = {}

    def add_task(self, task):
        """
        Add a task to the project plan.

        Args:
            task (Task): The task to add.
        """
        self.tasks.append(task)
        self.project_plan[task.name] = task

    def add_team_member(self, team_member):
        """
        Add a team member to the project.

        Args:
            team_member (TeamMember): The team member to add.
        """
        self.team_members.append(team_member)

    def assign_task(self, team_member, task):
        """
        Assign a task to a team member.

        Args:
            team_member (TeamMember): The team member to assign the task to.
            task (Task): The task to assign.
        """
        team_member.tasks.append(task)
        task.assigned_to = team_member

    def execute_task(self, task):
        """
        Execute a task.

        Args:
            task (Task): The task to execute.
        """
        task.status = "in_progress"
        print(f"Task '{task.name}' is being executed by {task.assigned_to.name}.")

    def resolve_issue(self, issue):
        """
        Resolve an issue.

        Args:
            issue (Issue): The issue to resolve.
        """
        print(f"Issue '{issue.name}' has been resolved.")
        issue.status = "resolved"


class Task:
    def __init__(self, name, duration, dependencies=None):
        """
        Initialize a new task.

        Args:
            name (str): The name of the task.
            duration (float): The duration of the task.
            dependencies (list, optional): The dependencies of the task. Defaults to None.
        """
        self.name = name
        self.duration = duration
        self.dependencies = dependencies if dependencies else []
        self.assigned_to = None
        self.status = "pending"


class TeamMember:
    def __init__(self, name, skills, availability):
        """
        Initialize a new team member.

        Args:
            name (str): The name of the team member.
            skills (list): The skills of the team member.
            availability (float): The availability of the team member.
        """
        self.name = name
        self.skills = skills
        self.availability = availability
        self.tasks = []


class Issue:
    def __init__(self, name, description, priority):
        """
        Initialize a new issue.

        Args:
            name (str): The name of the issue.
            description (str): The description of the issue.
            priority (str): The priority of the issue.
        """
        self.name = name
        self.description = description
        self.priority = priority
        self.status = "pending"


def main():
    # Create a new project
    project = Project("Project Synergy", "Software Development", 100000, "6 months")

    # Create tasks
    task1 = Task("Task 1", 10, ["Task 2"])
    task2 = Task("Task 2", 20)
    task3 = Task("Task 3", 30, ["Task 1"])

    # Add tasks to the project plan
    project.add_task(task1)
    project.add_task(task2)
    project.add_task(task3)

    # Create team members
    team_member1 = TeamMember("John Doe", ["Software Development"], 0.8)
    team_member2 = TeamMember("Jane Doe", ["Software Development"], 0.7)

    # Add team members to the project
    project.add_team_member(team_member1)
    project.add_team_member(team_member2)

    # Assign tasks to team members
    project.assign_task(team_member1, task1)
    project.assign_task(team_member2, task2)

    # Execute tasks
    project.execute_task(task1)
    project.execute_task(task2)

    # Create issues
    issue1 = Issue("Issue 1", "Technical problem", "high")
    issue2 = Issue("Issue 2", "Resource constraint", "low")

    # Resolve issues
    project.resolve_issue(issue1)
    project.resolve_issue(issue2)

    # Print the project plan
    print("Project Plan:")
    for task in project.tasks:
        print(f"Task: {task.name}, Duration: {task.duration}, Dependencies: {task.dependencies}, Assigned to: {task.assigned_to.name if task.assigned_to else 'Not assigned'}")

    # Print the team members
    print("\nTeam Members:")
    for team_member in project.team_members:
        print(f"Name: {team_member.name}, Skills: {team_member.skills}, Availability: {team_member.availability}")

    # Print the issues
    print("\nIssues:")
    for issue in [issue1, issue2]:
        print(f"Name: {issue.name}, Description: {issue.description}, Priority: {issue.priority}, Status: {issue.status}")


if __name__ == "__main__":
    main()