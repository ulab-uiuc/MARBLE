# task.py
class Task:
    def __init__(self, name, description, start_time=None, end_time=None, status=None):
        self.name = name
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.dependencies = []
        self.comments = []

    def add_dependency(self, task):
        self.dependencies.append(task)

    def update_status(self, status):
        self.status = status

    def add_comment(self, comment):
        self.comments.append(comment)

    def __str__(self):
        return f"Task: {self.name}, Status: {self.status}, Dependencies: {len(self.dependencies)}"


# user.py
class User:
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def update_task_status(self, task, status):
        task.update_status(status)

    def add_comment(self, task, comment):
        task.add_comment(comment)

    def __str__(self):
        return f"User: {self.name}, Tasks: {len(self.tasks)}"


# task_chain.py
class TaskChain:
    def __init__(self):
        self.tasks = []
        self.users = []

    def add_task(self, task):
        self.tasks.append(task)

    def add_user(self, user):
        self.users.append(user)

    def update_task_status(self, task, status):
        for user in self.users:
            user.update_task_status(task, status)

    def add_comment(self, task, comment):
        for user in self.users:
            user.add_comment(task, comment)

    def generate_report(self):
        completed_tasks = [task for task in self.tasks if task.status == "completed"]
        ongoing_tasks = [task for task in self.tasks if task.status == "in progress"]
        delayed_tasks = [task for task in self.tasks if task.status == "not started" and task.dependencies]

        return {
            "completed_tasks": completed_tasks,
            "ongoing_tasks": ongoing_tasks,
            "delayed_tasks": delayed_tasks,
        }

    def send_notification(self, task):
        for user in self.users:
            print(f"Notification to {user.name}: Task {task.name} is completed.")

    def visualize_dependencies(self):
        # This is a simplified version of a Gantt chart
        for task in self.tasks:
            print(f"Task: {task.name}, Dependencies: {len(task.dependencies)}")


# solution.py
class Solution:
    def __init__(self):
        self.task_chain = TaskChain()

    def create_task(self, name, description):
        task = Task(name, description)
        self.task_chain.add_task(task)
        return task

    def create_user(self, name):
        user = User(name)
        self.task_chain.add_user(user)
        return user

    def add_dependency(self, task1, task2):
        task1.add_dependency(task2)

    def update_task_status(self, task, status):
        self.task_chain.update_task_status(task, status)

    def add_comment(self, task, comment):
        self.task_chain.add_comment(task, comment)

    def generate_report(self):
        return self.task_chain.generate_report()

    def send_notification(self, task):
        self.task_chain.send_notification(task)

    def visualize_dependencies(self):
        self.task_chain.visualize_dependencies()


# main.py
def main():
    solution = Solution()

    task1 = solution.create_task("Task A", "This is task A")
    task2 = solution.create_task("Task B", "This is task B")
    task3 = solution.create_task("Task C", "This is task C")

    user1 = solution.create_user("John")
    user2 = solution.create_user("Jane")

    solution.add_dependency(task1, task2)
    solution.add_dependency(task2, task3)

    solution.update_task_status(task1, "completed")
    solution.update_task_status(task2, "in progress")
    solution.update_task_status(task3, "not started")

    solution.add_comment(task1, "This is a comment")
    solution.add_comment(task2, "This is another comment")

    solution.send_notification(task1)
    solution.visualize_dependencies()

    report = solution.generate_report()
    print("Report:")
    print(report)


if __name__ == "__main__":
    main()