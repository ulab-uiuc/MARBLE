# solution.py
# Import required libraries
from typing import List, Dict
from datetime import datetime

# Define a class for User Profile Management
class UserProfile:
    def __init__(self, user_id: int, name: str, email: str, skills: List[str], interests: List[str], past_projects: List[str]):
        """
        Initialize a user profile.

        Args:
        user_id (int): Unique identifier for the user.
        name (str): Name of the user.
        email (str): Email address of the user.
        skills (List[str]): List of skills the user possesses.
        interests (List[str]): List of interests the user has.
        past_projects (List[str]): List of past projects the user has worked on.
        """
        self.user_id = user_id
        self.name = name
        self.email = email
        self.skills = skills
        self.interests = interests
        self.past_projects = past_projects

    def edit_profile(self, name: str = None, email: str = None, skills: List[str] = None, interests: List[str] = None, past_projects: List[str] = None):
        """
        Edit the user profile.

        Args:
        name (str): New name of the user.
        email (str): New email address of the user.
        skills (List[str]): New list of skills the user possesses.
        interests (List[str]): New list of interests the user has.
        past_projects (List[str]): New list of past projects the user has worked on.
        """
        if name:
            self.name = name
        if email:
            self.email = email
        if skills:
            self.skills = skills
        if interests:
            self.interests = interests
        if past_projects:
            self.past_projects = past_projects

# Define a class for Project Creation and Management
class Project:class SearchAndMatch:
    def __init__(self, users: Dict[int, UserProfile], projects: Dict[int, Project]):
        self.users = users
        self.projects = projects

    def search_projects(self, skills: List[str], interests: List[str]) -> List[Project]:
        matching_projects = []
        for project in self.projects.values():
            if any(skill in project.required_skills for skill in skills) and any(interest in project.description for interest in interests):
                matching_projects.append(project)
        return matching_projects

    def suggest_projects(self, user_id: int) -> List[Project]:
        user = self.users.get(user_id)
        if user:
            return self.search_projects(user.skills, user.interests)
        return []    def suggest_projects(self, user_id: int) -> List[Project]:
        user = self.users.get(user_id)
        if user:
            return self.search_projects(user.skills, user.interests)
        return []        user = self.users.get(user_id)
        if not user:
            return []
        if user:
            return self.search_projects(user.skills, user.interests)
        return []

# Define a class for Project Collaboration Tools
class CollaborationTools:
    def __init__(self, projects: Dict[int, Project]):
        """
        Initialize the collaboration tools.

        Args:
        projects (Dict[int, Project]): Dictionary of projects.
        """
        self.projects = projects

    def send_message(self, project_id: int, message: str):
        """
        Send a message to a project team.

        Args:
        project_id (int): ID of the project.
        message (str): Message to send.
        """
        project = self.projects.get(project_id)
        if project:
            print(f"Message sent to project {project.title}: {message}")

    def share_code(self, project_id: int, code: str):
        """
        Share code with a project team.

        Args:
        project_id (int): ID of the project.
        code (str): Code to share.
        """
        project = self.projects.get(project_id)
        if project:
            print(f"Code shared with project {project.title}: {code}")

    def manage_tasks(self, project_id: int, tasks: List[str]):
        """
        Manage tasks for a project.

        Args:
        project_id (int): ID of the project.
        tasks (List[str]): List of tasks to manage.
        """
        project = self.projects.get(project_id)
        if project:
            print(f"Tasks managed for project {project.title}: {tasks}")

# Define test cases
def test_user_profile_creation():
    user = UserProfile(1, "John Doe", "john@example.com", ["Python", "Java"], ["Machine Learning", "Data Science"], ["Project 1", "Project 2"])
    assert user.user_id == 1
    assert user.name == "John Doe"
    assert user.email == "john@example.com"
    assert user.skills == ["Python", "Java"]
    assert user.interests == ["Machine Learning", "Data Science"]
    assert user.past_projects == ["Project 1", "Project 2"]

def test_project_creation():
    project = Project(1, "Project 1", "This is a project", ["Python", "Java"], [1, 2])
    assert project.project_id == 1
    assert project.title == "Project 1"
    assert project.description == "This is a project"
    assert project.required_skills == ["Python", "Java"]
    assert project.team_members == [1, 2]

def test_search_and_match():
    users = {1: UserProfile(1, "John Doe", "john@example.com", ["Python", "Java"], ["Machine Learning", "Data Science"], ["Project 1", "Project 2"])}
    projects = {1: Project(1, "Project 1", "This is a project", ["Python", "Java"], [1, 2])}
    search_and_match = SearchAndMatch(users, projects)
    matching_projects = search_and_match.search_projects(["Python", "Java"], ["Machine Learning", "Data Science"])
    assert len(matching_projects) == 1
    assert matching_projects[0].title == "Project 1"

def test_collaboration_tools():
    projects = {1: Project(1, "Project 1", "This is a project", ["Python", "Java"], [1, 2])}
    collaboration_tools = CollaborationTools(projects)
    collaboration_tools.send_message(1, "Hello, team!")
    collaboration_tools.share_code(1, "print('Hello, world!')")
    collaboration_tools.manage_tasks(1, ["Task 1", "Task 2"])

# Run test cases
test_user_profile_creation()
test_project_creation()
test_search_and_match()
test_collaboration_tools()

# Example usage
if __name__ == "__main__":
    users = {1: UserProfile(1, "John Doe", "john@example.com", ["Python", "Java"], ["Machine Learning", "Data Science"], ["Project 1", "Project 2"])}
    projects = {1: Project(1, "Project 1", "This is a project", ["Python", "Java"], [1, 2])}
    search_and_match = SearchAndMatch(users, projects)
    collaboration_tools = CollaborationTools(projects)

    # Create a new user profile
    user = UserProfile(2, "Jane Doe", "jane@example.com", ["Python", "JavaScript"], ["Web Development", "Data Science"], ["Project 3", "Project 4"])
    users[2] = user

    # Create a new project
    project = Project(2, "Project 2", "This is another project", ["Python", "JavaScript"], [1, 2])
    projects[2] = project

    # Search for projects
    matching_projects = search_and_match.search_projects(["Python", "JavaScript"], ["Web Development", "Data Science"])
    print("Matching projects:")
    for project in matching_projects:
        print(project.title)

    # Suggest projects to a user
    suggested_projects = search_and_match.suggest_projects(1)
    print("Suggested projects:")
    for project in suggested_projects:
        print(project.title)

    # Send a message to a project team
    collaboration_tools.send_message(1, "Hello, team!")

    # Share code with a project team
    collaboration_tools.share_code(1, "print('Hello, world!')")

    # Manage tasks for a project
    collaboration_tools.manage_tasks(1, ["Task 1", "Task 2"])