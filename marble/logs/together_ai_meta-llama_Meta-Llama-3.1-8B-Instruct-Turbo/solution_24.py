# solution.py
# Importing necessary libraries
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Database schema
class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Create user table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')

        # Create transactions table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                date DATE NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        # Create savings goals table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS savings_goals (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                goal_amount REAL NOT NULL,
                target_date DATE NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        # Commit changes
        self.conn.commit()

    def save_user(self, name, email, password):
        self.cursor.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, password))
        self.conn.commit()

    def save_transaction(self, user_id, date, amount, category):
        self.cursor.execute('INSERT INTO transactions (user_id, date, amount, category) VALUES (?, ?, ?, ?)', (user_id, date, amount, category))
        self.conn.commit()

    def save_savings_goal(self, user_id, goal_amount, target_date):
        self.cursor.execute('INSERT INTO savings_goals (user_id, goal_amount, target_date) VALUES (?, ?, ?)', (user_id, goal_amount, target_date))
        self.conn.commit()

    def get_user(self, email):
        self.cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        return self.cursor.fetchone()

    def get_transactions(self, user_id):
        self.cursor.execute('SELECT * FROM transactions WHERE user_id = ?', (user_id,))
        return self.cursor.fetchall()

    def get_savings_goals(self, user_id):
        self.cursor.execute('SELECT * FROM savings_goals WHERE user_id = ?', (user_id,))
        return self.cursor.fetchall()

# Frontend interface
class Frontend:
    def __init__(self, db):
        self.db = db

    def display_user_info(self, user):
        print(f'Name: {user[1]}')
        print(f'Email: {user[2]}')
        print(f'Password: {user[3]}')

    def display_transactions(self, transactions):
        for transaction in transactions:
            print(f'Date: {transaction[2]}')
            print(f'Amount: {transaction[3]}')
            print(f'Category: {transaction[4]}')
            print('------------------------')

    def display_savings_goals(self, goals):
        for goal in goals:
            print(f'Goal Amount: {goal[2]}')
            print(f'Target Date: {goal[3]}')
            print('------------------------')

# Backend interface
class Backend:
    def __init__(self, db):
        self.db = db

    def save_user(self, name, email, password):
        self.db.save_user(name, email, password)

    def save_transaction(self, user_id, date, amount, category):
        self.db.save_transaction(user_id, date, amount, category)

    def save_savings_goal(self, user_id, goal_amount, target_date):
        self.db.save_savings_goal(user_id, goal_amount, target_date)

    def get_user(self, email):
        return self.db.get_user(email)

    def get_transactions(self, user_id):
        return self.db.get_transactions(user_id)

    def get_savings_goals(self, user_id):
        return self.db.get_savings_goals()

# Data analysis
class DataAnalysis:
    def __init__(self, db):
        self.db = db

    def analyze_transactions(self, transactions):
        # Group transactions by category
        categories = {}
        for transaction in transactions:
            category = transaction[4]
            if category in categories:
                categories[category].append(transaction[3])
            else:
                categories[category] = [transaction[3]]

        # Calculate total amount for each category
        totals = {}
        for category, amounts in categories.items():
            totals[category] = sum(amounts)

        # Plot bar chart
        plt.bar(totals.keys(), totals.values())
        plt.xlabel('Category')
        plt.ylabel('Total Amount')
        plt.title('Transaction Analysis')
        plt.show()

    def analyze_savings_goals(self, goals):
        # Calculate progress towards each goal
        progress = {}
        for goal in goals:
            goal_amount = goal[2]
            target_date = goal[3]
            current_date = datetime.now().strftime('%Y-%m-%d')
            progress[goal[0]] = (datetime.strptime(current_date, '%Y-%m-%d') - datetime.strptime(target_date, '%Y-%m-%d')).days

        # Plot bar chart
        plt.bar(progress.keys(), progress.values())
        plt.xlabel('Goal ID')
        plt.ylabel('Days Until Goal')
        plt.title('Savings Goal Analysis')
        plt.show()

# Main function
def main():
    db = Database('budgetbuddy.db')
    frontend = Frontend(db)
    backend = Backend(db)
    data_analysis = DataAnalysis(db)

    # Create user
    backend.save_user('John Doe', 'johndoe@example.com', 'password123')

    # Save transactions
    backend.save_transaction(1, '2022-01-01', 100.0, 'Income')
    backend.save_transaction(1, '2022-01-02', 50.0, 'Expense')

    # Save savings goals
    backend.save_savings_goal(1, 1000.0, '2022-12-31')

    # Display user info
    user = backend.get_user('johndoe@example.com')
    frontend.display_user_info(user)

    # Display transactions
    transactions = backend.get_transactions(1)
    frontend.display_transactions(transactions)

    # Display savings goals
    goals = backend.get_savings_goals(1)
    frontend.display_savings_goals(goals)

    # Analyze transactions
    data_analysis.analyze_transactions(transactions)

    # Analyze savings goals
    data_analysis.analyze_savings_goals(goals)

if __name__ == '__main__':
    main()