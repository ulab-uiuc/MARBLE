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

    def join_project(self, project):
        """Adds a project to the user's list of projects."""
        self.projects.append(project)


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
        self.ideas = []  # List of proposed ideas

    def add_team_member(self, user):
        """Adds a team member to the project."""
        self.team_members.append(user)

    def propose_idea(self, idea):
        """Adds a proposed idea to the project."""
        self.ideas.append(idea)

    def create_task(self, task):
        """Adds a task to the project."""
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
        recipient (User or Project): Recipient of the message (either a user or a project).
        content (str): Content of the message.
        """
        self.id = id
        self.sender = sender
        self.recipient = recipient
        self.content = content


class Feedback:
    """Represents feedback in the CollaborativeProjectHub system."""
    
    def __init__(self, id, giver, receiver, rating, review):
        """
        Initializes a Feedback object.

        Args:
        id (int): Unique identifier for the feedback.
        giver (User): User giving the feedback.
        receiver (User): User receiving the feedback.
        rating (int): Rating given (e.g., 1-5).
        review (str): Review given.
        """
        self.id = id
        self.giver = giver
        self.receiver = receiver
        self.rating = rating
        self.review = review


class CollaborativeProjectHub:
    """Represents the CollaborativeProjectHub system."""
    
    def __init__(self):
        self.users = []  # List of users
        self.projects = []  # List of projects
        self.tasks = []  # List of tasks
        self.messages = []  # List of messages
        self.feedback = []  # List of feedback

    def create_user(self, id, name, skills, interests, availability):
        """Creates a new user and adds it to the system."""
        user = User(id, name, skills, interests, availability)
        self.users.append(user)
        return user

    def create_project(self, id, name, description):def create_task(self, id, name, description, deadline, project):        task = Task(id, name, description, deadline)project.tasks.append(task)        return task

    def send_message(self, id, sender, recipient, content):
        """Creates a new message and adds it to the system."""
        message = Message(id, sender, recipient, content)
        self.messages.append(message)
        return message

    def give_feedback(self, id, giver, receiver, rating, review):
        """Creates new feedback and adds it to the system."""
        feedback = Feedback(id, giver, receiver, rating, review)
        self.feedback.append(feedback)
        return feedback


# Example usage:

hub = CollaborativeProjectHub()

user1 = hub.create_user(1, "John Doe", ["Python", "JavaScript"], ["Web Development", "Machine Learning"], "full-time")
user2 = hub.create_user(2, "Jane Doe", ["Java", "C++"], ["Android App Development", "Game Development"], "part-time")

project = hub.create_project(1, "Collaborative Project", "A project for collaborative work")
project.add_team_member(user1)
project.add_team_member(user2)

task = hub.create_task(1, "Task 1", "Description of Task 1", "2024-07-31")
project.create_task(task)

message = hub.send_message(1, user1, user2, "Hello, let's work on the project!")
task = hub.create_task(1, "Task 1", "Description of Task 1", "2024-07-31", project)

feedback = hub.give_feedback(1, user1, user2, 5, "Great work!")

print("Users:")
for user in hub.users:
    print(f"ID: {user.id}, Name: {user.name}")

print("\nProjects:")
for project in hub.projects:
    print(f"ID: {project.id}, Name: {project.name}")

print("\nTasks:")
for task in hub.tasks:
    print(f"ID: {task.id}, Name: {task.name}")

print("\nMessages:")
for message in hub.messages:
    print(f"ID: {message.id}, Sender: {message.sender.name}, Recipient: {message.recipient.name}")

print("\nFeedback:")
for feedback in hub.feedback:
    print(f"ID: {feedback.id}, Giver: {feedback.giver.name}, Receiver: {feedback.receiver.name}")