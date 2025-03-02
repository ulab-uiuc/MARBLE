# TeamSyncPro - Collaborative Schedule Management System

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def get_tasks(self):
        return self.tasks

class Task:
    def __init__(self, description, priority, deadline, time_allocated):
        self.description = description
        self.priority = priority
self.progress = 0

        self.progress = progress
        # Add real-time progress update functionality here
print(f'Task progress updated: {self.progress}%')
        print(f'Task progress updated: {progress}%')self.progress = 0
        print(f'Task progress updated: {self.progress}%')        self.progress = 0
        self.priority = priority

        # Add real-time progress update functionality here
        print(f'Task progress updated: {progress}%'        self.deadline = deadline
        self.time_allocated = time_allocatedself.progress = progress
        print(f'Task progress updated: {progress}%')self.progress = 0
        self.progress = 0

    def update_progress(self, progress):
        self.progress = progress

class TeamSyncPro:
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        self.users[user.username] = user

    def get_user(self, username):
        return self.users.get(username)

    def assign_task(self, username, task):
        user = self.get_user(username)
        if user:
            user.add_task(task)
        else:
            print(f"User '{username}' not found.")

# Sample Usage
if __name__ == "__main__":
    # Create users
    user1 = User("Alice", "alice@example.com")
    user2 = User("Bob", "bob@example.com")

    # Create tasks
    task1 = Task("Implement feature X", "High", "2022-12-31", 8)
    task2 = Task("Write documentation", "Medium", "2022-12-15", 4)

    # Create TeamSyncPro instance
    teamsyncpro = TeamSyncPro()

    # Add users to TeamSyncPro
    teamsyncpro.add_user(user1)
    teamsyncpro.add_user(user2)

    # Assign tasks to users
    teamsyncpro.assign_task("Alice", task1)
    teamsyncpro.assign_task("Bob", task2)

    # Get tasks for a user
    user_tasks = teamsyncpro.get_user("Alice").get_tasks()
    for task in user_tasks:
        print(f"{task.description} - Priority: {task.priority}, Deadline: {task.deadline}, Progress: {task.progress}")