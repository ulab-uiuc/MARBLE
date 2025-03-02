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

    def create_profile(self):
        """Creates a user profile with skills, interests, and availability."""
        return {
            "username": self.username,
            "skills": self.skills,
            "interests": self.interests,
            "availability": self.availability
        }

    def add_project(self, project):
        """Adds a project to the user's list of projects."""
        self.projects.append(project)

    def add_review(self, review):
        """Adds a review to the user's list of reviews."""
        self.reviews.append(review)


class Project:
    """Class representing a project in the CollaborativeProjectHub."""
    
    def __init__(self, title, description):
        self.title = title  # Title of the project
        self.description = description  # Description of the project
        self.team_members = []  # List of users in the project team
        self.tasks = []  # List of tasks associated with the project
        self.votes = {}  # Dictionary to hold votes for project ideas

    def add_team_member(self, user):
        """Adds a user to the project team."""def vote_on_idea(self, user, idea):
        """Allows a user to vote on a project idea. If the user has already voted, update their vote."""
        if user.username in self.votes:
            self.votes[user.username] = idea  # Update existing vote
        else:
            self.votes[user.username] = idea  # Add new vote    def propose_task(self, task):
        """Proposes a new task for the project."""
        self.tasks.append(task)

    def vote_on_idea(self, user, idea):
        """Allows a user to vote on a project idea."""
        self.votes[user.username] = idea


class Task:
    """Class representing a task within a project."""
    
    def __init__(self, title, deadline):
        self.title = title  # Title of the task
        self.deadline = deadline  # Deadline for the task
        self.assigned_to = None  # User assigned to the task
        self.status = "Pending"  # Current status of the task

    def assign_to(self, user):
        """Assigns the task to a user."""
        self.assigned_to = user

    def update_status(self, status):
        """Updates the status of the task."""
        self.status = status


class MessagingSystem:
    """Class representing a messaging system for communication."""
    
    def __init__(self):
        self.messages = []  # List to hold messages

    def send_message(self, sender, recipient, content):
        """Sends a message from one user to another."""
        message = {
            "from": sender.username,
            "to": recipient.username,
            "content": content
        }
        self.messages.append(message)

    def group_message(self, sender, group, content):
        """Sends a message to a group of users."""
        for member in group:
            self.send_message(sender, member, content)


class FeedbackSystem:
    """Class representing a feedback system for user reviews."""
    
    def __init__(self):
        self.feedback = []  # List to hold feedback entries

    def give_feedback(self, reviewer, reviewee, rating, comment):
        """Allows a user to give feedback to another user."""
        feedback_entry = {
            "reviewer": reviewer.username,
            "reviewee": reviewee.username,
            "rating": rating,
            "comment": comment
        }
        self.feedback.append(feedback_entry)


class CollaborativeProjectHub:
    """Main class representing the CollaborativeProjectHub platform."""
    
    def __init__(self):
        self.users = []  # List of users in the platform
        self.projects = []  # List of projects in the platform
        self.messaging_system = MessagingSystem()  # Messaging system instance
        self.feedback_system = FeedbackSystem()  # Feedback system instance

    def register_user(self, username, skills, interests, availability):
        """Registers a new user in the platform."""
        user = User(username, skills, interests, availability)
        self.users.append(user)
        return user

    def create_project(self, title, description):
        """Creates a new project in the platform."""
        project = Project(title, description)
        self.projects.append(project)
        return project

    def report_issue(self, issue):
        """Handles user-reported issues."""
        print(f"Issue reported: {issue}")

    def suggest_feature(self, feature):
        """Handles user suggestions for new features."""
        print(f"Feature suggested: {feature}")


# Example usage of the CollaborativeProjectHub
if __name__ == "__main__":
    hub = CollaborativeProjectHub()
    
    # Register users
    user1 = hub.register_user("Alice", ["Python", "Design"], ["AI", "Art"], "Full-time")
    user2 = hub.register_user("Bob", ["Java", "Management"], ["Business", "Tech"], "Part-time")
    
    # Create a project
    project = hub.create_project("AI Art Generator", "A project to create art using AI.")
    
    # Add team members
    project.add_team_member(user1)
    project.add_team_member(user2)
    
    # Propose a task
    task1 = Task("Research AI Models", "2023-12-01")
    project.propose_task(task1)
    
    # Assign task
    task1.assign_to(user1)
    
    # Send a message
    hub.messaging_system.send_message(user1, user2, "Let's discuss the project idea.")
    
    # Give feedback
    hub.feedback_system.give_feedback(user1, user2, 5, "Great collaboration!")