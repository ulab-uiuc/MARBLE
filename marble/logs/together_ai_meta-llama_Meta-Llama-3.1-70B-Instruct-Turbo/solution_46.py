# office_task_scheduler.py

class User:
    """Represents a user in the system."""
    
    def __init__(self, username):
        """Initializes a new user with a given username."""
        self.username = username
        self.tasks = []

    def assign_task(self, task):
        """Assigns a task to the user."""
        self.tasks.append(task)

    def view_tasks(self):
        """Displays all tasks assigned to the user."""
        for task in self.tasks:
            print(task)


class Task:
    """Represents a task in the system."""
    
    def __init__(self, title, description, deadline, priority, assigned_to):
        """Initializes a new task with a given title, description, deadline, priority, and assigned user."""
        self.title = title
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.assigned_to = assigned_to
        self.status = "pending"
        self.comments = []

    def update_status(self, status):
        """Updates the status of the task."""
        self.status = status

    def add_comment(self, comment):
        """Adds a comment to the task."""
        self.comments.append(comment)

    def __str__(self):
        """Returns a string representation of the task."""
        return f"Title: {self.title}\nDescription: {self.description}\nDeadline: {self.deadline}\nPriority: {self.priority}\nAssigned to: {self.assigned_to.username}\nStatus: {self.status}"


class OfficeTaskScheduler:
    """Represents the office task scheduler system."""
    
    def __init__(self):
        """Initializes a new office task scheduler system."""
        self.users = {}
        self.tasks = []

    def create_user(self, username):
        """Creates a new user in the system."""
        if username not in self.users:
            self.users[username] = User(username)
            print(f"User {username} created successfully.")
        else:
            print(f"User {username} already exists.")

    def create_task(self, title, description, deadline, priority, assigned_to):
        """Creates a new task in the system."""
        if assigned_to in self.users:
            task = Task(title, description, deadline, priority, self.users[assigned_to])
            self.tasks.append(task)
            self.users[assigned_to].assign_task(task)
            print(f"Task {title} created successfully.")
        else:
            print(f"User {assigned_to} does not exist.")

    def view_user_tasks(self, username):
        """Displays all tasks assigned to a user."""
        if username in self.users:
            self.users[username].view_tasks()
        else:
            print(f"User {username} does not exist.")

    def update_task_status(self, task_title, status):
        """Updates the status of a task."""
        for task in self.tasks:
            if task.title == task_title:
                task.update_status(status)
                print(f"Task {task_title} status updated to {status}.")
                return
        print(f"Task {task_title} not found.")

    def add_task_comment(self, task_title, comment):def generate_report(self):
        # Calculate task completion rates
        completed_tasks = sum(1 for task in self.tasks if task.status == "completed")
        total_tasks = len(self.tasks)
        completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        print(f"Task Completion Rate: {completion_rate:.2f}%")

        # Calculate overdue tasks
        from datetime import datetime
        current_date = datetime.now().strftime("%Y-%m-%d")
        overdue_tasks = [task for task in self.tasks if task.deadline < current_date]
        print("Overdue Tasks:")
        for task in overdue_tasks:
            print(f"Task {task.title} is overdue.")

        # Calculate task distribution among team members
        print("Task Distribution Among Team Members:")
        for user in self.users.values():
            assigned_tasks = len(user.tasks)
            completed_tasks = sum(1 for task in user.tasks if task.status == "completed")
            completion_rate = (completed_tasks / assigned_tasks) * 100 if assigned_tasks > 0 else 0
            print(f"User {user.username} has {assigned_tasks} tasks assigned, {completed_tasks} tasks completed, and a completion rate of {completion_rate:.2f}%")        print(f"Task {task_title} not found.")

    def generate_report(self):
        """Generates a report on task completion rates, overdue tasks, and task distribution among team members."""
        print("Task Completion Rates:")
        for task in self.tasks:
            if task.status == "completed":
                print(f"Task {task.title} is completed.")
        print("\nOverdue Tasks:")
        for task in self.tasks:
            if task.deadline < "2024-02-09":
                print(f"Task {task.title} is overdue.")
        print("\nTask Distribution Among Team Members:")
        for user in self.users.values():
            print(f"User {user.username} has {len(user.tasks)} tasks assigned.")


def main():
    scheduler = OfficeTaskScheduler()

    while True:
        print("\n1. Create User")
        print("2. Create Task")
        print("3. View User Tasks")
        print("4. Update Task Status")
        print("5. Add Task Comment")
        print("6. Generate Report")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            scheduler.create_user(username)
        elif choice == "2":
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            deadline = input("Enter task deadline: ")
            priority = input("Enter task priority: ")
            assigned_to = input("Enter user to assign task to: ")
            scheduler.create_task(title, description, deadline, priority, assigned_to)
        elif choice == "3":
            username = input("Enter username: ")
            scheduler.view_user_tasks(username)
        elif choice == "4":
            task_title = input("Enter task title: ")
            status = input("Enter new status: ")
            scheduler.update_task_status(task_title, status)
        elif choice == "5":
            task_title = input("Enter task title: ")
            comment = input("Enter comment: ")
            scheduler.add_task_comment(task_title, comment)
        elif choice == "6":
            scheduler.generate_report()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()