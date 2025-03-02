# collaborative_project_hub.py

class User:
    """Represents a user in the CollaborativeProjectHub system."""
    
    def __init__(self, id, name, skills, interests, availability):
        """
        Initializes a User object.

        Args:
            id (int): Unique identifier for the user.
            name (str): Name of the user.
            skills (list): List of skills the user possesses.
            interests (list): List of interests the user has.
            availability (str): Availability of the user (e.g., "full-time", "part-time").
        """
        self.id = id
        self.name = name
        self.skills = skills
        self.interests = interests
        self.availability = availability
        self.projects = []  # List of projects the user is part of
        self.reputation = 0  # Reputation score of the user

    def join_project(self, project):
        """Adds the user to a project."""
        self.projects.append(project)

    def rate_team_member(self, team_member, rating):
        """Rates a team member's contribution."""
        team_member.reputation += rating


class Project:
    """Represents a project in the CollaborativeProjectHub system."""
    
    def __init__(self, id, name, description):
        """
        Initializes a Project object.

        Args:
            id (int): Unique identifier for the project.
            name (str): Name of the project.
            description (str): Description of the project.
        """
        self.id = id
        self.name = name
        self.description = description
        self.team_members = []  # List of team members
        self.tasks = []  # List of tasks
        self.ideas = []  # List of project ideas

    def add_team_member(self, team_member):
        """Adds a team member to the project."""
        self.team_members.append(team_member)

    def propose_idea(self, idea):
        """Proposes a project idea."""
        self.ideas.append(idea)

    def assign_task(self, task):
        """Assigns a task to a team member."""
        self.tasks.append(task)


class Task:
    """Represents a task in the CollaborativeProjectHub system."""
    
    def __init__(self, id, name, description, deadline):
        """
        Initializes a Task object.

        Args:
            id (int): Unique identifier for the task.
            name (str): Name of the task.
            description (str): Description of the task.
            deadline (str): Deadline for the task.
        """
        self.id = id
        self.name = name
        self.description = description
        self.deadline = deadline
        self.status = "pending"  # Status of the task (e.g., "pending", "in_progress", "completed")

    def update_status(self, status):
        """Updates the status of the task."""
        self.status = status


class Message:
    """Represents a message in the CollaborativeProjectHub system."""
    
    def __init__(self, id, sender, recipient, content):
        """
        Initializes a Message object.

        Args:
            id (int): Unique identifier for the message.
            sender (User): Sender of the message.
            recipient (User): Recipient of the message.
            content (str): Content of the message.
        """
        self.id = id
        self.sender = sender
        self.recipient = recipient
        self.content = content


class CollaborativeProjectHub:def create_project(self, id, name, description):def create_task(self, id, name, description, deadline):def send_message(self, id, sender, recipient, content):
        if any(message.id == id for message in self.messages):
            raise ValueError(f"Message with ID {id} already exists")message = Message(id, sender, recipient, content)
        self.messages.append(message)
        return message


# Example usage:

hub = CollaborativeProjectHub()

user1 = hub.create_user(1, "John Doe", ["Python", "JavaScript"], ["Software Development", "Web Development"], "full-time")
user2 = hub.create_user(2, "Jane Doe", ["Java", "C++"], ["Software Development", "Game Development"], "part-time")

project = hub.create_project(1, "Collaborative Project", "A project for collaborative development")

project.add_team_member(user1)
project.add_team_member(user2)

task = hub.create_task(1, "Task 1", "Description of Task 1", "2024-03-16")
project.assign_task(task)

message = hub.send_message(1, user1, user2, "Hello, Jane!")

print("Users:")
for user in hub.users:
    print(f"ID: {user.id}, Name: {user.name}, Skills: {user.skills}, Interests: {user.interests}, Availability: {user.availability}")

print("\nProjects:")
for project in hub.projects:
    print(f"ID: {project.id}, Name: {project.name}, Description: {project.description}")

print("\nTasks:")
for task in hub.tasks:
    print(f"ID: {task.id}, Name: {task.name}, Description: {task.description}, Deadline: {task.deadline}")

print("\nMessages:")
for message in hub.messages:
    print(f"ID: {message.id}, Sender: {message.sender.name}, Recipient: {message.recipient.name}, Content: {message.content}")