# budget_collaborator.py
import datetime
import matplotlib.pyplot as plt

class User:
    """Represents a user in the budgeting system."""
    def __init__(self, username, password, role):
        # Initialize user attributes
        self.username = username
        self.password = password
        self.role = role

class Budget:class Budget:
    """Represents a shared budget in the system."""
    def __init__(self):
        # Initialize budget attributes
        self.income = []
        self.expenses = []
        self.goals = []

    def update_goal_progress(self, amount):
        for goal in self.goals:
            goal['saved_amount'] = goal.get('saved_amount', 0) + amount
    def add_income(self, amount, category, description):
        # Add income to the budget
        self.income.append({"amount": amount, "category": category, "description": description})

    def add_expense(self, amount, category, description):
        # Add expense to the budget
        self.expenses.append({"amount": amount, "category": category, "description": description})

    def set_goal(self, goal, target_amount):
        # Set a financial goal
        self.goals.append({"goal": goal, "target_amount": target_amount})
self.goals[-1]['saved_amount'] = 0

    def get_budget_breakdown(self):
        # Get a breakdown of the budget
        income_total = sum([entry["amount"] for entry in self.income])
        expenses_total = sum([entry["amount"] for entry in self.expenses])
        return income_total, expenses_total

    def get_goal_progress(self):progress = []
        for goal in self.goals:
            if 'saved_amount' not in goal:
                goal['saved_amount'] = 0for goal in self.goals:progress.append({"goal": goal["goal"], "progress": goal.get('saved_amount', 0) / goal["target_amount"]})return progress

class BudgetCollaborator:
    """Represents the budgeting system."""
    def __init__(self):
        # Initialize system attributes
        self.users = []
        self.budgets = []
        self.chat_log = []

    def register_user(self, username, password, role):
        # Register a new user
        self.users.append(User(username, password, role))

    def create_budget(self):
        # Create a new shared budget
        self.budgets.append(Budget())

    def add_income(self, budget_index, amount, category, description):
        # Add income to a budget
        self.budgets[budget_index].add_income(amount, category, description)
self.budgets[budget_index].update_goal_progress(amount)

    def add_expense(self, budget_index, amount, category, description):
        # Add expense to a budget
        self.budgets[budget_index].add_expense(amount, category, description)

    def set_goal(self, budget_index, goal, target_amount):
        # Set a financial goal
        self.budgets[budget_index].set_goal(goal, target_amount)

    def get_budget_breakdown(self, budget_index):
        # Get a breakdown of a budget
        return self.budgets[budget_index].get_budget_breakdown()

    def get_goal_progress(self, budget_index):
        # Get progress towards financial goals
        return self.budgets[budget_index].get_goal_progress()

    def send_message(self, message):
        # Send a message to the chat log
        self.chat_log.append(message)

    def display_chat_log(self):
        # Display the chat log
        for message in self.chat_log:
            print(message)

    def display_budget_breakdown(self, budget_index):
        # Display a breakdown of a budget
        income_total, expenses_total = self.get_budget_breakdown(budget_index)
        print(f"Income: ${income_total}")
        print(f"Expenses: ${expenses_total}")

    def display_goal_progress(self, budget_index):
        # Display progress towards financial goals
        progress = self.get_goal_progress(budget_index)
        for goal in progress:
            print(f"Goal: {goal['goal']}, Progress: {goal['progress']}%")

    def provide_feedback(self, budget_index):
        # Provide adaptive feedback and suggestions
        income_total, expenses_total = self.get_budget_breakdown(budget_index)
        if expenses_total > income_total:
            print("You are overspending. Consider cutting costs or reallocating funds.")
        else:
            print("You are on track with your budget.")

    def visualize_budget(self, budget_index):
        # Visualize a budget breakdown
        income_total, expenses_total = self.get_budget_breakdown(budget_index)
        labels = ["Income", "Expenses"]
        sizes = [income_total, expenses_total]
        plt.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.axis('equal')
        plt.show()

def main():
    # Create a new budgeting system
    system = BudgetCollaborator()

    # Register users
    system.register_user("user1", "password1", "admin")
    system.register_user("user2", "password2", "user")

    # Create a new budget
    system.create_budget()

    # Add income and expenses
    system.add_income(0, 1000, "Salary", "Monthly salary")
    system.add_expense(0, 500, "Rent", "Monthly rent")

    # Set a financial goal
    system.set_goal(0, "Save for a car", 10000)

    # Display budget breakdown
    system.display_budget_breakdown(0)

    # Display goal progress
    system.display_goal_progress(0)

    # Provide feedback
    system.provide_feedback(0)

    # Visualize budget
    system.visualize_budget(0)

    # Send messages
    system.send_message("Hello, how are you?")
    system.send_message("I'm good, thanks!")

    # Display chat log
    system.display_chat_log()

if __name__ == "__main__":
    main()