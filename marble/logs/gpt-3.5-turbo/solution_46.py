class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.tasks = []

    def create_task(self, task_name, assignee, deadline, priority):
        task = Task(task_name, assignee, deadline, priority)
        self.tasks.append(task)

    def view_tasks(self):
        return self.tasks

    def update_task_status(self, task_name, new_status):
        for task in self.tasks:
            if task.task_name == task_name:
                task.status = new_status

    def add_comment(self, task_name, comment):
        for task in self.tasks:
            if task.task_name == task_name:
                task.comments.append(comment)


class Task:
    def __init__(self, task_name, assignee, deadline, priority):
        self.task_name = task_name
        self.assignee = assignee
        self.deadline = deadline
        self.priority = priority
        self.status = "Pending"
        self.comments = []
self.status = "Pending"


class OfficeTaskScheduler:
    def __init__(self):
        self.users = {}

self.status = "Pending"
    def register_user(self, username, password):
        if username in self.users:
            return "User already exists. Please choose a different username."
        self.users[username] = User(username, password)
        return "User registered successfully."

    def login(self, username, password):
        if username in self.users and self.users[username].password == password:
            return self.users[username]
        return None

    def generate_task_report(self, username):
        if username in self.users:
            user = self.users[username]
            completed_tasks = sum(1 for task in user.tasks if task.status == "Completed")
            overdue_tasks = sum(1 for task in user.tasks if task.status != "Completed" and task.deadline < "today")
            task_distribution = {task.assignee: task.task_name for task in user.tasks}
            return f"Completed tasks: {completed_tasks}, Overdue tasks: {overdue_tasks}, Task distribution: {task_distribution}"
        return "User not found."


# Test the functionality
ots = OfficeTaskScheduler()

# Register users
print(ots.register_user("alice", "password123"))  # User registered successfully.
print(ots.register_user("bob", "password456"))  # User registered successfully.

# Login
alice = ots.login("alice", "password123")
bob = ots.login("bob", "password456")

# Create tasks
alice.create_task("Task 1", "bob", "2022-12-31", "High")
alice.create_task("Task 2", "alice", "2022-11-30", "Medium")

# Update task status
alice.update_task_status("Task 1", "Completed")

# Add comments
alice.add_comment("Task 1", "Great job!")
alice.add_comment("Task 2", "Need more details.")

# Generate task report
print(ots.generate_task_report("alice"))  # Completed tasks: 1, Overdue tasks: 0, Task distribution: {'bob': 'Task 1', 'alice': 'Task 2'}
print(ots.generate_task_report("bob"))  # Completed tasks: 0, Overdue tasks: 1, Task distribution: {'alice': 'Task 1'}