# budget_buddy.py
# This is the main implementation of the BudgetBuddy system.

# Import required libraries
import tkinter as tk
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

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
        # Retrieve all transactions for a user
        self.cursor.execute('SELECT * FROM transactions WHERE user_id = ?', (user_id,))
        return self.cursor.fetchall()
    
    def get_user_savings_goals(self, user_id):
        # Retrieve all savings goals for a user
        self.cursor.execute('SELECT * FROM savings_goals WHERE user_id = ?', (user_id,))
        return self.cursor.fetchall()
    
    def get_user_expense_categories(self, user_id):
        # Retrieve all expense categories for a user
        self.cursor.execute('SELECT * FROM expense_categories WHERE user_id = ?', (user_id,))
        return self.cursor.fetchall()

# Frontend implementation
class BudgetBuddyApp:
    def __init__(self, root):
        # Initialize the frontend application
        self.root = root
        self.root.title('BudgetBuddy')
        
        # Create tabs for different features
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)
        
        self.dashboard_tab = ttk.Frame(self.notebook)
        self.transactions_tab = ttk.Frame(self.notebook)
        self.savings_goals_tab = ttk.Frame(self.notebook)
        self.expense_categories_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.dashboard_tab, text='Dashboard')
        self.notebook.add(self.transactions_tab, text='Transactions')
        self.notebook.add(self.savings_goals_tab, text='Savings Goals')
        self.notebook.add(self.expense_categories_tab, text='Expense Categories')
        
        # Create dashboard tab content
        self.dashboard_label = ttk.Label(self.dashboard_tab, text='Welcome to BudgetBuddy!')
        self.dashboard_label.pack(pady=20)
        
        # Create transactions tab content
        self.transactions_label = ttk.Label(self.transactions_tab, text='Transactions:')
        self.transactions_label.pack(pady=10)
        
        self.transactions_listbox = tk.Listbox(self.transactions_tab)
        self.transactions_listbox.pack(pady=10)
        
        self.add_transaction_button = ttk.Button(self.transactions_tab, text='Add Transaction', command=self.add_transaction)
        self.add_transaction_button.pack(pady=10)
        
        # Create savings goals tab content
        self.savings_goals_label = ttk.Label(self.savings_goals_tab, text='Savings Goals:')
        self.savings_goals_label.pack(pady=10)
        
        self.savings_goals_listbox = tk.Listbox(self.savings_goals_tab)
        self.savings_goals_listbox.pack(pady=10)
        
        self.add_savings_goal_button = ttk.Button(self.savings_goals_tab, text='Add Savings Goal', command=self.add_savings_goal)
        self.add_savings_goal_button.pack(pady=10)
        
        # Create expense categories tab content
        self.expense_categories_label = ttk.Label(self.expense_categories_tab, text='Expense Categories:')
        self.expense_categories_label.pack(pady=10)
        
        self.expense_categories_listbox = tk.Listbox(self.expense_categories_tab)
        self.expense_categories_listbox.pack(pady=10)
        
        self.add_expense_category_button = ttk.Button(self.expense_categories_tab, text='Add Expense Category', command=self.add_expense_category)
        self.add_expense_category_button.pack(pady=10)
        
        # Initialize database connection
        self.db = Database('budget_buddy.db')
        
        # Initialize user data
        self.user_id = 1  # Default user ID
        
    def add_transaction(self):
        # Add a new transaction
        self.add_transaction_window = tk.Toplevel(self.root)
        self.add_transaction_window.title('Add Transaction')
        
        self.date_label = ttk.Label(self.add_transaction_window, text='Date:')
        self.date_label.pack(pady=10)
        
        self.date_entry = ttk.Entry(self.add_transaction_window)
        self.date_entry.pack(pady=10)
        
        self.amount_label = ttk.Label(self.add_transaction_window, text='Amount:')
        self.amount_label.pack(pady=10)
        
        self.amount_entry = ttk.Entry(self.add_transaction_window)
        self.amount_entry.pack(pady=10)
        
        self.type_label = ttk.Label(self.add_transaction_window, text='Type:')
        self.type_label.pack(pady=10)
        
        self.type_entry = ttk.Entry(self.add_transaction_window)
        self.type_entry.pack(pady=10)
        
        self.add_transaction_button = ttk.Button(self.add_transaction_window, text='Add Transaction', command=self.save_transaction)
        self.add_transaction_button.pack(pady=10)
    
    def save_transaction(self):
        # Save the new transaction to the database
        date = self.date_entry.get()
        amount = float(self.amount_entry.get())
        type = self.type_entry.get()
        
        self.db.insert_transaction(self.user_id, date, amount, type)
        
        self.add_transaction_window.destroy()
        
        # Update transactions listbox
        self.transactions_listbox.delete(0, tk.END)
        transactions = self.db.get_user_transactions(self.user_id)
        for transaction in transactions:
            self.transactions_listbox.insert(tk.END, f'{transaction[2]} - {transaction[3]} - {transaction[4]}')
    
    def add_savings_goal(self):
        # Add a new savings goal
        self.add_savings_goal_window = tk.Toplevel(self.root)
        self.add_savings_goal_window.title('Add Savings Goal')
        
        self.goal_label = ttk.Label(self.add_savings_goal_window, text='Goal:')
        self.goal_label.pack(pady=10)
        
        self.goal_entry = ttk.Entry(self.add_savings_goal_window)
        self.goal_entry.pack(pady=10)
        
        self.target_amount_label = ttk.Label(self.add_savings_goal_window, text='Target Amount:')
        self.target_amount_label.pack(pady=10)
        
        self.target_amount_entry = ttk.Entry(self.add_savings_goal_window)
        self.target_amount_entry.pack(pady=10)
        
        self.add_savings_goal_button = ttk.Button(self.add_savings_goal_window, text='Add Savings Goal', command=self.save_savings_goal)
        self.add_savings_goal_button.pack(pady=10)
    
    def save_savings_goal(self):
        # Save the new savings goal to the database
        goal = self.goal_entry.get()
        target_amount = float(self.target_amount_entry.get())
        
        self.db.insert_savings_goal(self.user_id, goal, target_amount)
        
        self.add_savings_goal_window.destroy()
        
        # Update savings goals listbox
        self.savings_goals_listbox.delete(0, tk.END)
        savings_goals = self.db.get_user_savings_goals(self.user_id)
        for savings_goal in savings_goals:
            self.savings_goals_listbox.insert(tk.END, f'{savings_goal[2]} - {savings_goal[3]}')
    
    def add_expense_category(self):
        # Add a new expense category
        self.add_expense_category_window = tk.Toplevel(self.root)
        self.add_expense_category_window.title('Add Expense Category')
        
        self.category_label = ttk.Label(self.add_expense_category_window, text='Category:')
        self.category_label.pack(pady=10)
        
        self.category_entry = ttk.Entry(self.add_expense_category_window)
        self.category_entry.pack(pady=10)
        
        self.add_expense_category_button = ttk.Button(self.add_expense_category_window, text='Add Expense Category', command=self.save_expense_category)
        self.add_expense_category_button.pack(pady=10)
    
    def save_expense_category(self):
        # Save the new expense category to the database
        category = self.category_entry.get()
        
        self.db.insert_expense_category(self.user_id, category)
        
        self.add_expense_category_window.destroy()
        
        # Update expense categories listbox
        self.expense_categories_listbox.delete(0, tk.END)
        expense_categories = self.db.get_user_expense_categories(self.user_id)
        for expense_category in expense_categories:
            self.expense_categories_listbox.insert(tk.END, expense_category[2])

# Backend implementation
class BudgetBuddyBackend:
    def __init__(self):
        # Initialize backend services
        self.db = Database('budget_buddy.db')
        
    def get_user_data(self, user_id):
        # Retrieve user data from the database
        user_data = {
            'transactions': self.db.get_user_transactions(user_id),
            'savings_goals': self.db.get_user_savings_goals(user_id),
            'expense_categories': self.db.get_user_expense_categories(user_id)
        }
        return user_data

# Multi-Agent Collaboration
class BudgetBuddyCollaboration:
    def __init__(self):
        # Initialize collaboration services
        self.frontend = BudgetBuddyApp(tk.Tk())
        self.backend = BudgetBuddyBackend()
        
    def start_collaboration(self):
        # Start collaboration between frontend and backend
        self.frontend.root.mainloop()

# Main function
def main():
    collaboration = BudgetBuddyCollaboration()
    collaboration.start_collaboration()

if __name__ == '__main__':
    main()