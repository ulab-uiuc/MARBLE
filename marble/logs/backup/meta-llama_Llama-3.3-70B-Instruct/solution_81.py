# solution.py
# CollaborativeProjectHub system implementation

class User:
    """Represents a user in the CollaborativeProjectHub system."""
    def __init__(self, id, name, skills, interests, availability):
        """
        Initializes a User object.

        Args:
            id (int): Unique user ID.
            name (str): User name.
            skills (list): List of user skills.
            interests (list): List of user interests.
            availability (str): User availability.
        """
        self.id = id
        self.name = name
        self.skills = skills
        self.interests = interests
        self.availability = availability
        self.projects = []  # List of projects the user is part of

class Project:
    """Represents a project in the CollaborativeProjectHub system."""
    def __init__(self, id, name, description, team):
        """
        Initializes a Project object.

        Args:
            id (int): Unique project ID.
            name (str): Project name.
            description (str): Project description.
            team (list): List of team members.
        """
        self.id = id
        self.name = name
        self.description = description
        self.team = team
        self.tasks = []  # List of tasks in the project
        self.ideas = []  # List of proposed project ideas

class Task:
    """Represents a task in the CollaborativeProjectHub system."""
    def __init__(self, id, name, description, deadline, assigned_to):
        """
        Initializes a Task object.

        Args:
            id (int): Unique task ID.
            name (str): Task name.
            description (str): Task description.
            deadline (str): Task deadline.
            assigned_to (User): User assigned to the task.
        """
        self.id = id
        self.name = name
        self.description = description
        self.deadline = deadline
        self.assigned_to = assigned_to
        self.status = "Not Started"  # Task status

class Message:
    """Represents a message in the CollaborativeProjectHub system."""
    def __init__(self, id, sender, recipient, content):
        """
        Initializes a Message object.

        Args:
            id (int): Unique message ID.
            sender (User): User who sent the message.
            recipient (User): User who received the message.
            content (str): Message content.
        """
        self.id = id
        self.sender = sender
        self.recipient = recipient
        self.content = content

class CollaborativeProjectHub:
    """Represents the CollaborativeProjectHub system."""
    def __init__(self):
        self.users = []  # List of users in the system
        self.projects = []  # List of projects in the system
        self.tasks = []  # List of tasks in the system
        self.messages = []  # List of messages in the system

    def create_user(self, id, name, skills, interests, availability):
        """
        Creates a new user in the system.

        Args:
            id (int): Unique user ID.
            name (str): User name.
            skills (list): List of user skills.
            interests (list): List of user interests.
            availability (str): User availability.
        """
        new_user = User(id, name, skills, interests, availability)
        self.users.append(new_user)

    def create_project(self, id, name, description, team):
        """
        Creates a new project in the system.

        Args:
            id (int): Unique project ID.
            name (str): Project name.
            description (str): Project description.
            team (list): List of team members.
        """
        new_project = Project(id, name, description, team)
        self.projects.append(new_project)

    def create_task(self, id, name, description, deadline, assigned_to):
        """
        Creates a new task in the system.

        Args:
            id (int): Unique task ID.
            name (str): Task name.
            description (str): Task description.
            deadline (str): Task deadline.
            assigned_to (User): User assigned to the task.
        """
        new_task = Task(id, name, description, deadline, assigned_to)
        self.tasks.append(new_task)

    def create_message(self, id, sender, recipient, content):
        """
        Creates a new message in the system.

        Args:
            id (int): Unique message ID.
            sender (User): User who sent the message.
            recipient (User): User who received the message.
            content (str): Message content.
        """
        new_message = Message(id, sender, recipient, content)
        self.messages.append(new_message)

    def propose_project_idea(self, project_id, idea):def vote_on_project_idea(self, project_id, idea, user_id):
        project = next((p for p in self.projects if p.id == project_id), None)
        if project:
            idea_index = project.ideas.index(idea)
            # Initialize votes dictionary if it doesn't exist
            if not hasattr(project, 'votes'):
                project.votes = {}
            # Initialize idea votes if it doesn't exist
            if idea not in project.votes:
                project.votes[idea] = {}
            # Cast vote
            project.votes[idea][user_id] = Truedef assign_task(self, task_id, user_id):def track_progress(self, task_id):
        task = next((t for t in self.tasks if t.id == task_id), None)
        if task:
            # Update task status based on progress
            if task.status == 'Not Started':
                task.status = 'In Progress'
            elif task.status == 'In Progress':
                task.status = 'Completed'def send_message(self, message_id, sender_id, recipient_id, content):def rate_team_member(self, user_id, rating):
        user = next((u for u in self.users if u.id == user_id), None)
        if user:
            # Initialize ratings list if it doesn't exist
            if not hasattr(user, 'ratings'):
                user.ratings = []
            # Add rating to list
            user.ratings.append(rating)
            # Calculate average rating
            user.average_rating = sum(user.ratings) / len(user.ratings)def main():
    hub = CollaborativeProjectHub()

    # Create users
    hub.create_user(1, "John Doe", ["Python", "Java"], ["Software Development"], "Full-time")
    hub.create_user(2, "Jane Doe", ["JavaScript", "HTML/CSS"], ["Web Development"], "Part-time")

    # Create project
    hub.create_project(1, "Collaborative Project Hub", "A platform for collaborative project management", [1, 2])

    # Create task
    hub.create_task(1, "Implement user profiles", "Implement user profiles with skills, interests, and availability", "2024-03-01", hub.users[0])

    # Propose project idea
    hub.propose_project_idea(1, "Implement task management feature")

    # Vote on project idea
    hub.vote_on_project_idea(1, "Implement task management feature", 1)

    # Assign task
    hub.assign_task(1, 2)

    # Track progress
    hub.track_progress(1)

    # Send message
    hub.send_message(1, 1, 2, "Hello, how are you?")

    # Rate team member
    hub.rate_team_member(1, 5)

if __name__ == "__main__":
    main()