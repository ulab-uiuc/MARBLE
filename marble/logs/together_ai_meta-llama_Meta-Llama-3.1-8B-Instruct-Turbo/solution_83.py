# user.py
class User:
    def __init__(self, id, name, email, skills, interests, past_projects):
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
    def __init__(self, id, title, description, required_skills, team_members):
        self.id = id
        self.title = title
        self.description = description
        self.required_skills = required_skills
        self.team_members = team_members
        self.milestones = []

    def add_milestone(self, milestone):
        self.milestones.append(milestone)

    def __str__(self):
        return f"Project {self.title} ({self.id})"


# milestone.py
class Milestone:
    def __init__(self, id, title, description, deadline):
        self.id = id
        self.title = title
        self.description = description
        self.deadline = deadline

    def __str__(self):
        return f"Milestone {self.title} ({self.id})"


# message.py
class Message:
    def __init__(self, id, sender, recipient, content):
        self.id = id
        self.sender = sender
        self.recipient = recipient
        self.content = content

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient}: {self.content}"


# repository.py
class Repository:
    def __init__(self, id, project):
        self.id = id
        self.project = project
        self.files = []

    def add_file(self, file):
        self.files.append(file)

    def __str__(self):
        return f"Repository for project {self.project.title} ({self.id})"


# file.py
class File:
    def __init__(self, id, name, content):
        self.id = id
        self.name = name
        self.content = content

    def __str__(self):
        return f"File {self.name} ({self.id})"


# task.py
class Task:
    def __init__(self, id, title, description, deadline):
        self.id = id
        self.title = title
        self.description = description
        self.deadline = deadline

    def __str__(self):
        return f"Task {self.title} ({self.id})"


# solution.py
class CollaborateCraft:
    def __init__(self):
        self.users = []
        self.projects = []
        self.repositories = []
        self.messages = []
        self.tasks = []

    def create_user(self, id, name, email, skills, interests, past_projects):
        user = User(id, name, email, skills, interests, past_projects)
        self.users.append(user)
        return user

    def create_project(self, id, title, description, required_skills, team_members):
        project = Project(id, title, description, required_skills, team_members)
        self.projects.append(project)
        return project

    def create_repository(self, id, project):
        repository = Repository(id, project)
        self.repositories.append(repository)
        return repository

    def create_message(self, id, sender, recipient, content):
        message = Message(id, sender, recipient, content)
        self.messages.append(message)
        return message

    def create_task(self, id, title, description, deadline):
        task = Task(id, title, description, deadline)
        self.tasks.append(task)
        return task

    def search_users(self, skills, interests):
        matching_users = []
        for user in self.users:
            if skills.issubset(user.skills) and interests.issubset(user.interests):
                matching_users.append(user)
        return matching_users

    def search_projects(self, required_skills, team_members):
        matching_projects = []
        for project in self.projects:
            if required_skills.issubset(project.required_skills) and team_members.issubset(project.team_members):
                matching_projects.append(project)
        return matching_projects

    def match_users_with_projects(self, users, projects):
        matches = []
        for user in users:
            for project in projects:
                if user.skills.issubset(project.required_skills) and user.interests.issubset(project.required_skills):
                    matches.append((user, project))
        return matches

    def display_user_profile(self, user):
        print(f"User Profile: {user}")
        print(f"Skills: {user.skills}")
        print(f"Interests: {user.interests}")
        print(f"Past Projects: {user.past_projects}")

    def display_project_details(self, project):
        print(f"Project Details: {project}")
        print(f"Title: {project.title}")
        print(f"Description: {project.description}")
        print(f"Required Skills: {project.required_skills}")
        print(f"Team Members: {project.team_members}")
        print(f"Milestones: {project.milestones}")

    def display_repository_files(self, repository):
        print(f"Repository Files: {repository}")
        for file in repository.files:
            print(f"File: {file}")

    def display_message(self, message):
        print(f"Message: {message}")

    def display_task(self, task):
        print(f"Task: {task}")


# main.py
def main():
    collaborate_craft = CollaborateCraft()

    # Create users
    user1 = collaborate_craft.create_user(1, "John Doe", "john@example.com", ["Python", "Java"], ["Machine Learning", "Data Science"], ["Project 1", "Project 2"])
    user2 = collaborate_craft.create_user(2, "Jane Doe", "jane@example.com", ["Python", "JavaScript"], ["Web Development", "Mobile App Development"], ["Project 3", "Project 4"])

    # Create projects
    project1 = collaborate_craft.create_project(1, "Project 1", "This is a project about machine learning.", ["Python", "Java"], [user1, user2])
    project2 = collaborate_craft.create_project(2, "Project 2", "This is a project about data science.", ["Python", "R"], [user1, user2])

    # Create repositories
    repository1 = collaborate_craft.create_repository(1, project1)
    repository2 = collaborate_craft.create_repository(2, project2)

    # Create messages
    message1 = collaborate_craft.create_message(1, user1, user2, "Hello, Jane!")
    message2 = collaborate_craft.create_message(2, user2, user1, "Hi, John!")

    # Create tasks
    task1 = collaborate_craft.create_task(1, "Task 1", "This is a task about machine learning.", "2024-02-15")
    task2 = collaborate_craft.create_task(2, "Task 2", "This is a task about data science.", "2024-02-16")

    # Display user profiles
    collaborate_craft.display_user_profile(user1)
    collaborate_craft.display_user_profile(user2)

    # Display project details
    collaborate_craft.display_project_details(project1)
    collaborate_craft.display_project_details(project2)

    # Display repository files
    collaborate_craft.display_repository_files(repository1)
    collaborate_craft.display_repository_files(repository2)

    # Display messages
    collaborate_craft.display_message(message1)
    collaborate_craft.display_message(message2)

    # Display tasks
    collaborate_craft.display_task(task1)
    collaborate_craft.display_task(task2)


if __name__ == "__main__":
    main()