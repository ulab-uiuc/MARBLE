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
        return f"User('{self.username}', '{self.bio}', '{self.profile_picture}')"


# project.py
class Project:
    def __init__(self, title, description, tags, media):
        """
        Initialize a Project object.

        Args:
            title (str): The title of the project.
            description (str): The description of the project.
            tags (list): The tags of the project.
            media (str): The media of the project (e.g., photo, video).
        """
        self.title = title
        self.description = description
        self.tags = tags
        self.media = media
        self.comments = []

    def __str__(self):
        return f"Project('{self.title}', '{self.description}', '{self.tags}', '{self.media}')"


# group_project.py
class GroupProject:
    def __init__(self, title, description, tags, leader):
        """
        Initialize a GroupProject object.

        Args:
            title (str): The title of the group project.
            description (str): The description of the group project.
            tags (list): The tags of the group project.
            leader (User): The leader of the group project.
        """
        self.title = title
        self.description = description
        self.tags = tags
        self.leader = leader
        self.members = []
        self.tasks = []

    def __str__(self):
        return f"GroupProject('{self.title}', '{self.description}', '{self.tags}', '{self.leader.username}')"


# comment.py
class Comment:
    def __init__(self, text, upvotes, downvotes, user):
        """
        Initialize a Comment object.

        Args:
            text (str): The text of the comment.
            upvotes (int): The number of upvotes of the comment.
            downvotes (int): The number of downvotes of the comment.
            user (User): The user who made the comment.
        """
        self.text = text
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.user = user

    def __str__(self):
        return f"Comment('{self.text}', {self.upvotes}, {self.downvotes}, '{self.user.username}')"


# messaging.py
class Message:
    def __init__(self, text, sender, recipient):
        """
        Initialize a Message object.

        Args:
            text (str): The text of the message.
            sender (User): The user who sent the message.
            recipient (User): The user who received the message.
        """
        self.text = text
        self.sender = sender
        self.recipient = recipient

    def __str__(self):
        return f"Message('{self.text}', '{self.sender.username}', '{self.recipient.username}')"


# solution.py
class CollaborateCraft:
    def __init__(self):
        """
        Initialize a CollaborateCraft object.
        """
        self.users = []
        self.projects = []
        self.group_projects = []
        self.comments = []
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
        user = User(username, bio, profile_picture)
        self.users.append(user)
        return user

    def create_project(self, title, description, tags, media, user):
        """
        Create a new project.

        Args:
            title (str): The title of the project.
            description (str): The description of the project.
            tags (list): The tags of the project.
            media (str): The media of the project (e.g., photo, video).
            user (User): The user who created the project.

        Returns:
            Project: The created project.
        """
        project = Project(title, description, tags, media)
        user.posts.append(project)
        self.projects.append(project)
        return project

    def create_group_project(self, title, description, tags, leader):
        """
        Create a new group project.

        Args:
            title (str): The title of the group project.
            description (str): The description of the group project.
            tags (list): The tags of the group project.
            leader (User): The leader of the group project.

        Returns:
            GroupProject: The created group project.
        """
        group_project = GroupProject(title, description, tags, leader)
        leader.group_projects.append(group_project)
        self.group_projects.append(group_project)
        return group_project

    def leave_comment(self, text, upvotes, downvotes, user, project):
        """
        Leave a comment on a project.

        Args:
            text (str): The text of the comment.
            upvotes (int): The number of upvotes of the comment.
            downvotes (int): The number of downvotes of the comment.
            user (User): The user who left the comment.
            project (Project): The project on which the comment was left.

        Returns:
            Comment: The created comment.
        """
        comment = Comment(text, upvotes, downvotes, user)
        project.comments.append(comment)
        self.comments.append(comment)
        return comment

    def send_message(self, text, sender, recipient):
        """
        Send a message to another user.

        Args:
            text (str): The text of the message.
            sender (User): The user who sent the message.
            recipient (User): The user who received the message.

        Returns:
            Message: The created message.
        """
        message = Message(text, sender, recipient)
        sender.messages.append(message)
        recipient.messages.append(message)
        self.messages.append(message)
        return message

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


# Test cases
if __name__ == "__main__":
    craft = CollaborateCraft()

    # Create users
    user1 = craft.create_user("john", "I love crafting!", "https://example.com/john.jpg")
    user2 = craft.create_user("jane", "I'm a beginner crafter.", "https://example.com/jane.jpg")

    # Create projects
    project1 = craft.create_project("My First Project", "This is my first project!", ["knitting", "woodworking"], "photo.jpg", user1)
    project2 = craft.create_project("My Second Project", "This is my second project!", ["painting", "drawing"], "video.mp4", user2)

    # Create group projects
    group_project1 = craft.create_group_project("Our Group Project", "This is our group project!", ["knitting", "woodworking"], user1)
    group_project2 = craft.create_group_project("Our Other Group Project", "This is our other group project!", ["painting", "drawing"], user2)

    # Leave comments
    comment1 = craft.leave_comment("Great project!", 10, 0, user2, project1)
    comment2 = craft.leave_comment("Nice job!", 5, 0, user1, project2)

    # Send messages
    message1 = craft.send_message("Hi, how are you?", user1, user2)
    message2 = craft.send_message("Hi, I'm good thanks!", user2, user1)

    # Search
    results = craft.search("knitting")
    print(results)

    # Print results
    print("Users:")
    for user in craft.users:
        print(user)
    print("Projects:")
    for project in craft.projects:
        print(project)
    print("Group Projects:")
    for group_project in craft.group_projects:
        print(group_project)
    print("Comments:")
    for comment in craft.comments:
        print(comment)
    print("Messages:")
    for message in craft.messages:
        print(message)