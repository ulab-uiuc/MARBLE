
# project.py
class Project:def add_task(self, task):
        if task not in self.tasks:
            self.tasks.append(task)
            self.total_cost += task.cost
            self.total_duration += task.duration
        else:
            print("Task is already added to the project!")self.tasks.append(task)
        self.total_cost += task.cost
        self.total_duration += task.duration

    def add_team_member(self, team_member):
        self.team_members.append(team_member)

    def add_issue(self, issue):
        self.issues.append(issue)

    def resolve_issue(self, issue):
        self.issues.remove(issue)

    def deliver_project(self):
        # Check if all tasks are completed
        if all(task.completed for task in self.tasks):
            # Check if the project is within budget and timeline
            if self.budget >= 0 and self.timeline >= 0:
                print("Project delivered successfully!")
            else:
                print("Project budget or timeline exceeded!")
        else:
            print("Not all tasks are completed!")# project_synergy.py

class Task:def __init__(self, name, duration, cost, dependencies=None):self.name = name
        self.duration = duration
self.cost = cost
        self.dependencies = dependencies if dependencies else []
        self.completed = False

    def complete(self):
        """Marks the task as completed."""
        self.completed = True


class TeamMember:def assign_task(self, task):
        if task not in self.tasks:
            self.tasks.append(task)
            self.total_cost += task.cost if hasattr(task, 'cost') else 0
            self.total_duration += task.duration
        else:
            print("Task is already assigned to the team member!")self.tasks.append(task)self.total_cost += task.cost if hasattr(task, 'cost') else 0self.tasks.append(task)
        self.total_duration += task.duration
        # Assuming each task has a cost attribute
        self.total_cost += task.cost        self.tasks.append(task)

    def add_team_member(self, team_member):
        """Adds a team member to the project."""
        self.team_members.append(team_member)

    def add_issue(self, issue):
        """Adds an issue to the project."""
        self.issues.append(issue)

    def resolve_issue(self, issue):def deliver_project(self):
        # Check if all tasks are completed
        if all(task.completed for task in self.tasks):
            # Check if the project is within budget and timeline
            if self.total_cost <= self.budget and self.total_duration <= self.timeline:
                print("Project delivered successfully!")
            else:
                print("Project budget or timeline exceeded!")
        else:
            print("Not all tasks are completed!")        # Check if all tasks are completed
        if all(task.completed for task in self.tasks):
            # Check if the project is within budget
            if self.budget >= 0:
                # Check if the project is within timeline
                if self.timeline >= 0:
                    print("Project delivered successfully!")
                else:
                    print("Project timeline exceeded!")
            else:
                print("Project budget exceeded!")
        else:
            print("Not all tasks are completed!")


class ProjectSynergy:
    """Represents the Project Synergy game."""
    def __init__(self):
        self.project = None

    def setup_project(self):
        """Sets up the project."""
        name = input("Enter project name: ")
        budget = int(input("Enter project budget: "))
        timeline = int(input("Enter project timeline: "))
        self.project = Project(name, budget, timeline)

    def manage_team(self):
        """Manages the team."""
        while True:
            print("1. Add team member")
            print("2. Assign task to team member")
            print("3. Back")
            choice = input("Enter your choice: ")
            if choice == "1":
                name = input("Enter team member name: ")
                skills = input("Enter team member skills (comma separated): ").split(",")
                team_member = TeamMember(name, skills)
                self.project.add_team_member(team_member)
            elif choice == "2":
                if not self.project.team_members:
                    print("No team members added!")
                    continue
                print("Team Members:")
                for i, team_member in enumerate(self.project.team_members):
                    print(f"{i+1}. {team_member.name}")
                team_member_choice = int(input("Enter team member number: ")) - 1
                team_member = self.project.team_members[team_member_choice]
                if not self.project.tasks:
                    print("No tasks added!")
                    continue
                print("Tasks:")
                for i, task in enumerate(self.project.tasks):
                    print(f"{i+1}. {task.name}")
                task_choice = int(input("Enter task number: ")) - 1
                task = self.project.tasks[task_choice]
                team_member.assign_task(task)
            elif choice == "3":
                break
            else:
                print("Invalid choice!")

    def execute_tasks(self):
        """Executes the tasks."""
        while True:
            print("1. Complete task")
            print("2. Back")
            choice = input("Enter your choice: ")
            if choice == "1":
                if not self.project.tasks:
                    print("No tasks added!")
                    continue
                print("Tasks:")
                for i, task in enumerate(self.project.tasks):
                    print(f"{i+1}. {task.name}")
                task_choice = int(input("Enter task number: ")) - 1
                task = self.project.tasks[task_choice]
                task.complete()
            elif choice == "2":
                break
            else:
                print("Invalid choice!")

    def resolve_issues(self):
        """Resolves the issues."""
        while True:
            print("1. Add issue")
            print("2. Resolve issue")
            print("3. Back")
            choice = input("Enter your choice: ")
            if choice == "1":
                issue = input("Enter issue: ")
                self.project.add_issue(issue)
            elif choice == "2":
                if not self.project.issues:
                    print("No issues added!")
                    continue
                print("Issues:")
                for i, issue in enumerate(self.project.issues):
                    print(f"{i+1}. {issue}")
                issue_choice = int(input("Enter issue number: ")) - 1
                issue = self.project.issues[issue_choice]
                self.project.resolve_issue(issue)
            elif choice == "3":
                break
            else:
                print("Invalid choice!")

    def deliver_project(self):
        """Delivers the project."""
        self.project.deliver_project()

    def play(self):
        """Plays the game."""
        while True:
            print("1. Setup project")
            print("2. Manage team")
            print("3. Execute tasks")
            print("4. Resolve issues")
            print("5. Deliver project")
            print("6. Quit")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.setup_project()
            elif choice == "2":
                if not self.project:
                    print("Project not set up!")
                    continue
                self.manage_team()
            elif choice == "3":
                if not self.project:
                    print("Project not set up!")
                    continue
                self.execute_tasks()
            elif choice == "4":
                if not self.project:
                    print("Project not set up!")
                    continue
                self.resolve_issues()
            elif choice == "5":
                if not self.project:
                    print("Project not set up!")
                    continue
                self.deliver_project()
            elif choice == "6":
                break
            else:
                print("Invalid choice!")


if __name__ == "__main__":
    game = ProjectSynergy()
    game.play()