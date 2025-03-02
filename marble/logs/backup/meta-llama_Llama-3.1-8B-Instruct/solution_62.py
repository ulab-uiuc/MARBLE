# solution.py

# Importing required libraries
import datetime
import random
import threading

# Restaurant class
class Restaurant:
    def __init__(self, name):
        self.name = name
        self.menu = {
            "Burger": 10.99,
            "Pizza": 12.99,
            "Salad": 8.99
        }
        self.orders = []

    def send_order(self, order):
        print(f"Order sent to {self.name}: {order}")

    def update_order_status(self, order, status):
        for o in self.orders:
            if o["id"] == order["id"]:
                o["status"] = status
                break

# Delivery Agent class
class DeliveryAgent:
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def receive_task(self, task):
        self.tasks.append(task)
        print(f"Task assigned to {self.name}: {task}")

    def update_task_status(self, task, status):
        for t in self.tasks:
            if t["id"] == task["id"]:
                t["status"] = status
                break

# User class
class User:
    def __init__(self, name):
        self.name = name
        self.cart = []
        self.orders = []

    def add_item_to_cart(self, item, price):
        self.cart.append({"item": item, "price": price})

    def place_order(self, restaurant_name, delivery_agent_name):
        order_id = random.randint(1, 100)
        order = {
            "id": order_id,
            "restaurant": restaurant_name,
            "delivery_agent": delivery_agent_name,
            "items": self.cart,
            "status": "pending"
        }
        self.orders.append(order)
        self.cart = []
        return order_id

# MultiServe class
class MultiServe:
    def __init__(self):
        self.restaurants = []
        self.delivery_agents = []
        self.users = []

    def add_restaurant(self, name):
        self.restaurants.append(Restaurant(name))

    def add_delivery_agent(self, name):
        self.delivery_agents.append(DeliveryAgent(name))

    def add_user(self, name):
        self.users.append(User(name))

    def place_order(self, user_name, restaurant_name, delivery_agent_name):
        user = next((u for u in self.users if u.name == user_name), None)    restaurant = next((r for r in self.restaurants if r.name == restaurant_name), None)
    if not restaurant:
        raise ValueError(f"Restaurant '{restaurant_name}' does not exist in the system")order_id = user.place_order(restaurant_name, delivery_agent_name)
            restaurant.send_order({"id": order_id, "items": user.cart})
            delivery_agent.receive_task({"id": order_id, "items": user.cart})
            return order_id
        else:
            return None

    def update_order_status(self, order_id, status):
        for user in self.users:
            for order in user.orders:
                if order["id"] == order_id:
                    order["status"] = status
                    break
        for restaurant in self.restaurants:
            restaurant.update_order_status({"id": order_id, "items": []}, status)
        for delivery_agent in self.delivery_agents:
            delivery_agent.update_task_status({"id": order_id, "items": []}, status)

# Test cases
def test_place_order():
    multiserve = MultiServe()
    multiserve.add_restaurant("Restaurant 1")
    multiserve.add_restaurant("Restaurant 2")
    multiserve.add_delivery_agent("Agent 1")
    multiserve.add_delivery_agent("Agent 2")
    multiserve.add_user("User 1")
    order_id = multiserve.place_order("User 1", "Restaurant 1", "Agent 1")
    assert order_id is not None

def test_update_order_status():
    multiserve = MultiServe()
    multiserve.add_restaurant("Restaurant 1")
    multiserve.add_delivery_agent("Agent 1")
    multiserve.add_user("User 1")
    order_id = multiserve.place_order("User 1", "Restaurant 1", "Agent 1")
    multiserve.update_order_status(order_id, "delivered")
    for user in multiserve.users:
        for order in user.orders:
            assert order["status"] == "delivered"
    for restaurant in multiserve.restaurants:
        assert restaurant.orders[0]["status"] == "delivered"
    for delivery_agent in multiserve.delivery_agents:
        assert delivery_agent.tasks[0]["status"] == "delivered"

# Run test cases
test_place_order()
test_update_order_status()

# Run MultiServe application
multiserve = MultiServe()
multiserve.add_restaurant("Restaurant 1")
multiserve.add_restaurant("Restaurant 2")
multiserve.add_delivery_agent("Agent 1")
multiserve.add_delivery_agent("Agent 2")
multiserve.add_user("User 1")

# Simulate user interaction
user = multiserve.users[0]
user.add_item_to_cart("Burger", 10.99)
user.add_item_to_cart("Pizza", 12.99)
order_id = user.place_order("Restaurant 1", "Agent 1")

# Simulate delivery agent interaction
delivery_agent = multiserve.delivery_agents[0]
delivery_agent.receive_task({"id": order_id, "items": user.cart})

# Simulate order status update
multiserve.update_order_status(order_id, "delivered")

# Print order status
for user in multiserve.users:
    for order in user.orders:
        print(f"Order {order['id']} status: {order['status']}")
for restaurant in multiserve.restaurants:
    for order in restaurant.orders:
        print(f"Order {order['id']} status: {order['status']}")
for delivery_agent in multiserve.delivery_agents:
    for task in delivery_agent.tasks:
        print(f"Task {task['id']} status: {task['status']}")