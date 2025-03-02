# solution.py

# Import necessary libraries
from collections import defaultdict
import json
import random
import threading
import time

# User class to represent each user in the system
class User:
    def __init__(self, username, role='user'):
        self.username = username
        self.role = role
        self.budget = Budget()
    
    def add_income(self, amount, category, description=''):
        self.budget.add_income(amount, category, description)
    
    def add_expense(self, amount, category, description=''):
        self.budget.add_expense(amount, category, description)

# Budget class to manage income and expenses
class Budget:
    def __init__(self):
        self.income = defaultdict(float)
        self.expenses = defaultdict(float)
        self.goals = []
    
    def add_income(self, amount, category, description=''):
        self.income[category] += amount
        self.log_entry('income', amount, category, description)
    
    def add_expense(self, amount, category, description=''):
        self.expenses[category] += amount
        self.log_entry('expense', amount, category, description)
    
    def log_entry(self, entry_type, amount, category, description):
        print(f"{entry_type.capitalize()} logged: {amount} in {category} - {description}")
    
    def get_balance(self):
        total_income = sum(self.income.values())
        total_expenses = sum(self.expenses.values())
        return total_income - total_expenses
    
    def suggest_budgeting_tips(self):
        # Suggest tips based on overspending
        tips = []
        for category, expense in self.expenses.items():
            if expense > self.income.get(category, 0):
                tips.append(f"Consider reducing spending in {category}.")
        return tips

# BudgetCollaborator class to manage users and real-time updates
class BudgetCollaborator:
    def __init__(self):
        self.users = {}
        self.lock = threading.Lock()
    def notify_users(self, username, balance):
        for user in self.users.values():
            if user.username != username:
                print(f"{username} updated their budget. New balance: {balance}")
    
    def add_user(self, username, role='user'):
        if username not in self.users:
            self.users[username] = User(username, role)
            print(f"User {username} added with role {role}.")
        else:
            print(f"User {username} already exists.")
    
    def get_user(self, username):
        return self.users.get(username)
    
    def synchronize_budgets(self):
        # Simulate real-time synchronization
        while True:
            time.sleep(5)  # Check for updates every 5 seconds
            with self.lock:with self.lock:
                for user in self.users.values():
                    self.notify_users(user.username, user.budget.get_balance())                # For simplicity, we just print a message
                for user in self.users.values():
                    print(f"{user.username}'s budget: {user.budget.get_balance()}")

# Main function to demonstrate the functionality
def main():
    # Create the BudgetCollaborator instance
    budget_collaborator = BudgetCollaborator()
    
    # Add users
    budget_collaborator.add_user('Alice', 'admin')
    budget_collaborator.add_user('Bob', 'user')
    
    # Users adding income and expenses
    alice = budget_collaborator.get_user('Alice')
    alice.add_income(1000, 'Salary', 'Monthly salary')
    alice.add_expense(200, 'Groceries', 'Weekly groceries')
    
    bob = budget_collaborator.get_user('Bob')
    bob.add_income(800, 'Freelance', 'Freelance work')
    bob.add_expense(300, 'Entertainment', 'Movies and dining out')
    
    # Start the synchronization in a separate thread
    sync_thread = threading.Thread(target=budget_collaborator.synchronize_budgets)
    sync_thread.start()
    
    # Simulate some time passing
    time.sleep(10)
    
    # Show suggestions based on current budget status
    print(alice.budget.suggest_budgeting_tips())
    print(bob.budget.suggest_budgeting_tips())

# Run the main function
if __name__ == "__main__":
    main()