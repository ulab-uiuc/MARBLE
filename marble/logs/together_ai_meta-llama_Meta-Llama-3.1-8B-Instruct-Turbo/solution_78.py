# solution.py

# Importing required libraries
import threading
import time
import random
from datetime import datetime

# Class to represent a product
class Product:
    def __init__(self, name, category, brand, price, rating, availability):
        self.name = name
        self.category = category
        self.brand = brand
        self.price = price
        self.rating = rating
        self.availability = availability

# Class to represent a shopping list
class ShoppingList:
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.items = []
        self.shared = False

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item_name):
        self.items = [item for item in self.items if item.name != item_name]

    def modify_item(self, item_name, new_price, new_rating):
        for item in self.items:
            if item.name == item_name:
                item.price = new_price
                item.rating = new_rating
                break

# Class to represent a user
class User:
    def __init__(self, name):
        self.name = name
        self.shopping_lists = []
        self.preferences = {}

    def create_shopping_list(self, name):
        self.shopping_lists.append(ShoppingList(name, self.name))

    def add_to_shopping_list(self, list_name, item):
        for list in self.shopping_lists:
            if list.name == list_name:
                list.add_item(item)
                break

    def remove_from_shopping_list(self, list_name, item_name):
        for list in self.shopping_lists:
            if list.name == list_name:
                list.remove_item(item_name)
                break

    def modify_shopping_list_item(self, list_name, item_name, new_price, new_rating):
        for list in self.shopping_lists:
            if list.name == list_name:
                list.modify_item(item_name, new_price, new_rating)
                break

# Class to represent the ShopCollab application
class ShopCollab:
    def __init__(self):
        self.users = []
        self.products = []
        self.shopping_lists = []
        self.notifications = []

    def create_user(self, name):
        self.users.append(User(name))

    def create_product(self, name, category, brand, price, rating, availability):
        self.products.append(Product(name, category, brand, price, rating, availability))

    def create_shopping_list(self, name, owner):
        self.shopping_lists.append(ShoppingList(name, owner))

    def add_item_to_shopping_list(self, list_name, item_name):
        for list in self.shopping_lists:
            if list.name == list_name:
                for product in self.products:
                    if product.name == item_name:
                        list.add_item(product)
                        break
                break

    def remove_item_from_shopping_list(self, list_name, item_name):
        for list in self.shopping_lists:
            if list.name == list_name:
                for item in list.items:
                    if item.name == item_name:
                        list.remove_item(item_name)
                        break
                break

    def modify_shopping_list_item(self, list_name, item_name, new_price, new_rating):
        for list in self.shopping_lists:
            if list.name == list_name:
                for item in list.items:
                    if item.name == item_name:
                        item.price = new_price
                        item.rating = new_rating
                        break
                break

    def get_recommendations(self, user_name):
        user = next((user for user in self.users if user.name == user_name), None)
        if user:
            recommendations = []
            for product in self.products:
                if product.name not in user.preferences:
                    recommendations.append(product)
            return recommendations
        return []

    def send_notification(self, message):
        self.notifications.append(message)

    def search_products(self, query):
        results = []
        for product in self.products:
            if query.lower() in product.name.lower() or query.lower() in product.category.lower() or query.lower() in product.brand.lower():
                results.append(product)
        return results

# Main function
def main():
    shop_collab = ShopCollab()

    # Create users
    shop_collab.create_user("John")
    shop_collab.create_user("Jane")

    # Create products
    shop_collab.create_product("Product 1", "Category 1", "Brand 1", 10.99, 4.5, True)
    shop_collab.create_product("Product 2", "Category 2", "Brand 2", 9.99, 4.2, False)

    # Create shopping lists
    shop_collab.create_shopping_list("List 1", "John")
    shop_collab.create_shopping_list("List 2", "Jane")

    # Add items to shopping lists
    shop_collab.add_item_to_shopping_list("List 1", "Product 1")
    shop_collab.add_item_to_shopping_list("List 2", "Product 2")

    # Get recommendations
    print("Recommendations for John:")
    for product in shop_collab.get_recommendations("John"):
        print(product.name)

    # Send notification
    shop_collab.send_notification("Product 1 is now available!")

    # Search products
    print("Search results for 'Product 1':")
    for product in shop_collab.search_products("Product 1"):
        print(product.name)

# Run the main function
if __name__ == "__main__":
    main()