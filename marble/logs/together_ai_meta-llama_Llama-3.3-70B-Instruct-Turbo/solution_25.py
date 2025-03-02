# solution.py
import hashlib
import datetime
import unittest

# User class to store user information
class User:
    def __init__(self, username, password):
        # Hash the password for secure storage
        self.username = username
        self.password = self._hash_password(password)
        self.groups = []

    def _hash_password(self, password):
        # Use SHA-256 hashing for password security
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        # Check if the provided password matches the stored hash
        return self.password == self._hash_password(password)

# Group class to store group information
class Group:
    def __init__(self, name, goal, deadline):
        self.name = name
        self.goal = goal
        self.deadline = deadline
        self.contributions = {}
        self.members = []

    def add_member(self, user):
        # Add a user to the group
        self.members.append(user)
        user.groups.append(self)

    def contribute(self, user, amount):
        # Record a contribution from a user
        if user in self.members:logging.error("User is not a member of this group")
return {"error": "User is not a member of this group"}else:
                self.contributions[user] = amount
        else:
            raise ValueError("User is not a member of this group")

    def get_progress(self):
        # Calculate the total amount saved and the remaining amount needed
        total_saved = sum(self.contributions.values())
        remaining = self.goal - total_saved
        return total_saved, remaining

# Notification class to store notification information
class Notification:
    def __init__(self, message, deadline):
        self.message = message
        self.deadline = deadline

    def is_overdue(self):
        # Check if the notification is overdue
        return datetime.datetime.now() > self.deadline

# Chat class to store chat messages
class Chat:
    def __init__(self):
        self.messages = []

    def send_message(self, user, message):
        # Record a chat message from a user
        self.messages.append((user, message))

# FinancialCollaborator class to manage the system
class FinancialCollaborator:
    def __init__(self):
        self.users = {}
        self.groups = {}
        self.notifications = []
        self.chat = Chat()

    def create_user(self, username, password):
import logging
logging.basicConfig(level=logging.INFO)

        # Create a new user account
        if username not in self.users:logging.error("Username already exists")
return {"error": "Username already exists"}else:
            raise ValueError("Username already exists")

    def login(self, username, password):
        # Log in to an existing user account
        if username in self.users:
            if self.users[username].check_password(password):
                return self.users[username]
            else:
                raise ValueError("Incorrect password")
        else:
            raise ValueError("Username does not exist")

    def create_group(self, name, goal, deadline):
        # Create a new group
        if name not in self.groups:logging.error("Group name already exists")
return {"error": "Group name already exists"}else:
            raise ValueError("Group name already exists")

    def join_group(self, user, group_name):
        # Add a user to a group
        if group_name in self.groups:logging.error("Group does not exist")
return {"error": "Group does not exist"}else:
            raise ValueError("Group does not exist")

    def contribute(self, user, group_name, amount):
        # Record a contribution from a user to a group
        if group_name in self.groups:
            self.groups[group_name].contribute(user, amount)
        else:
            raise ValueError("Group does not exist")

    def get_progress(self, group_name):
        # Get the progress of a group
        if group_name in self.groups:
            return self.groups[group_name].get_progress()
        else:
            raise ValueError("Group does not exist")

    def send_notification(self, message, deadline):
        # Send a notification to all users
        self.notifications.append(Notification(message, deadline))

    def send_message(self, user, message):
        # Send a chat message from a user
        self.chat.send_message(user, message)

# Test cases
class TestFinancialCollaborator(unittest.TestCase):
    def test_user_creation(self):
        collaborator = FinancialCollaborator()try:
    collaborator.create_group("group1", 100, datetime.datetime.now())try:
    collaborator.join_group(user, "group1")try:
    collaborator.contribute(user, "group1", 50)try:
    total_saved, remaining = collaborator.get_progress("group1")
except ValueError as e:
    print(f"Error getting group progress: {e}")self.assertEqual(total_saved, 50)
        self.assertEqual(remaining, 50)

    def test_send_notification(self):
        collaborator = FinancialCollaborator()
        collaborator.send_notification("Hello, world!", datetime.datetime.now())
        self.assertEqual(len(collaborator.notifications), 1)

    def test_send_message(self):
        collaborator = FinancialCollaborator()
        collaborator.create_user("user1", "password1")
        user = collaborator.login("user1", "password1")
        collaborator.send_message(user, "Hello, world!")
        self.assertEqual(len(collaborator.chat.messages), 1)

if __name__ == "__main__":
    unittest.main()