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
        for category, budget in self.budgets.items():
            spent = self.expenses.get(category, 0)
            remaining = budget - spent
            status[category] = {'budget': budget, 'spent': spent, 'remaining': remaining}
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
        total_budgets = {}    def optimize_budget(self):
        """Suggest ways to reduce expenses or reallocate funds collaboratively."""
        suggestions = []
        total_expenses = self.get_group_summary()['total_expenses']
        total_budgets = self.get_group_summary()['total_budgets']
        for category in total_budgets:
            total_spent = total_expenses.get(category, 0)
            if total_spent > total_budgets[category]:
                suggestions.append(f"Overall spending on {category} exceeds the budget by {total_spent - total_budgets[category]}.")
            elif total_spent < total_budgets[category] * 0.5:
                suggestions.append(f"Consider reducing spending in {category} as total spent is only {total_spent} out of {total_budgets[category]}.")
        return suggestions        return suggestions


# Test cases for the MultiAgentBudgetOptimizer
def test_multi_agent_budget_optimizer():
    """Run test cases to validate the functionality of the MultiAgentBudgetOptimizer."""
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
    optimizer.add_expense("Bob", "utilities", 90)  # Exceeds budget

    # Get group summary
    summary = optimizer.get_group_summary()
    print("Group Summary:", summary)

    # Optimize budget
    suggestions = optimizer.optimize_budget()
    print("Optimization Suggestions:", suggestions)

# Uncomment the line below to run the test cases
# test_multi_agent_budget_optimizer()