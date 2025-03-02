# user.py
class User:
    def __init__(self, id, name, email, skills, interests, past_projects):
        """
        Initialize a User object.

        Args:
            id (int): Unique user ID.
            name (str): User name.
            email (str): User email.
            skills (list): List of user skills.
            interests (list): List of user interests.
            past_projects (list): List of user past projects.
        """
        self.id = id
        self.name = name
        self.email = email
        self.skills = skills
        self.interests = interests
        self.past_projects = past_projects

    def __str__(self):
        return f"User {self.name} ({self.email})"


# project.py
class Project:
    def __init__(self, id, title, description, required_skills, team_members, milestones):
        """
        Initialize a Project object.

        Args:
            id (int): Unique project ID.
            title (str): Project title.
            description (str): Project description.
            required_skills (list): List of required skills for the project.
            team_members (list): List of team members for the project.
            milestones (list): List of project milestones.
        """
        self.id = id
        self.title = title
        self.description = description
        self.required_skills = required_skills
        self.team_members = team_members
        self.milestones = milestones

    def __str__(self):
        return f"Project {self.title} ({self.id})"


# user_profile_manager.py
class UserProfileManager:
    def __init__(self):
        """
        Initialize a UserProfileManager object.
        """
        self.users = {}

    def create_user(self, id, name, email, skills, interests, past_projects):
        """
        Create a new user profile.

        Args:
            id (int): Unique user ID.
            name (str): User name.
            email (str): User email.
            skills (list): List of user skills.
            interests (list): List of user interests.
            past_projects (list): List of user past projects.

        Returns:
            User: The created user object.
        """
        if id in self.users:
            raise ValueError("User ID already exists")
        self.users[id] = User(id, name, email, skills, interests, past_projects)
        return self.users[id]

    def get_user(self, id):
        """
        Get a user profile by ID.

        Args:
            id (int): Unique user ID.

        Returns:
            User: The user object if found, otherwise None.
        """
        return self.users.get(id)

    def update_user(self, id, name=None, email=None, skills=None, interests=None, past_projects=None):
        """
        Update a user profile.

        Args:
            id (int): Unique user ID.
            name (str, optional): User name. Defaults to None.
            email (str, optional): User email. Defaults to None.
            skills (list, optional): List of user skills. Defaults to None.
            interests (list, optional): List of user interests. Defaults to None.
            past_projects (list, optional): List of user past projects. Defaults to None.
        """
        user = self.get_user(id)
        if user:
            if name:
                user.name = name
            if email:
                user.email = email
            if skills:
                user.skills = skills
            if interests:
                user.interests = interests
            if past_projects:
                user.past_projects = past_projects


# project_manager.py
class ProjectManager:
    def __init__(self):
        """
        Initialize a ProjectManager object.
        """
        self.projects = {}

    def create_project(self, id, title, description, required_skills, team_members, milestones):
        """
        Create a new project.

        Args:
            id (int): Unique project ID.
            title (str): Project title.
            description (str): Project description.
            required_skills (list): List of required skills for the project.
            team_members (list): List of team members for the project.
            milestones (list): List of project milestones.

        Returns:
            Project: The created project object.
        """
        if id in self.projects:
            raise ValueError("Project ID already exists")
        self.projects[id] = Project(id, title, description, required_skills, team_members, milestones)
        return self.projects[id]

    def get_project(self, id):
        """
        Get a project by ID.

        Args:
            id (int): Unique project ID.

        Returns:
            Project: The project object if found, otherwise None.
        """
        return self.projects.get(id)

    def update_project(self, id, title=None, description=None, required_skills=None, team_members=None, milestones=None):
        """
        Update a project.

        Args:
            id (int): Unique project ID.
            title (str, optional): Project title. Defaults to None.
            description (str, optional): Project description. Defaults to None.
            required_skills (list, optional): List of required skills for the project. Defaults to None.
            team_members (list, optional): List of team members for the project. Defaults to None.
            milestones (list, optional): List of project milestones. Defaults to None.
        """
        project = self.get_project(id)
        if project:
            if title:
                project.title = title
            if description:
                project.description = description
            if required_skills:
                project.required_skills = required_skills
            if team_members:
                project.team_members = team_members
            if milestones:
                project.milestones = milestones


# search_manager.py
class SearchManager:
    def __init__(self):
        """
        Initialize a SearchManager object.
        """
        self.users = {}
        self.projects = {}

    def add_user(self, user):
        """
        Add a user to the search index.

        Args:
            user (User): The user object to add.
        """
        self.users[user.id] = user

    def add_project(self, project):
        """
        Add a project to the search index.

        Args:
            project (Project): The project object to add.
        """
        self.projects[project.id] = project

    def search_users(self, query):
        """
        Search for users based on a query.

        Args:
            query (str): The search query.

        Returns:
            list: A list of user IDs that match the query.
        """
        results = []
        for user in self.users.values():
            if query in user.name or query in user.email or query in user.skills or query in user.interests:
                results.append(user.id)
        return results

    def search_projects(self, query):
        """
        Search for projects based on a query.

        Args:
            query (str): The search query.

        Returns:
            list: A list of project IDs that match the query.
        """
        results = []
        for project in self.projects.values():
            if query in project.title or query in project.description or query in project.required_skills:
                results.append(project.id)
        return results


# collaboration_manager.py
class CollaborationManager:
    def __init__(self):
        """
        Initialize a CollaborationManager object.
        """
        self.users = {}
        self.projects = {}

    def add_user(self, user):
        """
        Add a user to the collaboration system.

        Args:
            user (User): The user object to add.
        """
        self.users[user.id] = user

    def add_project(self, project):
        """
        Add a project to the collaboration system.

        Args:
            project (Project): The project object to add.
        """
        self.projects[project.id] = project

    def send_message(self, sender_id, recipient_id, message):
        """
        Send a message between two users.

        Args:
            sender_id (int): The ID of the sender.
            recipient_id (int): The ID of the recipient.
            message (str): The message to send.
        """
        sender = self.users.get(sender_id)
        recipient = self.users.get(recipient_id)
        if sender and recipient:
            print(f"Message from {sender.name} to {recipient.name}: {message}")


# solution.py
class CollaborateCraft:
    def __init__(self):
        """
        Initialize a CollaborateCraft object.
        """
        self.user_profile_manager = UserProfileManager()
        self.project_manager = ProjectManager()
        self.search_manager = SearchManager()
        self.collaboration_manager = CollaborationManager()

    def run(self):
        """
        Run the CollaborateCraft application.
        """
        while True:
            print("CollaborateCraft Menu:")
            print("1. Create User Profile")
            print("2. Create Project")
            print("3. Search for Users or Projects")
            print("4. Send Message")
            print("5. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.create_user_profile()
            elif choice == "2":
                self.create_project()
            elif choice == "3":
                self.search_users_or_projects()
            elif choice == "4":
                self.send_message()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")

    def create_user_profile(self):
        """
        Create a new user profile.
        """
        id = int(input("Enter user ID: "))
        name = input("Enter user name: ")
        email = input("Enter user email: ")
        skills = input("Enter user skills (comma-separated): ").split(",")
        interests = input("Enter user interests (comma-separated): ").split(",")
        past_projects = input("Enter user past projects (comma-separated): ").split(",")
        user = self.user_profile_manager.create_user(id, name, email, skills, interests, past_projects)
        print(f"User profile created for {user.name}")

    def create_project(self):
        """
        Create a new project.
        """
        id = int(input("Enter project ID: "))
        title = input("Enter project title: ")
        description = input("Enter project description: ")
        required_skills = input("Enter required skills (comma-separated): ").split(",")
        team_members = input("Enter team members (comma-separated): ").split(",")
        milestones = input("Enter milestones (comma-separated): ").split(",")
        project = self.project_manager.create_project(id, title, description, required_skills, team_members, milestones)
        print(f"Project created for {project.title}")

    def search_users_or_projects(self):
        """
        Search for users or projects.
        """
        query = input("Enter search query: ")
        results = self.search_manager.search_users(query)
        if results:
            print("Search results for users:")
            for result in results:
                user = self.user_profile_manager.get_user(result)
                print(f"{user.name} ({user.email})")
        else:
            print("No search results found for users")
        results = self.search_manager.search_projects(query)
        if results:
            print("Search results for projects:")
            for result in results:
                project = self.project_manager.get_project(result)
                print(f"{project.title} ({project.id})")
        else:
            print("No search results found for projects")

    def send_message(self):
        """
        Send a message between two users.
        """
        sender_id = int(input("Enter sender ID: "))
        recipient_id = int(input("Enter recipient ID: "))
        message = input("Enter message: ")
        self.collaboration_manager.send_message(sender_id, recipient_id, message)


if __name__ == "__main__":
    app = CollaborateCraft()
    app.run()