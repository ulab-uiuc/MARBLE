# solution.py
from datetime import datetime, timedelta
from typing import Dict, List

class User:
    """Represents a user in the system."""
    def __init__(self, username: str):
        self.username = username
        self.tasks = []

class Task:
    """Represents a task in the system."""
    def __init__(self, title: str, description: str, deadline: datetime, priority: str, status: str = "pending"):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.status = status
        self.comments = []

    def update_status(self, status: str):
        """Updates the status of the task."""
        self.status = status

    def add_comment(self, comment: str):
        """Adds a comment to the task."""
        self.comments.append(comment)

class OfficeTaskScheduler:
    """Manages tasks for multiple team members."""
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.tasks: Dict[str, Task] = {}

    def create_user(self, username: str):
        """Creates a new user in the system."""
        if username not in self.users:
            self.users[username] = User(username)
            print(f"User {username} created successfully.")
        else:
            print(f"User {username} already exists.")

    def create_task(self, title: str, description: str, deadline: str, priority: str, assigned_to: str):
        """Creates a new task and assigns it to a user."""
        if assigned_to in self.users:
            deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
            task = Task(title, description, deadline_date, priority)
            self.tasks[title] = task
            self.users[assigned_to].tasks.append(task)
            print(f"Task {title} created and assigned to {assigned_to} successfully.")
        else:
            print(f"User {assigned_to} does not exist.")

    def view_tasks(self, username: str):
        """Displays all tasks assigned to a user."""
        if username in self.users:
            user = self.users[username]
            print(f"Tasks assigned to {username}:")
            for task in user.tasks:
                print(f"Title: {task.title}, Deadline: {task.deadline.strftime('%Y-%m-%d')}, Priority: {task.priority}, Status: {task.status}")
        else:
            print(f"User {username} does not exist.")

    def update_task_status(self, task_title: str, new_status: str, username: str):
        """Updates the status of a task."""
        if task_title in self.tasks:
            task = self.tasks[task_title]
            if task in self.users[username].tasks:
                task.update_status(new_status)
                print(f"Task {task_title} status updated to {new_status} successfully.")
            else:
                print(f"Task {task_title} is not assigned to {username}.")
        else:
            print(f"Task {task_title} does not exist.")

    def add_comment(self, task_title: str, comment: str, username: str):
        """Adds a comment to a task."""
        if task_title in self.tasks:
            task = self.tasks[task_title]
            if task in self.users[username].tasks:
                task.add_comment(comment)
                print(f"Comment added to task {task_title} successfully.")
            else:
                print(f"Task {task_title} is not assigned to {username}.")
        else:
            print(f"Task {task_title} does not exist.")

    def generate_report(self):
        """Generates a report on task completion rates, overdue tasks, and task distribution."""
        completion_rate = 0
        overdue_tasks = 0
        task_distribution = {}
        for task in self.tasks.values():
            if task.status == "completed":
                completion_rate += 1
            if task.deadline < datetime.now():
                overdue_tasks += 1
            assigned_to = [user.username for user in self.users.values() if task in user.tasks][0]
            if assigned_to in task_distribution:
                task_distribution[assigned_to] += 1
            else:
                task_distribution[assigned_to] = 1
        print(f"Task completion rate: {completion_rate / len(self.tasks) * 100}%")
        print(f"Overdue tasks: {overdue_tasks}")
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
            deadline = input("Enter task deadline (YYYY-MM-DD): ")
            priority = input("Enter task priority: ")
            assigned_to = input("Enter username to assign task to: ")
            scheduler.create_task(title, description, deadline, priority, assigned_to)
        elif choice == "3":
            username = input("Enter username: ")
            scheduler.view_tasks(username)
        elif choice == "4":
            task_title = input("Enter task title: ")
            new_status = input("Enter new task status: ")
            username = input("Enter username: ")
            scheduler.update_task_status(task_title, new_status, username)
        elif choice == "5":
            task_title = input("Enter task title: ")
            comment = input("Enter comment: ")
            username = input("Enter username: ")
            scheduler.add_comment(task_title, comment, username)
        elif choice == "6":
            scheduler.generate_report()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()