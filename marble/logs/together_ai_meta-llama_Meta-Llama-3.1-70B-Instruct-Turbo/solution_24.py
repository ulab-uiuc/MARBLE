# budget_buddy.py

# Import necessary libraries
import sqlite3
from sqlite3 import Error
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

# Database class to handle database operations
class Database:
    def __init__(self, db_name):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_name)
            print("Connected to SQLite Database")
        except Error as e:
            print(e)

    def create_tables(self):
        # Create user profiles table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles
            (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT)
        ''')

        # Create financial transactions table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS financial_transactions
            (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, date TEXT, amount REAL, type TEXT, FOREIGN KEY(user_id) REFERENCES user_profiles(id))
        ''')

        # Create savings goals table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS savings_goals
            (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, goal TEXT, target REAL, FOREIGN KEY(user_id) REFERENCES user_profiles(id))
        ''')

        # Create expense categories table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS expense_categories
            (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, category TEXT, FOREIGN KEY(user_id) REFERENCES user_profiles(id))
        ''')

    def insert_user(self, name, email):
        self.conn.execute("INSERT INTO user_profiles (name, email) VALUES (?, ?)", (name, email))
        self.conn.commit()

    def insert_transaction(self, user_id, date, amount, type):
        self.conn.execute("INSERT INTO financial_transactions (user_id, date, amount, type) VALUES (?, ?, ?, ?)", (user_id, date, amount, type))
        self.conn.commit()

    def insert_savings_goal(self, user_id, goal, target):
        self.conn.execute("INSERT INTO savings_goals (user_id, goal, target) VALUES (?, ?, ?)", (user_id, goal, target))
        self.conn.commit()

    def insert_expense_category(self, user_id, category):
        self.conn.execute("INSERT INTO expense_categories (user_id, category) VALUES (?, ?)", (user_id, category))
        self.conn.commit()

    def get_user_transactions(self, user_id):
        cursor = self.conn.execute("SELECT * FROM financial_transactions WHERE user_id = ?", (user_id,))
        return cursor.fetchall()

    def get_user_savings_goals(self, user_id):
        cursor = self.conn.execute("SELECT * FROM savings_goals WHERE user_id = ?", (user_id,))
        return cursor.fetchall()

    def get_user_expense_categories(self, user_id):
        cursor = self.conn.execute("SELECT * FROM expense_categories WHERE user_id = ?", (user_id,))
        return cursor.fetchall()


# BudgetBuddy class to handle frontend operations
class BudgetBuddy:
    def __init__(self, root):
        self.root = root
        self.root.title("BudgetBuddy")
self.user_id = None
        self.root.geometry("800x600")

        # Create tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        self.dashboard_tab = ttk.Frame(self.notebook)
        self.transactions_tab = ttk.Frame(self.notebook)
        self.savings_goals_tab = ttk.Frame(self.notebook)
        self.expense_categories_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.dashboard_tab, text="Dashboard")
        self.notebook.add(self.transactions_tab, text="Transactions")
        self.notebook.add(self.savings_goals_tab, text="Savings Goals")
        self.notebook.add(self.expense_categories_tab, text="Expense Categories")

        # Create dashboard widgets
        self.dashboard_label = tk.Label(self.dashboard_tab, text="Welcome to BudgetBuddy!")
        self.dashboard_label.pack(pady=20)

        # Create transactions widgets
        self.transactions_label = tk.Label(self.transactions_tab, text="Transactions:")
        self.transactions_label.pack(pady=10)

        self.transactions_listbox = tk.Listbox(self.transactions_tab)
        self.transactions_listbox.pack(pady=10)

        self.add_transaction_button = tk.Button(self.transactions_tab, text="Add Transaction", command=self.add_transaction)
        self.add_transaction_button.pack(pady=10)

        # Create savings goals widgets
        self.savings_goals_label = tk.Label(self.savings_goals_tab, text="Savings Goals:")
        self.savings_goals_label.pack(pady=10)

        self.savings_goals_listbox = tk.Listbox(self.savings_goals_tab)
        self.savings_goals_listbox.pack(pady=10)

        self.add_savings_goal_button = tk.Button(self.savings_goals_tab, text="Add Savings Goal", command=self.add_savings_goal)
        self.add_savings_goal_button.pack(pady=10)

        # Create expense categories widgets
        self.expense_categories_label = tk.Label(self.expense_categories_tab, text="Expense Categories:")
        self.expense_categories_label.pack(pady=10)

        self.expense_categories_listbox = tk.Listbox(self.expense_categories_tab)
        self.expense_categories_listbox.pack(pady=10)

        self.add_expense_category_button = tk.Button(self.expense_categories_tab, text="Add Expense Category", command=self.add_expense_category)
        self.add_expense_category_button.pack(pady=10)

        # Create database object
        self.db = Database("budget_buddy.db")
        self.db.create_tables()

    def add_transaction(self):
        # Create add transaction window
        self.add_transaction_window = tk.Toplevel(self.root)
        self.add_transaction_window.title("Add Transaction")

        # Create add transaction widgets
        self.add_transaction_label = tk.Label(self.add_transaction_window, text="Add Transaction:")
        self.add_transaction_label.pack(pady=10)

        self.add_transaction_date_label = tk.Label(self.add_transaction_window, text="Date:")
        self.add_transaction_date_label.pack(pady=5)

        self.add_transaction_date_entry = tk.Entry(self.add_transaction_window)
        self.add_transaction_date_entry.pack(pady=5)

        self.add_transaction_amount_label = tk.Label(self.add_transaction_window, text="Amount:")
        self.add_transaction_amount_label.pack(pady=5)

        self.add_transaction_amount_entry = tk.Entry(self.add_transaction_window)
        self.add_transaction_amount_entry.pack(pady=5)

        self.add_transaction_type_label = tk.Label(self.add_transaction_window, text="Type:")
        self.add_transaction_type_label.pack(pady=5)

        self.add_transaction_type_entry = tk.Entry(self.add_transaction_window)
        self.add_transaction_type_entry.pack(pady=5)

        self.add_transaction_button = tk.Button(self.add_transaction_window, text="Add Transaction", command=self.add_transaction_to_db)
        self.add_transaction_button.pack(pady=10)

    def add_transaction_to_db(self):
        # Get transaction data from entriesself.db.insert_transaction(self.user_id, date, amount, type)    # Close add transaction window
        self.add_transaction_window.destroy()

    def add_savings_goal(self):
        # Create add savings goal window
        self.add_savings_goal_window = tk.Toplevel(self.root)
        self.add_savings_goal_window.title("Add Savings Goal")

        # Create add savings goal widgets
        self.add_savings_goal_label = tk.Label(self.add_savings_goal_window, text="Add Savings Goal:")
        self.add_savings_goal_label.pack(pady=10)

        self.add_savings_goal_goal_label = tk.Label(self.add_savings_goal_window, text="Goal:")
        self.add_savings_goal_goal_label.pack(pady=5)

        self.add_savings_goal_goal_entry = tk.Entry(self.add_savings_goal_window)
        self.add_savings_goal_goal_entry.pack(pady=5)

        self.add_savings_goal_target_label = tk.Label(self.add_savings_goal_window, text="Target:")
        self.add_savings_goal_target_label.pack(pady=5)

        self.add_savings_goal_target_entry = tk.Entry(self.add_savings_goal_window)
        self.add_savings_goal_target_entry.pack(pady=5)

        self.add_savings_goal_button = tk.Button(self.add_savings_goal_window, text="Add Savings Goal", command=self.add_savings_goal_to_db)
        self.add_savings_goal_button.pack(pady=10)

    def add_savings_goal_to_db(self):
        # Get savings goal data from entriesself.db.insert_savings_goal(self.user_id, goal, target)    # Close add savings goal window
        self.add_savings_goal_window.destroy()

    def add_expense_category(self):
        # Create add expense category window
        self.add_expense_category_window = tk.Toplevel(self.root)
        self.add_expense_category_window.title("Add Expense Category")

        # Create add expense category widgets
        self.add_expense_category_label = tk.Label(self.add_expense_category_window, text="Add Expense Category:")
        self.add_expense_category_label.pack(pady=10)

        self.add_expense_category_category_label = tk.Label(self.add_expense_category_window, text="Category:")
        self.add_expense_category_category_label.pack(pady=5)

        self.add_expense_category_category_entry = tk.Entry(self.add_expense_category_window)
        self.add_expense_category_category_entry.pack(pady=5)

        self.add_expense_category_button = tk.Button(self.add_expense_category_window, text="Add Expense Category", command=self.add_expense_category_to_db)
        self.add_expense_category_button.pack(pady=10)

    def add_expense_category_to_db(self):
        # Get expense category data from entriesself.db.insert_expense_category(self.user_id, category)    # Close add expense category window
        self.add_expense_category_window.destroy()

    def display_transactions(self):
        # Get transactions from database
        transactions = self.db.get_user_transactions(1)

        # Display transactions in listbox
        self.transactions_listbox.delete(0, tk.END)
        for transaction in transactions:
transactions = self.db.get_user_transactions(self.user_id)
            self.transactions_listbox.insert(tk.END, transaction)

    def display_savings_goals(self):
        # Get savings goals from database
        savings_goals = self.db.get_user_savings_goals(1)

        # Display savings goals in listbox
        self.savings_goals_listbox.delete(0, tk.END)
        for savings_goal in savings_goals:
savings_goals = self.db.get_user_savings_goals(self.user_id)
            self.savings_goals_listbox.insert(tk.END, savings_goal)

    def display_expense_categories(self):
        # Get expense categories from database
        expense_categories = self.db.get_user_expense_categories(1)

        # Display expense categories in listbox
        self.expense_categories_listbox.delete(0, tk.END)
        for expense_category in expense_categories:
expense_categories = self.db.get_user_expense_categories(self.user_id)
            self.expense_categories_listbox.insert(tk.END, expense_category)


# Create root window
root = tk.Tk()

# Create BudgetBuddy object
budget_buddy = BudgetBuddy(root)

# Display transactions, savings goals, and expense categories
budget_buddy.display_transactions()
budget_buddy.user_id = 1  # Replace with actual user ID after implementing user authentication
budget_buddy.display_savings_goals()
budget_buddy.display_expense_categories()

# Start main loop
root.mainloop()