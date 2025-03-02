# CollaborateCraft - Social Networking Application for Coding Projects

class UserProfile:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.skills = []
        self.interests = []
        self.past_projects = []

    def add_skill(self, skill):
        self.skills.append(skill)

    def add_interest(self, interest):
        self.interests.append(interest)

    def add_past_project(self, project):
        self.past_projects.append(project)

    def edit_profile(self, username=None, email=None):
        if username:
            self.username = username
        if email:
            self.email = email

class Project:
    def __init__(self, title, description, required_skills):
        self.title = title
        self.description = description
        self.required_skills = required_skills
        self.team_members = []
        self.milestones = []

    def add_team_member(self, user):def update_milestone(self, index, milestone):        if 0 <= index < len(self.milestones):    def delete_milestone(self, index):
        if 0 <= index < len(self.milestones):
    def add_milestone(self, milestone):
        self.milestones.append(milestone)
            del self.milestones[index]            del self.milestones[index]
    def add_milestone(self, milestone):
        self.milestones.append(milestone)

class CollaborateCraft:
    def __init__(self):
        self.users = {}
        self.projects = []

    def create_user_profile(self, username, email):
        if email in self.users:
            return "Email already exists. Please use a different email."
        user = UserProfile(username, email)
        self.users[email] = user
        return "User profile created successfully."

    def create_project(self, title, description, required_skills):
        project = Project(title, description, required_skills)
        self.projects.append(project)
        return "Project created successfully."

    def search_projects(self, skill):
        matched_projects = []
        for project in self.projects:
            if skill in project.required_skills:
                matched_projects.append(project)
        return matched_projects

# Test Cases
# User Profile Creation
collaborate_app = CollaborateCraft()
print(collaborate_app.create_user_profile("Alice", "alice@example.com"))  # User profile created successfully.
print(collaborate_app.create_user_profile("Bob", "alice@example.com"))  # Email already exists. Please use a different email.

# Project Creation
print(collaborate_app.create_project("Project A", "Description A", ["Python", "Django"]))  # Project created successfully.

# Search Projects
print(collaborate_app.search_projects("Python"))  # [Project object]

# Additional functionalities and test cases can be added as needed.