# solution.py

# CollaborateCraft: A social networking application for coding project collaboration

class UserProfile:
    """Class to manage user profiles in the CollaborateCraft application."""
    
    def __init__(self, username, email, skills=None, interests=None, projects=None):
        """Initialize a user profile with basic details."""
        self.username = username
        self.email = email
        self.skills = skills if skills else []
        self.interests = interests if interests else []
        self.projects = projects if projects else []

    def update_profile(self, skills=None, interests=None):
        """Update user skills and interests."""
        if skills:
            self.skills = skills
        if interests:
            self.interests = interests

    def add_project(self, project):
        """Add a project to the user's profile."""
        self.projects.append(project)

    def __str__(self):
        """Return a string representation of the user profile."""
        return f"UserProfile(username={self.username}, email={self.email}, skills={self.skills}, interests={self.interests}, projects={self.projects})"


class Project:
    """Class to manage projects in the CollaborateCraft application."""
    
    def __init__(self, title, description, required_skills):
        """Initialize a project with title, description, and required skills."""
        self.title = title
        self.description = description
        self.required_skills = required_skills
        self.team_members = []
        self.milestones = []

    def add_team_member(self, user):
        """Add a user to the project team."""
        self.team_members.append(user)

    def remove_team_member(self, user):
        """Remove a user from the project team."""
        self.team_members.remove(user)

    def set_milestone(self, milestone):
        """Set a milestone for the project."""
        self.milestones.append(milestone)

    def __str__(self):
        """Return a string representation of the project."""
        return f"Project(title={self.title}, description={self.description}, required_skills={self.required_skills}, team_members={self.team_members}, milestones={self.milestones})"


class CollaborateCraft:
    """Main class to manage the CollaborateCraft application."""
    
    def __init__(self):
        """Initialize the application with empty user and project lists."""
        self.users = []
        self.projects = []

    def create_user(self, username, email, skills=None, interests=None):
        """Create a new user profile."""
        user = UserProfile(username, email, skills, interests)
        self.users.append(user)
        return user

    def create_project(self, title, description, required_skills):
        """Create a new project."""
        project = Project(title, description, required_skills)
        self.projects.append(project)
        return project

    def search_users(self, skill=None, interest=None):
        """Search for users based on skills or interests."""
        results = []
        for user in self.users:
            if (skill and skill in user.skills) or (interest and interest in user.interests):
                results.append(user)
        return results

    def search_projects(self, required_skill=None):
        """Search for projects based on required skills."""
        results = []
        for project in self.projects:
            if required_skill and required_skill in project.required_skills:
                results.append(project)
        return results

    def match_projects(self, user):
        """Suggest projects based on user's skills."""
        matched_projects = []
        for project in self.projects:
            if any(skill in project.required_skills for skill in user.skills):
                matched_projects.append(project)
        return matched_projects


# Test cases for the application
def test_collaborate_craft():
    """Run test cases for the CollaborateCraft application."""
    app = CollaborateCraft()

    # Test user profile creation
    user1 = app.create_user("alice", "alice@example.com", skills=["Python", "Django"], interests=["AI", "Web Development"])
    user2 = app.create_user("bob", "bob@example.com", skills=["JavaScript", "React"], interests=["Web Development"])

    assert user1.username == "alice"
    assert user2.email == "bob@example.com"

    # Test project creation
    project1 = app.create_project("AI Research", "Research on AI algorithms", required_skills=["Python", "Machine Learning"])
    project2 = app.create_project("Web App", "Develop a web application", required_skills=["JavaScript", "React"])

    assert project1.title == "AI Research"
    assert project2.description == "Develop a web application"

    # Test user search
    found_users = app.search_users(skill="Python")
    assert len(found_users) == 1 and found_users[0].username == "alice"

    # Test project search
    found_projects = app.search_projects(required_skill="React")
    assert len(found_projects) == 1 and found_projects[0].title == "Web App"

    # Test project matching
    matched_projects = app.match_projects(user1)
    assert len(matched_projects) == 0  # Alice has no matching projects

    matched_projects = app.match_projects(user2)
    assert len(matched_projects) == 1 and matched_projects[0].title == "Web App"

# Run the test cases
if __name__ == "__main__":
    test_collaborate_craft()
    print("All tests passed!")