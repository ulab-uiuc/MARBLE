# solution.py
import threading
from datetime import datetime
from typing import Dict, List

# Define a class for User
class User:
    def __init__(self, id: int, name: str):
        # Initialize user with id and name
        self.id = id
        self.name = name
        # Initialize an empty shopping list for the user
        self.shopping_list = []

# Define a class for Product
class Product:
    def __init__(self, id: int, name: str, price: float, category: str, brand: str):class ShopCollab:
    def __init__(self):
        self.users = {}
        self.products = {}
        self.shopping_lists = {}
        self.lock = threading.Lock()def add_user(self, id: int, name: str):
    # Acquire the lock for thread safetydef add_product(self, id: int, name: str, price: float, category: str, brand: str):def add_shopping_list(self, id: int, name: str):
    # Acquire the lock for thread safety
    with self.lock:
        # Check if the shopping list already exists
        if id not in self.shopping_lists:
            # Create a new shopping list and add it to the dictionary
            self.shopping_lists[id] = ShoppingList(id, name)
            print(f"Shopping list {name} added successfully")
        else:
            print(f"Shopping list {name} already exists")def add_product_to_shopping_list(self, shopping_list_id: int, product_id: int):
        # Acquire the lock for thread safety
        with self.lock:
            # Check if the shopping list and product exist
            if shopping_list_id in self.shopping_lists and product_id in self.products:
                # Add the product to the shopping list
                self.shopping_lists[shopping_list_id].products.append(self.products[product_id])
                print(f"Product {self.products[product_id].name} added to shopping list {self.shopping_lists[shopping_list_id].name} successfully")
            else:
                print(f"Shopping list or product does not exist")

    # Method to remove a product from a shopping list
    def remove_product_from_shopping_list(self, shopping_list_id: int, product_id: int):
        # Acquire the lock for thread safety
        with self.lock:
            # Check if the shopping list and product exist
            if shopping_list_id in self.shopping_lists and product_id in self.products:
                # Remove the product from the shopping list
                self.shopping_lists[shopping_list_id].products = [product for product in self.shopping_lists[shopping_list_id].products if product.id != product_id]
                print(f"Product {self.products[product_id].name} removed from shopping list {self.shopping_lists[shopping_list_id].name} successfully")
            else:
                print(f"Shopping list or product does not exist")

    # Method to get recommendations for a user
    def get_recommendations(self, user_id: int):
        # Acquire the lock for thread safety
        with self.lock:
            # Check if the user exists
            if user_id in self.users:
                # Get the user's shopping list
                shopping_list = self.users[user_id].shopping_list
                # Get the products in the shopping list
                products = [product for product in shopping_list if product is not None]
                # Get the categories and brands of the products
                categories = [product.category for product in products]
                brands = [product.brand for product in products]
                # Get the recommended products
                recommended_products = [product for product in self.products.values() if product.category in categories and product.brand in brands]
                return recommended_products
            else:
                print(f"User does not exist")
                return []

    # Method to search for products
    def search_products(self, query: str):
        # Acquire the lock for thread safety
        with self.lock:
            # Get the products that match the query
            products = [product for product in self.products.values() if query.lower() in product.name.lower() or query.lower() in product.category.lower() or query.lower() in product.brand.lower()]
            return products

    # Method to get notifications for a user
    def get_notifications(self, user_id: int):
        # Acquire the lock for thread safety
        with self.lock:
            # Check if the user exists
            if user_id in self.users:
                # Get the user's shopping list
                shopping_list = self.users[user_id].shopping_list
                # Get the products in the shopping list
                products = [product for product in shopping_list if product is not None]
                # Get the notifications for the products
                notifications = []
                for product in products:
                    # Check if the product's price has dropped
                    if product.price < product.price * 0.9:
                        notifications.append(f"Price drop: {product.name} is now {product.price}")
                    # Check if the product is available
                    if product.price > 0:
                        notifications.append(f"Product available: {product.name}")
                return notifications
            else:
                print(f"User does not exist")
                return []

# Create a ShopCollab instance
shop_collab = ShopCollab()

# Add users
shop_collab.add_user(1, "John")
shop_collab.add_user(2, "Jane")

# Add products
shop_collab.add_product(1, "Apple", 1.99, "Fruit", "Apple Inc.")
shop_collab.add_product(2, "Banana", 0.99, "Fruit", "Banana Inc.")
shop_collab.add_product(3, "Orange", 2.99, "Fruit", "Orange Inc.")

# Add shopping lists
shop_collab.add_shopping_list(1, "John's shopping list")
shop_collab.add_shopping_list(2, "Jane's shopping list")

# Add products to shopping lists
shop_collab.add_product_to_shopping_list(1, 1)
shop_collab.add_product_to_shopping_list(1, 2)
shop_collab.add_product_to_shopping_list(2, 3)

# Get recommendations for a user
recommendations = shop_collab.get_recommendations(1)
print("Recommendations:")
for product in recommendations:
    print(product.name)

# Search for products
search_results = shop_collab.search_products("Apple")
print("Search results:")
for product in search_results:
    print(product.name)

# Get notifications for a user
notifications = shop_collab.get_notifications(1)
print("Notifications:")
for notification in notifications:
    print(notification)