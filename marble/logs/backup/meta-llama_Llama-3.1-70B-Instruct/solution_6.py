# multi_agent_budget_optimizer.py

class User:
    """Represents a user with a name and expenses."""
    def __init__(self, name):
        self.name = name
        self.expenses = {}

    def add_expense(self, category, amount):
        """Adds an expense to the user's expenses."""
        if category in self.expenses:
            self.expenses[category] += amount
        else:
            self.expenses[category] = amount

    def get_expenses(self):
        """Returns the user's expenses."""
        return self.expenses


class BudgetOptimizer:
    """Manages the budget for multiple users."""
    def __init__(self):
        self.users = {}
        self.budget_limits = {}

    def add_user(self, user):
        """Adds a user to the budget optimizer."""
        self.users[user.name] = user

    def set_budget_limit(self, category, limit):
        """Sets a budget limit for a category."""
        self.budget_limits[category] = limit

    def get_total_expenses(self):def get_remaining_budget(self):
def get_total_expenses(self):
    total_expenses = {}
    for user in self.users.values():
        for category, amount in user.get_expenses().items():total_expenses[category] = amountelse:
                total_expenses[category] = amount
    return total_expenses
        remaining_budget = {}
        for category, limit in self.budget_limits.items():total_expenses = self.get_total_expenses().get(category, 0)remaining_budget[category] = limit - total_expenses
        return remaining_budget        suggestions = []
        for category, remaining in self.get_remaining_budget().items():
            if remaining < 0:
                suggestions.append(f"Reduce expenses in {category} by {-remaining}")
            elif remaining > 0:
                suggestions.append(f"Reallocate {remaining} from {category} to other categories")
        return suggestions


class Dashboard:
    """Displays a summary of the group's financial status."""
    def __init__(self, budget_optimizer):
        self.budget_optimizer = budget_optimizer

    def display_summary(self):
        """Displays a summary of the group's financial status."""
        print("Total Expenses:")
        for category, amount in self.budget_optimizer.get_total_expenses().items():
            print(f"{category}: {amount}")
        print("Remaining Budget:")
        for category, amount in self.budget_optimizer.get_remaining_budget().items():
            print(f"{category}: {amount}")
        print("Suggestions:")
        for suggestion in self.budget_optimizer.optimize_budget():
            print(suggestion)


# Test cases
import unittest

class TestMultiAgentBudgetOptimizer(unittest.TestCase):
    def test_add_user(self):
        budget_optimizer = BudgetOptimizer()
        user = User("John")
        budget_optimizer.add_user(user)
        self.assertIn(user.name, budget_optimizer.users)

    def test_set_budget_limit(self):
        budget_optimizer = BudgetOptimizer()
        budget_optimizer.set_budget_limit("groceries", 100)
        self.assertIn("groceries", budget_optimizer.budget_limits)

    def test_get_total_expenses(self):
        budget_optimizer = BudgetOptimizer()
        user1 = User("John")
        user1.add_expense("groceries", 50)
        user2 = User("Jane")
        user2.add_expense("groceries", 30)
        budget_optimizer.add_user(user1)
        budget_optimizer.add_user(user2)
        self.assertEqual(budget_optimizer.get_total_expenses()["groceries"], 80)

    def test_get_remaining_budget(self):
        budget_optimizer = BudgetOptimizer()
        budget_optimizer.set_budget_limit("groceries", 100)
        user1 = User("John")
        user1.add_expense("groceries", 50)
        user2 = User("Jane")
        user2.add_expense("groceries", 30)
        budget_optimizer.add_user(user1)
        budget_optimizer.add_user(user2)
        self.assertEqual(budget_optimizer.get_remaining_budget()["groceries"], 20)

    def test_optimize_budget(self):
        budget_optimizer = BudgetOptimizer()
        budget_optimizer.set_budget_limit("groceries", 100)
        user1 = User("John")
        user1.add_expense("groceries", 150)
        budget_optimizer.add_user(user1)
        self.assertEqual(budget_optimizer.optimize_budget()[0], "Reduce expenses in groceries by 50")

if __name__ == "__main__":
    unittest.main()

# Example usage
budget_optimizer = BudgetOptimizer()
dashboard = Dashboard(budget_optimizer)

user1 = User("John")
user1.add_expense("groceries", 50)
user1.add_expense("entertainment", 100)

user2 = User("Jane")
user2.add_expense("groceries", 30)
user2.add_expense("utilities", 50)

budget_optimizer.add_user(user1)
budget_optimizer.add_user(user2)

budget_optimizer.set_budget_limit("groceries", 100)
budget_optimizer.set_budget_limit("entertainment", 200)
budget_optimizer.set_budget_limit("utilities", 100)

dashboard.display_summary()