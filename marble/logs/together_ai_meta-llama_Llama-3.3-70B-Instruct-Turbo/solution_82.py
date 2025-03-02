
def search_by_tag(self, keyword: str):
        import re
        matching_projects = [project for project in self.projects if any(re.search(keyword, tag) for tag in project.tags)]
        matching_group_projects = [group_project for group_project in self.group_projects if any(re.search(keyword, tag) for tag in group_project.tags)]
        return {
            'projects': matching_projects,
            'group_projects': matching_group_projects
        }# solution.py
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
        self.projects = []
        self.group_projects = []

# Define a class for Project
class Project:
    def __init__(self, title: str, description: str, tags: List[str], user: User):
        """
        Initialize a Project object.

        Args:
        - title (str): The title of the project.
        - description (str): The description of the project.
        - tags (List[str]): The tags of the project.
        - user (User): The user who posted the project.
        """
        self.title = title
        self.description = description
        self.tags = tags
        self.user = user
        self.comments = []

# Define a class for GroupProject
class GroupProject:
    def __init__(self, title: str, description: str, tags: List[str], leader: User):
        """
        Initialize a GroupProject object.

        Args:
        - title (str): The title of the group project.
        - description (str): The description of the group project.
        - tags (List[str]): The tags of the group project.
        - leader (User): The leader of the group project.
        """
        self.title = title
        self.description = description
        self.tags = tags
        self.leader = leader
        self.members = []
        self.tasks = []

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
        self.upvotes = 0
        self.downvotes = 0

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

# Define a class for CollaborateCraft
class CollaborateCraft:
    def __init__(self):
        """
        Initialize a CollaborateCraft object.
        """
        self.users = []
        self.projects = []
        self.group_projects = []
        self.messages = []

    def create_profile(self, username: str, bio: str, profile_picture: str):
        """
        Create a new user profile.

        Args:
        - username (str): The username of the user.
        - bio (str): The bio of the user.
        - profile_picture (str): The profile picture of the user.

        Returns:
        - User: The newly created user.
        """
        new_user = User(username, bio, profile_picture)
        self.users.append(new_user)
        return new_user

    def post_project(self, title: str, description: str, tags: List[str], user: User):
        """
        Post a new project.

        Args:
        - title (str): The title of the project.
        - description (str): The description of the project.
        - tags (List[str]): The tags of the project.
        - user (User): The user who posted the project.

        Returns:
        - Project: The newly posted project.
        """
        new_project = Project(title, description, tags, user)
        self.projects.append(new_project)
        user.projects.append(new_project)
        return new_project

    def create_group_project(self, title: str, description: str, tags: List[str], leader: User):
        """
        Create a new group project.

        Args:
        - title (str): The title of the group project.
        - description (str): The description of the group project.
        - tags (List[str]): The tags of the group project.
        - leader (User): The leader of the group project.

        Returns:
        - GroupProject: The newly created group project.
        """
        new_group_project = GroupProject(title, description, tags, leader)
        self.group_projects.append(new_group_project)
        leader.group_projects.append(new_group_project)
        return new_group_project

    def join_group_project(self, group_project: GroupProject, user: User):
        """
        Join a group project.

        Args:
        - group_project (GroupProject): The group project to join.
        - user (User): The user who wants to join the group project.
        """
        group_project.members.append(user)
        user.group_projects.append(group_project)

    def leave_comment(self, project: Project, text: str, user: User):
        """
        Leave a comment on a project.

        Args:
        - project (Project): The project to comment on.
        - text (str): The text of the comment.
        - user (User): The user who made the comment.

        Returns:
        - Comment: The newly created comment.
        """
        new_comment = Comment(text, user)
        project.comments.append(new_comment)
        return new_comment

    def send_message(self, text: str, sender: User, recipient: User):import re
def search(self, keyword: str):
    # Use regular expressions to allow for partial matches
    matching_users = [user for user in self.users if re.search(keyword, user.username) or re.search(keyword, user.bio)]
    matching_projects = [project for project in self.projects if re.search(keyword, project.title) or re.search(keyword, project.description) or any(re.search(keyword, tag) for tag in project.tags)]
    matching_group_projects = [group_project for group_project in self.group_projects if re.search(keyword, group_project.title) or re.search(keyword, group_project.description) or any(re.search(keyword, tag) for tag in group_project.tags)]
    return matching_users, matching_projects, matching_group_projects        matching_users = [user for user in self.users if keyword in user.username or keyword in user.bio]def search(self, keyword: str):
        # Use regular expressions to allow for partial matches
        import re
        matching_users = [user for user in self.users if re.search(keyword, user.username) or re.search(keyword, user.bio)]
        matching_projects = [project for project in self.projects if re.search(keyword, project.title) or re.search(keyword, project.description) or any(re.search(keyword, tag) for tag in project.tags)]
        matching_group_projects = [group_project for group_project in self.group_projects if re.search(keyword, group_project.title) or re.search(keyword, group_project.description) or any(re.search(keyword, tag) for tag in group_project.tags)]
        return {
            'users': matching_users,
            'projects': matching_projects,
            'group_projects': matching_group_projects
        }        return matching_users, matching_projects, matching_group_projects

# Test cases
def test_collaborate_craft():
    # Create a new CollaborateCraft object
    collaborate_craft = CollaborateCraft()

    # Create a new user profile
    user1 = collaborate_craft.create_profile("user1", "This is user1's bio", "user1.jpg")

    # Post a new project
    project1 = collaborate_craft.post_project("Project 1", "This is project 1's description", ["tag1", "tag2"], user1)

    # Create a new group project
    group_project1 = collaborate_craft.create_group_project("Group Project 1", "This is group project 1's description", ["tag1", "tag2"], user1)

    # Join the group project
    collaborate_craft.join_group_project(group_project1, user1)

    # Leave a comment on the project
    comment1 = collaborate_craft.leave_comment(project1, "This is a comment on project 1", user1)

    # Send a private message
    message1 = collaborate_craft.send_message("Hello, this is a private message", user1, user1)

    # Search for users, projects, and group projects
    matching_users, matching_projects, matching_group_projects = collaborate_craft.search("user1")

    # Print the results
    print("Matching users:")
    for user in matching_users:
        print(user.username)
    print("Matching projects:")
    for project in matching_projects:
        print(project.title)
    print("Matching group projects:")
    for group_project in matching_group_projects:
        print(group_project.title)

# Run the test cases
test_collaborate_craft()