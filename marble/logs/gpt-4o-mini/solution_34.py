# solution.py

class Task:
    """Class representing a task in the project."""
    
    def __init__(self, name, duration, dependencies=None):
        self.name = name  # Name of the task
        self.duration = duration  # Estimated duration of the task
        self.dependencies = dependencies if dependencies else []  # List of dependencies
        self.assigned_to = None  # Team member assigned to the task
        self.completed = False  # Task completion status

    def assign(self, team_member):
        """Assign a team member to the task."""
        self.assigned_to = team_member

    def complete(self):
        """Mark the task as completed."""
        self.completed = True


class TeamMember:
    """Class representing a team member."""
    
    def __init__(self, name, skills):
        self.name = name  # Name of the team member
        self.skills = skills  # List of skills
        self.tasks = []  # List of tasks assigned to the team member

    def assign_task(self, task):
        """Assign a task to the team member."""
        self.tasks.append(task)
        task.assign(self.name)


class Project:
    """Class representing the project management game."""
    
    def __init__(self, scope, budget, timeline):
        self.scope = scope  # Project scope
        self.budget = budget  # Project budget
        self.timeline = timeline  # Project timeline
        self.tasks = []  # List of tasks in the project
        self.team_members = []  # List of team members
        self.current_phase = "Setup"  # Current phase of the project

    def add_task(self, task):
        """Add a task to the project."""
        self.tasks.append(task)

    def add_team_member(self, team_member):
        """Add a team member to the project."""
        self.team_members.append(team_member)

    def setup_project(self):
        """Setup the project by defining scope, budget, and timeline."""
        print(f"Project '{self.scope}' setup complete with budget {self.budget} and timeline {self.timeline}.")
        self.current_phase = "Team Management"

    def manage_team(self):
        """Manage team by assigning tasks based on skills and availability."""
        if self.current_phase != "Team Management":
            print("Project setup must be completed before team management.")
            returnfor task in self.tasks:
            if all(dep.completed for dep in task.dependencies) and not task.assigned_to:
                for member in self.team_members:
                    if member.skills:
                        member.assign_task(task)
                        print(f"Assigned task '{task.name}' to team member '{member.name}'.")        self.current_phase = "Task Execution"

    def execute_tasks(self):
        """Execute tasks and monitor their progress."""
        if self.current_phase != "Task Execution":
            print("Team management must be completed before task execution.")
            return
        
        for task in self.tasks:
            if not task.completed:
                print(f"Executing task '{task.name}' assigned to '{task.assigned_to}'.")
                task.complete()  # Simulate task completion
                print(f"Task '{task.name}' completed.")

        self.current_phase = "Issue Resolution"

    def resolve_issues(self):
        """Resolve issues that arise during the project."""
        if self.current_phase != "Issue Resolution":
            print("Task execution must be completed before issue resolution.")
            return
        
        print("Resolving issues...")
        # Simulate issue resolution
        self.current_phase = "Project Delivery"

    def deliver_project(self):
        """Deliver the project ensuring all tasks are completed."""
        if self.current_phase != "Project Delivery":
            print("All previous phases must be completed before project delivery.")
            return
        
        all_completed = all(task.completed for task in self.tasks)
        if all_completed:
            print(f"Project '{self.scope}' delivered successfully within budget {self.budget}.")
        else:
            print("Project delivery failed: not all tasks are completed.")


# Example usage
if __name__ == "__main__":
    # Create a project
    project = Project("Project Synergy", 10000, "3 months")

    # Setup the project
    project.setup_project()

    # Create tasks
    task1 = Task("Design", 2)
    task2 = Task("Development", 5, dependencies=[task1])
    task3 = Task("Testing", 3, dependencies=[task2])

    # Add tasks to the project
    project.add_task(task1)
    project.add_task(task2)
    project.add_task(task3)

    # Create team members
    member1 = TeamMember("Alice", ["Design", "Development"])
    member2 = TeamMember("Bob", ["Testing", "Development"])

    # Add team members to the project
    project.add_team_member(member1)
    project.add_team_member(member2)

    # Manage the team
    project.manage_team()

    # Execute tasks
    project.execute_tasks()

    # Resolve issues
    project.resolve_issues()

    # Deliver the project
    project.deliver_project()