# solution.py
import sqlite3
from sqlite3 import Error
import logging
logging.basicConfig(level=logging.INFO)
import threading
import time
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from bs4 import BeautifulSoup

# Database class to handle database operations
class Database:self.lock = threading.Lock()
self.conn = sqlite3.connect(db_file)try:logging.error(f'An error occurred: {e}')    except Exception as e:
            print(f'An error occurred: {e}')
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        price = soup.find('span', {'class': 'price'}).text
        return float(price)

    def get_product_url(self, product_id):def get_price(self, product_id):
        try:
            url = self.get_product_url(product_id)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            price_element = soup.find('span', {'class': 'price'})
            if price_element:
                return float(price_element.text)
            else:
                return None
        except requests.exceptions.RequestException as e:
            print(f'An error occurred while retrieving the price: {e}')
            return None    def check_price_threshold(self, user_id, product_id):with self.lock:
    cursor = self.conn.cursor()cursor.execute("SELECT price_threshold FROM watchlist WHERE user_id = ? AND product_id = ?", (user_id, product_id))
        price_threshold = cursor.fetchone()[0]
        current_price = self.get_price(product_id)
        if current_price < price_threshold:
            return True
        return False

    def send_notification(self, user_id, product_id, message):with self.lock:
    cursor = self.conn.cursor()cursor.execute("INSERT INTO notifications (user_id, product_id, message) VALUES (?, ?, ?)", (user_id, product_id, message))
        self.conn.commit()

    def share_alert(self, user_id, group_id, product_id):with self.lock:
    cursor = self.conn.cursor()cursor.execute("SELECT * FROM user_groups WHERE group_id = ?", (group_id,))
        group_members = cursor.fetchall()
        for member in group_members:
            self.send_notification(member[0], product_id, "Price alert shared by user {}".format(user_id))

    def compare_prices(self, product_id):
        # Compare prices of a product across different online retailers
        url = self.get_product_url(product_id)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        prices = []
        for price in soup.find_all('span', {'class': 'price'}):
            prices.append(float(price.text))
        return prices

    def get_historical_price_trends(self, product_id):
        # Get historical price trends of a product
        url = self.get_product_url(product_id)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        prices = []
        for price in soup.find_all('span', {'class': 'price'}):
            prices.append(float(price.text))
        return prices

    def suggest_best_time_to_buy(self, product_id):
        # Suggest the best time to buy a product based on historical price trends
        prices = self.get_historical_price_trends(product_id)
        if prices:
            return "The best time to buy this product is when the price is at its lowest, which is {}".format(min(prices))
        return "No historical price trends available"

# PriceTrackerCollaborator class to handle user interactions
class PriceTrackerCollaborator:
    def __init__(self, db_file):
        self.db = Database(db_file)

    def register(self, email, password):
        # Register a new user
        user_id = self.db.register_user(email, password)
        print("User registered successfully with ID {}".format(user_id))

    def login(self, email, password):
        # Login an existing user
        user = self.db.login_user(email, password)
        if user:
            print("User logged in successfully with ID {}".format(user[0]))
            return user[0]
        print("Invalid email or password")
        return None

    def create_group(self, name):
        # Create a new group
        group_id = self.db.create_group(name)
        print("Group created successfully with ID {}".format(group_id))

    def join_group(self, user_id, group_id):
        # Join an existing group
        self.db.join_group(user_id, group_id)
        print("User joined group successfully")

    def add_product(self, url, name):
        # Add a new product
        product_id = self.db.add_product(url, name)
        print("Product added successfully with ID {}".format(product_id))
        return product_id

    def add_to_watchlist(self, user_id, product_id, price_threshold):
        # Add a product to the watchlist
        self.db.add_to_watchlist(user_id, product_id, price_threshold)
        print("Product added to watchlist successfully")

    def check_price_threshold(self, user_id, product_id):
        # Check if the price of a product has dropped below the threshold
        if self.db.check_price_threshold(user_id, product_id):
            print("Price of product {} has dropped below the threshold".format(product_id))
            self.db.send_notification(user_id, product_id, "Price alert: Product {} has dropped below the threshold".format(product_id))
        else:
            print("Price of product {} has not dropped below the threshold".format(product_id))

    def share_alert(self, user_id, group_id, product_id):
        # Share a price alert with a group
        self.db.share_alert(user_id, group_id, product_id)
        print("Price alert shared with group successfully")

    def compare_prices(self, product_id):
        # Compare prices of a product across different online retailers
        prices = self.db.compare_prices(product_id)
        print("Prices of product {} across different online retailers: {}".format(product_id, prices))

    def get_historical_price_trends(self, product_id):
        # Get historical price trends of a product
        prices = self.db.get_historical_price_trends(product_id)
        print("Historical price trends of product {}: {}".format(product_id, prices))

    def suggest_best_time_to_buy(self, product_id):
        # Suggest the best time to buy a product based on historical price trends
        suggestion = self.db.suggest_best_time_to_buy(product_id)
        print(suggestion)

# Test cases
def test_register():
    collaborator = PriceTrackerCollaborator("price_tracker.db")
    collaborator.register("user1@example.com", "password1")

def test_login():
    collaborator = PriceTrackerCollaborator("price_tracker.db")
    user_id = collaborator.login("user1@example.com", "password1")
    assert user_id == 1

def test_create_group():
    collaborator = PriceTrackerCollaborator("price_tracker.db")
    collaborator.create_group("Group1")

def test_join_group():
    collaborator = PriceTrackerCollaborator("price_tracker.db")
    user_id = collaborator.login("user1@example.com", "password1")
    group_id = 1
    collaborator.join_group(user_id, group_id)

def test_add_product():
    collaborator = PriceTrackerCollaborator("price_tracker.db")
    product_id = collaborator.add_product("https://example.com/product1", "Product1")
    assert product_id == 1

def test_add_to_watchlist():
    collaborator = PriceTrackerCollaborator("price_tracker.db")
    user_id = collaborator.login("user1@example.com", "password1")
    product_id = 1
    price_threshold = 100.0
    collaborator.add_to_watchlist(user_id, product_id, price_threshold)

def test_check_price_threshold():
    collaborator = PriceTrackerCollaborator("price_tracker.db")
    user_id = collaborator.login("user1@example.com", "password1")
    product_id = 1
    collaborator.check_price_threshold(user_id, product_id)

def test_share_alert():
    collaborator = PriceTrackerCollaborator("price_tracker.db")
    user_id = collaborator.login("user1@example.com", "password1")
    group_id = 1
    product_id = 1
    collaborator.share_alert(user_id, group_id, product_id)

def test_compare_prices():
    collaborator = PriceTrackerCollaborator("price_tracker.db")
    product_id = 1
    collaborator.compare_prices(product_id)

def test_get_historical_price_trends():
    collaborator = PriceTrackerCollaborator("price_tracker.db")
    product_id = 1
    collaborator.get_historical_price_trends(product_id)

def test_suggest_best_time_to_buy():
    collaborator = PriceTrackerCollaborator("price_tracker.db")
    product_id = 1
    collaborator.suggest_best_time_to_buy(product_id)

# Run test cases
test_register()
test_login()
test_create_group()
test_join_group()
test_add_product()
test_add_to_watchlist()
test_check_price_threshold()
test_share_alert()
test_compare_prices()
test_get_historical_price_trends()
test_suggest_best_time_to_buy()

# Main function
def main():
    db_file = "price_tracker.db"
    collaborator = PriceTrackerCollaborator(db_file)
    collaborator.db.create_tables()

    while True:
        print("1. Register")
        print("2. Login")
        print("3. Create Group")
        print("4. Join Group")
        print("5. Add Product")
        print("6. Add to Watchlist")
        print("7. Check Price Threshold")
        print("8. Share Alert")
        print("9. Compare Prices")
        print("10. Get Historical Price Trends")
        print("11. Suggest Best Time to Buy")
        print("12. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            collaborator.register(email, password)
        elif choice == "2":
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            user_id = collaborator.login(email, password)
            if user_id:
                print("User logged in successfully with ID {}".format(user_id))
        elif choice == "3":
            name = input("Enter group name: ")
            collaborator.create_group(name)
        elif choice == "4":
            user_id = int(input("Enter user ID: "))
            group_id = int(input("Enter group ID: "))
            collaborator.join_group(user_id, group_id)
        elif choice == "5":
            url = input("Enter product URL: ")
            name = input("Enter product name: ")
            product_id = collaborator.add_product(url, name)
            print("Product added successfully with ID {}".format(product_id))
        elif choice == "6":
            user_id = int(input("Enter user ID: "))
            product_id = int(input("Enter product ID: "))
            price_threshold = float(input("Enter price threshold: "))
            collaborator.add_to_watchlist(user_id, product_id, price_threshold)
        elif choice == "7":
            user_id = int(input("Enter user ID: "))
            product_id = int(input("Enter product ID: "))
            collaborator.check_price_threshold(user_id, product_id)
        elif choice == "8":
            user_id = int(input("Enter user ID: "))
            group_id = int(input("Enter group ID: "))
            product_id = int(input("Enter product ID: "))
            collaborator.share_alert(user_id, group_id, product_id)
        elif choice == "9":
            product_id = int(input("Enter product ID: "))
            collaborator.compare_prices(product_id)
        elif choice == "10":
            product_id = int(input("Enter product ID: "))
            collaborator.get_historical_price_trends(product_id)
        elif choice == "11":
            product_id = int(input("Enter product ID: "))
            collaborator.suggest_best_time_to_buy(product_id)
        elif choice == "12":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()