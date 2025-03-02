# user_management.py
class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.shopping_list = []
        self.budget = 0

class UserManagement:
    def __init__(self):
        self.users = {}

    def register(self, username, password, email):
        if username in self.users:
            print("Username already exists.")
            return
        self.users[username] = User(username, password, email)
        print("User registered successfully.")

    def login(self, username, password):
        if username not in self.users:
            print("Username does not exist.")
            return
        if self.users[username].password != password:
            print("Incorrect password.")
            return
        print("User logged in successfully.")

    def logout(self, username):
        if username not in self.users:
            print("Username does not exist.")
            return
        print("User logged out successfully.")

    def update_budget(self, username, budget):
        if username not in self.users:
            print("Username does not exist.")
            return
        self.users[username].budget = budget
        print("Budget updated successfully.")

    def get_user(self, username):
        if username not in self.users:
            print("Username does not exist.")
            return
        return self.users[username]


# product_comparison.py
class Product:
    def __init__(self, name, price, reviews):
        self.name = name
        self.price = price
        self.reviews = reviews

class ProductComparison:
    def __init__(self):
        self.products = {}

    def add_product(self, name, price, reviews):
        self.products[name] = Product(name, price, reviews)

    def get_product(self, name):
        if name not in self.products:
            print("Product does not exist.")
            return
        return self.products[name]

    def compare_products(self, product1, product2):
        if product1 not in self.products or product2 not in self.products:
            print("One or both products do not exist.")
            return
        print(f"Product 1: {self.products[product1].name}, Price: {self.products[product1].price}, Reviews: {self.products[product1].reviews}")
        print(f"Product 2: {self.products[product2].name}, Price: {self.products[product2].price}, Reviews: {self.products[product2].reviews}")


# collaborative_shopping_list.py
class CollaborativeShoppingList:
    def __init__(self):
        self.shopping_list = {}

    def add_item(self, username, item):
        if username not in self.shopping_list:
            self.shopping_list[username] = []
        self.shopping_list[username].append(item)
        print(f"Item '{item}' added to {username}'s shopping list.")

    def remove_item(self, username, item):
        if username not in self.shopping_list:
            print("Username does not exist.")
            return
        if item not in self.shopping_list[username]:
            print("Item does not exist in the shopping list.")
            return
        self.shopping_list[username].remove(item)
        print(f"Item '{item}' removed from {username}'s shopping list.")

    def get_shopping_list(self, username):
        if username not in self.shopping_list:
            print("Username does not exist.")
            return
        return self.shopping_list[username]


# budget_management.py
class BudgetManagement:
    def __init__(self):
        self.budgets = {}

    def set_budget(self, username, budget):
        self.budgets[username] = budget
        print(f"Budget set to {budget} for {username}.")

    def get_budget(self, username):
        if username not in self.budgets:
            print("Username does not exist.")
            return
        return self.budgets[username]

    def check_budget(self, username, amount):
        if username not in self.budgets:
            print("Username does not exist.")
            return
        if amount > self.budgets[username]:
            print(f"{username}'s budget is exceeded.")
        else:
            print(f"{username}'s budget is not exceeded.")


# recommendation_engine.py
class RecommendationEngine:
    def __init__(self):
        self.recommendations = {}

    def add_recommendation(self, username, product):
        if username not in self.recommendations:
            self.recommendations[username] = []
        self.recommendations[username].append(product)
        print(f"Product '{product}' recommended to {username}.")

    def get_recommendations(self, username):
        if username not in self.recommendations:
            print("Username does not exist.")
            return
        return self.recommendations[username]


# CollaborativeShoppingAssistant.py
class CollaborativeShoppingAssistant:
    def __init__(self):
        self.user_management = UserManagement()
        self.product_comparison = ProductComparison()
        self.collaborative_shopping_list = CollaborativeShoppingList()
        self.budget_management = BudgetManagement()
        self.recommendation_engine = RecommendationEngine()

    def register_user(self, username, password, email):
        self.user_management.register(username, password, email)

    def login_user(self, username, password):
        self.user_management.login(username, password)

    def logout_user(self, username):
        self.user_management.logout(username)

    def update_budget(self, username, budget):
        self.user_management.update_budget(username, budget)

    def add_product(self, name, price, reviews):
        self.product_comparison.add_product(name, price, reviews)

    def compare_products(self, product1, product2):
        self.product_comparison.compare_products(product1, product2)

    def add_item_to_shopping_list(self, username, item):
        self.collaborative_shopping_list.add_item(username, item)

    def remove_item_from_shopping_list(self, username, item):
        self.collaborative_shopping_list.remove_item(username, item)

    def get_shopping_list(self, username):
        return self.collaborative_shopping_list.get_shopping_list(username)

    def set_budget(self, username, budget):
        self.budget_management.set_budget(username, budget)

    def get_budget(self, username):
        return self.budget_management.get_budget(username)

    def check_budget(self, username, amount):
        self.budget_management.check_budget(username, amount)

    def add_recommendation(self, username, product):
        self.recommendation_engine.add_recommendation(username, product)

    def get_recommendations(self, username):
        return self.recommendation_engine.get_recommendations(username)


# solution.py
def main():
    assistant = CollaborativeShoppingAssistant()

    while True:
        print("1. Register User")
        print("2. Login User")
        print("3. Logout User")
        print("4. Update Budget")
        print("5. Add Product")
        print("6. Compare Products")
        print("7. Add Item to Shopping List")
        print("8. Remove Item from Shopping List")
        print("9. Get Shopping List")
        print("10. Set Budget")
        print("11. Get Budget")
        print("12. Check Budget")
        print("13. Add Recommendation")
        print("14. Get Recommendations")
        print("15. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            email = input("Enter email: ")
            assistant.register_user(username, password, email)
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            assistant.login_user(username, password)
        elif choice == "3":
            username = input("Enter username: ")
            assistant.logout_user(username)
        elif choice == "4":
            username = input("Enter username: ")
            budget = float(input("Enter budget: "))
            assistant.update_budget(username, budget)
        elif choice == "5":
            name = input("Enter product name: ")
            price = float(input("Enter product price: "))
            reviews = input("Enter product reviews: ")
            assistant.add_product(name, price, reviews)
        elif choice == "6":
            product1 = input("Enter product 1 name: ")
            product2 = input("Enter product 2 name: ")
            assistant.compare_products(product1, product2)
        elif choice == "7":
            username = input("Enter username: ")
            item = input("Enter item name: ")
            assistant.add_item_to_shopping_list(username, item)
        elif choice == "8":
            username = input("Enter username: ")
            item = input("Enter item name: ")
            assistant.remove_item_from_shopping_list(username, item)
        elif choice == "9":
            username = input("Enter username: ")
            print(assistant.get_shopping_list(username))
        elif choice == "10":
            username = input("Enter username: ")
            budget = float(input("Enter budget: "))
            assistant.set_budget(username, budget)
        elif choice == "11":
            username = input("Enter username: ")
            print(assistant.get_budget(username))
        elif choice == "12":
            username = input("Enter username: ")
            amount = float(input("Enter amount: "))
            assistant.check_budget(username, amount)
        elif choice == "13":
            username = input("Enter username: ")
            product = input("Enter product name: ")
            assistant.add_recommendation(username, product)
        elif choice == "14":
            username = input("Enter username: ")
            print(assistant.get_recommendations(username))
        elif choice == "15":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()