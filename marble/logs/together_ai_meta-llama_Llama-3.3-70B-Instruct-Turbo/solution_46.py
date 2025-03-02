# solution.py
from datetime import datetime, timedelta
from typing import Dict, List

class User:
    """Represents a user in the system."""
    def __init__(self, username: str):
        # Initialize the user with a username and an empty task list.
        self.username = username
        self.tasks = []

class Task:
    """Represents a task in the system."""
    def __init__(self, title: str, description: str, deadline: datetime, priority: str, status: str = "pending"):
        # Initialize the task with a title, description, deadline, priority, and status.
        self.title = title
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.status = status
        self.comments = []

    def update_status(self, status: str):
        # Update the status of the task.
        self.status = status

    def add_comment(self, comment: str):
        # Add a comment to the task.
        self.comments.append(comment)

class OfficeTaskScheduler:
def __init__(self):
        self.users = {}
        self.tasks = {}def create_task(self, title: str, description: str, deadline: datetime, priority: str, assigned_to: str):
def create_user(self, username: str):
        if username not in self.users:
            self.users[username] = User(username)
        print(f"User {username} created successfully.")
    if assigned_to not in self.users:
        raise ValueError(f"User {assigned_to} does not exist.")
    if deadline < datetime.now():
        raise ValueError("Deadline cannot be in the past.")
    for task_id, task in self.tasks.items():
        if task.title == title:
            raise ValueError("Task title already exists.")
    task_id = len(self.tasks) + 1
    self.tasks[task_id] = Task(title, description, deadline, priority)
    self.users[assigned_to].tasks.append(task_id)
    print(f"Task {title} created and assigned to {assigned_to} successfully.")def view_tasks(self, username: str):
        # View all tasks assigned to a user.
        if username in self.users:
            user_tasks = self.users[username].tasks
            for task_id in user_tasks:
                task = self.tasks[task_id]
                print(f"Task ID: {task_id}, Title: {task.title}, Deadline: {task.deadline}, Priority: {task.priority}, Status: {task.status}")
        else:
            print(f"User {username} does not exist.")

    def update_task_status(self, task_id: int, status: str, username: str):
        # Update the status of a task.
        if username in self.users and task_id in self.tasks:
            task = self.tasks[task_id]
            if task_id in self.users[username].tasks:
                task.update_status(status)
                print(f"Task {task_id} status updated to {status} successfully.")
            else:
                print(f"Task {task_id} is not assigned to {username}.")
        else:
            print(f"User {username} or task {task_id} does not exist.")

    def add_comment(self, task_id: int, comment: str, username: str):
        # Add a comment to a task.
        if username in self.users and task_id in self.tasks:
            task = self.tasks[task_id]
            if task_id in self.users[username].tasks:
                task.add_comment(comment)
                print(f"Comment added to task {task_id} successfully.")
            else:
                print(f"Task {task_id} is not assigned to {username}.")
        else:
            print(f"User {username} or task {task_id} does not exist.")

    def generate_report(self):if not self.tasks:
        print("No tasks in the system.")
        return
    completion_rate = 0overdue_tasks = 0
        task_distribution = {}
        for task_id, task in self.tasks.items():print(f"Task completion rate: {completion_rate / len(self.tasks) * 100 if self.tasks else 0}%")print(f"Overdue tasks: {overdue_tasks}")
        print("Task distribution:")
        for user, task_count in task_distribution.items():
            print(f"{user}: {task_count}")

def main():
    scheduler = OfficeTaskScheduler()
    while True:
        print("1. Create user")
        print("2. Create task")
        print("3. View tasks")
        print("4. Update task status")
        print("5. Add comment")
        print("6. Generate report")
        print("7. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            username = input("Enter username: ")
            scheduler.create_user(username)
        elif choice == "2":
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            deadline = datetime.strptime(input("Enter task deadline (YYYY-MM-DD): "), "%Y-%m-%d")
            priority = input("Enter task priority: ")
            assigned_to = input("Enter username to assign task to: ")
            scheduler.create_task(title, description, deadline, priority, assigned_to)
        elif choice == "3":
            username = input("Enter username: ")
            scheduler.view_tasks(username)
        elif choice == "4":
            task_id = int(input("Enter task ID: "))
            status = input("Enter new task status: ")
            username = input("Enter username: ")
            scheduler.update_task_status(task_id, status, username)
        elif choice == "5":
            task_id = int(input("Enter task ID: "))
            comment = input("Enter comment: ")
            username = input("Enter username: ")
            scheduler.add_comment(task_id, comment, username)
        elif choice == "6":
            scheduler.generate_report()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()