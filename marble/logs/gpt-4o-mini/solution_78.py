# solution.py

# Import necessary libraries
import json
from typing import List, Dict, Any, Optional

# Define a class to represent a shopping item
class ShoppingItem:
    def __init__(self, name: str, category: str, price: float, brand: str):
        self.name = name  # Name of the product
        self.category = category  # Category of the product
        self.price = price  # Price of the product
        self.brand = brand  # Brand of the product

# Define a class to represent a shopping list
class ShoppingList:
    def __init__(self, name: str, shared: bool = False):
        self.name = name  # Name of the shopping list
        self.shared = shared  # Indicates if the list is shared
        self.items: List[ShoppingItem] = []  # List of items in the shopping list

    def add_item(self, item: ShoppingItem):
        """Add an item to the shopping list."""
        self.items.append(item)

    def remove_item(self, item_name: str):
        """Remove an item from the shopping list by name."""
        self.items = [item for item in self.items if item.name != item_name]

    def get_items(self) -> List[Dict[str, Any]]:
        """Return a list of items in a serializable format."""
        return [{'name': item.name, 'category': item.category, 'price': item.price, 'brand': item.brand} for item in self.items]

# Define a class to represent a user
class User:
    def __init__(self, username: str):
        self.username = username  # Username of the user
        self.shopping_lists: Dict[str, ShoppingList] = {}  # Dictionary of shopping lists

    def create_shopping_list(self, list_name: str, shared: bool = False):
        """Create a new shopping list."""
        self.shopping_lists[list_name] = ShoppingList(list_name, shared)

    def get_shopping_list(self, list_name: str) -> Optional[ShoppingList]:
        """Get a shopping list by name."""
        return self.shopping_lists.get(list_name)

# Define a class for the recommendation system
class RecommendationSystem:
    def __init__(self):
        self.user_preferences: Dict[str, List[str]] = {}  # User preferences for recommendations

    def add_user_preference(self, username: str, item_name: str):
        """Add a user preference for recommendations."""
        if username not in self.user_preferences:
            self.user_preferences[username] = []
        self.user_preferences[username].append(item_name)

    def recommend_items(self, username: str) -> List[str]:
        """Recommend items based on user preferences."""
        return self.user_preferences.get(username, [])

# Define a class for the ShopCollab application
class ShopCollab:
    def __init__(self):
        self.users: Dict[str, User] = {}  # Dictionary of users
        self.recommendation_system = RecommendationSystem()  # Recommendation system instance

    def add_user(self, username: str):
        """Add a new user to the application."""
        self.users[username] = User(username)

    def get_user(self, username: str) -> Optional[User]:
        """Get a user by username."""
        return self.users.get(username)

    def notify_users(self, message: str):
        """Notify all users with a message."""
        print(f"Notification to all users: {message}")

# Example usage of the ShopCollab application
if __name__ == "__main__":
    app = ShopCollab()
    
    # Adding users
    app.add_user("Alice")
    app.add_user("Bob")

    # Creating shopping lists
    alice = app.get_user("Alice")
    alice.create_shopping_list("Groceries", shared=True)

    # Adding items to the shopping list
    groceries_list = alice.get_shopping_list("Groceries")
    groceries_list.add_item(ShoppingItem("Milk", "Dairy", 1.50, "BrandA"))
    groceries_list.add_item(ShoppingItem("Bread", "Bakery", 2.00, "BrandB"))

    # Displaying items in the shopping list
    print(json.dumps(groceries_list.get_items(), indent=2))

    # Adding user preferences for recommendations
    app.recommendation_system.add_user_preference("Alice", "Milk")
    app.recommendation_system.add_user_preference("Bob", "Bread")

    # Getting recommendations for Alice
    recommendations = app.recommendation_system.recommend_items("Alice")
    print(f"Recommendations for Alice: {recommendations}")

    # Notify users about a price drop
    app.notify_users("Price drop on Milk!")