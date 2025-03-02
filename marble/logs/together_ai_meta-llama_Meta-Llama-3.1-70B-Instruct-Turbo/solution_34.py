# project_synergy.py

class Task:
    """Represents a task in the project."""
    def __init__(self, name, duration, dependencies=None):
        """
        Initializes a Task object.

        Args:
            name (str): The name of the task.
            duration (int): The estimated duration of the task.
            dependencies (list, optional): A list of task names that this task depends on. Defaults to None.
        """
        self.name = name
        self.duration = duration
        self.dependencies = dependencies if dependencies else []
        self.completed = False

    def mark_completed(self):
        """Marks the task as completed."""
        self.completed = True


class TeamMember:
    """Represents a team member."""
    def __init__(self, name, skills):
        """
        Initializes a TeamMember object.

        Args:
            name (str): The name of the team member.
            skills (list): A list of skills the team member possesses.
        """
        self.name = name
        self.skills = skills
        self.tasks = []

    def assign_task(self, task):
        """Assigns a task to the team member."""
        self.tasks.append(task)


class Project:
    """Represents a project."""
    def __init__(self, name, budget, timeline):
        """
        Initializes a Project object.

        Args:
            name (str): The name of the project.
            budget (int): The budget of the project.
            timeline (int): The timeline of the project.
        """
        self.name = name
        self.budget = budget
        self.timeline = timeline
        self.tasks = []
        self.team_members = []

    def add_task(self, task):
        """Adds a task to the project."""
        self.tasks.append(task)

    def add_team_member(self, team_member):
        """Adds a team member to the project."""
        self.team_members.append(team_member)

    def assign_tasks(self):
        """Assigns tasks to team members based on their skills."""
        for task in self.tasks:
            for team_member in self.team_members:
                if any(skill in task.name for skill in team_member.skills):
                    team_member.assign_task(task)
                    break

    def execute_tasks(self):
        """Executes the tasks in the project."""
        for task in self.tasks:
            if not task.dependencies:
                task.mark_completed()
            else:
                for dependency in task.dependencies:
                    dependent_task = next((t for t in self.tasks if t.name == dependency), None)
                    if dependent_task and dependent_task.completed:
                        task.mark_completed()

    def resolve_issues(self):
        """Resolves issues in the project."""
        # This is a placeholder for issue resolution logic
        pass

    def deliver_project(self):
        """Delivers the project."""
        if all(task.completed for task in self.tasks):
            print("Project delivered successfully!")
        else:
            print("Project not delivered. Some tasks are still pending.")


def main():
    # Create a project
    project = Project("Software Development Project", 100000, 30)

    # Create tasks
    task1 = Task("Design", 5)
    task2 = Task("Development", 15, ["Design"])
    task3 = Task("Testing", 5, ["Development"])
    task4 = Task("Deployment", 5, ["Testing"])

    # Add tasks to the project
    project.add_task(task1)
    project.add_task(task2)
    project.add_task(task3)
    project.add_task(task4)

    # Create team members
    team_member1 = TeamMember("John", ["Design", "Development"])
    team_member2 = TeamMember("Alice", ["Testing", "Deployment"])

    # Add team members to the project
    project.add_team_member(team_member1)
    project.add_team_member(team_member2)

    # Assign tasks to team members
    project.assign_tasks()

    # Execute tasks
    project.execute_tasks()

    # Resolve issues
    project.resolve_issues()

    # Deliver the project
    project.deliver_project()


if __name__ == "__main__":
    main()