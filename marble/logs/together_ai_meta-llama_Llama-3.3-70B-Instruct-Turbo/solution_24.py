# budget_buddy.py
# This is the main implementation of the BudgetBuddy system.

# Import required libraries
import tkinter as tk
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt

# Database schema
class Database:
    def __init__(self, db_name):
        # Connect to the SQLite database
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        
        # Create tables if they do not exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users
            (id INTEGER PRIMARY KEY, name TEXT, email TEXT)
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions
            (id INTEGER PRIMARY KEY, user_id INTEGER, date TEXT, amount REAL, type TEXT)
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS savings_goals
            (id INTEGER PRIMARY KEY, user_id INTEGER, goal TEXT, target_amount REAL)
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expense_categories
            (id INTEGER PRIMARY KEY, user_id INTEGER, category TEXT)
        ''')
        
        # Commit changes
        self.conn.commit()
    
    def insert_user(self, name, email):
        # Insert a new user into the database
        self.cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        self.conn.commit()
    
    def insert_transaction(self, user_id, date, amount, type):
        # Insert a new transaction into the database
        self.cursor.execute('INSERT INTO transactions (user_id, date, amount, type) VALUES (?, ?, ?, ?)', (user_id, date, amount, type))
        self.conn.commit()
    
    def insert_savings_goal(self, user_id, goal, target_amount):
        # Insert a new savings goal into the database
        self.cursor.execute('INSERT INTO savings_goals (user_id, goal, target_amount) VALUES (?, ?, ?)', (user_id, goal, target_amount))
        self.conn.commit()
    
    def insert_expense_category(self, user_id, category):
        # Insert a new expense category into the database
        self.cursor.execute('INSERT INTO expense_categories (user_id, category) VALUES (?, ?)', (user_id, category))
        self.conn.commit()
    
    def get_user_transactions(self, user_id):
        # Retrieve all transactions for a given user
        self.cursor.execute('SELECT * FROM transactions WHERE user_id = ?', (user_id,))
        return self.cursor.fetchall()
    
    def get_user_savings_goals(self, user_id):
        # Retrieve all savings goals for a given user
        self.cursor.execute('SELECT * FROM savings_goals WHERE user_id = ?', (user_id,))
        return self.cursor.fetchall()
    
    def get_user_expense_categories(self, user_id):
        # Retrieve all expense categories for a given user
        self.cursor.execute('SELECT * FROM expense_categories WHERE user_id = ?', (user_id,))
        return self.cursor.fetchall()

# Backend system
class Backend:
    def __init__(self, db):
        # Initialize the backend system with a database connection
        self.db = db
    
    def process_transaction(self, user_id, date, amount, type):
        # Process a new transaction
        self.db.insert_transaction(user_id, date, amount, type)
    
    def process_savings_goal(self, user_id, goal, target_amount):
        # Process a new savings goal
        self.db.insert_savings_goal(user_id, goal, target_amount)
    
    def process_expense_category(self, user_id, category):
        # Process a new expense category
        self.db.insert_expense_category(user_id, category)
    
    def get_user_data(self, user_id):
        # Retrieve all data for a given user
        transactions = self.db.get_user_transactions(user_id)
        savings_goals = self.db.get_user_savings_goals(user_id)
        expense_categories = self.db.get_user_expense_categories(user_id)
        return transactions, savings_goals, expense_categories

# Frontend system
class Frontend:
    def __init__(self, backend):
        # Initialize the frontend system with a backend connection
        self.backend = backend
        self.root = tk.Tk()
        self.root.title("BudgetBuddy")
        
        # Create tabs for different features
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)
        
        self.transaction_tab = ttk.Frame(self.notebook)
        self.savings_goal_tab = ttk.Frame(self.notebook)
        self.expense_category_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.transaction_tab, text="Transactions")
        self.notebook.add(self.savings_goal_tab, text="Savings Goals")
        self.notebook.add(self.expense_category_tab, text="Expense Categories")
        
        # Create transaction tab
        self.transaction_label = ttk.Label(self.transaction_tab, text="Transactions:")
        self.transaction_label.pack()
        
        self.transaction_entry = ttk.Entry(self.transaction_tab)
self.transaction_amount_label = ttk.Label(self.transaction_tab, text="Amount:"); self.transaction_amount_label.pack(); self.transaction_amount_entry = ttk.Entry(self.transaction_tab); self.transaction_amount_entry.pack()
self.transaction_date_label = ttk.Label(self.transaction_tab, text="Date:"); self.transaction_date_label.pack(); self.transaction_date_entry = ttk.Entry(self.transaction_tab); self.transaction_date_entry.pack()
        self.transaction_entry.pack()
        
        self.transaction_button = ttk.Button(self.transaction_tab, text="Add Transaction", command=self.add_transaction)
        self.transaction_button.pack()
        
        # Create savings goal tab
        self.savings_goal_label = ttk.Label(self.savings_goal_tab, text="Savings Goals:")
        self.savings_goal_label.pack()
        
        self.savings_goal_entry = ttk.Entry(self.savings_goal_tab)
self.savings_goal_amount_label = ttk.Label(self.savings_goal_tab, text="Target Amount:"); self.savings_goal_amount_label.pack(); self.savings_goal_amount_entry = ttk.Entry(self.savings_goal_tab); self.savings_goal_amount_entry.pack()
self.savings_goal_name_label = ttk.Label(self.savings_goal_tab, text="Goal Name:"); self.savings_goal_name_label.pack(); self.savings_goal_name_entry = ttk.Entry(self.savings_goal_tab); self.savings_goal_name_entry.pack()
        self.savings_goal_entry.pack()
        
        self.savings_goal_button = ttk.Button(self.savings_goal_tab, text="Add Savings Goal", command=self.add_savings_goal)
        self.savings_goal_button.pack()
        
        # Create expense category tab
        self.expense_category_label = ttk.Label(self.expense_category_tab, text="Expense Categories:")
        self.expense_category_label.pack()
        
        self.expense_category_entry = ttk.Entry(self.expense_category_tab)
self.expense_category_name_label = ttk.Label(self.expense_category_tab, text="Category Name:"); self.expense_category_name_label.pack(); self.expense_category_name_entry = ttk.Entry(self.expense_category_tab); self.expense_category_name_entry.pack()
        self.expense_category_entry.pack()
        
        self.expense_category_button = ttk.Button(self.expense_category_tab, text="Add Expense Category", command=self.add_expense_category)
        self.expense_category_button.pack()
        
        # Create button to visualize data
        self.visualize_button = ttk.Button(self.root, text="Visualize Data", command=self.visualize_data)
        self.visualize_button.pack()
    
    def add_transaction(self):try:
    user_id = int(self.transaction_entry.get())
    if user_id <= 0:
        raise ValueError
except ValueError:
    self.transaction_label.config(text="Error: Invalid user ID")date = "2024-09-16"try:
    amount = float(self.transaction_amount_entry.get())
    if amount < 0:
        raise ValueError
except ValueError:
    self.transaction_amount_label.config(text="Error: Invalid amount")type = "income"
        self.backend.process_transaction(user_id, date, amount, type)
    
    def add_savings_goal(self):try:
    user_id = int(self.savings_goal_entry.get())
    if user_id <= 0:
        raise ValueError
except ValueError:
    self.savings_goal_label.config(text="Error: Invalid user ID")goal = "Save for a car"try:
    target_amount = float(self.savings_goal_amount_entry.get())
    if target_amount < 0:
        raise ValueError
except ValueError:
    self.savings_goal_amount_label.config(text="Error: Invalid target amount")self.backend.process_savings_goal(user_id, goal, target_amount)
    
    def add_expense_category(self):try:
    user_id = int(self.expense_category_entry.get())
    if user_id <= 0:
        raise ValueError
except ValueError:
    self.expense_category_label.config(text="Error: Invalid user ID")category = "Food"
        self.backend.process_expense_category(user_id, category)
    
    def visualize_data(self):
        # Visualize user data
        user_id = 1  # Replace with actual user ID
        transactions, savings_goals, expense_categories = self.backend.get_user_data(user_id)
        
        # Plot transactions
        transaction_amounts = [transaction[3] for transaction in transactions]
        plt.plot(transaction_amounts)
        plt.title("Transactions")
        plt.xlabel("Transaction ID")
        plt.ylabel("Amount")
        plt.show()
        
        # Plot savings goals
        savings_goal_amounts = [savings_goal[3] for savings_goal in savings_goals]
        plt.plot(savings_goal_amounts)
        plt.title("Savings Goals")
        plt.xlabel("Savings Goal ID")
        plt.ylabel("Target Amount")
        plt.show()
        
        # Plot expense categories
        expense_category_amounts = [expense_category[2] for expense_category in expense_categories]
        plt.plot(expense_category_amounts)
        plt.title("Expense Categories")
        plt.xlabel("Expense Category ID")
        plt.ylabel("Amount")
        plt.show()
    
    def run(self):
        # Run the frontend system
        self.root.mainloop()

# Main function
def main():
    # Create a database connection
    db = Database("budget_buddy.db")
    
    # Create a backend system
    backend = Backend(db)
    
    # Create a frontend system
    frontend = Frontend(backend)
    
    # Run the frontend system
    frontend.run()

if __name__ == "__main__":
    main()