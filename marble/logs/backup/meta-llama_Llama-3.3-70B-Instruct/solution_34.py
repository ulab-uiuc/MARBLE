# solution.py

class Task:
    """Represents a task in the project."""
    def __init__(self, name, duration, dependencies=None):
        # Initialize the task with a name, duration, and optional dependencies.
        self.name = name
        self.duration = duration
        self.dependencies = dependencies if dependencies else []
        self.status = "Not Started"

    def start(self):
        # Start the task.
        self.status = "In Progress"

    def complete(self):
        # Complete the task.
        self.status = "Completed"


class TeamMember:def assign_task(self, task):
        self.tasks.append(task)def __init__(self, name, skills):
self.workload = 0
        # Initialize the team member with a name and skills.
        self.name = name
        self.skills = skills
        self.tasks = []

    def assign_task(self, task):

        # Assign a task to the team member.
        self.tasks.append(task)


class Project:
    """Represents a project."""
    def __init__(self, name, scope, budget, timeline):
        # Initialize the project with a name, scope, budget, and timeline.
        self.name = name
        self.scope = scope
        self.budget = budget
        self.timeline = timeline
        self.tasks = []
        self.team_members = []

    def add_task(self, task):
        # Add a task to the project.
        self.tasks.append(task)

    def add_team_member(self, team_member):
        # Add a team member to the project.
        self.team_members.append(team_member)

    def assign_tasks(self):for task in self.tasks:
            available_team_members = [team_member for team_member in self.team_members if task.name in team_member.skills]
            if available_team_members:
                team_member_with_lowest_workload = min(available_team_members, key=lambda team_member: team_member.workload)
                team_member_with_lowest_workload.assign_task(task)
                team_member_with_lowest_workload.workload += task.durationdef execute_tasks(self):
        # Execute the tasks in the project.
        for task in self.tasks:
            task.start()
            # Simulate task execution (for demonstration purposes only).
            print(f"Task {task.name} is being executed by {', '.join([team_member.name for team_member in self.team_members if task in team_member.tasks])}")
            task.complete()

    def resolve_issues(self):
        # Resolve issues that arise during the project.
        # For demonstration purposes, assume there are no issues.
        print("No issues to resolve.")

    def deliver_project(self):
        # Deliver the project.
        print("Project delivered successfully.")


class ProjectSynergy:
    """Represents the ProjectSynergy game."""
    def __init__(self):
        # Initialize the game.
        self.project = None

    def setup_project(self):
        # Set up the project.
        name = input("Enter project name: ")
        scope = input("Enter project scope: ")
        budget = int(input("Enter project budget: "))
        timeline = int(input("Enter project timeline: "))

        self.project = Project(name, scope, budget, timeline)

        num_tasks = int(input("Enter number of tasks: "))
        for i in range(num_tasks):
            task_name = input(f"Enter task {i+1} name: ")
            task_duration = int(input(f"Enter task {i+1} duration: "))
            dependencies = input(f"Enter task {i+1} dependencies (comma-separated): ")
            dependencies = [dep.strip() for dep in dependencies.split(",")] if dependencies else []
            task = Task(task_name, task_duration, dependencies)
            self.project.add_task(task)

        num_team_members = int(input("Enter number of team members: "))
        for i in range(num_team_members):
            team_member_name = input(f"Enter team member {i+1} name: ")
            skills = input(f"Enter team member {i+1} skills (comma-separated): ")
            skills = [skill.strip() for skill in skills.split(",")]
            team_member = TeamMember(team_member_name, skills)
            self.project.add_team_member(team_member)

    def play_game(self):
        # Play the game.
        self.setup_project()
        self.project.assign_tasks()
        self.project.execute_tasks()
        self.project.resolve_issues()
        self.project.deliver_project()


if __name__ == "__main__":
    game = ProjectSynergy()
    game.play_game()