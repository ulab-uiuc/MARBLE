# solution.py

class User:
    """Class representing a user in the CollaborativeProjectHub."""
    
    def __init__(self, username, skills, interests, availability):
        self.username = username  # User's unique username
        self.skills = skills  # List of skills the user possesses
        self.interests = interests  # List of interests of the user
        self.availability = availability  # User's availability status
        self.projects = []  # List of projects the user is involved in
        self.reviews = []  # List of reviews received from other users

    def add_project(self, project):
        """Add a project to the user's list of projects."""
        self.projects.append(project)

    def add_review(self, review):
        """Add a review to the user's list of reviews."""
        self.reviews.append(review)


class Project:
    """Class representing a project in the CollaborativeProjectHub."""
    
    def __init__(self, name, description):
        self.name = name  # Project name
        self.description = description  # Project description
        self.team_members = []  # List of users in the project team
        self.tasks = []  # List of tasks associated with the project
        self.ideas = []  # List of project ideas proposed by team members

    def add_member(self, user):
        """Add a user to the project team."""
        self.team_members.append(user)
        user.add_project(self)

    def propose_idea(self, idea):
        """Propose a new project idea."""
        self.ideas.append(idea)

    def add_task(self, task):
        """Add a task to the project."""
        self.tasks.append(task)


class Task:
    """Class representing a task within a project."""
    
    def __init__(self, title, deadline):
        self.title = title  # Task title
        self.deadline = deadline  # Task deadline
        self.assignee = None  # User assigned to the task
        self.status = 'Pending'  # Current status of the task

    def assign(self, user):
        """Assign a user to the task."""
        self.assignee = user

    def update_status(self, status):
        """Update the status of the task."""
        self.status = status


class MessagingSystem:
    """Class representing a messaging system for communication."""
    
    def __init__(self):
        self.messages = []  # List of messages sent in the system

    def send_message(self, sender, recipient, content):
        """Send a direct message from one user to another."""
        message = {
            'sender': sender.username,
            'recipient': recipient.username,
            'content': content
        }
        self.messages.append(message)

    def group_message(self, sender, group, content):
        """Send a message to a group of users."""
        for member in group:
            self.send_message(sender, member, content)


class FeedbackSystem:
    """Class representing a feedback system for user reviews."""
    
    def __init__(self):
        self.feedbacks = []  # List of feedback entries

    def give_feedback(self, reviewer, reviewee, rating, comment):
        """Allow a user to give feedback to another user."""
        feedback = {
            'reviewer': reviewer.username,
            'reviewee': reviewee.username,
            'rating': rating,
            'comment': comment
        }
        self.feedbacks.append(feedback)
        reviewee.add_review(feedback)


class CollaborativeProjectHub:
    """Main class representing the CollaborativeProjectHub platform."""
    
    def __init__(self):
        self.users = []  # List of registered users
        self.projects = []  # List of projects created on the platform
        self.messaging_system = MessagingSystem()  # Messaging system instance
        self.feedback_system = FeedbackSystem()  # Feedback system instance

    def register_user(self, username, skills, interests, availability):
        """Register a new user on the platform."""
        user = User(username, skills, interests, availability)
        self.users.append(user)
        return user

    def create_project(self, name, description):
        """Create a new project on the platform."""
        project = Project(name, description)
        self.projects.append(project)
        return project

    def report_issue(self, issue):
        """Allow users to report issues or request support."""
        print(f"Issue reported: {issue}")

    def suggest_feature(self, feature):
        """Allow users to suggest new features for the platform."""
        print(f"Feature suggested: {feature}")


# Example usage of the CollaborativeProjectHub
if __name__ == "__main__":
    hub = CollaborativeProjectHub()
    
    # Register users
    alice = hub.register_user("Alice", ["Python", "Design"], ["AI", "Art"], "Full-time")
    bob = hub.register_user("Bob", ["Java", "Management"], ["Business", "Tech"], "Part-time")
    
    # Create a project
    project = hub.create_project("AI Art Generator", "A project to create art using AI.")
    
    # Add members to the project
    project.add_member(alice)
    project.add_member(bob)
    
    # Propose an idea
    project.propose_idea("Use GANs for generating art.")
    
    # Create and assign a task
    task = Task("Research GANs", "2023-12-01")
    task.assign(alice)
    project.add_task(task)
    
    # Send a message
    hub.messaging_system.send_message(alice, bob, "Let's discuss the project idea.")
    
    # Give feedback
    hub.feedback_system.give_feedback(alice, bob, 5, "Great collaboration!")
    
    # Report an issue
    hub.report_issue("Need more features for task management.")
    
    # Suggest a feature
    hub.suggest_feature("Add video conferencing for team meetings.")