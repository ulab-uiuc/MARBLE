# solution.py

# Importing required libraries
import datetime
import random
import time

# Restaurant class
class Restaurant:
    def __init__(self, name, menu):
        self.name = name
        self.menu = menu
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def get_order_status(self):
        return self.orders


# Delivery Agent class
class DeliveryAgent:
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def assign_task(self, task):
        self.tasks.append(task)

    def update_task_status(self, status):
        for task in self.tasks:
            if task['id'] == status['id']:
                task['status'] = status['status']
                break


# User class
class User:
    def __init__(self, name):
        self.name = name
        self.cart = []

    def add_item_to_cart(self, item):
        self.cart.append(item)

    def place_order(self, restaurant, delivery_agent):
        order = {
            'id': random.randint(1, 100),
            'items': self.cart,
            'restaurant': restaurant.name,
            'delivery_agent': delivery_agent.name
        }
        restaurant.add_order(order)
        delivery_agent.assign_task(order)
        return order


# System class
class System:
    def __init__(self):
        self.restaurants = []
        self.delivery_agents = []
        self.users = []

    def add_restaurant(self, restaurant):
        self.restaurants.append(restaurant)

    def add_delivery_agent(self, delivery_agent):
        self.delivery_agents.append(delivery_agent)

    def add_user(self, user):
        self.users.append(user)

    def send_order_details(self, order):
        for restaurant in self.restaurants:
            if restaurant.name == order['restaurant']:
                print(f"Sending order details to {restaurant.name}")
                # Simulate sending order details to the restaurant
                time.sleep(2)
                print(f"Order details sent to {restaurant.name}")

    def update_order_status(self, order, status):
        for restaurant in self.restaurants:
            if restaurant.name == order['restaurant']:
                restaurant.orders[order['id'] - 1]['status'] = status
                print(f"Order status updated for {restaurant.name}")

    def assign_delivery_task(self, order):
        for delivery_agent in self.delivery_agents:
            delivery_agent.assign_task(order)
            print(f"Delivery task assigned to {delivery_agent.name}")

    def notify_user(self, order):
        print(f"Notifying user that order is ready for pickup or has been delivered")


# Test cases
def test_user_places_order():
    system = System()
    user = User("John")
    restaurant = Restaurant("Pizza Hut", ["Pizza", "Burger"])
    delivery_agent = DeliveryAgent("Agent 1")
    system.add_user(user)
    system.add_restaurant(restaurant)
    system.add_delivery_agent(delivery_agent)
    order = user.place_order(restaurant, delivery_agent)
    system.send_order_details(order)
    system.assign_delivery_task(order)
    system.notify_user(order)


def test_system_updates_order_status():
    system = System()
    user = User("John")
    restaurant = Restaurant("Pizza Hut", ["Pizza", "Burger"])
    delivery_agent = DeliveryAgent("Agent 1")
    system.add_user(user)
    system.add_restaurant(restaurant)
    system.add_delivery_agent(delivery_agent)
    order = user.place_order(restaurant, delivery_agent)
    system.update_order_status(order, "Delivered")
    print("Order status updated")


def test_system_handles_edge_cases():
    system = System()
    user = User("John")
    restaurant = Restaurant("Pizza Hut", ["Pizza", "Burger"])
    delivery_agent = DeliveryAgent("Agent 1")
    system.add_user(user)
    system.add_restaurant(restaurant)
    system.add_delivery_agent(delivery_agent)
    order = user.place_order(restaurant, delivery_agent)
    # Simulate restaurant being unavailable
    restaurant.menu = []
    print("Restaurant unavailable")
    # Simulate delivery agent declining task
    delivery_agent.tasks = []
    print("Delivery agent declined task")
    # Simulate user canceling order
    user.cart = []
    print("User canceled order")


# Run test cases
test_user_places_order()
test_system_updates_order_status()
test_system_handles_edge_cases()

# Delivery Agent interface
def delivery_agent_interface():
    delivery_agent = DeliveryAgent("Agent 1")
    print("Delivery Agent Interface")
    print("1. View assigned tasks")
    print("2. Update task status")
    choice = input("Enter your choice: ")
    if choice == "1":
        print("Assigned tasks:")
        for task in delivery_agent.tasks:
            print(task)
    elif choice == "2":
        task_id = int(input("Enter task ID: "))
        status = input("Enter task status: ")
        delivery_agent.update_task_status({'id': task_id, 'status': status})
        print("Task status updated")


# Run delivery agent interface
delivery_agent_interface()

# User interface
def user_interface():
    user = User("John")
    print("User Interface")
    print("1. Browse menus")
    print("2. Add item to cart")
    print("3. Place order")
    choice = input("Enter your choice: ")
    if choice == "1":
        print("Menus:")
        for restaurant in system.restaurants:
            print(restaurant.name)
    elif choice == "2":
        item = input("Enter item to add to cart: ")
        user.add_item_to_cart(item)
        print("Item added to cart")
    elif choice == "3":
        restaurant_name = input("Enter restaurant name: ")
        for restaurant in system.restaurants:
            if restaurant.name == restaurant_name:
                order = user.place_order(restaurant, delivery_agent)
                print("Order placed")
                break


# Run user interface
user_interface()