class User:
    """Represents a user with a name and expenses."""
    def __init__(self, name):
        self.name = name
        self.expenses = {}
    def add_expense(self, category, amount):
        if amount < 0:
            raise ValueError("Expense amount cannot be negative")
        if category in self.expenses:
            self.expenses[category] += amount
        else:
            self.expenses[category] = amount    """Represents a user with a name and expenses."""
    def __init__(self, name):
    def get_expenses(self):
        # Return the user's expenses dictionary
        return self.expenses


class BudgetOptimizer:
    """Represents a budget optimizer with multiple users and budget limits."""
    def __init__(self):
    def calculate_average_spending(self, category):
        total_expenses = 0
        for user in self.users:
            if category in user.get_expenses():
                total_expenses += user.get_expenses()[category]
        return total_expenses / len(self.users)
        # Initialize the budget optimizer with an empty list of users and an empty dictionary to store budget limits
        self.users = []
        self.budget_limits = {}

    def add_user(self, user):
        # Add a user to the list of users
        self.users.append(user)

    def set_budget_limit(self, category, limit):
        # Set a budget limit for a category
        self.budget_limits[category] = limit

    def get_total_expenses(self):
        # Calculate the total expenses of all users
        total_expenses = {}
        for user in self.users:
            for category, amount in user.get_expenses().items():
                if category in total_expenses:
                    total_expenses[category] += amount
                else:
                    total_expenses[category] = amount
        return total_expenses

    def get_remaining_budget(self):def optimize_spending(self):
        suggestions = {}
        for category, limit in self.budget_limits.items():
            if category in self.get_total_expenses() and self.get_total_expenses()[category] > limit:
                suggestions[category] = f'Reduce expenses in {category} by {self.get_total_expenses()[category] - limit}'
            elif category in self.get_total_expenses() and self.get_total_expenses()[category] < limit:
                surplus = limit - self.get_total_expenses()[category]
                suggestions[category] = f'Reallocate {surplus} from {category} to other categories'
        for user in self.users:
            user_expenses = user.get_expenses()
            for category, amount in user_expenses.items():
                if category in self.budget_limits and amount > self.budget_limits[category] / len(self.users):
                    suggestions[category] = f'{user.name} can cut back on {category} by {amount - self.budget_limits[category] / len(self.users)}'
        return suggestions    def optimize_spending(self):
        # Suggest ways to reduce expenses or reallocate funds to meet the group's financial goals
        suggestions = []
        for category, limit in self.budget_limits.items():
            if category in self.get_total_expenses() and self.get_total_expenses()[category] > limit:
                suggestions.append(f"Reduce expenses in {category} by {self.get_total_expenses()[category] - limit}")
        return suggestions


class Dashboard:
    """Represents a dashboard that displays a summary of the group's financial status."""
    def __init__(self, budget_optimizer):
        # Initialize the dashboard with a budget optimizer
        self.budget_optimizer = budget_optimizer

    def display_summary(self):
        # Display a summary of the group's financial status
        print("Total Expenses:")
        for category, amount in self.budget_optimizer.get_total_expenses().items():
            print(f"{category}: {amount}")
        print("Remaining Budget:")
        for category, amount in self.budget_optimizer.get_remaining_budget().items():
            print(f"{category}: {amount}")
        print("Suggestions:")
        for suggestion in self.budget_optimizer.optimize_spending():
            print(suggestion)


# Test cases
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
    # Test displaying financial summaries for a group
    budget_optimizer = BudgetOptimizer()
    user1 = User("John")
    user1.add_expense("groceries", 100)
    user1.add_expense("entertainment", 200)
    user2 = User("Jane")
    user2.add_expense("groceries", 150)
    user2.add_expense("entertainment", 250)
    budget_optimizer.add_user(user1)
    budget_optimizer.add_user(user2)
    budget_optimizer.set_budget_limit("groceries", 500)
    budget_optimizer.set_budget_limit("entertainment", 1000)
    dashboard = Dashboard(budget_optimizer)
    dashboard.display_summary()

def test_optimizing_spending():
    # Test optimizing spending for a group
    budget_optimizer = BudgetOptimizer()
    user1 = User("John")
    user1.add_expense("groceries", 100)
    user1.add_expense("entertainment", 200)
    user2 = User("Jane")
    user2.add_expense("groceries", 150)
    user2.add_expense("entertainment", 250)
    budget_optimizer.add_user(user1)
    budget_optimizer.add_user(user2)
    budget_optimizer.set_budget_limit("groceries", 500)
    budget_optimizer.set_budget_limit("entertainment", 1000)
    assert budget_optimizer.optimize_spending() == []

def test_handling_invalid_inputs():
    # Test handling invalid inputs for a user
    user = User("John")
    try:
        user.add_expense("groceries", -100)
        assert False
    except ValueError:
        assert True

def test_exceeding_budget_limits():
    # Test exceeding budget limits for a category
    budget_optimizer = BudgetOptimizer()
    user1 = User("John")
    user1.add_expense("groceries", 100)
    user1.add_expense("entertainment", 200)
    user2 = User("Jane")
    user2.add_expense("groceries", 150)
    user2.add_expense("entertainment", 250)
    budget_optimizer.add_user(user1)
    budget_optimizer.add_user(user2)
    budget_optimizer.set_budget_limit("groceries", 500)
    budget_optimizer.set_budget_limit("entertainment", 1000)
    assert budget_optimizer.optimize_spending() == []

def test_managing_multiple_users():
    # Test managing multiple users with different spending patterns
    budget_optimizer = BudgetOptimizer()
    user1 = User("John")
    user1.add_expense("groceries", 100)
    user1.add_expense("entertainment", 200)
    user2 = User("Jane")
    user2.add_expense("groceries", 150)
    user2.add_expense("entertainment", 250)
    user3 = User("Bob")
    user3.add_expense("groceries", 200)
    user3.add_expense("entertainment", 300)
    budget_optimizer.add_user(user1)
    budget_optimizer.add_user(user2)
    budget_optimizer.add_user(user3)
    budget_optimizer.set_budget_limit("groceries", 500)
    budget_optimizer.set_budget_limit("entertainment", 1000)
    assert budget_optimizer.optimize_spending() == []

# Run test cases
test_inputting_expenses()
test_setting_budget_limits()
test_displaying_financial_summaries()
test_optimizing_spending()
test_handling_invalid_inputs()
test_exceeding_budget_limits()
test_managing_multiple_users()

# Create a budget optimizer and add users
budget_optimizer = BudgetOptimizer()
user1 = User("John")
user1.add_expense("groceries", 100)
user1.add_expense("entertainment", 200)
user2 = User("Jane")
user2.add_expense("groceries", 150)
user2.add_expense("entertainment", 250)
budget_optimizer.add_user(user1)
budget_optimizer.add_user(user2)

# Set budget limits
budget_optimizer.set_budget_limit("groceries", 500)
budget_optimizer.set_budget_limit("entertainment", 1000)

# Create a dashboard and display summary
dashboard = Dashboard(budget_optimizer)
dashboard.display_summary()