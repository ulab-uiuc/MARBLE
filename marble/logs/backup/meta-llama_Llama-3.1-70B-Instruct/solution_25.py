def __init__(self, username, password):
    self.username = usernameself.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())    self.groups = []    def join_group(self, group):
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
        self.members = []
        self.goals = []

    def add_member(self, user):
        """
        Add a member to the group.

        Args:
            user (User): The user to add.
        """
        self.members.append(user)

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
        self.contributions = {}def add_contribution(self, user, amount):
    if amount < 0:
        raise ValueError("Contribution amount cannot be negative")if user in self.contributions:
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
        self.users = {}
        self.groups = {}

    def create_user(self, username, password):
        """
        Create a new user.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            User: The created user.
        """
        if username in self.users:
            raise ValueError("Username already exists")
        user = User(username, password)
        self.users[username] = user
        return user

    def create_group(self, name):
        """
        Create a new group.

        Args:
            name (str): The name of the group.

        Returns:
            Group: The created group.
        """
        if name in self.groups:
            raise ValueError("Group name already exists")
        group = Group(name)
        self.groups[name] = group
        return group

    def add_user_to_group(self, username, group_name):
        """
        Add a user to a group.

        Args:
            username (str): The username of the user.
            group_name (str): The name of the group.
        """
        user = self.users.get(username)
        group = self.groups.get(group_name)
        if user and group:
            user.join_group(group)
            group.add_member(user)

    def create_goal(self, group_name, name, deadline, amount):
        """
        Create a new goal in a group.

        Args:
            group_name (str): The name of the group.
            name (str): The name of the goal.
            deadline (str): The deadline of the goal.
            amount (float): The amount of the goal.

        Returns:
            Goal: The created goal.
        """
        group = self.groups.get(group_name)
        if group:
            goal = Goal(name, deadline, amount)
            group.add_goal(goal)
            return goal

    def contribute_to_goal(self, username, group_name, goal_name, amount):
        """
        Contribute to a goal in a group.

        Args:
            username (str): The username of the user.
            group_name (str): The name of the group.
            goal_name (str): The name of the goal.
            amount (float): The amount of the contribution.
        """
        user = self.users.get(username)
        group = self.groups.get(group_name)
        if user and group:
            for goal in group.goals:
                if goal.name == goal_name:
                    goal.add_contribution(user, amount)
                    break

    def send_notification(self, username, message):
        """
        Send a notification to a user.

        Args:
            username (str): The username of the user.
            message (str): The message of the notification.
        """
        user = self.users.get(username)
        if user:
            notification = Notification(message)
            notification.send(user)


# test_financial_collaborator.py
import unittest
from financial_collaborator import FinancialCollaborator

class TestFinancialCollaborator(unittest.TestCase):
    def setUp(self):
        self.fc = FinancialCollaborator()

    def test_create_user(self):
        user = self.fc.create_user("test_user", "password")
        self.assertEqual(user.username, "test_user")

    def test_create_group(self):
        group = self.fc.create_group("test_group")
        self.assertEqual(group.name, "test_group")

    def test_add_user_to_group(self):
        user = self.fc.create_user("test_user", "password")
        group = self.fc.create_group("test_group")
        self.fc.add_user_to_group("test_user", "test_group")
        self.assertIn(user, group.members)

    def test_create_goal(self):
        group = self.fc.create_group("test_group")
        goal = self.fc.create_goal("test_group", "test_goal", "2024-01-01", 100.0)
        self.assertEqual(goal.name, "test_goal")

    def test_contribute_to_goal(self):
        user = self.fc.create_user("test_user", "password")
        group = self.fc.create_group("test_group")
        self.fc.add_user_to_group("test_user", "test_group")
        goal = self.fc.create_goal("test_group", "test_goal", "2024-01-01", 100.0)
        self.fc.contribute_to_goal("test_user", "test_group", "test_goal", 50.0)
        self.assertEqual(goal.contributions[user], 50.0)

    def test_send_notification(self):
        user = self.fc.create_user("test_user", "password")
        self.fc.send_notification("test_user", "Test notification")

if __name__ == "__main__":
    unittest.main()