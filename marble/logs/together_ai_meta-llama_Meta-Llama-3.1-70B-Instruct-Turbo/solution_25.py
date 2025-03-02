# user.py
class User:
    def __init__(self, username, password):import bcrypt
self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())self.groups = []
import bcrypt

    def join_group(self, group):
        """
        Add a group to the user's groups.

        Args:
            group (Group): The group to join.
        """
        self.groups.append(group)

    def __str__(self):
        return f"User('{self.username}')"


# group.py
class Group:
    def __init__(self, name):
        """
        Initialize a Group object.

        Args:
            name (str): The name of the group.
        """
        self.name = name
        self.users = []
        self.goals = []

    def add_user(self, user):
        """
        Add a user to the group.

        Args:
            user (User): The user to add.
        """
        self.users.append(user)

    def add_goal(self, goal):
        """
        Add a goal to the group.

        Args:
            goal (Goal): The goal to add.
        """
        self.goals.append(goal)

    def __str__(self):
        return f"Group('{self.name}')"


# goal.py
class Goal:
    def __init__(self, name, deadline, amount):
        """
        Initialize a Goal object.

        Args:
            name (str): The name of the goal.
            deadline (str): The deadline of the goal.
            amount (float): The amount of the goal.
        """
        self.name = name
        self.deadline = deadline
        self.amount = amount
        self.contributions = {}

    def add_contribution(self, user, amount):
        """
        Add a contribution to the goal.

        Args:
            user (User): The user who made the contribution.
            amount (float): The amount of the contribution.
        """
        if user in self.contributions:
            self.contributions[user] += amount
        else:
            self.contributions[user] = amount

    def get_progress(self):
        """
        Get the progress of the goal.

        Returns:
            float: The progress of the goal.
        """
        total_contributed = sum(self.contributions.values())
        return total_contributed / self.amount

    def __str__(self):
        return f"Goal('{self.name}')"


# notification.py
class Notification:
    def __init__(self, message):
        """
        Initialize a Notification object.

        Args:
            message (str): The message of the notification.
        """
        self.message = message

    def send(self, user):
        """
        Send the notification to a user.

        Args:
            user (User): The user to send the notification to.
        """
        print(f"Sending notification to {user.username}: {self.message}")


# financial_collaborator.py
class FinancialCollaborator:
    def __init__(self):
        """
        Initialize a FinancialCollaborator object.
        """
        self.users = []
        self.groups = []

    def create_user(self, username, password):
        """
        Create a new user.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            User: The created user.
        """
        user = User(username, password)
        self.users.append(user)
        return user

    def create_group(self, name):
        """
        Create a new group.

        Args:
            name (str): The name of the group.

        Returns:
            Group: The created group.
        """
        group = Group(name)
        self.groups.append(group)
        return group

    def create_goal(self, group, name, deadline, amount):
        """
        Create a new goal.

        Args:
            group (Group): The group to create the goal for.
            name (str): The name of the goal.
            deadline (str): The deadline of the goal.
            amount (float): The amount of the goal.

        Returns:
            Goal: The created goal.
        """
        goal = Goal(name, deadline, amount)
        group.add_goal(goal)
        return goal

    def contribute_to_goal(self, user, goal, amount):
        """
        Contribute to a goal.

        Args:
            user (User): The user who is contributing.
            goal (Goal): The goal to contribute to.
            amount (float): The amount to contribute.
        """
        goal.add_contribution(user, amount)

    def send_notification(self, user, message):
        """
        Send a notification to a user.

        Args:
            user (User): The user to send the notification to.
            message (str): The message of the notification.
        """
        notification = Notification(message)
        notification.send(user)


# test_financial_collaborator.py
import unittest
from financial_collaborator import FinancialCollaborator, User, Group, Goal

class TestFinancialCollaborator(unittest.TestCase):
    def test_create_user(self):import bcrypt
self.assertEqual(bcrypt.checkpw("test_password".encode('utf-8'), user.password), True)self.assertEqual(user.username, "test_user")
        self.assertEqual(user.password, "test_password")

    def test_create_group(self):
        financial_collaborator = FinancialCollaborator()
        group = financial_collaborator.create_group("test_group")
        self.assertEqual(group.name, "test_group")

    def test_create_goal(self):
        financial_collaborator = FinancialCollaborator()
        group = financial_collaborator.create_group("test_group")
        goal = financial_collaborator.create_goal(group, "test_goal", "2024-01-01", 100.0)
        self.assertEqual(goal.name, "test_goal")
        self.assertEqual(goal.deadline, "2024-01-01")
        self.assertEqual(goal.amount, 100.0)

    def test_contribute_to_goal(self):
        financial_collaborator = FinancialCollaborator()
        group = financial_collaborator.create_group("test_group")
        goal = financial_collaborator.create_goal(group, "test_goal", "2024-01-01", 100.0)
        user = financial_collaborator.create_user("test_user", "test_password")
        financial_collaborator.contribute_to_goal(user, goal, 50.0)
        self.assertEqual(goal.contributions[user], 50.0)

    def test_send_notification(self):
        financial_collaborator = FinancialCollaborator()
        user = financial_collaborator.create_user("test_user", "test_password")
        financial_collaborator.send_notification(user, "test_notification")

if __name__ == "__main__":
    unittest.main()