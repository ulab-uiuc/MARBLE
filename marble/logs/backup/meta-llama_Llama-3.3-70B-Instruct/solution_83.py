# solution.py
# CollaborateCraft Social Networking Application

# Import required libraries
from datetime import datetime
from typing import List, Dict

# Define a class for User Profile Management
class UserProfile:
    def __init__(self, name: str, email: str, skills: List[str], interests: List[str], past_projects: List[str]):
        """
        Initialize a user profile with name, email, skills, interests, and past projects.
        
        Args:
        name (str): The user's name.
        email (str): The user's email address.
        skills (List[str]): A list of the user's skills.
        interests (List[str]): A list of the user's interests.
        past_projects (List[str]): A list of the user's past projects.
        """
        self.name = name
        self.email = email
        self.skills = skills
        self.interests = interests
        self.past_projects = past_projects

    def edit_profile(self, name: str = None, email: str = None, skills: List[str] = None, interests: List[str] = None, past_projects: List[str] = None):
        """
        Edit a user's profile information.
        
        Args:
        name (str): The new name for the user.
        email (str): The new email address for the user.
        skills (List[str]): The new list of skills for the user.
        interests (List[str]): The new list of interests for the user.
        past_projects (List[str]): The new list of past projects for the user.
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
class Project:
    def __init__(self, title: str, description: str, required_skills: List[str], team_members: List[str] = None):
        """
        Initialize a project with title, description, required skills, and team members.
        
        Args:
        title (str): The project title.
        description (str): The project description.
        required_skills (List[str]): A list of required skills for the project.
        team_members (List[str]): A list of team members for the project.
        """
        self.title = title
        self.description = description
        self.required_skills = required_skills
        self.team_members = team_members if team_members else []

    def add_team_member(self, team_member: str):
        """
        Add a team member to the project.
        
        Args:
        team_member (str): The team member to add.
        """
        self.team_members.append(team_member)

    def remove_team_member(self, team_member: str):
        """
        Remove a team member from the project.
        
        Args:
        team_member (str): The team member to remove.
        """
        if team_member in self.team_members:
            self.team_members.remove(team_member)

# Define a class for Search and Matching
class SearchAndMatch:def search_projects(self, skills: List[str], interests: List[str]) -> List[Project]:def suggest_project_matches(self, user: UserProfile) -> List[Project]:
    # Assign weights to each skill and interest
    skill_weights = {skill: 1 for skill in user.skills}
    interest_weights = {interest: 1 for interest in user.interests}
    past_project_weights = {project: 1 for project in user.past_projects}
    
    # Initialize a dictionary to store the scores for each project
    project_scores = {}
    
    # Iterate over each project
    for project in self.projects:
        # Initialize the score for the current project to 0
        project_scores[project] = 0
        
        # Iterate over each required skill for the project
        for required_skill in project.required_skills:
            # If the user has the required skill, add the weight to the project's score
            if required_skill in skill_weights:
                project_scores[project] += skill_weights[required_skill]
        
        # Iterate over each interest
        for interest in user.interests:
            # If the project's description contains the interest, add the weight to the project's score
            if interest in project.description:
                project_scores[project] += interest_weights[interest]
        
        # Iterate over each past project
        for past_project in user.past_projects:
            # If the project's title contains the past project, add the weight to the project's score
            if past_project in project.title:
                project_scores[project] += past_project_weights[past_project]
    
    # Sort the projects by their scores in descending order and return the top matches
    return sorted(project_scores, key=project_scores.get, reverse=True)class CollaborationTools:class SearchAndMatch:
    def __init__(self, users: List[UserProfile], projects: List[Project]):
        self.users = users
        self.projects = projects

    def search_projects(self, skills: List[str], interests: List[str]) -> List[Project]:
        matching_projects = []
        for project in self.projects:
            if any(skill in project.required_skills for skill in skills) or any(interest in project.description for interest in interests):
                matching_projects.append(project)
        return matching_projects    def __init__(self, users: List[UserProfile], projects: List[Project]):
        self.users = users
        self.projects = projects

    def search_projects(self, skills: List[str], interests: List[str]) -> List[Project]:
        # Implement the search logic here
        pass

    def suggest_project_matches(self, user: UserProfile) -> List[Project]:
        # Implement the suggest project matches logic here
        passdef test_user_profile_creation():
    user = UserProfile("John Doe", "john@example.com", ["Python", "Java"], ["Machine Learning", "Web Development"], ["Project 1", "Project 2"])
    assert user.name == "John Doe"
    assert user.email == "john@example.com"
    assert user.skills == ["Python", "Java"]
    assert user.interests == ["Machine Learning", "Web Development"]
    assert user.past_projects == ["Project 1", "Project 2"]

def test_project_creation():
    project = Project("Project 1", "This is a project", ["Python", "Java"])
    assert project.title == "Project 1"
    assert project.description == "This is a project"
    assert project.required_skills == ["Python", "Java"]

def test_search_and_match():
    users = [UserProfile("John Doe", "john@example.com", ["Python", "Java"], ["Machine Learning", "Web Development"], ["Project 1", "Project 2"])]
    projects = [Project("Project 1", "This is a project", ["Python", "Java"])]
    search_and_match = SearchAndMatch(users, projects)
    matching_projects = search_and_match.search_projects(["Python", "Java"], ["Machine Learning", "Web Development"])
    assert len(matching_projects) == 1

def test_collaboration_tools():
    project = Project("Project 1", "This is a project", ["Python", "Java"])
    collaboration_tools = CollaborationTools(project)
    collaboration_tools.send_message("Hello, team!", "John Doe")
    assert len(collaboration_tools.messages) == 1
    collaboration_tools.add_code("print('Hello, world!')", "hello.py")
    assert len(collaboration_tools.code_repository) == 1
    collaboration_tools.add_task("Task 1", "John Doe")
    assert len(collaboration_tools.task_management_board) == 1

# Run test cases
test_user_profile_creation()
test_project_creation()
test_search_and_match()
test_collaboration_tools()

# Example usage
if __name__ == "__main__":
    user = UserProfile("John Doe", "john@example.com", ["Python", "Java"], ["Machine Learning", "Web Development"], ["Project 1", "Project 2"])
    project = Project("Project 1", "This is a project", ["Python", "Java"])
    search_and_match = SearchAndMatch([user], [project])
    matching_projects = search_and_match.search_projects(["Python", "Java"], ["Machine Learning", "Web Development"])
    print("Matching projects:")
    for project in matching_projects:
        print(project.title)
    collaboration_tools = CollaborationTools(project)
    collaboration_tools.send_message("Hello, team!", "John Doe")
    print("Messages:")
    for message in collaboration_tools.messages:
        print(f"{message[0]}: {message[1]}")
    collaboration_tools.add_code("print('Hello, world!')", "hello.py")
    print("Code repository:")
    for filename, code in collaboration_tools.code_repository.items():
        print(f"{filename}: {code}")
    collaboration_tools.add_task("Task 1", "John Doe")
    print("Task management board:")
    for task, assignee in collaboration_tools.task_management_board.items():
        print(f"{task}: {assignee}")