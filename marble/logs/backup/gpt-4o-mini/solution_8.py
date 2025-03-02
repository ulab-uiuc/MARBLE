# solution.py

# Import necessary libraries
import json
from collections import defaultdict
from typing import List, Dict, Any

# User class to represent each user in the system
class User:
    def __init__(self, username: str, role: str):
        self.username = username  # Username of the user
        self.role = role  # Role of the user (admin or regular)
        self.budget = Budget()  # Each user has a budget

# Budget class to manage budget data
class Budget:
    def __init__(self):
        self.income = 0.0  # Total income
        self.expenses = defaultdict(float)  # Dictionary to hold categorized expenses
        self.goals = []  # List to hold financial goals

    def add_income(self, amount: float):
        """Add income to the budget."""
        self.income += amount

    def add_expense(self, category: str, amount: float, note: str = ""):
        """Add an expense to the budget."""
        self.expenses[category] += amount

    def set_goal(self, goal: str):
        """Set a financial goal."""
        self.goals.append(goal)

    def get_budget_summary(self) -> Dict[str, Any]:
        """Get a summary of the budget."""
        return {
            "income": self.income,
            "expenses": dict(self.expenses),
            "goals": self.goals,
            "remaining_budget": self.income - sum(self.expenses.values())
        }

# BudgetCollaborator class to manage the collaborative budgeting system
class BudgetCollaborator:
    def __init__(self):
        self.users = {}  # Dictionary to hold users by username
        self.active_users = []  # List to hold currently active users

    def add_user(self, username: str, role: str):
        """Add a new user to the system."""
        if username not in self.users:
            self.users[username] = User(username, role)

    def login(self, username: str):
        """Log in a user and add them to active users."""
        if username in self.users:
            self.active_users.append(self.users[username])

    def logout(self, username: str):
        """Log out a user and remove them from active users."""
        self.active_users = [user for user in self.active_users if user.username != username]def sync_budget(self):
        """Synchronize budget data across all active users."""
        budget_summaries = {user.username: user.budget.get_budget_summary() for user in self.active_users}
        self.notify_users(budget_summaries)
        return budget_summaries

    def notify_users(self, budget_summaries: Dict[str, Any]):
        """Notify all active users of budget updates."""
        for user in self.active_users:
            # Here you would implement the logic to send updates to the user,
            # e.g., using websockets or a pub/sub model.
            print(f"{user.username}, your budget has been updated: {budget_summaries[user.username]}")    def provide_feedback(self):
        """Provide adaptive feedback based on budget status."""
        feedback = {}
        for user in self.active_users:
            total_expenses = sum(user.budget.expenses.values())
            if total_expenses > user.budget.income:
                feedback[user.username] = "You are over budget! Consider reducing expenses."
            else:
                feedback[user.username] = "You are within your budget."
        return feedback

    def get_visual_representation(self) -> Dict[str, Any]:
        """Get visual representation of budgets (placeholder)."""
        # This is a placeholder for visual representation logic
        return {user.username: user.budget.get_budget_summary() for user in self.active_users}

# Example usage
if __name__ == "__main__":
    # Create an instance of BudgetCollaborator
    budget_system = BudgetCollaborator()

    # Add users
    budget_system.add_user("alice", "admin")
    budget_system.add_user("bob", "regular")

    # Users log in
    budget_system.login("alice")
    budget_system.login("bob")

    # Users add income and expenses
    budget_system.users["alice"].budget.add_income(5000)
    budget_system.users["alice"].budget.add_expense("Food", 1200)
    budget_system.users["bob"].budget.add_income(3000)
    budget_system.users["bob"].budget.add_expense("Transport", 800)

    # Synchronize budgets
    print("Budget Synchronization:", budget_system.sync_budget())

    # Provide feedback
    print("Feedback:", budget_system.provide_feedback())

    # Get visual representation (placeholder)
    print("Visual Representation:", budget_system.get_visual_representation())