# solution.py

class User:
    """Class representing a user in the budget optimization system."""
    
    def __init__(self, username):
        """Initialize a user with a username and empty expenses and budgets."""
        self.username = username
        self.expenses = {}
        self.budgets = {}

    def add_expense(self, category, amount):
        """Add an expense for a specific category."""
        if category in self.expenses:
            self.expenses[category] += amount
        else:
            self.expenses[category] = amount

    def set_budget(self, category, amount):
        """Set a budget for a specific category."""
        self.budgets[category] = amount

    def get_total_expenses(self):
        """Calculate the total expenses of the user."""
        return sum(self.expenses.values())

    def get_budget_status(self):
        """Get the budget status for the user."""
        status = {}
        for category in self.budgets:
            spent = self.expenses.get(category, 0)
            remaining = self.budgets[category] - spent
            status[category] = {
                'budget': self.budgets[category],
                'spent': spent,
                'remaining': remaining
            }
        return status


class MultiAgentBudgetOptimizer:
    """Class to manage multiple users and their budgets collaboratively."""
    
    def __init__(self):
        """Initialize the budget optimizer with an empty user list."""
        self.users = {}

    def add_user(self, username):
        """Add a new user to the system."""
        if username not in self.users:
            self.users[username] = User(username)

    def add_expense(self, username, category, amount):
        """Add an expense for a specific user."""
        if username in self.users:
            self.users[username].add_expense(category, amount)

    def set_budget(self, username, category, amount):
        """Set a budget for a specific user."""
        if username in self.users:
            self.users[username].set_budget(category, amount)

    def get_group_summary(self):
        """Get a summary of the group's total expenses and budgets."""
        total_expenses = {}
        total_budgets = {}def optimize_budget(self):
        """Suggest ways to reduce expenses or reallocate funds based on group spending patterns."""
        suggestions = []
        total_expenses = self.get_group_summary()['total_expenses']
        total_budgets = self.get_group_summary()['total_budgets']
        for category in total_budgets:
            if total_expenses.get(category, 0) > total_budgets[category]:
                suggestions.append(f"Overall spending exceeds the budget for {category}. Consider reducing expenses across users.")
            elif total_expenses.get(category, 0) < total_budgets[category] * 0.5:
                suggestions.append(f"Overall spending is under budget for {category}. Consider reallocating funds to cover overspending in other categories.")
        for user in self.users.values():
            for category, spent in user.expenses.items():
                budget = user.budgets.get(category, 0)
                if spent > budget:
                    suggestions.append(f"{user.username} has exceeded the budget for {category}. Consider reducing expenses.")
                elif spent < budget * 0.5:
                    suggestions.append(f"{user.username} is under-spending in {category}. Consider reallocating funds.")
        return suggestions        return suggestions


# Test cases for the MultiAgentBudgetOptimizer
def test_multi_agent_budget_optimizer():
    """Run test cases to validate the functionality of the budget optimizer."""
    optimizer = MultiAgentBudgetOptimizer()
    
    # Add users
    optimizer.add_user("Alice")
    optimizer.add_user("Bob")

    # Set budgets
    optimizer.set_budget("Alice", "groceries", 200)
    optimizer.set_budget("Alice", "entertainment", 100)
    optimizer.set_budget("Bob", "groceries", 150)
    optimizer.set_budget("Bob", "utilities", 80)

    # Add expenses
    optimizer.add_expense("Alice", "groceries", 50)
    optimizer.add_expense("Alice", "entertainment", 120)  # Exceeds budget
    optimizer.add_expense("Bob", "groceries", 100)
    optimizer.add_expense("Bob", "utilities", 50)

    # Get group summary
    summary = optimizer.get_group_summary()
    print("Group Summary:", summary)

    # Optimize budget
    suggestions = optimizer.optimize_budget()
    print("Optimization Suggestions:", suggestions)

# Uncomment the following line to run the test cases
# test_multi_agent_budget_optimizer()