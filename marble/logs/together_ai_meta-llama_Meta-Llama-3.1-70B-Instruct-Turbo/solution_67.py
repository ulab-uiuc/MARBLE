# team_sync_pro.py

class User:
    """Represents a user in the TeamSyncPro system."""
    
    def __init__(self, username, password):
        """
        Initializes a User object.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.
        """
        self.username = username
        self.password = password
        self.tasks = []

    def add_task(self, task):
        """
        Adds a task to the user's task list.

        Args:
            task (Task): The task to add.
        """
        self.tasks.append(task)

    def view_tasks(self):
        """
        Displays the user's tasks.
        """
        print(f"Tasks for {self.username}:")
        for task in self.tasks:
            print(task)


class Task:
    """Represents a task in the TeamSyncPro system."""
    
    def __init__(self, name, priority, deadline, time_slot):
        """
        Initializes a Task object.

        Args:
            name (str): The name of the task.
            priority (str): The priority of the task.
            deadline (str): The deadline of the task.
            time_slot (str): The time slot allocated for the task.
        """
        self.name = name
        self.priority = priority
        self.deadline = deadline
        self.time_slot = time_slot
        self.status = "Not Started"

    def update_status(self, status):
        """
        Updates the status of the task.

        Args:
            status (str): The new status of the task.
        """
        self.status = status

    def __str__(self):
        return f"{self.name} - {self.priority} - {self.deadline} - {self.time_slot} - {self.status}"


class TeamSyncPro:
    """Represents the TeamSyncPro system."""
    
    def __init__(self):
        """
        Initializes the TeamSyncPro system.
        """
        self.users = {}

    def add_user(self, user):
        """
        Adds a user to the system.

        Args:
            user (User): The user to add.
        """
        self.users[user.username] = user

    def login(self, username, password):
        """
        Logs in a user to the system.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            User: The logged-in user, or None if the login fails.
        """
        if username in self.users and self.users[username].password == password:
            return self.users[username]
        else:
            return None

    def view_user_tasks(self, user):
        """
        Displays the tasks of a user.

        Args:
            user (User): The user whose tasks to display.
        """
        user.view_tasks()

    def add_task_to_user(self, user, task):
        """
        Adds a task to a user.

        Args:
            user (User): The user to whom to add the task.
            task (Task): The task to add.
        """
        user.add_task(task)

    def update_task_status(self, user, task_name, status):
        """
        Updates the status of a task.

        Args:
            user (User): The user who owns the task.
            task_name (str): The name of the task.
            status (str): The new status of the task.
        """
        for task in user.tasks:
            if task.name == task_name:
                task.update_status(status)
                break


def main():
    # Create the TeamSyncPro system
    team_sync_pro = TeamSyncPro()

    # Create users
    user1 = User("user1", "password1")
    user2 = User("user2", "password2")

    # Add users to the system
    team_sync_pro.add_user(user1)
    team_sync_pro.add_user(user2)

    # Login users
    logged_in_user1 = team_sync_pro.login("user1", "password1")
    logged_in_user2 = team_sync_pro.login("user2", "password2")

    # Create tasks
    task1 = Task("Task 1", "High", "2024-02-20", "10:00-12:00")
    task2 = Task("Task 2", "Low", "2024-02-25", "14:00-16:00")

    # Add tasks to users
    team_sync_pro.add_task_to_user(logged_in_user1, task1)
    team_sync_pro.add_task_to_user(logged_in_user2, task2)

    # View user tasks
    team_sync_pro.view_user_tasks(logged_in_user1)
    team_sync_pro.view_user_tasks(logged_in_user2)

    # Update task status
    team_sync_pro.update_task_status(logged_in_user1, "Task 1", "In Progress")
    team_sync_pro.view_user_tasks(logged_in_user1)


if __name__ == "__main__":
    main()