# BudgetCollaborator - Collaborative Budgeting System

class User:
    def __init__(self):
        self.categories = {}
        self.goal = 0
        self.transactions = []

    def update(self, category, amount):
        if category in self.categories:
            self.categories[category] += amount
        else:
            self.categories[category] = amount

    def set_goal(self, goal_amount):
        self.goal = goal_amount

    def add_transaction(self, amount, category, transaction_type, description):
        self.transactions.append({
            "amount": amount,
            "category": category,
            "type": transaction_type,
            "description": description
        })
    def __init__(self, username, role):
        self.username = username
        self.role = role
        self.budget = Budget()
    
    def update_budget(self, category, amount):
        self.budget.update(category, amount)
    
    def set_goal(self, goal_amount):
        self.budget.set_goal(goal_amount)
    
    def add_income(self, amount, category, description=""):
        self.budget.add_transaction(amount, category, "income", description)
    
    def add_expense(self, amount, category, description=""):
        self.budget.add_transaction(amount, category, "expense", description)


class Budget:
    def __init__(self):


class RealTimeSync:
    def __init__(self):
        # Initialize real-time synchronization mechanism
        pass

    def synchronize_data(self, data):
        # Synchronize budget data across all connected users
        pass
        self.categories = {}
        self.goal = 0
        self.transactions = []
    
    def update(self, category, amount):
        if category in self.categories:
            self.categories[category] += amount
        else:
            self.categories[category] = amount
    
    def set_goal(self, goal_amount):
        self.goal = goal_amount
    
    def add_transaction(self, amount, category, transaction_type, description):
        self.transactions.append({
            "amount": amount,
            "category": category,
            "type": transaction_type,
            "description": description
        })


class BudgetCollaborator:
    def __init__(self):
        self.users = {}
    
    def add_user(self, username, role):
        self.real_time_sync = RealTimeSync()
self.real_time_sync = RealTimeSync()
        if username not in self.users:
            self.users[username] = User(username, role)
    
    def get_user(self, username):
        return self.users.get(username, None)
    
    def update_budget(self, username, category, amount):
        user = self.get_user(username)
        if user:
            user.update_budget(category, amount)
    
    def set_goal(self, username, goal_amount):
        user = self.get_user(username)
        if user:
            user.set_goal(goal_amount)
    
    def add_income(self, username, amount, category, description=""):
        user = self.get_user(username)
        if user:
            user.add_income(amount, category, description)
    
    def add_expense(self, username, amount, category, description=""):
        user = self.get_user(username)
        if user:
            user.add_expense(amount, category, description)


# Example Usage
budget_system = BudgetCollaborator()

budget_system.add_user("Alice", "admin")
budget_system.add_user("Bob", "user")

budget_system.update_budget("Alice", "Groceries", 100)
budget_system.update_budget("Bob", "Entertainment", 50)

budget_system.set_goal("Alice", 500)

budget_system.add_income("Alice", 2000, "Salary", "Monthly income")
budget_system.add_expense("Bob", 100, "Dining", "Dinner with friends")