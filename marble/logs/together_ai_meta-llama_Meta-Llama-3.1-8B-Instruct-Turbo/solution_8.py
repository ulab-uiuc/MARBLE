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

    def add_income(self, category, amount):
        self.income[category] = amount

    def add_expense(self, category, amount):
        self.expenses[category] = amount

    def add_goal(self, category, target):
        self.goals[category] = target

    def add_note(self, category, note):
        self.notes[category] = note

    def get_budget_breakdown(self):
        breakdown = {}
        for category, amount in self.income.items():
            breakdown[category] = amount
        for category, amount in self.expenses.items():
            breakdown[category] = -amount
        return breakdown

    def get_adaptive_feedback(self):
        feedback = []
        for category, amount in self.expenses.items():
            if amount > 0:
                feedback.append(f"Over-spent in {category} by ${amount}")
        return feedback


# goal.py
class Goal:
    def __init__(self, category, target):
        self.category = category
        self.target = target

    def __str__(self):
        return f"Goal: {self.category} - Target: ${self.target}"


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
        self.budget = Budget()
        self.chat = Chat()

    def add_user(self, user):
        self.users[user.id] = user

    def login_user(self, username, password):
        for user in self.users.values():
            if user.username == username and user.password == password:
                return user
        return None

    def update_budget(self, user, category, amount):
        if user.role == "admin":
            self.budget.add_income(category, amount)
        else:
            self.budget.add_expense(category, amount)

    def get_budget_breakdown(self):
        return self.budget.get_budget_breakdown()

    def get_adaptive_feedback(self):
        return self.budget.get_adaptive_feedback()

    def add_goal(self, user, category, target):
        if user.role == "admin":
            self.budget.add_goal(category, target)

    def get_goals(self):
        return self.budget.goals

    def send_message(self, sender, message):
        self.chat.send_message(sender, message)

    def get_messages(self):
        return self.chat.get_messages()


# main.py
def main():
    collaborator = BudgetCollaborator()

    user1 = User(1, "john", "password", "admin")
    user2 = User(2, "jane", "password", "user")

    collaborator.add_user(user1)
    collaborator.add_user(user2)

    user1_logged_in = collaborator.login_user("john", "password")
    user2_logged_in = collaborator.login_user("jane", "password")

    if user1_logged_in and user2_logged_in:
        print("Both users logged in successfully")

        collaborator.update_budget(user1_logged_in, "rent", 1000)
        collaborator.update_budget(user2_logged_in, "rent", 500)

        print("Budget breakdown:")
        for category, amount in collaborator.get_budget_breakdown().items():
            print(f"{category}: ${amount}")

        print("Adaptive feedback:")
        for message in collaborator.get_adaptive_feedback():
            print(message)

        collaborator.add_goal(user1_logged_in, "savings", 1000)
        print("Goals:")
        for goal in collaborator.get_goals().values():
            print(goal)

        collaborator.send_message(user1_logged_in, "Hello, Jane!")
        collaborator.send_message(user2_logged_in, "Hi, John!")

        print("Chat messages:")
        for message in collaborator.get_messages():
            print(f"{message[0]}: {message[1]}")

    else:
        print("Failed to log in")

if __name__ == "__main__":
    main()