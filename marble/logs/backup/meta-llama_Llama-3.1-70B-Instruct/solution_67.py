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
        task (Task): The task to be added.
        """
        self.tasks.append(task)


class Task:
    """Represents a task in the TeamSyncPro system."""
    
    def __init__(self, title, description, priority, deadline, time_slot):
        """
        Initializes a Task object.
        
        Args:
        title (str): The title of the task.
        description (str): The description of the task.
        priority (int): The priority of the task.
        deadline (str): The deadline of the task.
        time_slot (str): The time slot allocated for the task.
        """
        self.title = title
        self.description = description
        self.priority = priority
        self.deadline = deadline
        self.time_slot = time_slot
        self.progress = 0

    def update_progress(self, progress):
        """
        Updates the progress of the task.
        
        Args:
        progress (int): The updated progress of the task.
        """
        self.progress = progress


class Project:
    """Represents a project in the TeamSyncPro system."""
    
    def __init__(self, title, description):
        """
        Initializes a Project object.
        
        Args:
        title (str): The title of the project.
        description (str): The description of the project.
        """
        self.title = title
        self.description = description
        self.tasks = []

    def add_task(self, task):
        """
        Adds a task to the project's task list.
        
        Args:
        task (Task): The task to be added.
        """
        self.tasks.append(task)


class TeamSyncPro:
    """Represents the TeamSyncPro system."""
    
    def __init__(self):
        """
        Initializes the TeamSyncPro system.
        """
        self.users = {}
self.logged_in_user = None
        self.projects = {}

    def register_user(self, username, password):
def logout_user(self):
    self.logged_in_user = None
        """
        Registers a new user in the system.
        
        Args:
        username (str): The username of the user.
        password (str): The password of the user.
        """
        self.users[username] = User(username, password)

    def login_user(self, username, password):if self.logged_in_user is None and username in self.users and self.users[username].password == password:return True
self.logged_in_user = username
        return False

    def create_project(self, title, description):
        """
        Creates a new project in the system.
        
        Args:
        title (str): The title of the project.
        description (str): The description of the project.
        """
        self.projects[title] = Project(title, description)

    def add_task_to_project(self, project_title, task):
        """
        Adds a task to a project in the system.
        
        Args:
        project_title (str): The title of the project.
        task (Task): The task to be added.
        """
        if project_title in self.projects:
            self.projects[project_title].add_task(task)

    def display_project_tasks(self, project_title):
        """
        Displays the tasks of a project in the system.
        
        Args:
        project_title (str): The title of the project.
        """
        if project_title in self.projects:
            for task in self.projects[project_title].tasks:
                print(f"Task: {task.title}, Priority: {task.priority}, Deadline: {task.deadline}, Progress: {task.progress}%")

    def send_message(self, sender, receiver, message):
        """
        Sends a message from one user to another in the system.
        
        Args:
        sender (str): The username of the sender.
        receiver (str): The username of the receiver.
        message (str): The message to be sent.
        """
        if sender in self.users and receiver in self.users:
            print(f"{sender} sent a message to {receiver}: {message}")


# Example usage
team_sync_pro = TeamSyncPro()

while True:
    print("1. Register User")
    print("2. Login User")
    print("3. Create Project")
    print("4. Add Task to Project")
    print("5. Display Project Tasks")
    print("6. Send Message")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        username = input("Enter username: ")
        password = input("Enter password: ")
        team_sync_pro.register_user(username, password)
    elif choice == "2":
        username = input("Enter username: ")
        password = input("Enter password: ")
        if team_sync_pro.login_user(username, password):
            print("Login successful")
        else:
            print("Invalid username or password")
    elif choice == "3":
        title = input("Enter project title: ")
        description = input("Enter project description: ")
        team_sync_pro.create_project(title, description)
    elif choice == "4":
        project_title = input("Enter project title: ")
        title = input("Enter task title: ")
        description = input("Enter task description: ")
        priority = int(input("Enter task priority: "))
        deadline = input("Enter task deadline: ")
        time_slot = input("Enter task time slot: ")
        task = Task(title, description, priority, deadline, time_slot)
        team_sync_pro.add_task_to_project(project_title, task)
    elif choice == "5":
        project_title = input("Enter project title: ")
        team_sync_pro.display_project_tasks(project_title)
    elif choice == "6":
        sender = input("Enter sender's username: ")
        receiver = input("Enter receiver's username: ")
        message = input("Enter message: ")
        team_sync_pro.send_message(sender, receiver, message)
    elif choice == "7":
        break
    else:
        print("Invalid choice")