# solution.py

class User:
    """Represents a user with a name and expenses."""
    
    def __init__(self, name):
        self.name = name
        self.expenses = {}
        self.budget = {}

    def add_expense(self, category, amount):
        """Adds an expense to the user's expenses."""
        if category in self.expenses:
            self.expenses[category] += amount
        else:
            self.expenses[category] = amount

    def view_budget(self):
        """Displays the user's budget."""
        return self.expenses

    def set_budget(self, category, amount):
        """Sets the user's budget for a category."""
        self.budget[category] = amount

    def view_budget_limit(self):
        """Displays the user's budget limit."""
        return self.budget


class MultiAgentBudgetOptimizer:
    """Represents a multi-agent budget optimizer with multiple users."""
    
    def __init__(self):
        self.users = {}

    def add_user(self, name):
        """Adds a user to the optimizer."""
        self.users[name] = User(name)

    def view_total_expenses(self):
        """Displays the total expenses of all users."""
        total_expenses = 0
        for user in self.users.values():
            for category, amount in user.expenses.items():
                total_expenses += amount
        return total_expenses

    def view_remaining_budget(self):
        """Displays the remaining budget of all users."""
        total_budget = 0
        for user in self.users.values():
            for category, amount in user.budget.items():
                total_budget += amount
        return total_budget - self.view_total_expenses()

    def view_individual_contributions(self):
        """Displays the individual contributions of all users."""
        contributions = {}
        for user in self.users.values():
            contributions[user.name] = self.view_total_expenses() / len(self.users)
        return contributions

    def optimize_spending(self):
        """Suggests ways to reduce expenses or reallocate funds."""
        suggestions = {}
        for user in self.users.values():
            for category, amount in user.expenses.items():
                if amount > user.budget.get(category, 0):
                    suggestions[category] = f"Reduce expenses in {category} by {amount - user.budget.get(category, 0)}"
        return suggestions


def test_multi_agent_budget_optimizer():
    """Tests the multi-agent budget optimizer."""
    optimizer = MultiAgentBudgetOptimizer()
    optimizer.add_user("Alice")
    optimizer.add_user("Bob")
    optimizer.users["Alice"].add_expense("Groceries", 100)
    optimizer.users["Bob"].add_expense("Entertainment", 200)
    optimizer.users["Alice"].set_budget("Groceries", 150)
    optimizer.users["Bob"].set_budget("Entertainment", 250)
    print("Total Expenses:", optimizer.view_total_expenses())
    print("Remaining Budget:", optimizer.view_remaining_budget())
    print("Individual Contributions:", optimizer.view_individual_contributions())
    print("Optimization Suggestions:", optimizer.optimize_spending())


if __name__ == "__main__":
    test_multi_agent_budget_optimizer()