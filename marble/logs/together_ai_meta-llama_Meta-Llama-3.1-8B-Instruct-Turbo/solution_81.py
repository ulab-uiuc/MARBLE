# solution.py

# Importing necessary libraries
import datetime
import random

# User class representing a user in the system
class User:
    def __init__(self, name, skills, interests, availability):
        self.name = name
        self.skills = skills
        self.interests = interests
        self.availability = availability
        self.reputation = 0
        self.contributions = []

# Project class representing a project in the system
class Project:
    def __init__(self, name, description, team):
        self.name = name
        self.description = description
        self.team = team
        self.tasks = []
        self.deadlines = {}

# Task class representing a task in the system
class Task:
    def __init__(self, name, description, deadline, assignee):
        self.name = name
        self.description = description
        self.deadline = deadline
        self.assignee = assignee
        self.status = "pending"

# Messaging system class
class MessagingSystem:
    def __init__(self):
        self.messages = {}

    def send_message(self, sender, recipient, message):
        if recipient not in self.messages:
            self.messages[recipient] = []
        self.messages[recipient].append((sender, message))

    def get_messages(self, recipient):
        return self.messages.get(recipient, [])

# Feedback system class
class FeedbackSystem:
    def __init__(self):
        self.reviews = {}

    def rate_contribution(self, reviewer, contributor, rating):
        if contributor not in self.reviews:
            self.reviews[contributor] = []
        self.reviews[contributor].append((reviewer, rating))

    def get_reviews(self, contributor):
        return self.reviews.get(contributor, [])

# CollaborativeProjectHub class
class CollaborativeProjectHub:
    def __init__(self):
        self.users = {}
        self.projects = {}
        self.messaging_system = MessagingSystem()
        self.feedback_system = FeedbackSystem()

    def create_user(self, name, skills, interests, availability):
        self.users[name] = User(name, skills, interests, availability)

    def create_project(self, name, description, team):
        self.projects[name] = Project(name, description, team)

    def propose_project_idea(self, project_name, project_description, proposer):
        if project_name not in self.projects:
            self.projects[project_name] = Project(project_name, project_description, [proposer])
            print(f"Project '{project_name}' proposed by {proposer}.")

    def join_project(self, project_name, user_name):
        if project_name in self.projects:
            self.projects[project_name].team.append(user_name)
            print(f"{user_name} joined project '{project_name}'.")

    def assign_task(self, project_name, task_name, assignee):
        if project_name in self.projects and task_name not in self.projects[project_name].tasks:
            self.projects[project_name].tasks.append(Task(task_name, "", datetime.date.today() + datetime.timedelta(days=7), assignee))
            print(f"Task '{task_name}' assigned to {assignee} in project '{project_name}'.")

    def send_message(self, sender, recipient, message):
        self.messaging_system.send_message(sender, recipient, message)

    def rate_contribution(self, reviewer, contributor, rating):
        self.feedback_system.rate_contribution(reviewer, contributor, rating)

    def get_feedback(self, contributor):
        return self.feedback_system.get_reviews(contributor)

# Example usage
hub = CollaborativeProjectHub()

# Create users
hub.create_user("John", ["Python", "JavaScript"], ["Web Development", "Machine Learning"], "Available")
hub.create_user("Jane", ["Java", "C++"], ["Mobile App Development", "Data Science"], "Available")

# Create project
hub.create_project("Project A", "A web development project", ["John", "Jane"])

# Propose project idea
hub.propose_project_idea("Project A", "A web development project", "John")

# Join project
hub.join_project("Project A", "Jane")

# Assign task
hub.assign_task("Project A", "Task 1", "John")

# Send message
hub.send_message("John", "Jane", "Hello, Jane!")

# Rate contribution
hub.rate_contribution("Jane", "John", 5)

# Get feedback
print(hub.get_feedback("John"))