# BudgetSync - Collaborative Budgeting Application

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.profile = {}  # Personal financial data and permissions
        self.shared_budgets = []  # List of shared budgets the user is part of

    def create_budget(self, budget_name, goals, categories):
        # Create a new shared budget
        budget = Budget(budget_name, goals, categories)
        self.shared_budgets.append(budget)

    def invite_user_to_budget(self, budget, user, access_level):
        # Invite another user to join a shared budget
        budget.invite_user(user, access_level)


class Budget:
    def __init__(self, name, goals, categories):
        self.name = name
        self.goals = goals
        self.categories = categories
        self.users = {}  # Users and their access levels in this budget

    def invite_user(self, user, access_level):
        # Invite a user to join this budget with a specific access level
        self.users[user] = access_level


class Dashboard:
    def __init__(self):def update_income(self, amount, category):        self.expenses += amount
        self.calculate_total_budget()
        if category in self.spending_breakdown:
            self.spending_breakdown[category] += amount
        else:
            self.spending_breakdown[category] = amount
        # Calculate the total budget by subtracting expenses from income
        self.total_budget = self.income - self.expenses

    def set_budget_goals(self, goals):
        # Set budget goals and calculate progress towards those goals
        total_goals = sum(goals.values())
        self.progress = (self.total_budget / total_goals) * 100


# Sample Usage
if __name__ == "__main__":
    # Create users
    user1 = User("Alice", "alice@example.com", "password1")
    user2 = User("Bob", "bob@example.com", "password2")

    # Create a shared budget
    user1.create_budget("Household Budget", {"Savings": 1000, "Groceries": 500}, ["Food", "Utilities"])
    
    # Invite user2 to the shared budget
    user1.invite_user_to_budget(user1.shared_budgets[0], user2, "edit")

    # Update income and expenses on the dashboard
    dashboard = Dashboard()
    dashboard.update_income(3000)
    dashboard.update_expenses(200, "Food")
    dashboard.update_expenses(100, "Utilities")
    dashboard.set_budget_goals({"Savings": 1000, "Groceries": 500})

    # Display dashboard information
    print("Total Budget:", dashboard.total_budget)
    print("Spending Breakdown:", dashboard.spending_breakdown)
    print("Progress towards Budget Goals:", dashboard.progress)