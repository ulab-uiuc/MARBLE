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
        self.projects = []
        self.group_projects = []
        self.comments = []
        self.messages = []

    def create_project(self, project_name, project_description, project_tags):
        """
        Create a new project.

        Args:
        project_name (str): The name of the project.
        project_description (str): The description of the project.
        project_tags (list): The tags of the project.

        Returns:
        Project: The created project.
        """
        project = Project(project_name, project_description, project_tags)
        self.projects.append(project)
        return project

    def join_group_project(self, group_project):
        """
        Join a group project.

        Args:
        group_project (GroupProject): The group project to join.
        """
        self.group_projects.append(group_project)

    def leave_comment(self, project, comment):
        """
        Leave a comment on a project.

        Args:
        project (Project): The project to leave a comment on.
        comment (str): The comment to leave.
        """
        self.comments.append(Comment(project, comment))

    def send_message(self, recipient, message):
        """
        Send a message to another user.

        Args:
        recipient (User): The recipient of the message.
        message (str): The message to send.
        """
        self.messages.append(Message(recipient, message))


# project.py
class Project:
    def __init__(self, project_name, project_description, project_tags):
        """
        Initialize a Project object.

        Args:
        project_name (str): The name of the project.
        project_description (str): The description of the project.
        project_tags (list): The tags of the project.
        """
        self.project_name = project_name
        self.project_description = project_description
        self.project_tags = project_tags
        self.comments = []

    def add_comment(self, comment):
        """
        Add a comment to the project.

        Args:
        comment (Comment): The comment to add.
        """
        self.comments.append(comment)


# group_project.py
class GroupProject:
    def __init__(self, project_name, project_description, project_tags, leader):
        """
        Initialize a GroupProject object.

        Args:
        project_name (str): The name of the project.
        project_description (str): The description of the project.
        project_tags (list): The tags of the project.
        leader (User): The leader of the project.
        """
        self.project_name = project_name
        self.project_description = project_description
        self.project_tags = project_tags
        self.leader = leader
        self.members = []
        self.tasks = []

    def add_member(self, member):
        """
        Add a member to the group project.

        Args:
        member (User): The member to add.
        """
        self.members.append(member)

    def assign_task(self, task):
        """
        Assign a task to the group project.

        Args:
        task (Task): The task to assign.
        """
        self.tasks.append(task)


# comment.py
class Comment:
    def __init__(self, project, comment):
        """
        Initialize a Comment object.

        Args:
        project (Project): The project the comment is on.
        comment (str): The comment.
        """
        self.project = project
        self.comment = comment
        self.upvotes = 0
        self.downvotes = 0

    def upvote(self):
        """
        Upvote the comment.
        """
        self.upvotes += 1

    def downvote(self):
        """
        Downvote the comment.
        """
        self.downvotes += 1


# message.py
class Message:
    def __init__(self, recipient, message):
        """
        Initialize a Message object.

        Args:
        recipient (User): The recipient of the message.
        message (str): The message.
        """
        self.recipient = recipient
        self.message = message


# task.py
class Task:
    def __init__(self, task_name, task_description):
        """
        Initialize a Task object.

        Args:
        task_name (str): The name of the task.
        task_description (str): The description of the task.
        """
        self.task_name = task_name
        self.task_description = task_description
        self.status = "Not Started"


# search.py
class Search:
    def __init__(self, users, projects, group_projects):
        """
        Initialize a Search object.

        Args:
        users (list): The list of users.
        projects (list): The list of projects.
        group_projects (list): The list of group projects.
        """
        self.users = users
        self.projects = projects
        self.group_projects = group_projects

    def search_users(self, keyword):
        """
        Search for users by keyword.

        Args:
        keyword (str): The keyword to search for.

        Returns:
        list: The list of users that match the keyword.
        """
        return [user for user in self.users if keyword in user.username or keyword in user.bio]

    def search_projects(self, keyword):
        """
        Search for projects by keyword.

        Args:
        keyword (str): The keyword to search for.

        Returns:
        list: The list of projects that match the keyword.
        """
        return [project for project in self.projects if keyword in project.project_name or keyword in project.project_description]

    def search_group_projects(self, keyword):
        """
        Search for group projects by keyword.

        Args:
        keyword (str): The keyword to search for.

        Returns:
        list: The list of group projects that match the keyword.
        """
        return [group_project for group_project in self.group_projects if keyword in group_project.project_name or keyword in group_project.project_description]


# solution.py
def main():
    # Create users
    user1 = User("user1", "This is user1's bio", "user1's profile picture")
    user2 = User("user2", "This is user2's bio", "user2's profile picture")

    # Create projects
    project1 = user1.create_project("Project1", "This is project1's description", ["tag1", "tag2"])
    project2 = user2.create_project("Project2", "This is project2's description", ["tag3", "tag4"])

    # Create group project
    group_project = GroupProject("Group Project", "This is group project's description", ["tag5", "tag6"], user1)
    group_project.add_member(user2)

    # Leave comments
    user1.leave_comment(project2, "This is a comment on project2")
    user2.leave_comment(project1, "This is a comment on project1")

    # Send messages
    user1.send_message(user2, "This is a message from user1 to user2")
    user2.send_message(user1, "This is a message from user2 to user1")

    # Search for users, projects, and group projects
    search = Search([user1, user2], [project1, project2], [group_project])
    print("Search results for users:")
    for user in search.search_users("user"):
        print(user.username)
    print("Search results for projects:")
    for project in search.search_projects("project"):
        print(project.project_name)
    print("Search results for group projects:")
    for group_project in search.search_group_projects("group"):
        print(group_project.project_name)


if __name__ == "__main__":
    main()