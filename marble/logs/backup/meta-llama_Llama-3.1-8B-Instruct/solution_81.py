# solution.py

# Importing required libraries
import datetime
import random

# User class to store user information
class User:
    def __init__(self, id, name, skills, interests, availability):
        self.id = id
        self.name = name
        self.skills = skills
        self.interests = interests
        self.availability = availability
        self.reputation = 0
        self.contributions = []

# Project class to store project information
class Project:
    def __init__(self, id, name, description, team):
        self.id = id
        self.name = name
        self.description = description
        self.team = team
        self.tasks = []
        self.deadlines = {}

# Task class to store task information
class Task:
    def __init__(self, id, name, description, deadline, assigned_to):
        self.id = id
        self.name = name
        self.description = description
        self.deadline = deadline
        self.assigned_to = assigned_to
        self.status = "Not Started"

# Messaging system class to handle messages
class MessagingSystem:
    def __init__(self):
        self.messages = {}

    def send_message(self, sender, recipient, message):
        if recipient in self.messages:
            self.messages[recipient].append((sender, message))
        else:
            self.messages[recipient] = [(sender, message)]

    def get_messages(self, recipient):
        return self.messages.get(recipient, [])

# Feedback system class to handle feedback
class FeedbackSystem:
    def __init__(self):
        self.feedback = {}

    def give_feedback(self, giver, receiver, rating, comment):
        if receiver in self.feedback:
            self.feedback[receiver].append((giver, rating, comment))
        else:
            self.feedback[receiver] = [(giver, rating, comment)]

    def get_feedback(self, receiver):
        return self.feedback.get(receiver, [])

# CollaborativeProjectHub class to manage the system
class CollaborativeProjectHub:
    def __init__(self):
        self.users = {}
        self.projects = {}
        self.messaging_system = MessagingSystem()
        self.feedback_system = FeedbackSystem()

    def create_user(self, id, name, skills, interests, availability):
        self.users[id] = User(id, name, skills, interests, availability)

    def create_project(self, id, name, description, team):
        self.projects[id] = Project(id, name, description, team)

    def add_task(self, project_id, task):
        self.projects[project_id].tasks.append(task)

    def assign_task(self, project_id, task_id, user_id):
        task = self.projects[project_id].tasks[task_id]
        task.assigned_to = user_id

    def send_message(self, sender_id, recipient_id, message):
        self.messaging_system.send_message(self.users[sender_id], self.users[recipient_id], message)

    def give_feedback(self, giver_id, receiver_id, rating, comment):
        self.feedback_system.give_feedback(self.users[giver_id], self.users[receiver_id], rating, comment)

    def get_messages(self, user_id):
        return self.messaging_system.get_messages(self.users[user_id])

    def get_feedback(self, user_id):
        return self.feedback_system.get_feedback(self.users[user_id])

# Example usage
hub = CollaborativeProjectHub()

# Create users
hub.create_user(1, "John Doe", ["Python", "JavaScript"], ["Machine Learning", "Data Science"], "Available")
hub.create_user(2, "Jane Doe", ["Java", "C++"], ["Web Development", "Mobile App Development"], "Available")

# Create project
hub.create_project(1, "Machine Learning Project", "A project to develop a machine learning model", [1, 2])

# Add tasks
task1 = Task(1, "Task 1", "Develop a machine learning model", datetime.date(2024, 7, 31), None)
task2 = Task(2, "Task 2", "Train the model", datetime.date(2024, 8, 15), None)
hub.add_task(1, task1)
hub.add_task(1, task2)

# Assign tasks
hub.assign_task(1, 1, 1)
hub.assign_task(1, 2, 2)

# Send messages
hub.send_message(1, 2, "Hello, let's work on the project!")
hub.send_message(2, 1, "Hi, I'm ready to start working on the project!")

# Give feedback
hub.give_feedback(1, 2, 5, "Great job on the project!")
hub.give_feedback(2, 1, 5, "Great job on the project!")

# Get messages and feedback
print("Messages:")
for message in hub.get_messages(1):
    print(f"{message[0].name}: {message[1]}")
print("\nFeedback:")
for feedback in hub.get_feedback(1):
    print(f"{feedback[0].name}: {feedback[1]}/5 - {feedback[2]}")