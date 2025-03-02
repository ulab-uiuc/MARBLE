# solution.py

# Import necessary libraries
from datetime import datetime, timedelta
import hashlib
import json

# User class to handle user-related functionalities
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = self.hash_password(password)
        self.groups = []

    def hash_password(self, password):
        # Hash the password for secure storage
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        # Check if the provided password matches the stored hashed password
        return self.password == self.hash_password(password)

# Group class to manage financial goals and contributions
class Group:
    def __init__(self, name, goal_amount, deadline):
        self.name = name
        self.goal_amount = goal_amount
        self.deadline = deadline
        self.contributions = {}
        self.total_contributed = 0

    def add_contribution(self, user, amount):
        # Add a user's contribution to the group
        if user.username in self.contributions:
            self.contributions[user.username] += amount
        else:
            self.contributions[user.username] = amount
        self.total_contributed += amount

    def get_progress(self):
        # Calculate the remaining amount needed to reach the goal
        remaining = self.goal_amount - self.total_contributed
        return {
            "total_contributed": self.total_contributed,
            "remaining": remaining,
            "goal_amount": self.goal_amount
        }

# FinancialCollaborator class to manage users and groups
class FinancialCollaborator:
    def __init__(self):
        self.users = {}
        self.groups = {}

    def create_user(self, username, password):
        # Create a new user if the username is not already taken
        if username in self.users:
            raise ValueError("Username already exists.")
        self.users[username] = User(username, password)        # Validate goal_amount and deadline
        if goal_amount <= 0:
            raise ValueError("Goal amount must be a positive number.")
        if deadline <= datetime.now():
            raise ValueError("Deadline must be a future date.")
        # Create a new group and add the user to it
        if group_name in self.groups:
            raise ValueError("Group name already exists.")
        group = Group(group_name, goal_amount, deadline)
        self.groups[group_name] = group
        user.groups.append(group)    def join_group(self, user, group_name):
        # Allow a user to join an existing group
        group = self.groups.get(group_name)
        if group:
            user.groups.append(group)
        else:
            raise ValueError("Group does not exist.")

    def add_contribution(self, user, group_name, amount):
        # Add a contribution to a specific group
        group = self.groups.get(group_name)
        if group:
            group.add_contribution(user, amount)
        else:
            raise ValueError("Group does not exist.")

    def get_dashboard(self, user):
        # Get the dashboard information for the user's groups
        dashboard = {}
        for group in user.groups:
            dashboard[group.name] = group.get_progress()
        return dashboard

# Example usage
if __name__ == "__main__":
    fc = FinancialCollaborator()
    
    # Create users
    fc.create_user("alice", "password123")
    fc.create_user("bob", "password456")
    
    # User login
    alice = fc.login("alice", "password123")
    bob = fc.login("bob", "password456")
    
    # Create a group
    fc.create_group(alice, "Vacation Fund", 3000, datetime.now() + timedelta(days=30))
    
    # Users contribute to the group
    fc.add_contribution(alice, "Vacation Fund", 1000)
    fc.add_contribution(bob, "Vacation Fund", 500)
    
    # Get dashboard for Alice
    dashboard = fc.get_dashboard(alice)
    print(json.dumps(dashboard, indent=4))

# Note: This is a simplified version of the Financial Collaborator system.
# In a real-world application, you would implement persistent storage (e.g., a database),
# user input validation, error handling, and a user interface.