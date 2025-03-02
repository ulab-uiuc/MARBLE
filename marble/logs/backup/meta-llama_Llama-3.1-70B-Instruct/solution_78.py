# shopcollab.py

import threading
from datetime import datetime
from typing import Dict, List

class Product:
    """Represents a product with its details."""
    def __init__(self, id: int, name: str, category: str, brand: str, price: float, rating: float, availability: bool):
        self.id = id
        self.name = name
        self.category = category
        self.brand = brand
        self.price = price
        self.rating = rating
        self.availability = availability

class User:
    """Represents a user with their shopping lists and preferences."""
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.shopping_lists: Dict[str, List[Product]] = {}
        self.preferences: Dict[str, List[str]] = {}

class ShoppingList:
    """Represents a shopping list with its products and users."""
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.products: List[Product] = []
        self.users: List[User] = []

class ShopCollab:
    """The main application class."""
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.shopping_lists: Dict[int, ShoppingList] = {}
        self.products: Dict[int, Product] = {}
        self.recommendations: Dict[int, List[Product]] = {}
        self.lock = threading.Lock()

    def add_user(self, id: int, name: str):
        """Adds a new user to the application."""
        with self.lock:
            self.users[id] = User(id, name)

    def add_shopping_list(self, id: int, name: str):
        """Adds a new shopping list to the application."""
        with self.lock:
            self.shopping_lists[id] = ShoppingList(id, name)

    def add_product(self, id: int, name: str, category: str, brand: str, price: float, rating: float, availability: bool):
        """Adds a new product to the application."""
        with self.lock:
            self.products[id] = Product(id, name, category, brand, price, rating, availability)

    def add_product_to_shopping_list(self, shopping_list_id: int, product_id: int):
        """Adds a product to a shopping list."""
        with self.lock:
            shopping_list = self.shopping_lists.get(shopping_list_id)
            product = self.products.get(product_id)
            if shopping_list and product:
                shopping_list.products.append(product)
                print(f"Product {product.name} added to shopping list {shopping_list.name}")

    def remove_product_from_shopping_list(self, shopping_list_id: int, product_id: int):
        """Removes a product from a shopping list."""
        with self.lock:
            shopping_list = self.shopping_lists.get(shopping_list_id)
            product = self.products.get(product_id)
            if shopping_list and product:
                shopping_list.products = [p for p in shopping_list.products if p.id != product_id]
                print(f"Product {product.name} removed from shopping list {shopping_list.name}")

    def generate_recommendations(self, user_id: int):
        """Generates product recommendations for a user based on their preferences and shopping history."""
        with self.lock:
            user = self.users.get(user_id)
            if user:
                recommendations = []
                for preference in user.preferences.values():
                    for product in self.products.values():
                        if product.category in preference:
                            recommendations.append(product)
                self.recommendations[user_id] = recommendations
                print(f"Recommendations generated for user {user.name}")

    def search_products(self, query: str):
        """Searches for products by name, category, or brand."""
        with self.lock:
            results = []
            for product in self.products.values():
                if query in product.name or query in product.category or query in product.brand:
                    results.append(product)
            return results

    def notify_users(self, shopping_list_id: int, message: str):
        """Notifies users of changes to a shopping list."""
        with self.lock:
            shopping_list = self.shopping_lists.get(shopping_list_id)
            if shopping_list:
                for user in shopping_list.users:
                    print(f"Notification sent to user {user.name}: {message}")

def main():
    shopcollab = ShopCollab()

    # Add users
    shopcollab.add_user(1, "John Doe")
    shopcollab.add_user(2, "Jane Doe")

    # Add shopping lists
    shopcollab.add_shopping_list(1, "Groceries")
    shopcollab.add_shopping_list(2, "Electronics")

    # Add products
    shopcollab.add_product(1, "Apple", "Fruit", "Granny Smith", 1.99, 4.5, True)
    shopcollab.add_product(2, "Samsung TV", "Electronics", "Samsung", 999.99, 4.8, True)
    shopcollab.add_product(3, "Banana", "Fruit", "Cavendish", 0.99, 4.2, True)

    # Add products to shopping lists
    shopcollab.add_product_to_shopping_list(1, 1)
    shopcollab.add_product_to_shopping_list(1, 3)
    shopcollab.add_product_to_shopping_list(2, 2)

    # Generate recommendations
    shopcollab.generate_recommendations(1)

    # Search for products
    results = shopcollab.search_products("Fruit")
    for product in results:
        print(product.name)

    # Notify users of changes to a shopping list
    shopcollab.notify_users(1, "Product added to shopping list")

if __name__ == "__main__":
    main()