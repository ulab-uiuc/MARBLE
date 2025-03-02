# user.py
class User:
    def __init__(self, id, name, email, skills, interests, past_projects):
        """
        Initialize a User object.

        Args:
        id (int): Unique identifier for the user.
        name (str): Name of the user.
        email (str): Email address of the user.
        skills (list): List of skills the user possesses.
        interests (list): List of interests the user has.
        past_projects (list): List of past projects the user has worked on.
        """
        self.id = id
        self.name = name
        self.email = email
        self.skills = skills
        self.interests = interests
        self.past_projects = past_projects

    def __str__(self):
        return f"User {self.name} with email {self.email}"


# project.py
class Project:
    def __init__(self, id, title, description, required_skills, team_members, milestones):
    def __init__(self, id, title, description, required_skills, team_members, milestones, tags):
        """
        Initialize a Project object.

        Args:
        id (int): Unique identifier for the project.
        title (str): Title of the project.
        description (str): Description of the project.
        required_skills (list): List of skills required for the project.
        team_members (list): List of team members working on the project.
        milestones (list): List of milestones for the project.
        """
        self.id = id
        self.title = title
        self.description = description
        self.required_skills = required_skills
        self.team_members = team_members
        self.milestones = milestones
        self.tags = tags

    def __str__(self):
        return f"Project {self.title} with description {self.description}"


# collaborate_craft.py
class CollaborateCraft:
    def __init__(self):
        """
        Initialize a CollaborateCraft object.
        """
        self.users = []
        self.projects = []

    def create_user(self, id, name, email, skills, interests, past_projects):
        """
        Create a new user.

        Args:
        id (int): Unique identifier for the user.
        name (str): Name of the user.
        email (str): Email address of the user.
        skills (list): List of skills the user possesses.
        interests (list): List of interests the user has.
        past_projects (list): List of past projects the user has worked on.

        Returns:
        User: The newly created user.
        """
        user = User(id, name, email, skills, interests, past_projects)
        self.users.append(user)
        return user

    def create_project(self, id, title, description, required_skills, team_members, milestones):
        """
        Create a new project.

        Args:
        id (int): Unique identifier for the project.
        title (str): Title of the project.
        description (str): Description of the project.
        required_skills (list): List of skills required for the project.
        team_members (list): List of team members working on the project.
        milestones (list): List of milestones for the project.

        Returns:
        Project: The newly created project.
        """
        project = Project(id, title, description, required_skills, team_members, milestones)
        self.projects.append(project)
        return project

    def search_users(self, skills, interests):
        """
        Search for users based on skills and interests.

        Args:
        skills (list): List of skills to search for.
        interests (list): List of interests to search for.

        Returns:
        list: List of users that match the search criteria.
        """
        matching_users = []
        for user in self.users:
            if any(skill in user.skills for skill in skills) and any(interest in user.interests for interest in interests):
                matching_users.append(user)
        return matching_users

    def search_projects(self, required_skills):def match_users_with_projects(self, user):if any(skill in project.required_skills for skill in user.skills) and any(interest in project.tags for interest in user.interests):matching_projects.append(project)
        return matching_projects

    def match_users_with_projects(self, user):
        """
        Match a user with projects based on their skills and interests.

        Args:
        user (User): The user to match with projects.

        Returns:
        list: List of projects that match the user's skills and interests.
        """
        matching_projects = []
        for project in self.projects:
            if any(skill in user.skills for skill in project.required_skills) and any(interest in user.interests for interest in project.description):
                matching_projects.append(project)
        return matching_projects


# test_collaborate_craft.py
import unittest
from collaborate_craft import CollaborateCraft, User, Project

class TestCollaborateCraft(unittest.TestCase):
    def test_create_user(self):
        collaborate_craft = CollaborateCraft()
        user = collaborate_craft.create_user(1, "John Doe", "john@example.com", ["Python", "Java"], ["Machine Learning", "Data Science"], ["Project 1", "Project 2"])
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "john@example.com")
        self.assertEqual(user.skills, ["Python", "Java"])
        self.assertEqual(user.interests, ["Machine Learning", "Data Science"])
        self.assertEqual(user.past_projects, ["Project 1", "Project 2"])

    def test_create_project(self):
        collaborate_craft = CollaborateCraft()
        project = collaborate_craft.create_project(1, "Project 1", "This is a project", ["Python", "Java"], ["John Doe", "Jane Doe"], ["Milestone 1", "Milestone 2"])
        self.assertEqual(project.title, "Project 1")
        self.assertEqual(project.description, "This is a project")
        self.assertEqual(project.required_skills, ["Python", "Java"])
        self.assertEqual(project.team_members, ["John Doe", "Jane Doe"])
        self.assertEqual(project.milestones, ["Milestone 1", "Milestone 2"])

    def test_search_users(self):
        collaborate_craft = CollaborateCraft()
        user1 = collaborate_craft.create_user(1, "John Doe", "john@example.com", ["Python", "Java"], ["Machine Learning", "Data Science"], ["Project 1", "Project 2"])
        user2 = collaborate_craft.create_user(2, "Jane Doe", "jane@example.com", ["Python", "C++"], ["Machine Learning", "Web Development"], ["Project 3", "Project 4"])
        matching_users = collaborate_craft.search_users(["Python"], ["Machine Learning"])
        self.assertEqual(len(matching_users), 2)
        self.assertIn(user1, matching_users)
        self.assertIn(user2, matching_users)

    def test_search_projects(self):
        collaborate_craft = CollaborateCraft()
        project1 = collaborate_craft.create_project(1, "Project 1", "This is a project", ["Python", "Java"], ["John Doe", "Jane Doe"], ["Milestone 1", "Milestone 2"])
        project2 = collaborate_craft.create_project(2, "Project 2", "This is another project", ["Python", "C++"], ["John Doe", "Jane Doe"], ["Milestone 3", "Milestone 4"])
        matching_projects = collaborate_craft.search_projects(["Python"])
        self.assertEqual(len(matching_projects), 2)
        self.assertIn(project1, matching_projects)
        self.assertIn(project2, matching_projects)

    def test_match_users_with_projects(self):
        collaborate_craft = CollaborateCraft()
        user = collaborate_craft.create_user(1, "John Doe", "john@example.com", ["Python", "Java"], ["Machine Learning", "Data Science"], ["Project 1", "Project 2"])
        project1 = collaborate_craft.create_project(1, "Project 1", "This is a project", ["Python", "Java"], ["John Doe", "Jane Doe"], ["Milestone 1", "Milestone 2"])
        project2 = collaborate_craft.create_project(2, "Project 2", "This is another project", ["Python", "C++"], ["John Doe", "Jane Doe"], ["Milestone 3", "Milestone 4"])
        matching_projects = collaborate_craft.match_users_with_projects(user)
        self.assertEqual(len(matching_projects), 2)
        self.assertIn(project1, matching_projects)
        self.assertIn(project2, matching_projects)

if __name__ == "__main__":
    unittest.main()