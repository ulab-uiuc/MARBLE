# solution.py

# Import necessary libraries
import json
from typing import List, Dict, Any, Optional

# User class to represent a user in the application
class User:
    def __init__(self, username: str):
        self.username = username
        self.shopping_lists = []  # List of shopping lists owned by the user

# ShoppingList class to represent a shopping list
class ShoppingList:
    def __init__(self, name: str, owner: User):
        self.name = name
        self.owner = owner
        self.items = []  # List of items in the shopping list
        self.shared_users = []  # List of users with whom the list is shared

    def add_item(self, item: str):
        """Add an item to the shopping list."""
        self.items.append(item)
        self.notify_users(f"{item} has been added to {self.name}.")

    def remove_item(self, item: str):
        """Remove an item from the shopping list."""
        if item in self.items:
            self.items.remove(item)
            self.notify_users(f"{item} has been removed from {self.name}.")

    def notify_users(self, message: str):
        """Notify all users sharing the list."""
        for user in self.shared_users:
            print(f"Notification to {user.username}: {message}")

    def share_with(self, user: User):
        """Share the shopping list with another user."""
        if user not in self.shared_users:
            self.shared_users.append(user)
            user.shopping_lists.append(self)
            self.notify_users(f"{self.name} has been shared with {user.username}.")

# RecommendationSystem class to handle product recommendations
class RecommendationSystem:
    def __init__(self):
        self.user_preferences = {}  # Store user preferences
        self.product_database = []  # Simulated product database

    def add_product(self, product: Dict[str, Any]):
        """Add a product to the product database."""
        self.product_database.append(product)

    def recommend_products(self, user: User) -> List[Dict[str, Any]]:
        """Recommend products based on user preferences."""
        recommendations = []
        preferences = self.user_preferences.get(user.username, [])
        for product in self.product_database:
            if product['category'] in preferences:        return recommendations

    def get_previous_purchases(self, user: User) -> List[str]:
        """Retrieve previous purchases for the user."""
        # Logic to retrieve previous purchases
        return []

    def get_group_activity(self, user: User) -> List[str]:
        """Retrieve items added or modified in shared lists by group members."""
        # Logic to track group activities
        return []        return recommendations

    def update_preferences(self, user: User, preference: str):
        """Update user preferences based on interactions."""
        if user.username not in self.user_preferences:
            self.user_preferences[user.username] = []
        self.user_preferences[user.username].append(preference)

# Search function to find products
def search_products(products: List[Dict[str, Any]], query: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Search for products based on a query and optional filters."""
    results = [product for product in products if query.lower() in product['name'].lower()]
    
    if filters:
        if 'price' in filters:
            results = [product for product in results if product['price'] <= filters['price']]
        if 'rating' in filters:
            results = [product for product in results if product['rating'] >= filters['rating']]
        if 'availability' in filters:
            results = [product for product in results if product['availability'] == filters['availability']]
    
    return results

# Example usage
if __name__ == "__main__":
    # Create users
    alice = User("Alice")
    bob = User("Bob")

    # Create a shopping list
    grocery_list = ShoppingList("Grocery List", alice)

    # Share the list with Bob
    grocery_list.share_with(bob)

    # Add items to the list
    grocery_list.add_item("Milk")
    grocery_list.add_item("Eggs")

    # Remove an item from the list
    grocery_list.remove_item("Milk")

    # Initialize recommendation system and add products
    recommender = RecommendationSystem()
    recommender.add_product({"name": "Organic Milk", "category": "Dairy", "price": 3.50, "rating": 4.5, "availability": "in stock"})
    recommender.add_product({"name": "Free-range Eggs", "category": "Dairy", "price": 2.50, "rating": 4.7, "availability": "in stock"})

    # Update user preferences
    recommender.update_preferences(alice, "Dairy")
    recommender.update_preferences(bob, "Dairy")

    # Get recommendations for Alice
    recommendations = recommender.recommend_products(alice)
    print("Recommendations for Alice:", recommendations)

    # Search for products
    search_results = search_products(recommender.product_database, "Milk", {"price": 4.00, "rating": 4.0})
    print("Search results for 'Milk':", search_results)