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

    def update_task_status(self, task, status):
        """Update the status of a task in the group project."""
        for task_assignment in self.tasks:
            if task_assignment.task == task:
                task_assignment.status = status
                break

    def view_progress(self):
        """View the progress of tasks in the group project."""
        progress = {task_assignment.task: task_assignment.status for task_assignment in self.tasks}
        return progress

    def assign_task(self, task, user):
        """Assign a task to a user in the group project."""
        task_assignment = TaskAssignment(task, user)
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

class TaskAssignment:
    """Class representing a task assigned in a group project."""
    
    def __init__(self, task, user):
        self.task = task
        self.user = user

class CollaborateCraft:
    """Main class to manage the CollaborateCraft application."""
    
    def __init__(self):
        self.users = []  # List to hold all users in the application
        self.projects = []  # List to hold all projects

    def register_user(self, username, bio, profile_picture):
        """Register a new user in the application."""
        user = User(username, bio, profile_picture)
        self.users.append(user)
        return user

    def search(self, keyword):
        """Search for users, projects, and group projects based on a keyword."""
        results = {        results = {
            'users': [user for user in self.users if keyword in user.username or keyword in user.bio],
            'projects': [project for project in self.projects if keyword in project.title or keyword in project.description or any(tag for tag in project.tags if keyword in tag)],
            'group_projects': [group for group in self.projects if isinstance(group, GroupProject) and (keyword in group.title or any(tag for tag in group.title if keyword in tag))]
        }        return results

# Test cases to validate the functionality of the application
def test_collaborate_craft():
    app = CollaborateCraft()
    
    # Test user registration
    user1 = app.register_user("CraftyAlice", "Loves knitting and painting.", "alice.jpg")
    user2 = app.register_user("BobTheBuilder", "Woodworking enthusiast.", "bob.jpg")
    
    assert user1.username == "CraftyAlice"
    assert user2.bio == "Woodworking enthusiast."
    
    # Test project creation
    project1 = user1.create_project("Knitting a Sweater", "A cozy sweater for winter.", ["sweater.jpg"], ["knitting"])
    assert project1.title == "Knitting a Sweater"
    
    # Test commenting on a project
    comment1 = project1.add_comment(user2, "This looks great!")
    assert comment1.content == "This looks great!"
    
    # Test group project creation
    group_project = GroupProject("Community Quilt", user1)
    group_project.invite_member(user2)
    assert user2 in group_project.members
    
    # Test sending messages
    user1.send_message(user2, "Let's collaborate on a project!")
    assert len(user2.messages) == 1
    
    # Test searching
    search_results = app.search("Crafty")
    assert len(search_results['users']) == 1  # Should find CraftyAlice

# Run the test cases
test_collaborate_craft()