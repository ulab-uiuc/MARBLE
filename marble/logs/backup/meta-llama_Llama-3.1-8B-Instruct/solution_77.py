# user.py
class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.watchlist = []
        self.groups = []

    def add_product(self, product):
        self.watchlist.append(product)

    def add_group(self, group):
        self.groups.append(group)

    def __str__(self):
        return f"User: {self.email}"


# product.py
class Product:
    def __init__(self, url, name, price):
        self.url = url
        self.name = name
        self.price = price
        self.thresholds = []

    def add_threshold(self, threshold):
        self.thresholds.append(threshold)

    def __str__(self):
        return f"Product: {self.name} - Price: {self.price}"


# threshold.py
class Threshold:
    def __init__(self, price, user):
        self.price = price
        self.user = user

    def __str__(self):
        return f"Threshold: {self.price} - User: {self.user.email}"


# group.py
class Group:
    def __init__(self, name):
        self.name = name
        self.members = []
        self.products = []

    def add_member(self, member):
        self.members.append(member)

    def add_product(self, product):
        self.products.append(product)

    def __str__(self):
        return f"Group: {self.name}"


# price_tracker.py
class PriceTracker:
    def __init__(self):
        self.users = []
        self.products = []
        self.groups = []

    def register_user(self, email, password):
        user = User(email, password)
        self.users.append(user)
        return user

    def login_user(self, email, password):
        for user in self.users:
            if user.email == email and user.password == password:
                return user
        return None

    def create_group(self, name):
        group = Group(name)
        self.groups.append(group)
        return group

    def add_product(self, url, name, price):
        product = Product(url, name, price)
        self.products.append(product)
        return product

    def add_threshold(self, product, price, user):
        product.add_threshold(Threshold(price, user))

    def share_alert(self, product, group):
        group.add_product(product)

    def compare_prices(self, product):
        # This method would compare prices across different online retailers
        # For simplicity, it just returns the current price
        return product.price

    def get_price_trend(self, product):
        # This method would provide insights on historical price trends
        # For simplicity, it just returns a random trend
        return "Increasing"

    def suggest_purchase(self, product):
        # This method would suggest the best time to make a purchase
        # For simplicity, it just returns a random suggestion
        return "Now"

    def notify_user(self, user, product):
        # This method would notify the user via email or in-app notifications
        # For simplicity, it just prints a message
        print(f"Notification: {product.name} is now below your threshold of {product.thresholds[0].price}")


# solution.py
class PriceTrackerCollaborator:
    def __init__(self):
        self.price_tracker = PriceTracker()

    def run(self):
        while True:
            print("1. Register User")
            print("2. Login User")
            print("3. Create Group")
            print("4. Add Product")
            print("5. Add Threshold")
            print("6. Share Alert")
            print("7. Compare Prices")
            print("8. Get Price Trend")
            print("9. Suggest Purchase")
            print("10. Notify User")
            print("11. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                email = input("Enter email: ")
                password = input("Enter password: ")
                self.price_tracker.price_tracker.register_user(email, password)
            elif choice == "2":
                email = input("Enter email: ")
                password = input("Enter password: ")
                user = self.price_tracker.price_tracker.login_user(email, password)
                if user:
                    print("User logged in successfully")
                else:
                    print("Invalid email or password")
            elif choice == "3":
                name = input("Enter group name: ")
                group = self.price_tracker.price_tracker.create_group(name)
                print(f"Group {name} created successfully")
            elif choice == "4":
                url = input("Enter product URL: ")
                name = input("Enter product name: ")
                price = float(input("Enter product price: "))
                product = self.price_tracker.price_tracker.add_product(url, name, price)
                print(f"Product {name} added successfully")
            elif choice == "5":
                product_name = input("Enter product name: ")
                price = float(input("Enter price threshold: "))
                user_email = input("Enter user email: ")
                user = next((user for user in self.price_tracker.price_tracker.users if user.email == user_email), None)
                if user:
                    product = next((product for product in self.price_tracker.price_tracker.products if product.name == product_name), None)
                    if product:
                        self.price_tracker.price_tracker.add_threshold(product, price, user)
                        print(f"Threshold added successfully for product {product_name}")
                    else:
                        print("Product not found")
                else:
                    print("User not found")
            elif choice == "6":
                product_name = input("Enter product name: ")
                group_name = input("Enter group name: ")
                group = next((group for group in self.price_tracker.price_tracker.groups if group.name == group_name), None)
                if group:
                    product = next((product for product in self.price_tracker.price_tracker.products if product.name == product_name), None)
                    if product:
                        self.price_tracker.price_tracker.share_alert(product, group)
                        print(f"Alert shared successfully for product {product_name}")
                    else:
                        print("Product not found")
                else:
                    print("Group not found")
            elif choice == "7":
                product_name = input("Enter product name: ")
                product = next((product for product in self.price_tracker.price_tracker.products if product.name == product_name), None)
                if product:
                    print(f"Current price of product {product_name}: {self.price_tracker.price_tracker.compare_prices(product)}")
                else:
                    print("Product not found")
            elif choice == "8":
                product_name = input("Enter product name: ")
                product = next((product for product in self.price_tracker.price_tracker.products if product.name == product_name), None)
                if product:
                    print(f"Price trend of product {product_name}: {self.price_tracker.price_tracker.get_price_trend(product)}")
                else:
                    print("Product not found")
            elif choice == "9":
                product_name = input("Enter product name: ")
                product = next((product for product in self.price_tracker.price_tracker.products if product.name == product_name), None)
                if product:
                    print(f"Suggested purchase time for product {product_name}: {self.price_tracker.price_tracker.suggest_purchase(product)}")
                else:
                    print("Product not found")
            elif choice == "10":
                user_email = input("Enter user email: ")
                product_name = input("Enter product name: ")
                user = next((user for user in self.price_tracker.price_tracker.users if user.email == user_email), None)
                if user:
                    product = next((product for product in self.price_tracker.price_tracker.products if product.name == product_name), None)
                    if product:
                        self.price_tracker.price_tracker.notify_user(user, product)
                    else:
                        print("Product not found")
                else:
                    print("User not found")
            elif choice == "11":
                break
            else:
                print("Invalid choice")


if __name__ == "__main__":
    collaborator = PriceTrackerCollaborator()
    collaborator.run()