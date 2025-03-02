class User:
    def __init__(self, name):
        self.name = name
        self.expenses = {}
        self.budget = {}
    
    def add_expense(self, category, amount):
        if category in self.expenses:
            self.expenses[category] += amount
        else:
            self.expenses[category] = amount
    
    def set_budget(self, category, limit):
        self.budget[category] = limit


class MultiAgentBudgetOptimizer:
    def __init__(self):
        self.users = {}
    
    def add_user(self, user):
        self.users[user.name] = user
    
    def get_total_expenses(self):
        total_expenses = {}
        for user in self.users.values():
            for category, amount in user.expenses.items():
                if category in total_expenses:
                    total_expenses[category] += amount
                else:
                    total_expenses[category] = amount
        return total_expenses
    
    def get_remaining_budget(self):
        total_budget = {}
        for user in self.users.values():
            for category, limit in user.budget.items():
                if category in total_budget:
                    total_budget[category] += limit
                else:
                    total_budget[category] = limit
        
        total_expenses = self.get_total_expenses()
        remaining_budget = {}
        for category, limit in total_budget.items():
            total_expense = total_expenses.get(category, 0)
            remaining_budget[category] = limit - total_expense
        
        return remaining_budget
    
    def get_individual_contributions(self):
        individual_contributions = {}
        total_expenses = self.get_total_expenses()
        for user in self.users.values():
            total_expense = sum(user.expenses.values())
            individual_contributions[user.name] = total_expense
        return individual_contributions
    
    def suggest_optimization(self):
        total_expenses = self.get_total_expenses()
        remaining_budget = self.get_remaining_budget()
        optimization_suggestions = {}
        for category, limit in remaining_budget.items():
            total_expense = total_expenses.get(category, 0)
            if total_expense > limit:
                optimization_suggestions[category] = f"Reduce expenses in {category} to stay within budget."
            else:
                optimization_suggestions[category] = f"You have remaining budget in {category}."
        return optimization_suggestions


# Test cases
def run_tests():
    user1 = User("Alice")
    user1.add_expense("Groceries", 100)
    user1.add_expense("Entertainment", 50)
    user1.set_budget("Groceries", 200)
    user1.set_budget("Entertainment", 100)
    
    user2 = User("Bob")
    user2.add_expense("Groceries", 150)
    user2.add_expense("Utilities", 80)
    user2.set_budget("Groceries", 300)
    user2.set_budget("Utilities", 100)
    
    optimizer = MultiAgentBudgetOptimizer()
    optimizer.add_user(user1)
    optimizer.add_user(user2)
    
    # Test financial summaries
    assert optimizer.get_total_expenses() == {'Groceries': 250, 'Entertainment': 50, 'Utilities': 80}
    assert optimizer.get_remaining_budget() == {'Groceries': 50, 'Entertainment': 50, 'Utilities': 20}
    assert optimizer.get_individual_contributions() == {'Alice': 150, 'Bob': 230}
    
    # Test optimization suggestions
    assert optimizer.suggest_optimization() == {'Groceries': 'You have remaining budget in Groceries.', 'Entertainment': 'You have remaining budget in Entertainment.', 'Utilities': 'You have remaining budget in Utilities.'}
    
    print("All tests passed successfully!")

    # Test edge cases and invalid inputs
assert optimizer.suggest_optimization() == {'Groceries': 'Reduce expenses in Groceries to stay within budget.', 'Entertainment': 'Reduce expenses in Entertainment to stay within budget.', 'Utilities': 'Reduce expenses in Utilities to stay within budget.'}
    user5 = User("Eve")
    user5.add_expense("Groceries", -50)
    user5.add_expense("Entertainment", 0)
    user5.set_budget("Groceries", 100)
    user5.set_budget("Entertainment", 50)
    
    user6 = User("Frank")
    user6.add_expense("Groceries", 150)
    user6.add_expense("Utilities", 120)
    user6.set_budget("Groceries", 200)
    user6.set_budget("Utilities", 100)
    
    optimizer.add_user(user5)
    optimizer.add_user(user6)
    
    assert optimizer.get_total_expenses() == {'Groceries': 50, 'Entertainment': 0, 'Utilities': 120}
    assert optimizer.get_remaining_budget() == {'Groceries': 50, 'Entertainment': 50, 'Utilities': -20}
    assert optimizer.get_individual_contributions() == {'Alice': 150, 'Bob': 230, 'Eve': -50, 'Frank': 270}
    assert optimizer.suggest_optimization() == {'Groceries': 'Reduce expenses in Groceries to stay within budget.', 'Entertainment': 'You have remaining budget in Entertainment.', 'Utilities': 'Reduce expenses in Utilities to stay within budget.'}


if __name__ == "__main__":
    run_tests()
    # Test edge cases and invalid inputs
    user3 = User("Charlie")
    user3.add_expense("Groceries", 300)
    user3.add_expense("Entertainment", 120)
    user3.set_budget("Groceries", 200)
    user3.set_budget("Entertainment", 100)
    
    user4 = User("David")
    user4.add_expense("Groceries", 250)
    user4.add_expense("Utilities", 120)
    user4.set_budget("Groceries", 300)
    user4.set_budget("Utilities", 100)
    
    optimizer.add_user(user3)
    optimizer.add_user(user4)
    
    assert optimizer.get_total_expenses() == {'Groceries': 800, 'Entertainment': 190, 'Utilities': 200}
    assert optimizer.get_remaining_budget() == {'Groceries': -50, 'Entertainment': -90, 'Utilities': -20}
    assert optimizer.get_individual_contributions() == {'Alice': 150, 'Bob': 230, 'Charlie': 420, 'David': 370}
    assert optimizer.suggest_optimization() == {'Groceries': 'Reduce expenses in Groceries to stay within budget.', 'Entertainment': 'Reduce expenses in Entertainment to stay within budget.', 'Utilities': 'Reduce expenses in Utilities to stay within budget.'}
