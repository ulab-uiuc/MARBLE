# user.py
class User:
    def __init__(self, username, bio, profile_picture):
        """
        Initialize a User object.

        Args:
            username (str): The username of the user.
            bio (str): The bio of the user.
            profile_picture (str): The profile picture of the user.
        """
        self.username = username
        self.bio = bio
        self.profile_picture = profile_picture
        self.posts = []
        self.comments = []
        self.group_projects = []

    def __str__(self):
        return f"User: {self.username}, Bio: {self.bio}, Profile Picture: {self.profile_picture}"


# project.py
class Project:
    def __init__(self, title, description, tags, media):
        """
        Initialize a Project object.

        Args:
            title (str): The title of the project.
            description (str): The description of the project.
            tags (list): A list of tags for the project.
            media (str): The media (photo or video) of the project.
        """
        self.title = title
        self.description = description
        self.tags = tags
        self.media = media
        self.comments = []
        self.upvotes = 0
        self.downvotes = 0

    def __str__(self):
        return f"Project: {self.title}, Description: {self.description}, Tags: {self.tags}, Media: {self.media}"


# group_project.py
class GroupProject:
    def __init__(self, title, description, tags, leader):
        """
        Initialize a GroupProject object.

        Args:
            title (str): The title of the group project.
            description (str): The description of the group project.
            tags (list): A list of tags for the group project.
            leader (User): The leader of the group project.
        """
        self.title = title
        self.description = description
        self.tags = tags
        self.leader = leader
        self.members = []
        self.tasks = []
        self.progress = 0

    def __str__(self):
        return f"Group Project: {self.title}, Description: {self.description}, Tags: {self.tags}, Leader: {self.leader.username}"


# messaging.py
class Message:
    def __init__(self, sender, recipient, content):
        """
        Initialize a Message object.

        Args:
            sender (User): The sender of the message.
            recipient (User): The recipient of the message.
            content (str): The content of the message.
        """
        self.sender = sender
        self.recipient = recipient
        self.content = content

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}: {self.content}"


# solution.py
class CollaborateCraft:
    def __init__(self):
        """
        Initialize the CollaborateCraft application.
        """
        self.users = []
        self.projects = []
        self.group_projects = []
        self.messages = []

    def create_user(self, username, bio, profile_picture):
        """
        Create a new user.

        Args:
            username (str): The username of the user.
            bio (str): The bio of the user.
            profile_picture (str): The profile picture of the user.

        Returns:
            User: The created user.
        """
        new_user = User(username, bio, profile_picture)
        self.users.append(new_user)
        return new_user

    def create_project(self, title, description, tags, media, user):
        """
        Create a new project.

        Args:
            title (str): The title of the project.
            description (str): The description of the project.
            tags (list): A list of tags for the project.
            media (str): The media (photo or video) of the project.
            user (User): The user who created the project.

        Returns:
            Project: The created project.
        """
        new_project = Project(title, description, tags, media)
        user.posts.append(new_project)
        self.projects.append(new_project)
        return new_project

    def create_group_project(self, title, description, tags, leader):
        """
        Create a new group project.

        Args:
            title (str): The title of the group project.
            description (str): The description of the group project.
            tags (list): A list of tags for the group project.
            leader (User): The leader of the group project.

        Returns:
            GroupProject: The created group project.
        """
        new_group_project = GroupProject(title, description, tags, leader)
        leader.group_projects.append(new_group_project)
        self.group_projects.append(new_group_project)
        return new_group_project

    def leave_comment(self, project, user, content):
        """
        Leave a comment on a project.

        Args:
            project (Project): The project to leave a comment on.
            user (User): The user leaving the comment.
            content (str): The content of the comment.

        Returns:
            Comment: The created comment.
        """
        new_comment = Comment(project, user, content)
        project.comments.append(new_comment)
        user.comments.append(new_comment)
        return new_comment

    def send_message(self, sender, recipient, content):
        """
        Send a message to another user.

        Args:
            sender (User): The user sending the message.
            recipient (User): The user receiving the message.
            content (str): The content of the message.

        Returns:
            Message: The sent message.
        """
        new_message = Message(sender, recipient, content)
        self.messages.append(new_message)
        return new_message

    def search(self, query):
        """
        Search for users, projects, and group projects based on a query.

        Args:
            query (str): The query to search for.

        Returns:
            list: A list of search results.
        """
        results = []
        for user in self.users:
            if query in user.username or query in user.bio:
                results.append(user)
        for project in self.projects:
            if query in project.title or query in project.description:
                results.append(project)
        for group_project in self.group_projects:
            if query in group_project.title or query in group_project.description:
                results.append(group_project)
        return results


# comment.py
class Comment:
    def __init__(self, project, user, content):
        """
        Initialize a Comment object.

        Args:
            project (Project): The project the comment is on.
            user (User): The user who left the comment.
            content (str): The content of the comment.
        """
        self.project = project
        self.user = user
        self.content = content
        self.upvotes = 0
        self.downvotes = 0

    def __str__(self):
        return f"Comment on {self.project.title} by {self.user.username}: {self.content}"


# solution.py (continued)
if __name__ == "__main__":
    # Create a new CollaborateCraft application
    app = CollaborateCraft()

    # Create a new user
    user1 = app.create_user("john_doe", "I love crafting!", "https://example.com/john_doe.jpg")

    # Create a new project
    project1 = app.create_project("My Crafting Project", "This is my crafting project.", ["knitting", "woodworking"], "https://example.com/project1.jpg", user1)

    # Leave a comment on the project
    comment1 = app.leave_comment(project1, user1, "Great project!")

    # Send a message to another user
    user2 = app.create_user("jane_doe", "I love crafting too!", "https://example.com/jane_doe.jpg")
    message1 = app.send_message(user1, user2, "Hey, I love your project!")

    # Search for users, projects, and group projects
    results = app.search("crafting")
    for result in results:
        print(result)

    # Create a new group project
    group_project1 = app.create_group_project("Our Group Project", "This is our group project.", ["knitting", "woodworking"], user1)

    # Add users to the group project
    group_project1.members.append(user1)
    group_project1.members.append(user2)

    # Assign tasks to the group project
    group_project1.tasks.append("Task 1")
    group_project1.tasks.append("Task 2")

    # Track progress on the group project
    group_project1.progress = 50

    # Print the group project details
    print(group_project1)