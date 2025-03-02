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
        task.assign(self)

    def complete_task(self, task):
        """Mark a task as completed by the team member."""
        if task in self.tasks:
            task.complete()


class Project:
    """Class representing the project."""
    
    def __init__(self, name, budget, timeline):
        self.name = name  # Name of the project
        self.budget = budget  # Budget for the project
        self.timeline = timeline  # Timeline for the project
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
        if self.current_phase == "Setup":
            print(f"Project '{self.name}' setup complete.")
            self.current_phase = "Team Management"
        else:
            print("Project setup already completed.")

    def manage_team(self):
        """Manage team by assigning tasks to team members."""
        if self.current_phase == "Team Management":for task in self.tasks:
                if all(dep.completed for dep in task.dependencies):
                    for member in self.team_members:
                        if member.skills and task.name in member.skills and not task.assigned_to:
                            member.assign_task(task)
                            print(f"Assigned task '{task.name}' to {member.name}.")            self.current_phase = "Task Execution"
        else:
            print("Team management can only begin after project setup.")

    def execute_tasks(self):
        """Execute tasks and monitor progress."""
        if self.current_phase == "Task Execution":
            for task in self.tasks:
                if not task.completed:
                    print(f"Executing task '{task.name}' assigned to {task.assigned_to.name}.")
                    # Simulate task completion
                    task.complete()
                    print(f"Task '{task.name}' completed.")
            self.current_phase = "Issue Resolution"
        else:
            print("Task execution can only begin after team management.")

    def resolve_issues(self):
        """Resolve issues that arise during the project."""
        if self.current_phase == "Issue Resolution":
            print("Resolving issues...")
            # Simulate issue resolution
            self.current_phase = "Project Delivery"
        else:
            print("Issue resolution can only begin after task execution.")

    def deliver_project(self):
        """Deliver the project."""
        if self.current_phase == "Project Delivery":
            if all(task.completed for task in self.tasks):
                print(f"Project '{self.name}' delivered successfully within budget of {self.budget}.")
            else:
                print("Not all tasks are completed. Project cannot be delivered.")
        else:
            print("Project delivery can only begin after issue resolution.")


# Example usage
if __name__ == "__main__":
    # Create a project
    project = Project("ProjectSynergy", budget=10000, timeline=30)

    # Setup the project
    project.setup_project()

    # Create tasks
    task1 = Task("Design", duration=5)
    task2 = Task("Development", duration=10, dependencies=[task1])
    task3 = Task("Testing", duration=5, dependencies=[task2])

    # Add tasks to the project
    project.add_task(task1)
    project.add_task(task2)
    project.add_task(task3)

    # Create team members
    alice = TeamMember("Alice", skills=["Design", "Development"])
    bob = TeamMember("Bob", skills=["Development", "Testing"])

    # Add team members to the project
    project.add_team_member(alice)
    project.add_team_member(bob)

    # Manage the team
    project.manage_team()

    # Execute tasks
    project.execute_tasks()

    # Resolve issues
    project.resolve_issues()

    # Deliver the project
    project.deliver_project()