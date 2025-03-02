# models.py
from dataclasses import dataclass
from typing import List

@dataclass
class User:
    """User model"""
    id: int
    email: str
    password: str

@dataclass
class Group:
    """Group model"""
    id: int
    name: str
    users: List[User]

@dataclass
class Product:
    """Product model"""
    id: int
    url: str
    name: str
    price: float

@dataclass
class PriceAlert:
    """Price alert model"""
    id: int
    product: Product
    threshold: float
    user: User

@dataclass
class PriceUpdate:
    """Price update model"""
    id: int
    product: Product
    new_price: float

# database.py
from typing import List, Dict
from models import User, Group, Product, PriceAlert, PriceUpdate

class Database:
    """Database class"""
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.groups: Dict[int, Group] = {}
        self.products: Dict[int, Product] = {}
        self.price_alerts: Dict[int, PriceAlert] = {}
        self.price_updates: Dict[int, PriceUpdate] = {}

    def add_user(self, user: User):
        """Add a user to the database"""
        self.users[user.id] = user

    def add_group(self, group: Group):
        """Add a group to the database"""
        self.groups[group.id] = group

    def add_product(self, product: Product):
        """Add a product to the database"""
        self.products[product.id] = product

    def add_price_alert(self, price_alert: PriceAlert):
        """Add a price alert to the database"""
        self.price_alerts[price_alert.id] = price_alert

    def add_price_update(self, price_update: PriceUpdate):
        """Add a price update to the database"""
        self.price_updates[price_update.id] = price_update

# price_tracker.py
from models import User, Product, PriceAlert
from database import Database
import threading
import time
from typing import List

class PriceTracker:
    """Price tracker class"""
    def __init__(self, database: Database):
        self.database = database
        self.lock = threading.Lock()

    def add_product(self, user: User, product: Product):
        """Add a product to the user's watchlist"""
        with self.lock:
            self.database.add_product(product)
            print(f"Product {product.name} added to {user.email}'s watchlist")

    def set_price_threshold(self, user: User, product: Product, threshold: float):
        """Set a price threshold for a product"""
        with self.lock:
            price_alert = PriceAlert(id=len(self.database.price_alerts) + 1, product=product, threshold=threshold, user=user)
            self.database.add_price_alert(price_alert)
            print(f"Price threshold set to {threshold} for {product.name} by {user.email}")

    def check_price(self, product: Product):
        """Check the price of a product"""
        # Simulate checking the price of a product
        new_price = product.price * 0.9
        return new_price

    def update_price(self, product: Product, new_price: float):
        """Update the price of a product"""
        with self.lock:
            price_update = PriceUpdate(id=len(self.database.price_updates) + 1, product=product, new_price=new_price)
            self.database.add_price_update(price_update)
            print(f"Price of {product.name} updated to {new_price}")

    def notify_user(self, user: User, product: Product, new_price: float):
        """Notify a user about a price update"""
        print(f"Notifying {user.email} about price update of {product.name} to {new_price}")

    def track_price(self, user: User, product: Product):
        """Track the price of a product"""
        while True:
            new_price = self.check_price(product)
            if new_price < product.price:
                self.update_price(product, new_price)
                self.notify_user(user, product, new_price)
            time.sleep(60)  # Check price every 60 seconds

    def start_tracking(self, user: User, product: Product):
        """Start tracking the price of a product"""
        threading.Thread(target=self.track_price, args=(user, product)).start()

# group.py
from models import User, Group
from database import Database
from typing import List

class GroupManager:
    """Group manager class"""
    def __init__(self, database: Database):
        self.database = database

    def create_group(self, name: str):
        """Create a new group"""
        group = Group(id=len(self.database.groups) + 1, name=name, users=[])
        self.database.add_group(group)
        print(f"Group {name} created")

    def add_user_to_group(self, user: User, group: Group):
        """Add a user to a group"""
        group.users.append(user)
        print(f"{user.email} added to group {group.name}")

    def share_price_alert(self, user: User, group: Group, price_alert: PriceAlert):
        """Share a price alert with a group"""
        print(f"Sharing price alert for {price_alert.product.name} with group {group.name}")

# main.py
from models import User, Product, PriceAlert
from database import Database
from price_tracker import PriceTracker
from group import GroupManager

def main():
    database = Database()
    price_tracker = PriceTracker(database)
    group_manager = GroupManager(database)

    user1 = User(id=1, email="user1@example.com", password="password1")
    user2 = User(id=2, email="user2@example.com", password="password2")
    database.add_user(user1)
    database.add_user(user2)

    group = Group(id=1, name="Group1", users=[])
    database.add_group(group)

    product1 = Product(id=1, url="https://example.com/product1", name="Product1", price=100.0)
    product2 = Product(id=2, url="https://example.com/product2", name="Product2", price=200.0)
    database.add_product(product1)
    database.add_product(product2)

    price_tracker.add_product(user1, product1)
    price_tracker.add_product(user2, product2)

    price_tracker.set_price_threshold(user1, product1, 90.0)
    price_tracker.set_price_threshold(user2, product2, 180.0)

    price_tracker.start_tracking(user1, product1)
    price_tracker.start_tracking(user2, product2)

    group_manager.add_user_to_group(user1, group)
    group_manager.add_user_to_group(user2, group)

    price_alert = PriceAlert(id=1, product=product1, threshold=90.0, user=user1)
    group_manager.share_price_alert(user1, group, price_alert)

if __name__ == "__main__":
    main()