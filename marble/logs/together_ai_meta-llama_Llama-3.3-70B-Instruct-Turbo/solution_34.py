# solution.py

class Task:
    """Represents a task in the project."""
    def __init__(self, name, duration, dependencies=None):
        # Initialize task with name, duration, and dependencies
        self.name = name
        self.duration = duration
        self.dependencies = dependencies if dependencies else []
        self.status = "Not Started"

    def start_task(self):
        # Start the task
        self.status = "In Progress"

    def complete_task(self):
        # Complete the task
        self.status = "Completed"


class TeamMember:
    """Represents a team member."""
    def __init__(self, name, skills, availability):
        # Initialize team member with name, skills, and availability
        self.name = name
        self.skills = skills
        self.availability = availability
        self.tasks = []

    def assign_task(self, task):
        # Assign a task to the team member
        self.tasks.append(task)


class Project:
    """Represents a project."""
    def __init__(self, name, scope, budget, timeline):
        # Initialize project with name, scope, budget, and timeline
        self.name = name
        self.scope = scope
        self.budget = budget
        self.timeline = timeline
        self.tasks = []
        self.team_members = []

    def add_task(self, task):
        # Add a task to the project
        self.tasks.append(task)

    def add_team_member(self, team_member):def assign_tasks(self):
    # Create a dictionary to store the dependencies of each taskimport networkx as nx
def assign_tasks(self):
    # Create a directed graph of tasks and their dependencies
    G = nx.DiGraph()
    for task in self.tasks:
        G.add_node(task.name)
        for dependency in task.dependencies:
            G.add_edge(dependency, task.name)
    # Use topological sorting to order the tasks in a way that respects their dependencies
    sorted_tasks = list(nx.topological_sort(G))
    # Assign tasks to team members based on their skills, availability, and workload
    for task_name in sorted_tasks:
        task = next(t for t in self.tasks if t.name == task_name)
        for team_member in self.team_members:
            if task_name in team_member.skills and team_member.availability >= task.duration:
                team_member.assign_task(task)
                team_member.availability -= task.duration
                break# Assign tasks to team members based on their skills, availability, and workload
    for task in sorted_tasks:
        for team_member in self.team_members:
            if task.name in team_member.skills and team_member.availability >= task.duration:
                team_member.assign_task(task)
                team_member.availability -= task.duration
                assigned_tasks.add(task.name)
                # Remove the assigned task from the dependent tasks
                for dependent_task in dependent_tasks[task.name]:
                    task_dependencies[dependent_task].remove(task.name)
                    if not task_dependencies[dependent_task]:
                        independent_tasks.add(dependent_task)
                breakdef execute_tasks(self):
        # Execute tasks and monitor progress
        for task in self.tasks:
            task.start_task()
            print(f"Task {task.name} started")
            # Simulate task execution
            import time
            time.sleep(1)
            task.complete_task()
            print(f"Task {task.name} completed")

    def resolve_issues(self):
        # Resolve issues that arise during the project
        print("Resolving issues...")
        # Simulate issue resolution
        import time
        time.sleep(1)
        print("Issues resolved")

    def deliver_project(self):
        # Deliver the project
        print("Delivering project...")
        # Simulate project delivery
        import time
        time.sleep(1)
        print("Project delivered")


def project_setup():
    """Set up the project."""
    project_name = input("Enter project name: ")
    scope = input("Enter project scope: ")
    budget = int(input("Enter project budget: "))
    timeline = int(input("Enter project timeline: "))

    project = Project(project_name, scope, budget, timeline)

    num_tasks = int(input("Enter number of tasks: "))
    for i in range(num_tasks):
        task_name = input(f"Enter task {i+1} name: ")
        duration = int(input(f"Enter task {i+1} duration: "))
        dependencies = input(f"Enter task {i+1} dependencies (comma-separated): ")
        dependencies = dependencies.split(",") if dependencies else []
        task = Task(task_name, duration, dependencies)
        project.add_task(task)

    num_team_members = int(input("Enter number of team members: "))
    for i in range(num_team_members):
        team_member_name = input(f"Enter team member {i+1} name: ")
        skills = input(f"Enter team member {i+1} skills (comma-separated): ")
        skills = skills.split(",") if skills else []
        availability = int(input(f"Enter team member {i+1} availability: "))
        team_member = TeamMember(team_member_name, skills, availability)
        project.add_team_member(team_member)

    return project


def main():
    """Main function."""
    project = project_setup()
    project.assign_tasks()
    project.execute_tasks()
    project.resolve_issues()
    project.deliver_project()


if __name__ == "__main__":
    main()