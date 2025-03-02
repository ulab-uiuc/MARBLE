# solution.py
# CollaborateCraft Social Networking Application

# Import required libraries
from datetime import datetime
from typing import List, Dict

# Define a class for User
class User:
    def __init__(self, username: str, bio: str, profile_picture: str):
        """
        Initialize a User object.

        Args:
        - username (str): The username of the user.
        - bio (str): The bio of the user.
        - profile_picture (str): The profile picture of the user.
        """
        self.username = username
        self.bio = bio
        self.profile_picture = profile_picture
        self.projects = []  # List to store user's projects
        self.group_projects = []  # List to store user's group projects
        self.messages = []  # List to store user's messages

# Define a class for Project
class Project:
    def __init__(self, title: str, description: str, tags: List[str], media: str):
        """
        Initialize a Project object.

        Args:
        - title (str): The title of the project.
        - description (str): The description of the project.
        - tags (List[str]): The tags of the project.
        - media (str): The media (photo or video) of the project.
        """
        self.title = title
        self.description = description
        self.tags = tags
        self.media = media
        self.comments = []  # List to store project comments

# Define a class for GroupProject
class GroupProject:
    def __init__(self, title: str, description: str, leader: User):
        """
        Initialize a GroupProject object.

        Args:
        - title (str): The title of the group project.
        - description (str): The description of the group project.
        - leader (User): The leader of the group project.
        """
        self.title = title
        self.description = description
        self.leader = leader
        self.members = []  # List to store group project members
        self.tasks = []  # List to store group project tasks

# Define a class for Comment
class Comment:
    def __init__(self, text: str, user: User):
        """
        Initialize a Comment object.

        Args:
        - text (str): The text of the comment.
        - user (User): The user who made the comment.
        """
        self.text = text
        self.user = user
        self.upvotes = 0  # Number of upvotes for the comment
        self.downvotes = 0  # Number of downvotes for the comment

# Define a class for Message
class Message:
    def __init__(self, text: str, sender: User, recipient: User):
        """
        Initialize a Message object.

        Args:
        - text (str): The text of the message.
        - sender (User): The sender of the message.
        - recipient (User): The recipient of the message.
        """
        self.text = text
        self.sender = sender
        self.recipient = recipient

# Define the CollaborateCraft application
class CollaborateCraft:
    def __init__(self):
        """
        Initialize the CollaborateCraft application.
        """
        self.users = []  # List to store all users
        self.projects = []  # List to store all projects
        self.group_projects = []  # List to store all group projects

    def create_profile(self, username: str, bio: str, profile_picture: str):
        """
        Create a new user profile.

        Args:
        - username (str): The username of the user.
        - bio (str): The bio of the user.
        - profile_picture (str): The profile picture of the user.

        Returns:
        - User: The newly created user object.
        """
        new_user = User(username, bio, profile_picture)
        self.users.append(new_user)
        return new_user

    def post_project(self, user: User, title: str, description: str, tags: List[str], media: str):
        """
        Post a new project.

        Args:
        - user (User): The user who is posting the project.
        - title (str): The title of the project.
        - description (str): The description of the project.
        - tags (List[str]): The tags of the project.
        - media (str): The media (photo or video) of the project.

        Returns:
        - Project: The newly created project object.
        """
        new_project = Project(title, description, tags, media)
        user.projects.append(new_project)
        self.projects.append(new_project)
        return new_project

    def create_group_project(self, leader: User, title: str, description: str):
        """
        Create a new group project.

        Args:
        - leader (User): The leader of the group project.
        - title (str): The title of the group project.
        - description (str): The description of the group project.

        Returns:
        - GroupProject: The newly created group project object.
        """
        new_group_project = GroupProject(title, description, leader)
        leader.group_projects.append(new_group_project)
        self.group_projects.append(new_group_project)
        return new_group_project

    def join_group_project(self, user: User, group_project: GroupProject):
        """
        Join a group project.

        Args:
        - user (User): The user who is joining the group project.
        - group_project (GroupProject): The group project to join.
        """
        group_project.members.append(user)

    def leave_comment(self, user: User, project: Project, text: str):
        """
        Leave a comment on a project.

        Args:
        - user (User): The user who is leaving the comment.
        - project (Project): The project to comment on.
        - text (str): The text of the comment.

        Returns:
        - Comment: The newly created comment object.
        """
        new_comment = Comment(text, user)
        project.comments.append(new_comment)
        return new_comment

    def send_message(self, sender: User, recipient: User, text: str):from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def search(self, keyword: str):
    results = []
    for user in self.users:
        if fuzz.partial_ratio(keyword.lower(), user.username.lower()) > 60 or fuzz.partial_ratio(keyword.lower(), user.bio.lower()) > 60:
            results.append(user)
    for project in self.projects:
        if (fuzz.partial_ratio(keyword.lower(), project.title.lower()) > 60 or 
            fuzz.partial_ratio(keyword.lower(), project.description.lower()) > 60 or 
            any(fuzz.partial_ratio(keyword.lower(), tag.lower()) > 60 for tag in project.tags)):
            results.append(project)
    for group_project in self.group_projects:
        if fuzz.partial_ratio(keyword.lower(), group_project.title.lower()) > 60 or fuzz.partial_ratio(keyword.lower(), group_project.description.lower()) > 60:
            results.append(group_project)
    return results        results = []
        for user in self.users:
            if keyword in user.username or keyword in user.bio:
                results.append(user)
        for project in self.projects:
            if keyword in project.title or keyword in project.description:
                results.append(project)
        for group_project in self.group_projects:
            if keyword in group_project.title or keyword in group_project.description:
                results.append(group_project)
        return results

# Test cases
def test_collaborate_craft():
    app = CollaborateCraft()

    # Create users
    user1 = app.create_profile("user1", "bio1", "profile_picture1")
    user2 = app.create_profile("user2", "bio2", "profile_picture2")

    # Post projects
    project1 = app.post_project(user1, "project1", "description1", ["tag1", "tag2"], "media1")
    project2 = app.post_project(user2, "project2", "description2", ["tag3", "tag4"], "media2")

    # Create group project
    group_project = app.create_group_project(user1, "group_project", "description")

    # Join group project
    app.join_group_project(user2, group_project)

    # Leave comments
    comment1 = app.leave_comment(user1, project1, "comment1")
    comment2 = app.leave_comment(user2, project2, "comment2")

    # Send messages
    message1 = app.send_message(user1, user2, "message1")
    message2 = app.send_message(user2, user1, "message2")

    # Search
    results = app.search("user1")

    # Print results
    print("Users:")
    for user in app.users:
        print(user.username)
    print("Projects:")
    for project in app.projects:
        print(project.title)
    print("Group Projects:")
    for group_project in app.group_projects:
        print(group_project.title)
    print("Comments:")
    for project in app.projects:
        for comment in project.comments:
            print(comment.text)
    print("Messages:")
    for user in app.users:
        for message in user.messages:
            print(message.text)
    print("Search Results:")
    for result in results:
        if isinstance(result, User):
            print(result.username)
        elif isinstance(result, Project):
            print(result.title)
        elif isinstance(result, GroupProject):
            print(result.title)

# Run test cases
test_collaborate_craft()