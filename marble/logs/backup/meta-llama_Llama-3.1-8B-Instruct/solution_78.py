# solution.py

# Importing required libraries
import threading
import time
import random
from typing import Dict, List

# Class to represent a product
class Product:
    def __init__(self, name: str, category: str, brand: str, price: float, rating: float, availability: bool):
        self.name = name
        self.category = category
        self.brand = brand
        self.price = price
        self.rating = rating
        self.availability = availability

# Class to represent a shopping list
class ShoppingList:
    def __init__(self, name: str):
        self.name = name
        self.items: Dict[str, Product] = {}

    def add_item(self, product: Product):
        self.items[product.name] = product

    def remove_item(self, product_name: str):
        if product_name in self.items:
            del self.items[product_name]

    def update_item(self, product_name: str, new_product: Product):
        if product_name in self.items:
            self.items[product_name] = new_product

# Class to represent a user
class User:
    def __init__(self, name: str):
        self.name = name
        self.shopping_lists: Dict[str, ShoppingList] = {}
        self.preferences: Dict[str, float] = {}

    def create_shopping_list(self, list_name: str):
        self.shopping_lists[list_name] = ShoppingList(list_name)

    def add_to_shopping_list(self, list_name: str, product: Product):
        if list_name in self.shopping_lists:
            self.shopping_lists[list_name].add_item(product)

    def remove_from_shopping_list(self, list_name: str, product_name: str):
        if list_name in self.shopping_lists:
            self.shopping_lists[list_name].remove_item(product_name)

    def update_shopping_list(self, list_name: str, product_name: str, new_product: Product):
        if list_name in self.shopping_lists:
            self.shopping_lists[list_name].update_item(product_name, new_product)

# Class to represent the ShopCollab application
class ShopCollab:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.products: Dict[str, Product] = {}
        self.recommendations: Dict[str, List[Product]] = {}
        self.notifications: Dict[str, List[str]] = {}

    def create_user(self, user_name: str):
        self.users[user_name] = User(user_name)

    def create_product(self, product_name: str, category: str, brand: str, price: float, rating: float, availability: bool):
        self.products[product_name] = Product(product_name, category, brand, price, rating, availability)

    def add_to_recommendations(self, user_name: str, product: Product):
        if user_name in self.recommendations:
            self.recommendations[user_name].append(product)
        else:
            self.recommendations[user_name] = [product]

    def send_notification(self, user_name: str, message: str):
        if user_name in self.notifications:
            self.notifications[user_name].append(message)
        else:
            self.notifications[user_name] = [message]

    def search_products(self, query: str, filter_by: str = None):
        results = []
        for product in self.products.values():
            if query.lower() in product.name.lower() or query.lower() in product.category.lower() or query.lower() in product.brand.lower():
                if filter_by is None or (filter_by == 'price' and product.price <= 100) or (filter_by == 'rating' and product.rating >= 4) or (filter_by == 'availability' and product.availability):
                    results.append(product)
        return results

# Function to simulate real-time updates
def simulate_real_time_updates(shop_collab: ShopCollab):
    while True:
        # Simulate price drops
        for product in shop_collab.products.values():
            if random.random() < 0.1:
                product.price -= 1
                print(f"Price drop: {product.name} now costs {product.price}")

        # Simulate product availability changes
        for product in shop_collab.products.values():
            if random.random() < 0.1:
                product.availability = not product.availability
                print(f"Availability change: {product.name} is now {'available' if product.availability else 'unavailable'}")

        # Simulate user interactions
        for user in shop_collab.users.values():
            if random.random() < 0.1:
                list_name = random.choice(list(user.shopping_lists.keys()))
                product_name = random.choice(list(user.shopping_lists[list_name].items.keys()))
                new_product = shop_collab.products[product_name]
                user.update_shopping_list(list_name, product_name, new_product)
                print(f"User {user.name} updated shopping list {list_name} with {product_name}")

        time.sleep(1)

# Main function
def main():
    shop_collab = ShopCollab()

    # Create users
    shop_collab.create_user("User1")
    shop_collab.create_user("User2")

    # Create products
    shop_collab.create_product("Product1", "Category1", "Brand1", 10.99, 4.5, True)
    shop_collab.create_product("Product2", "Category2", "Brand2", 9.99, 4.2, False)

    # Add products to recommendations
    shop_collab.add_to_recommendations("User1", shop_collab.products["Product1"])
    shop_collab.add_to_recommendations("User2", shop_collab.products["Product2"])

    # Simulate real-time updates
    threading.Thread(target=simulate_real_time_updates, args=(shop_collab,)).start()

    # Search products
    results = shop_collab.search_products("Product1")
    print("Search results:")
    for result in results:
        print(result.name)

    # Send notifications
    shop_collab.send_notification("User1", "Price drop: Product1 now costs 9.99")
    shop_collab.send_notification("User2", "Product2 is now available")

    # Print notifications
    for user, notifications in shop_collab.notifications.items():
        print(f"Notifications for {user}:")
        for notification in notifications:
            print(notification)

if __name__ == "__main__":
    main()