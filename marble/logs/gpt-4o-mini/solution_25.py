# solution.py

# Import necessary libraries
import hashlib
import uuid
from datetime import datetime, timedelta
from collections import defaultdict

# User class to handle user-related operations
class User:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = self.hash_password(password)
        self.groups = []

    def hash_password(self, password):
        # Hash the password for secure storage
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        # Check if the provided password matches the stored hash
        return self.password_hash == self.hash_password(password)

# Group class to manage financial goals and contributions
class Group:
    def __init__(self, name):
        self.name = name
        self.members = {}
        self.goal = None
        self.contributions = defaultdict(float)

    def add_member(self, user):
        # Add a user to the group
        self.members[user.username] = user

    def set_goal(self, amount, deadline):def set_goal(self, amount, deadline):
        # Validate amount and deadline
        if amount <= 0:
            raise ValueError('Amount must be a positive number.')
        if deadline <= datetime.now():
            raise ValueError('Deadline must be a future date.')
        # Set a financial goal for the group
        self.goal = {'amount': amount, 'deadline': deadline, 'created_at': datetime.now()}        self.goal = {'amount': amount, 'deadline': deadline, 'created_at': datetime.now()}

    def add_contribution(self, username, amount):
        # Add a contribution from a user
        if username in self.members:
            self.contributions[username] += amount

    def get_progress(self):
        # Calculate the total contributions and remaining amount
        total_contributed = sum(self.contributions.values())
        remaining = self.goal['amount'] - total_contributed if self.goal else 0
        return total_contributed, remaining

# FinancialCollaborator class to manage users and groups
class FinancialCollaborator:
    def __init__(self):
        self.users = {}
        self.groups = {}

    def create_user(self, username, password):
        # Create a new user account
        if username in self.users:
            raise ValueError("User already exists.")
        self.users[username] = User(username, password)

    def login(self, username, password):
        # Authenticate a user
        user = self.users.get(username)
        if user and user.check_password(password):
            return user
        raise ValueError("Invalid username or password.")

    def create_group(self, group_name):
        # Create a new group
        if group_name in self.groups:
            raise ValueError("Group already exists.")
        self.groups[group_name] = Group(group_name)

    def join_group(self, username, group_name):
        # Add a user to an existing group
        user = self.users.get(username)
        group = self.groups.get(group_name)
        if user and group:
            group.add_member(user)
            user.groups.append(group_name)
        else:
            raise ValueError("User or group not found.")

    def set_group_goal(self, group_name, amount, deadline):
        # Set a financial goal for a group
        group = self.groups.get(group_name)
        if group:
            group.set_goal(amount, deadline)
        else:
            raise ValueError("Group not found.")

    def add_contribution(self, username, group_name, amount):
        # Add a contribution to a group's goal
        group = self.groups.get(group_name)
        if group:
            group.add_contribution(username, amount)
        else:
            raise ValueError("Group not found.")

    def get_dashboard(self, username, group_name):
        # Get the progress dashboard for a user in a group
        group = self.groups.get(group_name)
        if group:
            total_contributed, remaining = group.get_progress()
            return {
                'total_contributed': total_contributed,
                'remaining': remaining,
                'goal': group.goal
            }
        raise ValueError("Group not found.")

# Example usage
if __name__ == "__main__":
    fc = FinancialCollaborator()
    fc.create_user("alice", "password123")
    fc.create_user("bob", "password456")

    fc.create_group("Vacation Fund")
    fc.join_group("alice", "Vacation Fund")
    fc.join_group("bob", "Vacation Fund")

    fc.set_group_goal("Vacation Fund", 2000, datetime.now() + timedelta(days=30))
    fc.add_contribution("alice", "Vacation Fund", 500)
    fc.add_contribution("bob", "Vacation Fund", 300)

    dashboard = fc.get_dashboard("alice", "Vacation Fund")
    print(dashboard)  # Display the dashboard for Alice

# Test cases can be added below to validate the functionality
# These would typically be in a separate test file