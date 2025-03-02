# budget_sync.py

class User:
    """Represents a user with a unique profile and permissions to access shared budgets."""
    
    def __init__(self, username, password, email):
        """
        Initializes a User object.

        Args:
            username (str): The username chosen by the user.
            password (str): The password chosen by the user.
            email (str): The email address of the user.
        """
        self.username = username
        self.password = password
        self.email = email
        self.budgets = []  # List of Budget objects the user is a part of

    def add_budget(self, budget):
        """Adds a budget to the user's list of budgets."""
        self.budgets.append(budget)


class Budget:
    """Represents a shared budget with its own set of goals and categories."""
    
    def __init__(self, name, owner):
        """
        Initializes a Budget object.

        Args:
            name (str): The name of the budget.
            owner (User): The owner of the budget.
        """
        self.name = name
        self.owner = owner
        self.users = [owner]  # List of User objects with access to the budget
        self.income = 0
        self.expenses = {}  # Dictionary of expense categories and amounts
        self.goals = {}  # Dictionary of budget goals and targets

    def add_user(self, user, access_level):
        """
        Adds a user to the budget with a specified access level.

        Args:
            user (User): The user to add to the budget.
            access_level (str): The access level of the user (e.g., 'view-only', 'edit').
        """
        self.users.append(user)
        user.add_budget(self)

    def update_income(self, amount):
        """Updates the budget's income."""
        self.income = amount

    def add_expense(self, category, amount):
        """Adds an expense to the budget."""
        if category in self.expenses:
            self.expenses[category] += amount
        else:
            self.expenses[category] = amount

    def add_goal(self, goal, target):
        """Adds a budget goal to the budget."""
        self.goals[goal] = target


class Dashboard:
    """Represents a shared dashboard for tracking income, expenses, and budget goals."""
    
    def __init__(self, budget):
        """
        Initializes a Dashboard object.

        Args:
            budget (Budget): The budget associated with the dashboard.
        """
        self.budget = budget

    def display_budget(self):
        """Displays the budget's income, expenses, and goals."""
        print(f"Income: {self.budget.income}")
        print("Expenses:")
        for category, amount in self.budget.expenses.items():
            print(f"{category}: {amount}")
        print("Goals:")
        for goal, target in self.budget.goals.items():
            print(f"{goal}: {target}")


class NotificationSystem:
    """Represents a notification system that alerts users to important budget updates."""
    
    def __init__(self):
        self.notifications = []  # List of notification messages

    def send_notification(self, message):
        """Sends a notification to all users."""
        self.notifications.append(message)
        print(f"Notification: {message}")


class FeedbackMechanism:
    """Represents a feedback mechanism where users can provide input on the application's performance."""
    
    def __init__(self):
        self.feedback = []  # List of feedback messages

    def submit_feedback(self, message):
        """Submits feedback from a user."""
        self.feedback.append(message)
        print(f"Feedback: {message}")


# Example usage:

# Create users
user1 = User("john", "password123", "john@example.com")
user2 = User("jane", "password456", "jane@example.com")

# Create a budget
budget = Budget("Household Budget", user1)

# Add users to the budget
budget.add_user(user2, "edit")

# Update income and expenses
budget.update_income(5000)
budget.add_expense("Rent", 1500)
budget.add_expense("Groceries", 500)

# Add budget goals
budget.add_goal("Save for a down payment", 20000)

# Display the budget
dashboard = Dashboard(budget)
dashboard.display_budget()

# Send notifications
notification_system = NotificationSystem()
notification_system.send_notification("Budget goal reached: Save for a down payment")

# Submit feedback
feedback_mechanism = FeedbackMechanism()
feedback_mechanism.submit_feedback("The application is very user-friendly, but it would be great to have more visualization options.")