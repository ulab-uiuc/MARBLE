# user.py
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.groups = []

    def __str__(self):
        return f"User: {self.username}"


# group.py
class Group:
    def __init__(self, name):
        self.name = name
        self.users = []
        self.goals = []

    def add_user(self, user):
        self.users.append(user)

    def add_goal(self, goal):
        self.goals.append(goal)

    def __str__(self):
        return f"Group: {self.name}"


# goal.py
class Goal:
    def __init__(self, name, deadline, budget):
        self.name = name
        self.deadline = deadline
        self.budget = budget
        self.contributions = {}

    def add_contribution(self, user, amount):
        self.contributions[user.username] = amount

    def __str__(self):
        return f"Goal: {self.name}, Deadline: {self.deadline}, Budget: {self.budget}"


# financial_collaborator.py
class FinancialCollaborator:
    def __init__(self):
        self.users = {}
        self.groups = {}

    def create_user(self, username, password):
        if username not in self.users:
            self.users[username] = User(username, password)
            return self.users[username]
        else:
            return None

    def create_group(self, name):
        if name not in self.groups:
            self.groups[name] = Group(name)
            return self.groups[name]
        else:
            return None

    def add_user_to_group(self, username, group_name):
        if username in self.users and group_name in self.groups:
            self.groups[group_name].add_user(self.users[username])
            self.users[username].groups.append(self.groups[group_name])
            return True
        else:
            return False

    def set_goal(self, group_name, goal_name, deadline, budget):
        if group_name in self.groups:def set_goal(self, group_name, goal_name, deadline, budget, position=None):\n    if group_name in self.groups:\n        if position is None:\n            self.groups[group_name].add_goal(Goal(goal_name, deadline, budget))\n        else:\n            self.groups[group_name].goals.insert(position, Goal(goal_name, deadline, budget))\n        return True\n    else:\n        return Falsereturn True
        else:
            return False

    def add_contribution(self, group_name, username, amount):
        if group_name in self.groups and username in self.users:
            self.groups[group_name].goals[0].add_contribution(self.users[username], amount)
            return True
        else:
            return False

    def get_dashboard(self, username):
        if username in self.users:
            dashboard = {}
            for group in self.users[username].groups:
                dashboard[group.name] = {}
                for goal in group.goals:
                    dashboard[group.name][goal.name] = {
                        "total_saved": sum([contribution for contribution in goal.contributions.values()]),
                        "my_contribution": goal.contributions.get(username, 0),
                        "remaining_amount": goal.budget - sum([contribution for contribution in goal.contributions.values()])
                    }
            return dashboard
        else:
            return None


# solution.py
from user import User
from group import Group
from goal import Goal
from financial_collaborator import FinancialCollaborator

# Create a Financial Collaborator instance
collaborator = FinancialCollaborator()

# Create users
user1 = collaborator.create_user("user1", "password1")
user2 = collaborator.create_user("user2", "password2")

# Create groups
group1 = collaborator.create_group("group1")
group2 = collaborator.create_group("group2")

# Add users to groups
collaborator.add_user_to_group("user1", "group1")
collaborator.add_user_to_group("user2", "group1")

# Set goals
collaborator.set_goal("group1", "goal1", "2024-01-01", 1000)

# Add contributions
collaborator.add_contribution("group1", "user1", 500)
collaborator.add_contribution("group1", "user2", 500)

# Get dashboard
dashboard = collaborator.get_dashboard("user1")
print(dashboard)

# Test cases
def test_create_user():
    user = collaborator.create_user("user3", "password3")
    assert user is not None
    assert user.username == "user3"

def test_create_group():
    group = collaborator.create_group("group3")
    assert group is not None
    assert group.name == "group3"

def test_add_user_to_group():
    result = collaborator.add_user_to_group("user3", "group3")
    assert result is True

def test_set_goal():
    result = collaborator.set_goal("group3", "goal3", "2024-01-01", 1000)
    assert result is True

def test_add_contribution():
    result = collaborator.add_contribution("group3", "user3", 500)
    assert result is True

def test_get_dashboard():
    dashboard = collaborator.get_dashboard("user3")
    assert dashboard is not None

test_create_user()
test_create_group()
test_add_user_to_group()
test_set_goal()
test_add_contribution()
test_get_dashboard()