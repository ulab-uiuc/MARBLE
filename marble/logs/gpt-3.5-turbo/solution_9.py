class Project:
    def __init__(self, name, start_date, end_date, description):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)


class Task:
    def __init__(self, name, assignee, deadline):
        self.name = name
        self.assignee = assignee
        self.deadline = deadline
        self.status = "Not Started"


class User:
    def __init__(self, name):
        self.name = name
        self.tasks_completed = 0
        self.total_tasks = 0
        self.average_completion_time = 0
        self.feedback = []


class TeamCollaborationManager:
    def __init__(self):
        self.projects = []
        self.users = []

    def create_project(self, name, start_date, end_date, description):
        project = Project(name, start_date, end_date, description)
        self.projects.append(project)
        return project

    def create_task(self, project, name, assignee, deadline):
        task = Task(name, assignee, deadline)
        project.add_task(task)

    def create_user(self, name):
        user = User(name)
        self.users.append(user)
        return user

    def complete_task(self, user, task):
        task.status = "Completed"
        user.tasks_completed += 1

    def assign_task(self, task, assignee):
        task.assignee = assignee

    def track_task_status(self, task):
        return task.status

    def give_feedback(self, user, feedback):
        user.feedback.append(feedback)

    def generate_report(self):        # Implement logic to generate reports on project progress, team performance, and individual performance metrics
        # Your implementation logic here        pass

        # Implement logic to generate reports on project progress, team performance, and individual performance metrics
        # Your implementation logic here
        pass


# Test cases
if __name__ == "__main__":
    # Create Team Collaboration Manager
    tcm = TeamCollaborationManager()

    # Create users
    user1 = tcm.create_user("Alice")
    user2 = tcm.create_user("Bob")

    # Create project
    project1 = tcm.create_project("Project A", "2022-10-01", "2022-12-31", "Description of Project A")

    # Create tasks within the project
    tcm.create_task(project1, "Task 1", user1, "2022-11-15")
    tcm.create_task(project1, "Task 2", user2, "2022-11-30")

    # Assign and complete tasks
    task1 = project1.tasks[0]
    tcm.assign_task(task1, user1)
    tcm.complete_task(user1, task1)

    task2 = project1.tasks[1]
    tcm.assign_task(task2, user2)

    # Track task status
    print(tcm.track_task_status(task1))  # Output: Completed
    print(tcm.track_task_status(task2))  # Output: Not Started

    # Give feedback
    tcm.give_feedback(user2, "Great job on Task 2!")

    # Generate reports
    tcm.generate_report()