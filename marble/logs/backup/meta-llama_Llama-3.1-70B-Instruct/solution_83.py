# user.py
class User:
    def __init__(self, id, name, email, skills=None, interests=None, past_projects=None):
        """
        Initialize a User object.

        Args:
            id (int): Unique identifier for the user.
            name (str): Name of the user.
            email (str): Email address of the user.
            skills (list, optional): List of skills the user possesses. Defaults to None.
            interests (list, optional): List of interests the user has. Defaults to None.
            past_projects (list, optional): List of past projects the user has worked on. Defaults to None.
        """
        self.id = id
        self.name = name
        self.email = email
        self.skills = skills if skills else []
        self.interests = interests if interests else []
        self.past_projects = past_projects if past_projects else []

    def add_skill(self, skill):
        """
        Add a skill to the user's skills list.

        Args:
            skill (str): Skill to add.
        """
        self.skills.append(skill)

    def add_interest(self, interest):
        """
        Add an interest to the user's interests list.

        Args:
            interest (str): Interest to add.
        """
        self.interests.append(interest)

    def add_past_project(self, project):
        """
        Add a past project to the user's past projects list.

        Args:
            project (str): Past project to add.
        """
        self.past_projects.append(project)


# project.py
class Project:
    def __init__(self, id, title, description, required_skills=None, team_members=None, milestones=None):
        """
        Initialize a Project object.

        Args:
            id (int): Unique identifier for the project.
            title (str): Title of the project.
            description (str): Description of the project.
            required_skills (list, optional): List of skills required for the project. Defaults to None.
            team_members (list, optional): List of team members working on the project. Defaults to None.
            milestones (list, optional): List of milestones for the project. Defaults to None.
        """
        self.id = id
        self.title = title
        self.description = description
        self.required_skills = required_skills if required_skills else []
        self.team_members = team_members if team_members else []
        self.milestones = milestones if milestones else []

    def add_required_skill(self, skill):
        """
        Add a required skill to the project's required skills list.

        Args:
            skill (str): Required skill to add.
        """
        self.required_skills.append(skill)

    def add_team_member(self, user):
        """
        Add a team member to the project's team members list.

        Args:
            user (User): Team member to add.
        """
        self.team_members.append(user)

    def add_milestone(self, milestone):
        """
        Add a milestone to the project's milestones list.

        Args:
            milestone (str): Milestone to add.
        """
        self.milestones.append(milestone)


# collaboration_tools.py
class CollaborationTools:
    def __init__(self):
        """
        Initialize a CollaborationTools object.
        """
        self.messages = []
        self.code_repository = {}
        self.task_management_boards = {}

    def send_message(self, message):
        """
        Send a message to the team.

        Args:
            message (str): Message to send.
        """
        self.messages.append(message)

    def add_code(self, code, filename):
        """
        Add code to the code repository.

        Args:
            code (str): Code to add.
            filename (str): Filename for the code.
        """
        self.code_repository[filename] = code

    def create_task_management_board(self, project_id):
        """
        Create a task management board for a project.

        Args:
            project_id (int): ID of the project.
        """
        self.task_management_boards[project_id] = []

    def add_task(self, project_id, task):
        """
        Add a task to a task management board.

        Args:
            project_id (int): ID of the project.
            task (str): Task to add.
        """
        self.task_management_boards[project_id].append(task)


# search_and_matching.py
class SearchAndMatching:
    def __init__(self, users, projects):
        """
        Initialize a SearchAndMatching object.

        Args:
            users (list): List of User objects.
            projects (list): List of Project objects.
        """
        self.users = users
        self.projects = projects

    def search_users(self, skills=None, interests=None):
        """
        Search for users based on skills and interests.

        Args:
            skills (list, optional): List of skills to search for. Defaults to None.
            interests (list, optional): List of interests to search for. Defaults to None.

        Returns:
            list: List of User objects that match the search criteria.
        """
        matching_users = []
        for user in self.users:
            if skills and any(skill in user.skills for skill in skills):
                matching_users.append(user)
            if interests and any(interest in user.interests for interest in interests):
                matching_users.append(user)
        return matching_users

    def search_projects(self, required_skills=None, title=None):
        """
        Search for projects based on required skills and title.

        Args:
            required_skills (list, optional): List of required skills to search for. Defaults to None.
            title (str, optional): Title to search for. Defaults to None.

        Returns:
            list: List of Project objects that match the search criteria.
        """
        matching_projects = []
        for project in self.projects:
            if required_skills and any(skill in project.required_skills for skill in required_skills):
                matching_projects.append(project)
            if title and project.title == title:
                matching_projects.append(project)
        return matching_projects

    def match_users_with_projects(self, user):
        """
        Match a user with projects based on their skills and interests.

        Args:
            user (User): User to match with projects.

        Returns:
            list: List of Project objects that match the user's skills and interests.
        """
        matching_projects = []
        for project in self.projects:
            if any(skill in project.required_skills for skill in user.skills):
                matching_projects.append(project)
            if any(interest in project.description for interest in user.interests):
                matching_projects.append(project)
        return matching_projects


# test_cases.py
import unittest
from user import User
from project import Project
from collaboration_tools import CollaborationTools
from search_and_matching import SearchAndMatching

class TestCollaborateCraft(unittest.TestCase):
    def test_user_profile_creation(self):
        user = User(1, "John Doe", "johndoe@example.com")
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "johndoe@example.com")

    def test_project_creation(self):
        project = Project(1, "Test Project", "This is a test project")
        self.assertEqual(project.title, "Test Project")
        self.assertEqual(project.description, "This is a test project")

    def test_collaboration_tools(self):
        collaboration_tools = CollaborationTools()
        collaboration_tools.send_message("Hello, team!")
        self.assertEqual(collaboration_tools.messages, ["Hello, team!"])
        collaboration_tools.add_code("print('Hello, world!')", "hello.py")
        self.assertEqual(collaboration_tools.code_repository, {"hello.py": "print('Hello, world!')"})

    def test_search_and_matching(self):
        user1 = User(1, "John Doe", "johndoe@example.com")
        user1.add_skill("Python")
        user1.add_interest("Machine Learning")
        user2 = User(2, "Jane Doe", "janedoe@example.com")
        user2.add_skill("Java")
        user2.add_interest("Web Development")
        project1 = Project(1, "Test Project", "This is a test project")
        project1.add_required_skill("Python")
        project2 = Project(2, "Another Project", "This is another project")
        project2.add_required_skill("Java")
        search_and_matching = SearchAndMatching([user1, user2], [project1, project2])
        matching_users = search_and_matching.search_users(skills=["Python"])
        self.assertEqual(matching_users, [user1])
        matching_projects = search_and_matching.search_projects(required_skills=["Java"])
        self.assertEqual(matching_projects, [project2])
        matching_projects = search_and_matching.match_users_with_projects(user1)
        self.assertEqual(matching_projects, [project1])

if __name__ == "__main__":
    unittest.main()