# solution.py
import hashlib
import datetime
import unittest

# User class to store user information
class User:
    def __init__(self, username, password):
        # Store username and hashed password
        self.username = username
        self.password = self._hash_password(password)
        self.groups = []

    def _hash_password(self, password):
        # Hash password using SHA-256
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        # Check if provided password matches the stored hash
        return self.password == self._hash_password(password)

# Group class to store group information
class Group:
    def __init__(self, name, goal, deadline):
        # Store group name, goal, and deadline
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
        if user in self.contributions:
            self.contributions[user] += amount
        else:
            self.contributions[user] = amount

    def get_progress(self):
        # Calculate the total amount saved and the remaining amount needed
        total_saved = sum(self.contributions.values())
        remaining = self.goal - total_saved
        return total_saved, remaining

# FinancialCollaborator class to manage users and groups
class FinancialCollaborator:
    def __init__(self):
        # Store users and groups
        self.users = {}
        self.groups = {}

    def create_user(self, username, password):
        # Create a new user
        if username in self.users:
            raise ValueError("Username already exists")
        self.users[username] = User(username, password)

    def login(self, username, password):
        # Login a user
        if username not in self.users:
            raise ValueError("Username does not exist")
        if not self.users[username].check_password(password):
            raise ValueError("Incorrect password")
        return self.users[username]

    def create_group(self, name, goal, deadline):
        # Create a new group
        if name in self.groups:
            raise ValueError("Group name already exists")
        self.groups[name] = Group(name, goal, deadline)
        self.groups[name].notification.send_notification(f'Group {name} created with goal {goal} and deadline {deadline}')

    def join_group(self, user, group_name):
        # Add a user to a group
        if group_name not in self.groups:
            raise ValueError("Group does not exist")
        self.groups[group_name].add_member(user)

    def contribute(self, user, group_name, amount):
        # Record a contribution from a user to a group
        if group_name not in self.groups:
            raise ValueError("Group does not exist")
        self.groups[group_name].contribute(user, amount)
        self.groups[group_name].notification.send_notification(f'{user.username} contributed {amount} to {group_name}')

    def get_progress(self, group_name):
        # Get the progress of a group
        if group_name not in self.groups:
            raise ValueError("Group does not exist")
        return self.groups[group_name].get_progress()
        total_saved, remaining = self.groups[group_name].get_progress()
        self.groups[group_name].notification.send_notification(f'Group {group_name} progress: {total_saved} saved, {remaining} remaining')

# Chat class to facilitate communication among group members
class Chat:
    def __init__(self):
    def send_message(self, group_name, user, message):
        self.groups[group_name].chat.send_message(f'{user.username}: {message}')
        self.notification = Notification()
        self.chat = Chat()
        # Store messages
        self.messages = []

    def send_message(self, message):
        # Send a message
        self.messages.append(message)

    def get_messages(self):
        # Get all messages
        return self.messages

# Notification class to send notifications and reminders
class Notification:
    def __init__(self):
        # Store notifications
        self.notifications = []

    def send_notification(self, notification):
        # Send a notification
        self.notifications.append(notification)

    def get_notifications(self):
        # Get all notifications
        return self.notifications

# Test cases
class TestFinancialCollaborator(unittest.TestCase):
    def test_user_creation(self):
        collaborator = FinancialCollaborator()
        collaborator.create_user("user1", "password1")
        self.assertIn("user1", collaborator.users)

    def test_login(self):
        collaborator = FinancialCollaborator()
        collaborator.create_user("user1", "password1")
        user = collaborator.login("user1", "password1")
        self.assertEqual(user.username, "user1")

    def test_group_creation(self):
        collaborator = FinancialCollaborator()
        collaborator.create_group("group1", 100, datetime.date(2024, 12, 31))
        self.assertIn("group1", collaborator.groups)

    def test_join_group(self):
        collaborator = FinancialCollaborator()
        collaborator.create_user("user1", "password1")
        collaborator.create_group("group1", 100, datetime.date(2024, 12, 31))
        user = collaborator.login("user1", "password1")
        collaborator.join_group(user, "group1")
        self.assertIn(user, collaborator.groups["group1"].members)

    def test_contribute(self):
        collaborator = FinancialCollaborator()
        collaborator.create_user("user1", "password1")
        collaborator.create_group("group1", 100, datetime.date(2024, 12, 31))
        user = collaborator.login("user1", "password1")
        collaborator.join_group(user, "group1")
        collaborator.contribute(user, "group1", 50)
        self.assertEqual(collaborator.groups["group1"].contributions[user], 50)

    def test_get_progress(self):
        collaborator = FinancialCollaborator()
        collaborator.create_user("user1", "password1")
        collaborator.create_group("group1", 100, datetime.date(2024, 12, 31))
        user = collaborator.login("user1", "password1")
        collaborator.join_group(user, "group1")
        collaborator.contribute(user, "group1", 50)
        total_saved, remaining = collaborator.get_progress("group1")
        self.assertEqual(total_saved, 50)
        self.assertEqual(remaining, 50)

if __name__ == "__main__":
    unittest.main()