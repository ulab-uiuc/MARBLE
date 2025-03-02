# shopcollab.py

import threading
from datetime import datetime
from typing import Dict, List

class User:
    """Represents a user in the ShopCollab application."""
    
    def __init__(self, username: str):
        self.username = username
        self.shopping_lists: Dict[str, ShoppingList] = {}
        self.preferences: Dict[str, int] = {}
        self.purchases: Dict[str, int] = {}

    def create_shopping_list(self, list_name: str):
        """Creates a new shopping list for the user."""
        self.shopping_lists[list_name] = ShoppingList(list_name)

    def add_item_to_list(self, list_name: str, item: str):
        """Adds an item to a shopping list."""
        if list_name in self.shopping_lists:
            self.shopping_lists[list_name].add_item(item)
        else:
            print("Shopping list not found.")

    def remove_item_from_list(self, list_name: str, item: str):
        """Removes an item from a shopping list."""
        if list_name in self.shopping_lists:
            self.shopping_lists[list_name].remove_item(item)
        else:
            print("Shopping list not found.")

    def update_preferences(self, item: str, rating: int):
        """Updates the user's preferences."""
        self.preferences[item] = rating

    def update_purchases(self, item: str, quantity: int):
        """Updates the user's purchases."""
        self.purchases[item] = quantity


class ShoppingList:
    """Represents a shopping list in the ShopCollab application."""
    
    def __init__(self, list_name: str):
        self.list_name = list_name
        self.items: List[str] = []
self.lock = threading.Lock()
        self.users: List[User] = []

    def add_item(self, item: str):with self.lock: self.items.append(item)self.notify_users(f"Item '{item}' added to the list.")

    def remove_item(self, item: str):with self.lock: if item in self.items: self.items.remove(item)self.notify_users(f"Item '{item}' removed from the list.")
        else:
            print("Item not found in the list.")

    def add_user(self, user: User):
        """Adds a user to the shopping list."""
        self.users.append(user)

    def notify_users(self, message: str):
        """Notifies all users in the shopping list."""
        for user in self.users:
            print(f"Notification for {user.username}: {message}")


class RecommendationSystem:
    """Represents the recommendation system in the ShopCollab application."""
    
    def __init__(self):
        self.users: List[User] = []

    def add_user(self, user: User):
        """Adds a user to the recommendation system."""
        self.users.append(user)

    def suggest_products(self, user: User):
        """Suggests products to a user based on their preferences and purchases."""
        suggested_products = []
        for item, rating in user.preferences.items():
            if rating > 3:
                suggested_products.append(item)
        for item, quantity in user.purchases.items():
            if quantity > 1:
                suggested_products.append(item)
        return suggested_products


class SearchFunction:
    """Represents the search function in the ShopCollab application."""
    
    def __init__(self):
        self.products: Dict[str, Dict[str, str]] = {}

    def add_product(self, product_name: str, category: str, brand: str, price: str, rating: str, availability: str):
        """Adds a product to the search function."""
        self.products[product_name] = {
            "category": category,
            "brand": brand,
            "price": price,
            "rating": rating,
            "availability": availability
        }

    def search_products(self, query: str):
        """Searches for products based on the query."""
        results = []
        for product, details in self.products.items():
            if query in product or query in details["category"] or query in details["brand"]:
                results.append(product)
        return results

    def filter_results(self, results: List[str], filter_by: str, value: str):
        """Filters the search results based on the filter_by and value."""
        filtered_results = []
        for result in results:
            if filter_by == "price" and self.products[result]["price"] == value:
                filtered_results.append(result)
            elif filter_by == "rating" and self.products[result]["rating"] == value:
                filtered_results.append(result)
            elif filter_by == "availability" and self.products[result]["availability"] == value:
                filtered_results.append(result)
        return filtered_results


class NotificationSystem:
    """Represents the notification system in the ShopCollab application."""
    
    def __init__(self):
        self.notifications: List[str] = []

    def add_notification(self, notification: str):
        """Adds a notification to the notification system."""
        self.notifications.append(notification)

    def send_notifications(self):
        """Sends all notifications in the notification system."""
        for notification in self.notifications:
            print(notification)


class ShopCollab:
    """Represents the ShopCollab application."""
    
    def __init__(self):
        self.users: List[User] = []
        self.shopping_lists: List[ShoppingList] = []
        self.recommendation_system = RecommendationSystem()
        self.search_function = SearchFunction()
        self.notification_system = NotificationSystem()

    def add_user(self, user: User):
        """Adds a user to the ShopCollab application."""
        self.users.append(user)
        self.recommendation_system.add_user(user)

    def create_shopping_list(self, list_name: str, user: User):
        """Creates a new shopping list in the ShopCollab application."""
        shopping_list = ShoppingList(list_name)
        shopping_list.add_user(user)
        self.shopping_lists.append(shopping_list)
        user.shopping_lists[list_name] = shopping_list

    def start(self):
        """Starts the ShopCollab application."""
        # Create users
        user1 = User("user1")
        user2 = User("user2")

        # Create shopping lists
        self.create_shopping_list("list1", user1)
        self.create_shopping_list("list2", user2)

        # Add items to shopping lists
        user1.add_item_to_list("list1", "item1")
        user1.add_item_to_list("list1", "item2")
        user2.add_item_to_list("list2", "item3")

        # Update user preferences
        user1.update_preferences("item1", 5)
        user2.update_preferences("item3", 4)

        # Update user purchases
        user1.update_purchases("item1", 2)
        user2.update_purchases("item3", 1)

        # Suggest products to users
        suggested_products = self.recommendation_system.suggest_products(user1)
        print(f"Suggested products for {user1.username}: {suggested_products}")

        # Search for products
        self.search_function.add_product("product1", "category1", "brand1", "price1", "rating1", "availability1")
        self.search_function.add_product("product2", "category2", "brand2", "price2", "rating2", "availability2")
        results = self.search_function.search_products("product")
        print(f"Search results: {results}")

        # Filter search results
        filtered_results = self.search_function.filter_results(results, "price", "price1")
        print(f"Filtered results: {filtered_results}")

        # Send notifications
        self.notification_system.add_notification("Notification 1")
        self.notification_system.add_notification("Notification 2")
        self.notification_system.send_notifications()


if __name__ == "__main__":
    shopcollab = ShopCollab()
    shopcollab.start()