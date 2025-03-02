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
    def __init__(self, name, deadline, budget):
        self.name = name
        self.deadline = deadline
        self.budget = budget
        self.members = []
        self.contributions = {}
        self.milestones = []

    def add_member(self, user):
        self.members.append(user)
        user.groups.append(self)

    def add_contribution(self, user, amount):
        if user in self.members:
            if user in self.contributions:
                self.contributions[user] += amount
            else:
                self.contributions[user] = amount
        else:
            raise ValueError("User is not a member of this group")

    def add_milestone(self, name, deadline):
        self.milestones.append((name, deadline))

    def __str__(self):
        return f"Group: {self.name}"

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
            raise ValueError("Username already exists")

    def create_group(self, name, deadline, budget):
        if name not in self.groups:
            self.groups[name] = Group(name, deadline, budget)
            return self.groups[name]
        else:
            raise ValueError("Group already exists")

    def join_group(self, username, group_name):
        if username in self.users:
            if group_name in self.groups:
                self.groups[group_name].add_member(self.users[username])
            else:
                raise ValueError("Group does not exist")
        else:
            raise ValueError("User does not exist")

    def set_goal(self, group_name, deadline, budget):
        if group_name in self.groups:
            self.groups[group_name].deadline = deadline
            self.groups[group_name].budget = budget
        else:
            raise ValueError("Group does not exist")

    def contribute(self, username, group_name, amount):
        if username in self.users:
            if group_name in self.groups:
                self.groups[group_name].add_contribution(self.users[username], amount)
            else:
                raise ValueError("Group does not exist")
        else:
            raise ValueError("User does not exist")

    def add_milestone(self, group_name, name, deadline):
        if group_name in self.groups:
            self.groups[group_name].add_milestone(name, deadline)
        else:
            raise ValueError("Group does not exist")

    def get_progress(self, username):
        if username in self.users:
            progress = {}
            for group in self.users[username].groups:
                total_amount = sum(self.groups[group.name].contributions.values())
                progress[group.name] = {
                    "total_amount": total_amount,
                    "amount_contributed": self.groups[group.name].contributions.get(username, 0),
                    "remaining_amount": self.groups[group.name].budget - total_amount
                }
            return progress
        else:
            raise ValueError("User does not exist")

    def send_notification(self, group_name, message):
        if group_name in self.groups:
            for member in self.groups[group_name].members:
                print(f"Notification sent to {member.username}: {message}")
        else:
            raise ValueError("Group does not exist")

# solution.py
from user import User
from group import Group
from financial_collaborator import FinancialCollaborator

def main():
    collaborator = FinancialCollaborator()

    # Create users
    user1 = collaborator.create_user("user1", "password1")
    user2 = collaborator.create_user("user2", "password2")

    # Create group
    group = collaborator.create_group("group1", "2024-07-31", 1000)

    # Join group
    collaborator.join_group("user1", "group1")
    collaborator.join_group("user2", "group1")

    # Set goal
    collaborator.set_goal("group1", "2024-07-31", 1000)

    # Contribute
    collaborator.contribute("user1", "group1", 500)
    collaborator.contribute("user2", "group1", 500)

    # Add milestone
    collaborator.add_milestone("group1", "Milestone 1", "2024-07-15")

    # Get progress
    print(collaborator.get_progress("user1"))

    # Send notification
    collaborator.send_notification("group1", "Reminder: Deadline is approaching")

if __name__ == "__main__":
    main()