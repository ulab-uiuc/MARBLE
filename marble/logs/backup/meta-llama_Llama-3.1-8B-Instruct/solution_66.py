# task.py
class Task:
    def __init__(self, name, description, start_time=None, end_time=None, status="not started"):
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
        return f"Task: {self.name}\nDescription: {self.description}\nStatus: {self.status}\nDependencies: {self.dependencies}\nComments: {self.comments}"


# task_chain.py
class TaskChain:
    def __init__(self):
        self.tasks = {}
        self.users = {}

    def create_task(self, name, description, user):
        if name not in self.tasks:
            self.tasks[name] = Task(name, description)
            self.users[name] = user
            return self.tasks[name]
        else:
            return None

    def add_dependency(self, task_name, dependent_task_name):
        if task_name in self.tasks and dependent_task_name in self.tasks:
            self.tasks[task_name].add_dependency(self.tasks[dependent_task_name])
            return True
        else:
            return False

    def update_status(self, task_name, status):
        if task_name in self.tasks:
            self.tasks[task_name].update_status(status)
            return True
        else:
            return False

    def add_comment(self, task_name, comment):
        if task_name in self.tasks:
            self.tasks[task_name].add_comment(comment)
            return True
        else:
            return False

    def get_task(self, task_name):
        return self.tasks.get(task_name)

    def get_user(self, task_name):
        return self.users.get(task_name)

    def generate_report(self):
        report = ""
        for task in self.tasks.values():
            report += f"Task: {task.name}\nDescription: {task.description}\nStatus: {task.status}\nDependencies: {task.dependencies}\nComments: {task.comments}\n\n"
        return report


# notification.py
class Notification:
    def __init__(self, task_name, message):
        self.task_name = task_name
        self.message = message

    def send_notification(self, user):
        print(f"Notification sent to {user}: {self.message}")


# solution.py
from task import Task
from task_chain import TaskChain
from notification import Notification

def main():
    task_chain = TaskChain()

    # Create tasks
    task_a = task_chain.create_task("Task A", "This is task A", "John")
    task_b = task_chain.create_task("Task B", "This is task B", "Jane")
    task_c = task_chain.create_task("Task C", "This is task C", "Bob")

    # Add dependencies
    task_chain.add_dependency("Task A", "Task B")
    task_chain.add_dependency("Task B", "Task C")

    # Update status
    task_chain.update_status("Task A", "in progress")
    task_chain.update_status("Task B", "not started")
    task_chain.update_status("Task C", "completed")

    # Add comments
    task_chain.add_comment("Task A", "This is a comment for task A")
    task_chain.add_comment("Task B", "This is a comment for task B")
    task_chain.add_comment("Task C", "This is a comment for task C")

    # Generate report
    report = task_chain.generate_report()
    print(report)

    # Send notifications
    notification_a = Notification("Task A", "Task A is completed")
    notification_b = Notification("Task B", "Task B is about to start")
    notification_c = Notification("Task C", "Task C is completed")
    task_chain.get_user("Task A").send_notification(notification_a)
    task_chain.get_user("Task B").send_notification(notification_b)
    task_chain.get_user("Task C").send_notification(notification_c)

if __name__ == "__main__":
    main()