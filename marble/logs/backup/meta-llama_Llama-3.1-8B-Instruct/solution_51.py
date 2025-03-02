
from bcrypt import checkpw
def login_user(self, username, password):
    for user in self.users.values():
        if user.username == username and checkpw(password.encode(), user.password):
            return user
    return None# user.py
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
    def __init__(self, id, name, owner_id):
        self.id = id
        self.name = name
        self.owner_id = owner_id
        self.users = []
        self.image = None

    def add_user(self, user):
        self.users.append(user)

    def remove_user(self, user):
        self.users.remove(user)

    def __str__(self):
        return f"Project(id={self.id}, name='{self.name}', owner_id={self.owner_id})"


# image.py
class Image:
    def __init__(self, id, data):
        self.id = id
        self.data = data

    def __str__(self):
        return f"Image(id={self.id}, data={self.data})"


# solution.py
import hashlib
import uuid
from user import User
from project import Project
from image import Image

class PhotoCollab:
    def __init__(self):
        self.users = {}
        self.projects = {}
        self.images = {}

    def create_user(self, username, email, password):
        # Hash the password for security
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user_id = str(uuid.uuid4())
        self.users[user_id] = User(user_id, username, email, hashed_password)
        return self.users[user_id]

    def login_user(self, username, password):
        for user in self.users.values():from bcrypt import hashpw, gensalt
hashed_password = hashpw(password.encode(), gensalt())return user
        return None

    def create_project(self, name, owner_id):
        project_id = str(uuid.uuid4())
        self.projects[project_id] = Project(project_id, name, owner_id)
        return self.projects[project_id]

    def add_user_to_project(self, project_id, user_id):
        project = self.projects.get(project_id)
        if project:
            project.add_user(self.users.get(user_id))

    def remove_user_from_project(self, project_id, user_id):
        project = self.projects.get(project_id)
        if project:
            project.remove_user(self.users.get(user_id))

    def create_image(self, data):
        image_id = str(uuid.uuid4())
        self.images[image_id] = Image(image_id, data)
        return self.images[image_id]

    def add_image_to_project(self, project_id, image_id):
        project = self.projects.get(project_id)
        if project:
            project.image = self.images.get(image_id)

    def edit_image(self, image_id, data):
        image = self.images.get(image_id)
        if image:
            image.data = data

    def get_project_image(self, project_id):
        project = self.projects.get(project_id)
        if project:
            return project.image

    def get_project_users(self, project_id):
        project = self.projects.get(project_id)
        if project:
            return project.users

# Usage
collab = PhotoCollab()

# Create users
user1 = collab.create_user("john", "john@example.com", "password123")
user2 = collab.create_user("jane", "jane@example.com", "password456")

# Create project
project = collab.create_project("My Project", user1.id)

# Add users to project
collab.add_user_to_project(project.id, user1.id)
collab.add_user_to_project(project.id, user2.id)

# Create image
image = collab.create_image("image_data")

# Add image to project
collab.add_image_to_project(project.id, image.id)

# Edit image
collab.edit_image(image.id, "new_image_data")

# Get project image
project_image = collab.get_project_image(project.id)
print(project_image)

# Get project users
project_users = collab.get_project_users(project.id)
for user in project_users:
    print(user)