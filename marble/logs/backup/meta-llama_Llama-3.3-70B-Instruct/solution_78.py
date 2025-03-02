# solution.py
import threading
from datetime import datetime
from typing import Dict, List

# Define a class for User
class User:
    def __init__(self, id: int, name: str):    def add_product(self, product: Product):    def remove_product(self, product: Product):
        with self.lock:
            self.products.remove(product)        self.products.remove(product)

    def add_user(self, user: User):
        # Add a user to the shopping list
        self.users.append(user)

    def remove_user(self, user: User):
        # Remove a user from the shopping list
        self.users.remove(user)

# Define a class for RecommendationSystem
class RecommendationSystem:
    def __init__(self):
        # Initialize an empty dictionary to store user preferences
        self.user_preferences = {}

    def update_user_preferences(self, user: User, product: Product):
        # Update user preferences based on product interactions
        if user.id not in self.user_preferences:
            self.user_preferences[user.id] = []
        self.user_preferences[user.id].append(product)

    def get_recommendations(self, user: User):
        # Get product recommendations based on user preferences
        if user.id not in self.user_preferences:
            return []
        # For simplicity, return the last 5 products interacted with by the user
        return self.user_preferences[user.id][-5:]

# Define a class for NotificationSystem
class NotificationSystem:
    def __init__(self):
        # Initialize an empty list to store notifications
        self.notifications = []

    def add_notification(self, message: str):
        # Add a notification to the list
        self.notifications.append(message)

    def get_notifications(self):
        # Get all notifications
        return self.notifications

# Define a class for SearchFunction
class SearchFunction:
    def __init__(self):
        # Initialize an empty list to store products
        self.products = []

    def add_product(self, product: Product):
        # Add a product to the list
        self.products.append(product)

    def search(self, query: str):
        # Search for products by name, category, or brand
        results = []
        for product in self.products:
            if query.lower() in product.name.lower() or query.lower() in product.category.lower() or query.lower() in product.brand.lower():
                results.append(product)
        return results

    def filter(self, products: List[Product], price: float = None, rating: float = None, availability: bool = None):
        # Filter search results by price, rating, and availability
        filtered_results = products
        if price is not None:
            filtered_results = [product for product in filtered_results if product.price <= price]
        if rating is not None:
            # For simplicity, assume rating is based on product price
            filtered_results = [product for product in filtered_results if product.price >= rating * 10]
        if availability is not None:
            # For simplicity, assume availability is based on product price
            filtered_results = [product for product in filtered_results if product.price > 0]
        return filtered_results

# Define a class for ShopCollab
class ShopCollab:
    def __init__(self):
        # Initialize an empty list to store users
        self.users = []
        # Initialize an empty list to store shopping lists
        self.shopping_lists = []
        # Initialize an empty list to store products
        self.products = []
        # Initialize the recommendation system
        self.recommendation_system = RecommendationSystem()
        # Initialize the notification system
        self.notification_system = NotificationSystem()
        # Initialize the search function
        self.search_function = SearchFunction()

    def create_user(self, name: str):
        # Create a new user
        user = User(len(self.users) + 1, name)
        self.users.append(user)
        return user

    def create_shopping_list(self, name: str):
        # Create a new shopping list
        shopping_list = ShoppingList(len(self.shopping_lists) + 1, name)
        self.shopping_lists.append(shopping_list)
        return shopping_list

    def create_product(self, name: str, price: float, category: str, brand: str):    def add_product_to_shopping_list(self, shopping_list: ShoppingList, product: Product):    def remove_product_from_shopping_list(self, shopping_list: ShoppingList, product: Product):
        shopping_list.remove_product(product)
        # Add a notification
        self.notification_system.add_notification(f"Product {product.name} removed from shopping list {shopping_list.name}")        shopping_list.remove_product(product)
        # Add a notification
        self.notification_system.add_notification(f"Product {product.name} removed from shopping list {shopping_list.name}")

    def get_recommendations(self, user: User):
        # Get product recommendations for a user
        return self.recommendation_system.get_recommendations(user)

    def search(self, query: str):
        # Search for products
        return self.search_function.search(query)

    def filter(self, products: List[Product], price: float = None, rating: float = None, availability: bool = None):
        # Filter search results
        return self.search_function.filter(products, price, rating, availability)

# Create a ShopCollab instance
shop_collab = ShopCollab()

# Create users
user1 = shop_collab.create_user("John")
user2 = shop_collab.create_user("Jane")

# Create shopping lists
shopping_list1 = shop_collab.create_shopping_list("Groceries")
shopping_list2 = shop_collab.create_shopping_list("Electronics")

# Add users to shopping lists
shopping_list1.add_user(user1)
shopping_list1.add_user(user2)
shopping_list2.add_user(user1)

# Create products
product1 = shop_collab.create_product("Apple", 1.99, "Fruit", "Local")
product2 = shop_collab.create_product("Samsung TV", 999.99, "Electronics", "Samsung")
product3 = shop_collab.create_product("Banana", 0.99, "Fruit", "Local")

# Add products to shopping lists
shop_collab.add_product_to_shopping_list(shopping_list1, product1)
shop_collab.add_product_to_shopping_list(shopping_list1, product3)
shop_collab.add_product_to_shopping_list(shopping_list2, product2)

# Get recommendations
recommendations = shop_collab.get_recommendations(user1)
print("Recommendations for user1:")
for product in recommendations:
    print(product.name)

# Search for products
search_results = shop_collab.search("Fruit")
print("Search results for 'Fruit':")
for product in search_results:
    print(product.name)

# Filter search results
filtered_results = shop_collab.filter(search_results, price=2.0)
print("Filtered search results for 'Fruit' with price <= 2.0:")
for product in filtered_results:
    print(product.name)

# Get notifications
notifications = shop_collab.notification_system.get_notifications()
print("Notifications:")
for notification in notifications:
    print(notification)