# models.py
from dataclasses import dataclass
from typing import List

@dataclass
class User:
    """Represents a user in the application."""
    email: str
    password: str
    groups: List[str] = None
    watchlist: List[str] = None

@dataclass
class Group:
    """Represents a group in the application."""
    name: str
    members: List[str] = None
    shared_alerts: List[str] = None

@dataclass
class Product:
    """Represents a product in the application."""
    url: str
    price_threshold: float = None
    current_price: float = None
    price_history: List[float] = None

@dataclass
class Alert:
    """Represents a price alert in the application."""
    product_url: str
    price_threshold: float
    shared_with: List[str] = None


# database.py
from typing import Dict, List
from models import User, Group, Product, Alert

class Database:
    """Simulates a database for the application."""
    def __init__(self):
        self.users: Dict[str, User] = {}self.alerts: Dict[str, List[Alert]] = {}self.products: Dict[str, Product] = {}
        self.alerts: Dict[str, Alert] = {}

    def add_user(self, user: User):
        self.users[user.email] = user

    def add_group(self, group: Group):
        self.groups[group.name] = group

    def add_product(self, product: Product):
        self.products[product.url] = product

    def add_alert(self, alert: Alert):
        self.alerts[alert.product_url] = alert


# price_tracker.py
from typing import List
from models import Product, Alert
from database import Database

class PriceTracker:
    """Tracks prices for products and sends notifications."""
    def __init__(self, database: Database):
        self.database = database

    def update_price(self, product_url: str, new_price: float):
        """Updates the price of a product and sends notifications if necessary."""
        product = self.database.products.get(product_url)
        if product:
            product.current_price = new_price
            product.price_history.append(new_price)
            self.check_price_threshold(product)

    def check_price_threshold(self, product: Product):if alerts:
    for alert in alerts:
        if product.current_price < alert.price_threshold:for user_email in alert.shared_with:
                print(f"Sending notification to {user_email} about {product.url}")

    def compare_prices(self, product_url: str):
        """Compares prices across different online retailers for the same product."""
        # Simulate comparing prices
        print(f"Comparing prices for {product_url}")


# price_tracker_collaborator.py
from typing import List
from models import User, Group, Product, Alert
from database import Database
from price_tracker import PriceTracker

class PriceTrackerCollaborator:
    """Enables multiple users to collaboratively track and manage price alerts."""
    def __init__(self):
        self.database = Database()
        self.price_tracker = PriceTracker(self.database)

    def register_user(self, email: str, password: str):
        """Registers a new user."""
        user = User(email, password)
        self.database.add_user(user)

    def create_group(self, group_name: str):
        """Creates a new group."""
        group = Group(group_name)
        self.database.add_group(group)

    def add_product_to_watchlist(self, user_email: str, product_url: str):
        """Adds a product to a user's watchlist."""
        user = self.database.users.get(user_email)
        if user:
            user.watchlist.append(product_url)
            product = Product(product_url)
            self.database.add_product(product)

    def set_price_threshold(self, user_email: str, product_url: str, price_threshold: float):
        """Sets a price threshold for a product."""
        user = self.database.users.get(user_email)
        if user:
            product = self.database.products.get(product_url)
            if product:
                product.price_threshold = price_threshold
                alert = Alert(product_url, price_threshold)
                self.database.add_alert(alert)

    def share_alert(self, user_email: str, product_url: str, group_name: str):
        """Shares a price alert with a group."""
        user = self.database.users.get(user_email)
        if user:
            group = self.database.groups.get(group_name)
            if group:
                alert = self.database.alerts.get(product_url)
                if alert:
                    alert.shared_with.append(group_name)

    def get_price_history(self, product_url: str):
        """Gets the price history for a product."""
        product = self.database.products.get(product_url)
        if product:
            return product.price_history

    def get_best_time_to_buy(self, product_url: str):
        """Gets the best time to buy a product based on historical price trends."""
        # Simulate getting the best time to buy
        print(f"Getting best time to buy for {product_url}")


# main.py
from price_tracker_collaborator import PriceTrackerCollaborator

def main():
    price_tracker_collaborator = PriceTrackerCollaborator()

    # Register users
    price_tracker_collaborator.register_user("user1@example.com", "password1")
    price_tracker_collaborator.register_user("user2@example.com", "password2")

    # Create groups
    price_tracker_collaborator.create_group("group1")
    price_tracker_collaborator.create_group("group2")

    # Add products to watchlist
    price_tracker_collaborator.add_product_to_watchlist("user1@example.com", "https://example.com/product1")
    price_tracker_collaborator.add_product_to_watchlist("user2@example.com", "https://example.com/product2")

    # Set price thresholds
    price_tracker_collaborator.set_price_threshold("user1@example.com", "https://example.com/product1", 100.0)
    price_tracker_collaborator.set_price_threshold("user2@example.com", "https://example.com/product2", 200.0)

    # Share alerts
    price_tracker_collaborator.share_alert("user1@example.com", "https://example.com/product1", "group1")
    price_tracker_collaborator.share_alert("user2@example.com", "https://example.com/product2", "group2")

    # Get price history
    print(price_tracker_collaborator.get_price_history("https://example.com/product1"))

    # Get best time to buy
    price_tracker_collaborator.get_best_time_to_buy("https://example.com/product1")

if __name__ == "__main__":
    main()