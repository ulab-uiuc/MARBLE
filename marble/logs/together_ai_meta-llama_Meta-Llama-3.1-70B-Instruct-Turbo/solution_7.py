# budget_sync.py

import datetime
import matplotlib.pyplot as plt
from typing import Dict, List

class User:
    """Represents a user with a unique profile and permissions."""
    
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.budgets = {}  # Dictionary to store budgets with their permissions

    def add_budget(self, budget_name: str, permission: str):
        """Adds a budget to the user's profile with the specified permission."""
        self.budgets[budget_name] = permission

    def remove_budget(self, budget_name: str):
        """Removes a budget from the user's profile."""
        if budget_name in self.budgets:
            del self.budgets[budget_name]


class Budget:
    """Represents a shared budget with goals, categories, and users."""
    
    def __init__(self, name: str):
        self.name = name
        self.goals = {}  # Dictionary to store budget goals
        self.categories = {}  # Dictionary to store budget categories
        self.users = {}  # Dictionary to store users with their permissions

    def add_goal(self, goal_name: str, target_amount: float):
        """Adds a budget goal with a target amount."""
        self.goals[goal_name] = target_amount

    def add_category(self, category_name: str):
        """Adds a budget category."""
        self.categories[category_name] = 0.0  # Initialize category amount to 0.0

    def add_user(self, user: User, permission: str):
        """Adds a user to the budget with the specified permission."""
        self.users[user.username] = permission

    def update_category_amount(self, category_name: str, amount: float):
        """Updates the amount of a budget category."""
        if category_name in self.categories:
            self.categories[category_name] += amount

    def get_total_budget(self):
        """Calculates the total budget by summing up all category amounts."""
        return sum(self.categories.values())

    def get_spending_breakdown(self):
        """Returns a dictionary with the spending breakdown of each category."""
        return self.categories


class BudgetSync:
    """Represents the BudgetSync application."""
    
    def __init__(self):
        self.users = {}  # Dictionary to store users
        self.budgets = {}  # Dictionary to store budgets

    def sign_up(self, username: str, password: str):
        """Creates a new user account."""
        self.users[username] = User(username, password)

    def log_in(self, username: str, password: str):
        """Logs in an existing user."""
        if username in self.users and self.users[username].password == password:
            return self.users[username]
        else:
            return None

    def create_budget(self, budget_name: str):
        """Creates a new shared budget."""
        self.budgets[budget_name] = Budget(budget_name)

    def get_budget(self, budget_name: str):
        """Returns a budget by its name."""
        if budget_name in self.budgets:
            return self.budgets[budget_name]
        else:
            return None

    def visualize_budget_breakdown(self, budget_name: str):
        """Visualizes the budget breakdown using a pie chart."""
        budget = self.get_budget(budget_name)
        if budget:
            categories = budget.get_spending_breakdown()
            labels = list(categories.keys())
            sizes = list(categories.values())
            plt.pie(sizes, labels=labels, autopct='%1.1f%%')
            plt.title('Budget Breakdown')
            plt.show()


def main():
    budget_sync = BudgetSync()

    # Sign up users
    budget_sync.sign_up('user1', 'password1')
    budget_sync.sign_up('user2', 'password2')

    # Log in users
    user1 = budget_sync.log_in('user1', 'password1')
    user2 = budget_sync.log_in('user2', 'password2')

    # Create a shared budget
    budget_sync.create_budget('shared_budget')

    # Get the shared budget
    budget = budget_sync.get_budget('shared_budget')

    # Add users to the budget
    budget.add_user(user1, 'edit')
    budget.add_user(user2, 'view-only')

    # Add budget goals and categories
    budget.add_goal('save_for_vacation', 1000.0)
    budget.add_category('housing')
    budget.add_category('food')

    # Update category amounts
    budget.update_category_amount('housing', 500.0)
    budget.update_category_amount('food', 200.0)

    # Visualize budget breakdown
    budget_sync.visualize_budget_breakdown('shared_budget')

    # Print total budget and spending breakdown
    print('Total Budget:', budget.get_total_budget())
    print('Spending Breakdown:', budget.get_spending_breakdown())


if __name__ == '__main__':
    main()