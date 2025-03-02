# project.py
class Project:
    def __init__(self, name, scope, budget, timeline):
        """
        Initialize a project with name, scope, budget, and timeline.
        
        Args:
            name (str): Project name.
            scope (str): Project scope.
            budget (float): Project budget.
            timeline (str): Project timeline.
        """
        self.name = name
        self.scope = scope
        self.budget = budget
        self.timeline = timeline
        self.tasks = []
        self.team_members = []
        self.issues = []

    def add_task(self, task):
        """
        Add a task to the project plan.
        
        Args:
            task (Task): Task object to be added.
        """
        self.tasks.append(task)

    def add_team_member(self, team_member):
        """
        Add a team member to the project team.
        
        Args:
            team_member (TeamMember): Team member object to be added.
        """
        self.team_members.append(team_member)

    def resolve_issue(self, issue):
        """
        Resolve an issue that arises during the project.
        
        Args:
            issue (Issue): Issue object to be resolved.
        """
        self.issues.append(issue)


class Task:
    def __init__(self, name, duration, dependencies=None):
        """
        Initialize a task with name, duration, and dependencies.
        
        Args:
            name (str): Task name.
            duration (float): Task duration.
            dependencies (list): List of task names that this task depends on.
        """
        self.name = name
        self.duration = duration
        self.dependencies = dependencies if dependencies else []
        self.status = "Not Started"


class TeamMember:
    def __init__(self, name, skills, availability):
        """
        Initialize a team member with name, skills, and availability.
        
        Args:
            name (str): Team member name.
            skills (list): List of skills that the team member has.
            availability (list): List of tasks that the team member is available to work on.
        """
        self.name = name
        self.skills = skills
        self.availability = availability


class Issue:
    def __init__(self, name, priority, resolution):
        """
        Initialize an issue with name, priority, and resolution.
        
        Args:
            name (str): Issue name.
            priority (str): Issue priority (e.g., High, Medium, Low).
            resolution (str): Issue resolution.
        """
        self.name = name
        self.priority = priority
        self.resolution = resolution


class ProjectSynergy:
    def __init__(self):
        """
        Initialize the ProjectSynergy game.
        """
        self.project = None

    def setup_project(self):
        """
        Set up the project by defining the scope, budget, and timeline.
        """
        name = input("Enter project name: ")
        scope = input("Enter project scope: ")
        budget = float(input("Enter project budget: "))
        timeline = input("Enter project timeline: ")
        self.project = Project(name, scope, budget, timeline)
        print("Project set up successfully!")

    def manage_team(self):
        """
        Manage the team by assigning tasks to team members.
        """
        if not self.project:
            print("Please set up the project first!")
            return
        for team_member in self.project.team_members:
            print(f"Available tasks for {team_member.name}:")
            for task in self.project.tasks:
                if task.name in team_member.availability:
                    print(task.name)
            task_name = input(f"Assign a task to {team_member.name}: ")
            for task in self.project.tasks:
                if task.name == task_name:
                    task.status = "In Progress"
                    team_member.availability.remove(task_name)
                    print(f"Task {task_name} assigned to {team_member.name}!")
                    break
        print("Team managed successfully!")

    def execute_tasks(self):
        """
        Execute the tasks by monitoring the progress of each task.
        """
        if not self.project:
            print("Please set up the project first!")
            return
        for task in self.project.tasks:
            if task.status == "In Progress":
                print(f"Task {task.name} is in progress...")
                task.status = "Completed"
                print(f"Task {task.name} completed successfully!")
        print("Tasks executed successfully!")

    def resolve_issues(self):
        """
        Resolve issues that arise during the project.
        """
        if not self.project:
            print("Please set up the project first!")
            return
        issue_name = input("Enter issue name: ")
        issue_priority = input("Enter issue priority: ")
        issue_resolution = input("Enter issue resolution: ")
        self.project.resolve_issue(Issue(issue_name, issue_priority, issue_resolution))
        print("Issue resolved successfully!")

    def deliver_project(self):
        """
        Deliver the project by ensuring that all tasks are completed, the project is within budget, and the quality standards are met.
        """
        if not self.project:
            print("Please set up the project first!")
            return
        if all(task.status == "Completed" for task in self.project.tasks):
            print("All tasks completed successfully!")
        if self.project.budget > 0:
            print("Project is within budget!")
        print("Project delivered successfully!")


def main():
    game = ProjectSynergy()
    while True:
        print("\nProject Synergy Game")
        print("1. Set up project")
        print("2. Manage team")
        print("3. Execute tasks")
        print("4. Resolve issues")
        print("5. Deliver project")
        print("6. Quit")
        choice = input("Enter your choice: ")
        if choice == "1":
            game.setup_project()
        elif choice == "2":
            game.manage_team()
        elif choice == "3":
            game.execute_tasks()
        elif choice == "4":
            game.resolve_issues()
        elif choice == "5":
            game.deliver_project()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()