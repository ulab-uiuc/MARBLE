# budget_collaborator.py

import threading
import time
from datetime import datetime
import matplotlib.pyplot as plt

class User:
    """Represents a user in the budgeting system."""
    
    def __init__(self, username, password, role):
        """
        Initializes a User object.
        
        Args:
        username (str): The username chosen by the user.
        password (str): The password chosen by the user.
        role (str): The role of the user (e.g., 'admin' or 'user').
        """
        self.username = username
        self.password = password
        self.role = role

class Budget:
    """Represents a shared budget in the budgeting system."""
    
    def __init__(self):
        """
        Initializes a Budget object.
        
        Attributes:
        income (float): The total income in the budget.
        expenses (dict): A dictionary of expense categories and their corresponding amounts.
        goals (dict): A dictionary of financial goals and their corresponding target amounts.
        """
        self.income = 0
        self.expenses = {}
        self.goals = {}
        self.lock = threading.Lock()  # For synchronization

    def add_income(self, amount):
        """
        Adds income to the budget.
        
        Args:
        amount (float): The amount of income to add.
        """
        with self.lock:
            self.income += amount

    def add_expense(self, category, amount):
        """
        Adds an expense to the budget.
        
        Args:
        category (str): The category of the expense.
        amount (float): The amount of the expense.
        """
        with self.lock:
            if category in self.expenses:
                self.expenses[category] += amount
            else:
                self.expenses[category] = amount

    def add_goal(self, goal, target_amount):
        """
        Adds a financial goal to the budget.
        
        Args:
        goal (str): The name of the goal.
        target_amount (float): The target amount for the goal.
        """
        with self.lock:
            self.goals[goal] = target_amount

    def get_budget_breakdown(self):
        """
        Returns a dictionary representing the budget breakdown.
        
        Returns:
        dict: A dictionary with income, expenses, and goals.
        """
        with self.lock:
            return {
                'income': self.income,
                'expenses': self.expenses,
                'goals': self.goals
            }

    def provide_feedback(self):
        """
        Provides adaptive feedback based on the budget's current status.
        
        Returns:
        str: A message with feedback and suggestions.
        """
        with self.lock:
            feedback = ""
            if self.income < sum(self.expenses.values()):
                feedback += "You are overspending. Consider reducing expenses in categories like "
                feedback += ", ".join([category for category, amount in self.expenses.items() if amount > self.income * 0.1])
            for goal, target_amount in self.goals.items():
                if sum(self.expenses.values()) > target_amount:
                    feedback += f"\nYou are not meeting your goal of {goal}. Consider allocating more funds towards it."
            return feedback

class BudgetCollaborator:
    """Represents the budgeting system."""
    
    def __init__(self):
        """
        Initializes a BudgetCollaborator object.
        
        Attributes:
        users (dict): A dictionary of users in the system.
        budget (Budget): The shared budget.
        """
        self.users = {}
        self.budget = Budget()
self.logged_in_users = set()

    def add_user(self, user):def login(self, username, password):
    if username in self.logged_in_users:
        raise Exception("User is already logged in")
    if username in self.users and self.users[username].password == password:
        self.logged_in_users.add(username)
        return True
    raise Exception("Invalid username or password")def add_income(self, amount):
        """
        Adds income to the budget.
        
        Args:
        amount (float): The amount of income to add.
        """
        self.budget.add_income(amount)

    def add_expense(self, category, amount):
        """
        Adds an expense to the budget.
        
        Args:
        category (str): The category of the expense.
        amount (float): The amount of the expense.
        """
        self.budget.add_expense(category, amount)

    def add_goal(self, goal, target_amount):
        """
        Adds a financial goal to the budget.
        
        Args:
        goal (str): The name of the goal.
        target_amount (float): The target amount for the goal.
        """
        self.budget.add_goal(goal, target_amount)

    def get_budget_breakdown(self):
        """
        Returns a dictionary representing the budget breakdown.
        
        Returns:
        dict: A dictionary with income, expenses, and goals.
        """
        return self.budget.get_budget_breakdown()

    def provide_feedback(self):
        """
        Provides adaptive feedback based on the budget's current status.
        
        Returns:
        str: A message with feedback and suggestions.
        """
        return self.budget.provide_feedback()

    def visualize_budget(self):
        """
        Visualizes the budget breakdown using a pie chart.
        """
        breakdown = self.get_budget_breakdown()
        labels = list(breakdown['expenses'].keys())
        sizes = list(breakdown['expenses'].values())
        plt.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.title('Budget Breakdown')
        plt.show()

def main():
    # Create a budgeting system
    system = BudgetCollaborator()

    # Create users
    user1 = User('user1', 'password1', 'user')
    user2 = User('user2', 'password2', 'admin')

    # Add users to the system
    system.add_user(user1)
    system.add_user(user2)

    # Login users
    if system.login('user1', 'password1'):
        print("User 1 logged in successfully")
    if system.login('user2', 'password2'):
        print("User 2 logged in successfully")

    # Add income and expenses
    system.add_income(1000)
    system.add_expense('Rent', 300)
    system.add_expense('Food', 200)
    system.add_expense('Transportation', 100)

    # Add financial goals
    system.add_goal('Save for a car', 5000)
    system.add_goal('Pay off debt', 2000)

    # Get budget breakdown
    breakdown = system.get_budget_breakdown()
    print("Budget Breakdown:")
    print(breakdown)

    # Provide feedback
    feedback = system.provide_feedback()
    print("Feedback:")
    print(feedback)

    # Visualize budget
    system.visualize_budget()

if __name__ == "__main__":
    main()