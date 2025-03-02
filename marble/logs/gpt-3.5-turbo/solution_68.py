class Task:
    def __init__(self, name, duration, priority, dependencies=None):
        self.name = name
        self.duration = duration
        self.priority = priority
        self.dependencies = dependencies if dependencies else []

class User:
    def __init__(self, name):
        self.name = name
        self.tasks = []

class CollaborativeSchedulePlanner:
    def __init__(self):
        self.users = {}
        self.shared_schedule = {}

    def add_user(self, user):
        if user.name not in self.users:
            self.users[user.name] = user
            self.shared_schedule[user.name] = []

    def add_task(self, user_name, task):
        if user_name in self.users:
            self.users[user_name].tasks.append(task)
            self.shared_schedule[user_name].append(task)

    def edit_task(self, user_name, task_index, new_task):def generate_report(self, user_name):
        if user_name in self.users:
            tasks = self.users[user_name].tasks
            for task in tasks:
                print(f"Task: {task.name}, Duration: {task.duration}, Priority: {task.priority}, Dependencies: {task.dependencies}")
            print()            for task in tasks:
                print(f"Task: {task.name}, Duration: {task.duration}, Priority: {task.priority}, Dependencies: {task.dependencies}")
            print()

# Example Usage
if __name__ == "__main__":
    planner = CollaborativeSchedulePlanner()

    user1 = User("Alice")
    user2 = User("Bob")

    task1 = Task("Task 1", 2, 1)
    task2 = Task("Task 2", 3, 2, dependencies=["Task 1"])

    planner.add_user(user1)
    planner.add_user(user2)

    planner.add_task("Alice", task1)
    planner.add_task("Bob", task2)

    planner.generate_report()