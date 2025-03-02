# user.py
class User:
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
        self.budget = Budget()

    def __str__(self):
        return f"User {self.username} ({self.role})"


# budget.py
class Budget:
    def __init__(self):
        self.income = {}
        self.expenses = {}
        self.goals = {}
        self.notes = {}

    def add_income(self, category, amount, note=""):
        self.income[category] = {"amount": amount, "note": note}

    def add_expense(self, category, amount, note=""):
        self.expenses[category] = {"amount": amount, "note": note}

    def add_goal(self, category, target_amount, note=""):
        self.goals[category] = {"target_amount": target_amount, "note": note}

    def add_note(self, category, note):
        self.notes[category] = note

    def get_budget_breakdown(self):
        income_total = sum(amount for amount in self.income.values())
        expense_total = sum(amount for amount in self.expenses.values())
        return {"income": income_total, "expenses": expense_total}

    def get_adaptive_feedback(self):
        feedback = []
        for category, expense in self.expenses.items():
            if expense["amount"] > 0.8 * sum(amount for amount in self.income.values()):
                feedback.append(f"Category {category} is consistently over-spent. Consider cutting costs or reallocating funds.")
        return feedback


# goal.py
class Goal:
    def __init__(self, category, target_amount, note=""):
        self.category = category
        self.target_amount = target_amount
        self.note = note

    def __str__(self):
        return f"Goal: {self.category} - Target Amount: {self.target_amount}"


# chat.py
class Chat:
    def __init__(self):
        self.messages = []

    def send_message(self, sender, message):
        self.messages.append((sender, message))

    def get_messages(self):
        return self.messages


# solution.py
class BudgetCollaborator:
    def __init__(self):
        self.users = {}
        self.chat = Chat()

    def add_user(self, id, username, password, role):
        self.users[id] = User(id, username, password, role)

    def login(self, id, password):
        if id in self.users and self.users[id].password == password:
            return self.users[id]
        return None

    def update_budget(self, user_id, category, amount, note=""):
        user = self.users[user_id]
        user.budget.add_income(category, amount, note)

    def get_budget_breakdown(self, user_id):
        user = self.users[user_id]
        return user.budget.get_budget_breakdown()

    def get_adaptive_feedback(self, user_id):
        user = self.users[user_id]
        return user.budget.get_adaptive_feedback()

    def add_goal(self, user_id, category, target_amount, note=""):
        user = self.users[user_id]
        user.budget.add_goal(category, target_amount, note)

    def send_message(self, sender_id, recipient_id, message):
        sender = self.users[sender_id]
        recipient = self.users[recipient_id]
        self.chat.send_message(sender, message)
        self.chat.send_message(recipient, message)

    def get_messages(self, user_id):
        user = self.users[user_id]
        return self.chat.get_messages()


# main.py
def main():
    budget_collaborator = BudgetCollaborator()

    # Add users
    budget_collaborator.add_user(1, "John", "password123", "admin")
    budget_collaborator.add_user(2, "Jane", "password456", "user")

    # Login users
    user1 = budget_collaborator.login(1, "password123")
    user2 = budget_collaborator.login(2, "password456")

    # Update budget
    budget_collaborator.update_budget(1, "Income", 1000)
    budget_collaborator.update_budget(2, "Expense", 500)

    # Get budget breakdown
    print(budget_collaborator.get_budget_breakdown(1))

    # Get adaptive feedback
    print(budget_collaborator.get_adaptive_feedback(1))

    # Add goal
    budget_collaborator.add_goal(1, "Savings", 1000)

    # Send message
    budget_collaborator.send_message(1, 2, "Hello, Jane!")

    # Get messages
    print(budget_collaborator.get_messages(2))


if __name__ == "__main__":
    main()