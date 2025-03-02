# solution.py

class User:
    """Class representing a user in the CollaborateCraft application."""
    
    def __init__(self, username, bio, profile_picture):
        self.username = username
        self.bio = bio
        self.profile_picture = profile_picture
        self.projects = []  # List to hold user's projects
        self.group_projects = []  # List to hold user's group projects
        self.messages = []  # List to hold user's messages

    def create_project(self, title, description, media, tags):
        """Create a new crafting project."""
        project = Project(title, description, media, tags, self)
        self.projects.append(project)
        return project

    def send_message(self, recipient, content):
        """Send a private message to another user."""
        message = Message(self, recipient, content)
        self.messages.append(message)
        recipient.messages.append(message)

class Project:
    """Class representing a crafting project."""
    
    def __init__(self, title, description, media, tags, creator):
        self.title = title
        self.description = description
        self.media = media  # List of media (photos/videos)
        self.tags = tags
        self.creator = creator
        self.comments = []  # List to hold comments on the project
        self.group_project = None  # Reference to group project if applicable

    def add_comment(self, user, content):
        """Add a comment to the project."""
        comment = Comment(user, content)
        self.comments.append(comment)
        return comment

class GroupProject:
    """Class representing a group project."""
    
    def __init__(self, title, leader):
        self.title = title
        self.leader = leader
        self.members = [leader]  # List of members in the group project
        self.tasks = []  # List to hold tasks for the project

    def invite_member(self, user):
        """Invite a user to join the group project."""
        if user not in self.members:
            self.members.append(user)
            user.group_projects.append(self)

    def assign_task(self, task, user):
        """Assign a task to a user in the group project."""
        task_assignment = Task(task, user)
        self.tasks.append(task_assignment)

class Comment:
    """Class representing a comment on a project."""
    
    def __init__(self, user, content):
        self.user = user
        self.content = content
        self.upvotes = 0
        self.downvotes = 0

    def upvote(self):
        """Upvote the comment."""
        self.upvotes += 1

    def downvote(self):
        """Downvote the comment."""
        self.downvotes += 1

class Message:
    """Class representing a private message between users."""
    
    def __init__(self, sender, recipient, content):
        self.sender = sender
        self.recipient = recipient
        self.content = content

class Task:
    """Class representing a task in a group project."""
    
    def __init__(self, description, assignee):
        self.description = description
        self.assignee = assignee
        self.completed = False

    def mark_completed(self):
        """Mark the task as completed."""
        self.completed = True

class CollaborateCraft:
    """Main class to manage the CollaborateCraft application."""
    
    def __init__(self):
        self.users = []  # List to hold all users
        self.projects = []  # List to hold all projects

    def register_user(self, username, bio, profile_picture):
        """Register a new user in the application."""
        user = User(username, bio, profile_picture)
        self.users.append(user)
        return user

    def search(self, keyword):
        """Search for users, projects, or group projects based on a keyword."""
        results = {
            "users": [user for user in self.users if keyword in user.username or keyword in user.bio],
            "projects": [project for project in self.projects if keyword in project.title or keyword in project.description],
            "group_projects": [group for group in self.projects if isinstance(group, GroupProject) and keyword in group.title]        "group_projects": [group for group in self.projects if isinstance(group, GroupProject) and (keyword in group.title or keyword in group.leader.username)]        }
        return results

# Example test cases
if __name__ == "__main__":
    app = CollaborateCraft()
    
    # Test case 1: Create a user profile
    user1 = app.register_user("CraftyAlice", "Loves knitting and painting.", "alice_profile.jpg")
    
    # Test case 2: User creates a project
    project1 = user1.create_project("Knitting a Sweater", "A cozy sweater for winter.", ["sweater.jpg"], ["knitting"])
    
    # Test case 3: User comments on a project
    comment1 = project1.add_comment(user1, "This looks amazing!")
    
    # Test case 4: User sends a private message
    user2 = app.register_user("BobTheBuilder", "Woodworking enthusiast.", "bob_profile.jpg")
    user1.send_message(user2, "Hey Bob, check out my new project!")
    
    # Test case 5: Search for users
    search_results = app.search("Crafty")
    
    # Print search results
    print("Search Results:", search_results)