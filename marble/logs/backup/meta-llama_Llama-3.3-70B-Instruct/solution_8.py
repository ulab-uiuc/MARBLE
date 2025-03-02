import bcrypt
class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.role = role# solution.py
import datetime
import matplotlib.pyplot as plt

# User class to store user information
class User:import bcrypt; self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())self.role = role

# Budget class to store budget information
class Budget:
    def __init__(self):
class DuplicateUsernameError(Exception):
        pass
        """
        Initialize a Budget object.
        """
        self.income = []
        self.expenses = []
        self.goals = []

    def add_income(self, amount, category, description):
        """
        Add income to the budget.

        Args:
        amount (float): The amount of income.
        category (str): The category of income (e.g., 'salary', 'investment').
        description (str): A description of the income.
        """
        self.income.append({'amount': amount, 'category': category, 'description': description})

    def add_expense(self, amount, category, description):
        """
        Add an expense to the budget.

        Args:
        amount (float): The amount of the expense.
        category (str): The category of the expense (e.g., 'housing', 'food').
        description (str): A description of the expense.
        """
        self.expenses.append({'amount': amount, 'category': category, 'description': description})

    def add_goal(self, goal, target_amount):
        """
        Add a financial goal to the budget.

        Args:
        goal (str): The financial goal (e.g., 'save for a house', 'pay off debt').
        target_amount (float): The target amount for the goal.
        """
        self.goals.append({'goal': goal, 'target_amount': target_amount})

    def get_budget_breakdown(self):
        """
        Get a breakdown of the budget.

        Returns:
        dict: A dictionary containing the total income, total expenses, and remaining balance.
        """
        total_income = sum([i['amount'] for i in self.income])
        total_expenses = sum([e['amount'] for e in self.expenses])
        remaining_balance = total_income - total_expenses
        return {'total_income': total_income, 'total_expenses': total_expenses, 'remaining_balance': remaining_balance}

    def get_expense_categories(self):
        """
        Get a list of expense categories.

        Returns:
        list: A list of unique expense categories.
        """
        categories = [e['category'] for e in self.expenses]
        return list(set(categories))

    def get_expense_amounts(self):
        """
        Get a list of expense amounts.

        Returns:
        list: A list of expense amounts.
        """
        amounts = [e['amount'] for e in self.expenses]
        return amounts

# Chat class to store chat messages
class Chat:
    def __init__(self):
        """
        Initialize a Chat object.
        """
        self.messages = []

    def add_message(self, user, message):
        """
        Add a message to the chat.

        Args:
        user (User): The user who sent the message.
        message (str): The message.
        """
        self.messages.append({'user': user.username, 'message': message})

# BudgetCollaborator class to manage the budget and chat
class BudgetCollaborator:
    def __init__(self):
        """
        Initialize a BudgetCollaborator object.
        """
        self.users = []
        self.budget = Budget()
        self.chat = Chat()

    def add_user(self, user):if user.username in [u.username for u in self.users]:
            raise DuplicateUsernameError('Username already exists')def login(self, username, password):
self.users.append(user)for user in self.users:
            if user.username == username and bcrypt.checkpw(password.encode('utf-8'), user.password):
                return userreturn None

    def get_budget(self):
        """
        Get the current budget.

        Returns:
        Budget: The current budget.
        """
        return self.budget

    def get_chat(self):
        """
        Get the current chat.

        Returns:
        Chat: The current chat.
        """
        return self.chat

# Create a BudgetCollaborator object
budget_collaborator = BudgetCollaborator()

# Create some users
user1 = User('user1', 'password1', 'admin')
user2 = User('user2', 'password2', 'user')

# Add the users to the system
budget_collaborator.add_user(user1)
budget_collaborator.add_user(user2)

# Login as user1
logged_in_user = budget_collaborator.login('user1', 'password1')

# Add some income and expenses to the budget
budget_collaborator.get_budget().add_income(1000, 'salary', 'Monthly salary')
budget_collaborator.get_budget().add_expense(500, 'housing', 'Rent')
budget_collaborator.get_budget().add_expense(200, 'food', 'Groceries')

# Add a financial goal to the budget
budget_collaborator.get_budget().add_goal('save for a house', 10000)

# Get the budget breakdown
budget_breakdown = budget_collaborator.get_budget().get_budget_breakdown()
print('Budget Breakdown:')
print(f'Total Income: {budget_breakdown["total_income"]}')
print(f'Total Expenses: {budget_breakdown["total_expenses"]}')
print(f'Remaining Balance: {budget_breakdown["remaining_balance"]}')

# Get the expense categories and amounts
expense_categories = budget_collaborator.get_budget().get_expense_categories()
expense_amounts = budget_collaborator.get_budget().get_expense_amounts()
print('Expense Categories:')
print(expense_categories)
print('Expense Amounts:')
print(expense_amounts)

# Create a pie chart to visualize the expense categories
plt.pie(expense_amounts, labels=expense_categories, autopct='%1.1f%%')
plt.title('Expense Categories')
plt.show()

# Add some messages to the chat
budget_collaborator.get_chat().add_message(user1, 'Hello, how are you?')
budget_collaborator.get_chat().add_message(user2, 'I am good, thanks. How about you?')

# Get the chat messages
chat_messages = budget_collaborator.get_chat().messages
print('Chat Messages:')
for message in chat_messages:
    print(f'{message["user"]}: {message["message"]}')