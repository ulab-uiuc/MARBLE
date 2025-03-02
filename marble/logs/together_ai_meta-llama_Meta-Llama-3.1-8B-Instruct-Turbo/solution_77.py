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
        self.shared_alerts = []

    def add_member(self, member):
        self.members.append(member)

    def share_alert(self, alert):
        self.shared_alerts.append(alert)

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

    def share_alert(self, group, alert):
        group.share_alert(alert)

    def compare_prices(self, product):
        # This method would compare prices across different online retailers
        # For simplicity, it's not implemented here
        pass

    def get_price_trend(self, product):
        # This method would provide insights on historical price trends
        # For simplicity, it's not implemented here
        pass


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
            print("9. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                email = input("Enter email: ")
                password = input("Enter password: ")
                user = self.price_tracker.register_user(email, password)
                print(f"User {user.email} registered successfully")
            elif choice == "2":
                email = input("Enter email: ")
                password = input("Enter password: ")
                user = self.price_tracker.login_user(email, password)
                if user:
                    print(f"User {user.email} logged in successfully")
                else:
                    print("Invalid email or password")
            elif choice == "3":
                name = input("Enter group name: ")
                group = self.price_tracker.create_group(name)
                print(f"Group {group.name} created successfully")
            elif choice == "4":
                url = input("Enter product URL: ")
                name = input("Enter product name: ")
                price = float(input("Enter product price: "))
                product = self.price_tracker.add_product(url, name, price)
                print(f"Product {product.name} added successfully")
            elif choice == "5":
                url = input("Enter product URL: ")
                name = input("Enter product name: ")
                price = float(input("Enter price threshold: "))
                user_email = input("Enter user email: ")
                user = next((user for user in self.price_tracker.price_tracker.users if user.email == user_email), None)
                if user:
                    product = next((product for product in self.price_tracker.price_tracker.products if product.name == name), None)
                    if product:
                        self.price_tracker.add_threshold(product, price, user)
                        print(f"Threshold {price} added for product {product.name} by user {user.email}")
                    else:
                        print("Product not found")
                else:
                    print("User not found")
            elif choice == "6":
                group_name = input("Enter group name: ")
                group = next((group for group in self.price_tracker.price_tracker.groups if group.name == group_name), None)
                if group:
                    alert_name = input("Enter alert name: ")
                    alert_price = float(input("Enter alert price: "))
                    user_email = input("Enter user email: ")
                    user = next((user for user in self.price_tracker.price_tracker.users if user.email == user_email), None)
                    if user:
                        product = next((product for product in self.price_tracker.price_tracker.products if product.name == alert_name), None)
                        if product:
                            self.price_tracker.share_alert(group, Threshold(alert_price, user))
                            print(f"Alert {alert_price} shared with group {group_name} by user {user.email}")
                        else:
                            print("Product not found")
                    else:
                        print("User not found")
                else:
                    print("Group not found")
            elif choice == "7":
                url = input("Enter product URL: ")
                name = input("Enter product name: ")
                product = next((product for product in self.price_tracker.price_tracker.products if product.name == name), None)
                if product:
                    self.price_tracker.compare_prices(product)
                    print(f"Prices compared for product {product.name}")
                else:
                    print("Product not found")
            elif choice == "8":
                url = input("Enter product URL: ")
                name = input("Enter product name: ")
                product = next((product for product in self.price_tracker.price_tracker.products if product.name == name), None)
                if product:
                    self.price_tracker.get_price_trend(product)
                    print(f"Price trend for product {product.name} retrieved")
                else:
                    print("Product not found")
            elif choice == "9":
                break
            else:
                print("Invalid choice")


if __name__ == "__main__":
    collaborator = PriceTrackerCollaborator()
    collaborator.run()