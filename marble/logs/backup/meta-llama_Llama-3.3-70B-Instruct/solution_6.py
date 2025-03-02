# solution.py

class User:
    """Represents a user with a name and expenses."""
    def __init__(self, name):
        # Initialize the user with a name and an empty dictionary to store expenses
        self.name = name
        self.expenses = {}

    def add_expense(self, category, amount):
        # Add an expense to the user's expenses dictionary
        if category in self.expenses:
            self.expenses[category] += amount
        else:
            self.expenses[category] = amount

    def get_expenses(self):
        # Return the user's expenses dictionary
        return self.expenses


class BudgetOptimizer:def set_budget_limit(self, category, limit):
    self.budget_limits[category] = limitdef get_total_expenses(self):def optimize_spending(self):
def get_total_expenses(self):
    total_expenses = {}
    for user in self.users:
        for category, amount in user.get_expenses().items():
            if category in total_expenses:
                total_expenses[category] += amount
            else:
                total_expenses[category] = amount
    return total_expenses
    suggestions = []
    total_expenses = self.get_total_expenses()
    for category, amount in total_expenses.items():
        if category in self.budget_limits and amount > self.budget_limits[category]:
            suggestions.append(f'Reduce expenses in {category} by {amount - self.budget_limits[category]}')
    return suggestionsclass Dashboard:def display_summary(self):
    print("Financial Summary:")
    print("--------------------")
    print("Total Expenses:")
    for category, amount in self.budget_optimizer.get_total_expenses().items():
        print(f"{category}: {amount}")
    print("Remaining Budget:")
    for category, amount in self.budget_optimizer.get_remaining_budget().items():
        print(f"{category}: {amount}")
    print("Suggestions:")
    for suggestion in self.budget_optimizer.optimize_spending():
        print(suggestion)# Test cases
def test_inputting_expenses():
    # Test inputting expenses for a user
    user = User("John")
    user.add_expense("groceries", 100)
    user.add_expense("entertainment", 200)
    assert user.get_expenses() == {"groceries": 100, "entertainment": 200}

def test_setting_budget_limits():
    # Test setting budget limits for a category
    budget_optimizer = BudgetOptimizer()
    budget_optimizer.set_budget_limit("groceries", 500)
    budget_optimizer.set_budget_limit("entertainment", 1000)
    assert budget_optimizer.budget_limits == {"groceries": 500, "entertainment": 1000}

def test_displaying_financial_summaries():
    # Test displaying financial summaries
    budget_optimizer = BudgetOptimizer()
    user1 = User("John")
    user1.add_expense("groceries", 100)
    user1.add_expense("entertainment", 200)
    budget_optimizer.add_user(user1)
    user2 = User("Jane")
    user2.add_expense("groceries", 150)
    user2.add_expense("entertainment", 250)
    budget_optimizer.add_user(user2)
    budget_optimizer.set_budget_limit("groceries", 500)
    budget_optimizer.set_budget_limit("entertainment", 1000)
    dashboard = Dashboard(budget_optimizer)
    dashboard.display_summary()

def test_optimizing_spending():
    # Test optimizing spending
    budget_optimizer = BudgetOptimizer()
    user1 = User("John")
    user1.add_expense("groceries", 100)
    user1.add_expense("entertainment", 200)
    budget_optimizer.add_user(user1)
    user2 = User("Jane")
    user2.add_expense("groceries", 150)
    user2.add_expense("entertainment", 250)
    budget_optimizer.add_user(user2)
    budget_optimizer.set_budget_limit("groceries", 500)
    budget_optimizer.set_budget_limit("entertainment", 1000)
    assert budget_optimizer.optimize_spending() == []

def test_exceeding_budget_limits():
    # Test exceeding budget limits
    budget_optimizer = BudgetOptimizer()
    user1 = User("John")
    user1.add_expense("groceries", 100)
    user1.add_expense("entertainment", 200)
    budget_optimizer.add_user(user1)
    user2 = User("Jane")
    user2.add_expense("groceries", 150)
    user2.add_expense("entertainment", 250)
    budget_optimizer.add_user(user2)
    budget_optimizer.set_budget_limit("groceries", 200)
    budget_optimizer.set_budget_limit("entertainment", 300)
    assert budget_optimizer.optimize_spending() == ["Reduce expenses in groceries by 50", "Reduce expenses in entertainment by 150"]

# Run test cases
test_inputting_expenses()
test_setting_budget_limits()
test_displaying_financial_summaries()
test_optimizing_spending()
test_exceeding_budget_limits()

# Create a budget optimizer and add users
budget_optimizer = BudgetOptimizer()
user1 = User("John")
user1.add_expense("groceries", 100)
user1.add_expense("entertainment", 200)
budget_optimizer.add_user(user1)
user2 = User("Jane")
user2.add_expense("groceries", 150)
user2.add_expense("entertainment", 250)
budget_optimizer.add_user(user2)

# Set budget limits
budget_optimizer.set_budget_limit("groceries", 500)
budget_optimizer.set_budget_limit("entertainment", 1000)

# Create a dashboard and display financial summary
dashboard = Dashboard(budget_optimizer)
dashboard.display_summary()