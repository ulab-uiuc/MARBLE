class Task:
    def __init__(self, description, deadline, priority, assigned_to=None, status="Not Started"):
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.assigned_to = assigned_to
        self.status = status

class User:
    def __init__(self, name):
        self.name = name
        self.tasks_assigned = []
        self.tasks_completed = []

class OfficeTaskCollaborator:
    def __init__(self):
        self.users = {}

    def create_user(self, name):
        if name not in self.users:
            self.users[name] = User(name)
            return True
        return False

    def create_task(self, description, deadline, priority, assigned_to=None):
        task = Task(description, deadline, priority, assigned_to)
        if assigned_to:
            if assigned_to in self.users:
                self.users[assigned_to].tasks_assigned.append(task)
            else:
                return "User does not exist."
        return task

    def update_task_status(self, task, status):
        task.status = status
        if status == "Completed":
            self.users[task.assigned_to].tasks_completed.append(task)

if task.assigned_to not in self.users:
            return "Invalid user. Task assignment failed."
    def generate_task_report(self):
        for user in self.users.values():
            print(f"User: {user.name}")
            print("Assigned Tasks:")
            for task in user.tasks_assigned:
                print(f"Description: {task.description}, Deadline: {task.deadline}, Status: {task.status}")
            print("Completed Tasks:")
            for task in user.tasks_completed:
                print(f"Description: {task.description}, Deadline: {task.deadline}, Status: {task.status}")

# Test the functionality
office_collaborator = OfficeTaskCollaborator()

# Create users
office_collaborator.create_user("Alice")
office_collaborator.create_user("Bob")

# Create tasks
task1 = office_collaborator.create_task("Task 1", "2022-12-31", "High", "Alice")
task2 = office_collaborator.create_task("Task 2", "2022-11-30", "Medium", "Bob")

# Update task status
office_collaborator.update_task_status(task1, "In Progress")
office_collaborator.update_task_status(task2, "Completed")

# Generate task report
office_collaborator.generate_task_report()