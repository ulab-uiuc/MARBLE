# user.py
class User:
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    def __str__(self):
        return f"User(id={self.id}, username='{self.username}', email='{self.email}')"


# project.py
class Project:
    def __init__(self, id, name, image_url, owner_id):
        self.id = id
        self.name = name
        self.image_url = image_url
        self.owner_id = owner_id
        self.collaborators = []
        self.edits = []

    def add_collaborator(self, user):
        self.collaborators.append(user)

    def add_edit(self, edit):
        self.edits.append(edit)

    def __str__(self):
        return f"Project(id={self.id}, name='{self.name}', image_url='{self.image_url}')"


# edit.py
class Edit:
    def __init__(self, id, project_id, user_id, edit_type, edit_data):
        self.id = id
        self.project_id = project_id
        self.user_id = user_id
        self.edit_type = edit_type
        self.edit_data = edit_data

    def __str__(self):
        return f"Edit(id={self.id}, project_id={self.project_id}, user_id={self.user_id}, edit_type='{self.edit_type}')"


# solution.py
import uuid
import hashlib
import datetime

class PhotoCollab:
    def __init__(self):
        self.users = {}
        self.projects = {}

    def create_user(self, username, email, password):
        # Hash the password for security
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user_id = str(uuid.uuid4())
        self.users[user_id] = User(user_id, username, email, hashed_password)
        return self.users[user_id]

    def login_user(self, username, password):
        for user in self.users.values():
            if user.username == username and user.password == hashlib.sha256(password.encode()).hexdigest():
                return user
        return None

    def create_project(self, name, image_url, owner_id):
        project_id = str(uuid.uuid4())
        project = Project(project_id, name, image_url, owner_id)
        self.projects[project_id] = project
        return project

    def add_collaborator(self, project_id, user_id):
        project = self.projects.get(project_id)
        if project:
            project.add_collaborator(self.users.get(user_id))

    def add_edit(self, project_id, user_id, edit_type, edit_data):
        project = self.projects.get(project_id)
        if project:
            edit = Edit(str(uuid.uuid4()), project_id, user_id, edit_type, edit_data)
            project.add_edit(edit)

    def get_project_edits(self, project_id):
        project = self.projects.get(project_id)
        if project:
            return project.edits
        return []

    def get_project_collaborators(self, project_id):
        project = self.projects.get(project_id)
        if project:
            return project.collaborators
        return []

# Usage
photo_collab = PhotoCollab()

# Create users
user1 = photo_collab.create_user("john", "john@example.com", "password123")
user2 = photo_collab.create_user("jane", "jane@example.com", "password456")

# Create project
project = photo_collab.create_project("My Project", "https://example.com/image.jpg", user1.id)

# Add collaborators
photo_collab.add_collaborator(project.id, user2.id)

# Add edits
photo_collab.add_edit(project.id, user1.id, "brightness", 50)
photo_collab.add_edit(project.id, user2.id, "contrast", 75)

# Get project edits and collaborators
edits = photo_collab.get_project_edits(project.id)
collaborators = photo_collab.get_project_collaborators(project.id)

print("Project Edits:")
for edit in edits:
    print(edit)

print("\nProject Collaborators:")
for collaborator in collaborators:
    print(collaborator)