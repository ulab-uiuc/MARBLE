# user.py
class User:
    def __init__(self, id, name, email, password, permissions):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.permissions = permissions
        self.budgets = []

    def add_budget(self, budget):
        self.budgets.append(budget)

    def remove_budget(self, budget):
        self.budgets.remove(budget)


# budget.py
class Budget:
    def __init__(self, id, name, goals, categories):
        self.id = id
        self.name = name
        self.goals = goals
        self.categories = categories
        self.users = []

    def add_user(self, user, permission):
        self.users.append((user, permission))

    def remove_user(self, user):
        self.users = [(u, p) for u, p in self.users if u != user]


# dashboard.py
class Dashboard:
    def __init__(self):
        self.income = 0
        self.expenses = 0
        self.budget = 0
        self.goals = {}

    def update_income(self, amount):
        self.income += amount

    def update_expenses(self, amount):
        self.expenses += amount

    def update_budget(self, amount):
        self.budget += amount

    def update_goal(self, category, amount):
        if category in self.goals:
            self.goals[category] += amount
        else:
            self.goals[category] = amount


# notification.py
class Notification:
    def __init__(self, message, user):
        self.message = message
        self.user = user

    def send_notification(self):
        print(f"Notification sent to {self.user.name}: {self.message}")


# feedback.py
class Feedback:
    def __init__(self, message, user):
        self.message = message
        self.user = user

    def send_feedback(self):
        print(f"Feedback received from {self.user.name}: {self.message}")


# solution.py
class BudgetSync:
    def __init__(self):
        self.users = []
        self.budgets = []
        self.dashboard = Dashboard()

    def create_user(self, id, name, email, password, permissions):
        user = User(id, name, email, password, permissions)
        self.users.append(user)
        return user

    def create_budget(self, id, name, goals, categories):
        budget = Budget(id, name, goals, categories)
        self.budgets.append(budget)
        return budget

    def add_user_to_budget(self, user, budget, permission):
        budget.add_user(user, permission)
        user.add_budget(budget)

    def remove_user_from_budget(self, user, budget):
        budget.remove_user(user)
        user.remove_budget(budget)

    def update_dashboard(self, income, expenses, budget):
        self.dashboard.update_income(income)
        self.dashboard.update_expenses(expenses)
        self.dashboard.update_budget(budget)

    def update_budget_goal(self, category, amount):
        self.dashboard.update_goal(category, amount)

    def send_notification(self, message, user):
        notification = Notification(message, user)
        notification.send_notification()

    def send_feedback(self, message, user):
        feedback = Feedback(message, user)
        feedback.send_feedback()


# main.py
def main():
    budget_sync = BudgetSync()

    # Create users
    user1 = budget_sync.create_user(1, "John Doe", "john@example.com", "password123", ["view-only", "edit"])
    user2 = budget_sync.create_user(2, "Jane Doe", "jane@example.com", "password123", ["view-only"])

    # Create budget
    budget = budget_sync.create_budget(1, "Family Budget", ["save $1000", "spend $500"], ["income", "expenses"])

    # Add users to budget
    budget_sync.add_user_to_budget(user1, budget, "view-only")
    budget_sync.add_user_to_budget(user2, budget, "view-only")

    # Update dashboard
    budget_sync.update_dashboard(1000, 500, 500)
    budget_sync.update_budget_goal("income", 1000)

    # Send notification
    budget_sync.send_notification("Budget goal reached!", user1)

    # Send feedback
    budget_sync.send_feedback("Great app!", user2)


if __name__ == "__main__":
    main()