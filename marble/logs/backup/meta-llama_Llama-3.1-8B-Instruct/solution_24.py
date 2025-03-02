# solution.py
# Importing required libraries
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# Database schema
class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
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
        self.conn.commit()

    def save_user(self, name, email):
        self.cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        self.conn.commit()

    def save_transaction(self, user_id, date, amount, category):
        self.cursor.execute('INSERT INTO transactions (user_id, date, amount, category) VALUES (?, ?, ?, ?)', (user_id, date, amount, category))
        self.conn.commit()

    def get_user_transactions(self, user_id):
        self.cursor.execute('SELECT * FROM transactions WHERE user_id = ?', (user_id,))
        return self.cursor.fetchall()

# BudgetBuddy class
class BudgetBuddy:
    def __init__(self, db_name):
        self.db = Database(db_name)

    def save_user(self, name, email):
        self.db.save_user(name, email)

    def save_transaction(self, user_id, date, amount, category):
        self.db.save_transaction(user_id, date, amount, category)

    def get_user_transactions(self, user_id):
        return self.db.get_user_transactions(user_id)

    def visualize_transactions(self, user_id):
        transactions = self.get_user_transactions(user_id)
        dates = [transaction[2] for transaction in transactions]
        amounts = [transaction[3] for transaction in transactions]
        plt.bar(dates, amounts)
        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.title('User Transactions')
        plt.show()

# Main function
def main():
    budget_buddy = BudgetBuddy('budget_buddy.db')
    while True:
        print('1. Save user')
        print('2. Save transaction')
        print('3. Get user transactions')
        print('4. Visualize transactions')
        print('5. Exit')
        choice = input('Choose an option: ')
        if choice == '1':
            name = input('Enter user name: ')
            email = input('Enter user email: ')
            budget_buddy.save_user(name, email)
        elif choice == '2':
            user_id = int(input('Enter user ID: '))
            date = input('Enter transaction date (YYYY-MM-DD): ')
            amount = float(input('Enter transaction amount: '))
            category = input('Enter transaction category: ')
            budget_buddy.save_transaction(user_id, date, amount, category)
        elif choice == '3':
            user_id = int(input('Enter user ID: '))
            transactions = budget_buddy.get_user_transactions(user_id)
            for transaction in transactions:
                print(f'Date: {transaction[2]}, Amount: {transaction[3]}, Category: {transaction[4]}')
        elif choice == '4':
            user_id = int(input('Enter user ID: '))
            budget_buddy.visualize_transactions(user_id)
        elif choice == '5':
            break
        else:
            print('Invalid option')

if __name__ == '__main__':
    main()