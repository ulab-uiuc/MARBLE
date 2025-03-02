# budget_buddy.py

# Import required libraries
import sqlite3
from sqlite3 import Error
from datetime import datetime
import matplotlib.pyplot as plt

# Database class to handle database operations
class Database:def create_tables(self):def insert_user(self, name, email):def insert_transaction(self, user_id, date, amount, type, category):def insert_savings_goal(self, user_id, goal, target_amount):def insert_expense_category(self, user_id, category):
    try:
        self.conn.execute("INSERT INTO expense_categories (user_id, category) VALUES (?, ?)", (user_id, category))
        self.conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting expense category: {e}")def get_user_transactions(self, user_id):
        cursor = self.conn.execute("SELECT * FROM financial_transactions WHERE user_id = ?", (user_id,))
        return cursor.fetchall()

    def get_user_savings_goals(self, user_id):
        cursor = self.conn.execute("SELECT * FROM savings_goals WHERE user_id = ?", (user_id,))
        return cursor.fetchall()

    def get_user_expense_categories(self, user_id):
        cursor = self.conn.execute("SELECT * FROM expense_categories WHERE user_id = ?", (user_id,))
        return cursor.fetchall()

# BudgetBuddy class to handle user interactions
class BudgetBuddy:
    def __init__(self, db_name):
        self.db = Database(db_name)

    def create_user(self):
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        self.db.insert_user(name, email)
        print("User created successfully!")

    def add_transaction(self):
        user_id = int(input("Enter your user ID: "))
        date = input("Enter the transaction date (YYYY-MM-DD): ")
        amount = float(input("Enter the transaction amount: "))
        type = input("Enter the transaction type (income/expense): ")
        category = input("Enter the transaction category: ")
        self.db.insert_transaction(user_id, date, amount, type, category)
        print("Transaction added successfully!")

    def add_savings_goal(self):
        user_id = int(input("Enter your user ID: "))
        goal = input("Enter your savings goal: ")
        target_amount = float(input("Enter your target amount: "))
        self.db.insert_savings_goal(user_id, goal, target_amount)
        print("Savings goal added successfully!")

    def add_expense_category(self):
        user_id = int(input("Enter your user ID: "))
        category = input("Enter the expense category: ")
        self.db.insert_expense_category(user_id, category)
        print("Expense category added successfully!")

    def view_transactions(self):
        user_id = int(input("Enter your user ID: "))
        transactions = self.db.get_user_transactions(user_id)
        for transaction in transactions:
            print(transaction)

    def view_savings_goals(self):
        user_id = int(input("Enter your user ID: "))
        savings_goals = self.db.get_user_savings_goals(user_id)
        for savings_goal in savings_goals:
            print(savings_goal)

    def view_expense_categories(self):
        user_id = int(input("Enter your user ID: "))
        expense_categories = self.db.get_user_expense_categories(user_id)
        for expense_category in expense_categories:
            print(expense_category)

    def visualize_expenses(self):
        user_id = int(input("Enter your user ID: "))
        transactions = self.db.get_user_transactions(user_id)
        categories = []
        amounts = []
        for transaction in transactions:
            if transaction[4] not in categories:
                categories.append(transaction[4])
                amounts.append(transaction[3])
            else:
                index = categories.index(transaction[4])
                amounts[index] += transaction[3]
        plt.bar(categories, amounts)
        plt.xlabel("Category")
        plt.ylabel("Amount")
        plt.title("Expenses by Category")
        plt.show()

# Main function
def main():
    db_name = "budget_buddy.db"
    budget_buddy = BudgetBuddy(db_name)
    budget_buddy.db.create_tables()

    while True:
        print("1. Create User")
        print("2. Add Transaction")
        print("3. Add Savings Goal")
        print("4. Add Expense Category")
        print("5. View Transactions")
        print("6. View Savings Goals")
        print("7. View Expense Categories")
        print("8. Visualize Expenses")
        print("9. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            budget_buddy.create_user()
        elif choice == 2:
            budget_buddy.add_transaction()
        elif choice == 3:
            budget_buddy.add_savings_goal()
        elif choice == 4:
            budget_buddy.add_expense_category()
        elif choice == 5:
            budget_buddy.view_transactions()
        elif choice == 6:
            budget_buddy.view_savings_goals()
        elif choice == 7:
            budget_buddy.view_expense_categories()
        elif choice == 8:
            budget_buddy.visualize_expenses()
        elif choice == 9:
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()