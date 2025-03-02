# solution.py
# CollaborativeProjectHub system implementation

class User:
    """Represents a user in the CollaborativeProjectHub system."""
    def __init__(self, id, name, skills, interests, availability):
        # Initialize user attributes
        self.id = id
self.tasks = []
        self.name = name
        self.skills = skills
        self.interests = interests
        self.availability = availability
        self.projects = []  # List of projects the user is part of
        self.reputation = 0  # Initial reputation score

    def create_profile(self):
        # Create a user profile
        print(f"User {self.name} created with skills: {self.skills}, interests: {self.interests}, and availability: {self.availability}")

    def join_project(self, project):
        # Join a project
        self.projects.append(project)
        print(f"User {self.name} joined project {project.name}")

    def rate_team_member(self, team_member, rating):
        # Rate a team member's contribution
        team_member.reputation += rating
        print(f"User {self.name} rated team member {team_member.name} with a rating of {rating}")


class Project:
    """Represents a project in the CollaborativeProjectHub system."""
    def __init__(self, id, name, description):
    def add_team_member(self, team_member):
        self.team_members.append(team_member)
        print(f'Team member {team_member.name} added to project {self.name}')
        # Initialize project attributes
        self.id = id
        self.name = name
        self.description = description
        self.team_members = []  # List of team members
        self.tasks = []  # List of tasks
        self.project_ideas = []  # List of proposed project ideas

    def create_project(self):
        # Create a project
        print(f"Project {self.name} created with description: {self.description}")

    def propose_project_idea(self, idea):
        # Propose a project idea
        self.project_ideas.append(idea)
        print(f"Project idea {idea} proposed for project {self.name}")

    def discuss_project_idea(self, idea):
        # Discuss a proposed project idea
        print(f"Project idea {idea} is being discussed for project {self.name}")

    def vote_on_project_idea(self, idea):
        # Vote on a proposed project idea
        print(f"Project idea {idea} is being voted on for project {self.name}")

    def assign_task(self, task, team_member):
        # Assign a task to a team member
        self.tasks.append(task)
        team_member.tasks.append(task)
        print(f"Task {task.name} assigned to team member {team_member.name} in project {self.name}")

    def track_progress(self):
        # Track progress of tasks in the project
        print(f"Tracking progress of tasks in project {self.name}")


class Task:
    """Represents a task in the CollaborativeProjectHub system."""
    def __init__(self, id, name, description, deadline):
    def update_status(self, status):
        self.status = status
        print(f'Task {self.name} status updated to {status}')
        # Initialize task attributes
        self.id = id
        self.name = name
        self.description = description
        self.deadline = deadline
        self.status = "Not Started"  # Initial task status

    def create_task(self):
        # Create a task
        print(f"Task {self.name} created with description: {self.description} and deadline: {self.deadline}")

    def update_status(self, status):
        # Update the status of a task
        self.status = status
        print(f"Task {self.name} status updated to {status}")


class Message:
    """Represents a message in the CollaborativeProjectHub system."""
    def __init__(self, id, content, sender, recipient):
        # Initialize message attributes
        self.id = id
        self.content = content
        self.sender = sender
        self.recipient = recipient

    def send_message(self):
        # Send a message
        print(f"Message {self.content} sent from {self.sender.name} to {self.recipient.name}")


class CollaborativeProjectHub:
    """Represents the CollaborativeProjectHub system."""
    def __init__(self):
        # Initialize the system
        self.users = []  # List of users
        self.projects = []  # List of projects
        self.tasks = []  # List of tasks
        self.messages = []  # List of messages

    def create_user(self, id, name, skills, interests, availability):
        # Create a user
        user = User(id, name, skills, interests, availability)
        self.users.append(user)
        user.create_profile()

    def create_project(self, id, name, description):
        # Create a project
        project = Project(id, name, description)
        self.projects.append(project)
        project.create_project()

    def propose_project_idea(self, project_id, idea):
        # Propose a project idea
        project = next((p for p in self.projects if p.id == project_id), None)
        if project:
            project.propose_project_idea(idea)

    def discuss_project_idea(self, project_id, idea):
        # Discuss a proposed project idea
        project = next((p for p in self.projects if p.id == project_id), None)
        if project:
            project.discuss_project_idea(idea)

    def vote_on_project_idea(self, project_id, idea):
        # Vote on a proposed project idea
        project = next((p for p in self.projects if p.id == project_id), None)
        if project:
            project.vote_on_project_idea(idea)

    def assign_task(self, project_id, task_id, team_member_id):def track_progress(self, project_id):
        project = next((p for p in self.projects if p.id == project_id), None)
        if project:
            completed_tasks = 0
            tasks_in_progress = 0
            not_started_tasks = 0
            for task in project.tasks:
                if task.status == 'Completed':
                    completed_tasks += 1
                elif task.status == 'In Progress':
                    tasks_in_progress += 1
                else:
                    not_started_tasks += 1
            print(f'Project {project.name} progress: {completed_tasks} tasks completed, {tasks_in_progress} tasks in progress, {not_started_tasks} tasks not started')    def send_message(self, sender_id, recipient_id, content):
        # Send a message
        sender = next((u for u in self.users if u.id == sender_id), None)
        recipient = next((u for u in self.users if u.id == recipient_id), None)
        if sender and recipient:
            message = Message(len(self.messages) + 1, content, sender, recipient)
            self.messages.append(message)
            message.send_message()

    def rate_team_member(self, user_id, team_member_id, rating):
        # Rate a team member's contribution
        user = next((u for u in self.users if u.id == user_id), None)
        team_member = next((u for u in self.users if u.id == team_member_id), None)
        if user and team_member:
            user.rate_team_member(team_member, rating)


# Example usage
hub = CollaborativeProjectHub()

# Create users
hub.create_user(1, "John Doe", ["Software Development", "Data Science"], ["AI", "Machine Learning"], "Full-time")
hub.create_user(2, "Jane Doe", ["Software Development", "Web Development"], ["Front-end", "Back-end"], "Part-time")

# Create projects
hub.create_project(1, "AI Project", "Develop an AI model for image classification")
hub.create_project(2, "Web Development Project", "Develop a web application for e-commerce")

# Propose project ideas
hub.propose_project_idea(1, "Use CNN for image classification")
hub.propose_project_idea(2, "Use React for front-end development")

# Discuss project ideas
hub.discuss_project_idea(1, "Use CNN for image classification")
hub.discuss_project_idea(2, "Use React for front-end development")

# Vote on project ideas
hub.vote_on_project_idea(1, "Use CNN for image classification")
hub.vote_on_project_idea(2, "Use React for front-end development")

# Assign tasks
task1 = Task(1, "Develop CNN model", "Develop a CNN model for image classification", "2024-03-01")
task2 = Task(2, "Develop front-end", "Develop the front-end of the web application", "2024-03-15")
hub.tasks.append(task1)
hub.tasks.append(task2)
hub.assign_task(1, 1, 1)
hub.assign_task(2, 2, 2)

# Track progress
hub.track_progress(1)
hub.track_progress(2)

# Send messages
hub.send_message(1, 2, "Hello, how are you?")
hub.send_message(2, 1, "I'm good, thanks!")

# Rate team members
hub.rate_team_member(1, 2, 5)
hub.rate_team_member(2, 1, 4)