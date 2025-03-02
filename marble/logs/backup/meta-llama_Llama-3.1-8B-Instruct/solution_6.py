# solution.py

# Importing necessary libraries
import unittest
from typing import Dict, List

# Defining a class for User
class User:
    def __init__(self, name: str, budget: Dict[str, float]):
        """
        Initialize a User object.

        Args:
        name (str): The name of the user.
        budget (Dict[str, float]): A dictionary representing the user's budget, where keys are categories and values are budget limits.
        """
        self.name = name
        self.budget = budget
        self.expenses = {}

    def add_expense(self, category: str, amount: float):
        """
        Add an expense to the user's expenses.

        Args:
        category (str): The category of the expense.
        amount (float): The amount of the expense.
        """
        if category in self.budget and amount <= self.budget[category]:
            self.expenses[category] = self.expenses.get(category, 0) + amount
        else:
            print(f"Invalid expense: {category} {amount}")

    def view_budget(self):
        """
        Print the user's budget.
        """
        print(f"Budget for {self.name}:")
        for category, limit in self.budget.items():
            print(f"{category}: {limit}")

    def view_expenses(self):
        """
        Print the user's expenses.
        """
        print(f"Expenses for {self.name}:")
        for category, amount in self.expenses.items():
            print(f"{category}: {amount}")


# Defining a class for MultiAgentBudgetOptimizer
class MultiAgentBudgetOptimizer:
    def __init__(self):
        """
        Initialize a MultiAgentBudgetOptimizer object.
        """
        self.users = {}
        self.group_budget = {}

    def add_user(self, name: str, budget: Dict[str, float]):
        """
        Add a user to the optimizer.

        Args:
        name (str): The name of the user.
        budget (Dict[str, float]): A dictionary representing the user's budget, where keys are categories and values are budget limits.
        """
        self.users[name] = User(name, budget)
        self.group_budget[name] = budget

    def view_group_budget(self):
        """
        Print the group's budget.
        """
        print("Group Budget:")
        for category, limit in self.group_budget.items():
            print(f"{category}: {limit}")

    def view_group_expenses(self):
        """
        Print the group's expenses.
        """
        print("Group Expenses:")
        for category, amount in self.get_group_expenses().items():
            print(f"{category}: {amount}")

    def get_group_expenses(self) -> Dict[str, float]:
        """
        Get the group's expenses.

        Returns:
        Dict[str, float]: A dictionary representing the group's expenses, where keys are categories and values are total expenses.
        """
        group_expenses = {}
        for user in self.users.values():
            for category, amount in user.expenses.items():
                group_expenses[category] = group_expenses.get(category, 0) + amount
        return group_expenses

    def optimize_spending(self):
        """
        Optimize the group's spending by suggesting ways to reduce expenses or reallocate funds.
        """
        group_expenses = self.get_group_expenses()
        for category, amount in group_expenses.items():
            if amount > sum(self.group_budget.values()):
                print(f"Warning: {category} expenses exceed group budget")
            else:
                print(f"Category {category} expenses: {amount}")
                print(f"Suggested reduction: {amount - sum([self.group_budget[user] for user in self.users if category in self.group_budget[user]])}")


# Defining test cases
class TestMultiAgentBudgetOptimizer(unittest.TestCase):
    def test_add_user(self):
        optimizer = MultiAgentBudgetOptimizer()
        optimizer.add_user("User1", {"Groceries": 100, "Entertainment": 50})
        self.assertIn("User1", optimizer.users)

    def test_view_group_budget(self):
        optimizer = MultiAgentBudgetOptimizer()
        optimizer.add_user("User1", {"Groceries": 100, "Entertainment": 50})
        optimizer.view_group_budget()

    def test_view_group_expenses(self):
        optimizer = MultiAgentBudgetOptimizer()
        optimizer.add_user("User1", {"Groceries": 100, "Entertainment": 50})
        optimizer.users["User1"].add_expense("Groceries", 20)
        optimizer.view_group_expenses()

    def test_optimize_spending(self):
        optimizer = MultiAgentBudgetOptimizer()
        optimizer.add_user("User1", {"Groceries": 100, "Entertainment": 50})
        optimizer.users["User1"].add_expense("Groceries", 20)
        optimizer.optimize_spending()


if __name__ == "__main__":
    unittest.main()