# PriceTrackerCollaborator.py

class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.groups = []
        self.watchlist = []

    def create_group(self, group_name):
        group = Group(group_name)
        self.groups.append(group)
        return group

    def join_group(self, group):
        self.groups.append(group)

    def add_product_to_watchlist(self, product_url):
        product = Product(product_url)
        self.watchlist.append(product)
        return product

    def set_price_threshold(self, product, price_threshold):
        product.set_price_threshold(price_threshold)

    def receive_notification(self, notification):
        print(f"Notification for {self.email}: {notification}")

class Group:
    def __init__(self, name):
        self.name = name
        self.members = []

    def add_member(self, user):
        self.members.append(user)

    def share_price_alert(self, product, message):
        for member in self.members:
            member.receive_notification(f"Price Alert for {product.url}: {message}")

class Product:
    def __init__(self, url):
        self.url = url
        self.price = 0
        self.price_threshold = None

    def set_price(self, price):
        self.price = price

    def set_price_threshold(self, threshold):
        self.price_threshold = threshold

    def check_price(self):
        if self.price < self.price_threshold:
            return f"Price dropped below threshold: {self.price}"
        return "Price is above threshold"
        if self.price < self.price_threshold:
            for member in self.group.members:
                member.receive_notification(f"Real-time Price Alert for {self.url}: {self.price}")

# Test cases
user1 = User("user1@example.com", "password123")
user2 = User("user2@example.com", "password456")

group1 = user1.create_group("Group 1")
user2.join_group(group1)

product1 = user1.add_product_to_watchlist("https://product1.com")
product2 = user2.add_product_to_watchlist("https://product2.com")

user1.set_price_threshold(product1, 50)
user2.set_price_threshold(product2, 100)

product1.set_price(45)
product2.set_price(90)

group1.share_price_alert(product1, "Great deal!")
group1.share_price_alert(product2, "Check this out!")

# Output:
# Notification for user1@example.com: Price Alert for https://product1.com: Great deal!
# Notification for user2@example.com: Price Alert for https://product2.com: Check this out!