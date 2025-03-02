# solution.py

# Import necessary libraries
from collections import defaultdict
import random
import time

# Define a class to represent a Restaurant
class Restaurant:
    def __init__(self, name):
        self.name = name
        self.menu = {}
        self.orders = []

    def add_item_to_menu(self, item_name, price):
        """Add an item to the restaurant's menu."""
        self.menu[item_name] = price

    def receive_order(self, order):
        """Receive an order and add it to the restaurant's orders."""
        self.orders.append(order)

    def is_available(self):
        """Check if the restaurant is available to take orders."""
        return True  # For simplicity, we assume all restaurants are available

# Define a class to represent a Delivery Agent
class DeliveryAgent:
    def __init__(self, name):
        self.name = name
        self.assigned_orders = []

    def assign_order(self, order):
        """Assign an order to the delivery agent."""
        self.assigned_orders.append(order)

    def update_order_status(self, order, status):
        """Update the status of the assigned order."""
        order['status'] = status

# Define a class to represent the MultiServe system
class MultiServe:
    def __init__(self):
        self.restaurants = []
        self.delivery_agents = []
        self.orders = []

    def add_restaurant(self, restaurant):
        """Add a restaurant to the system."""
        self.restaurants.append(restaurant)

    def add_delivery_agent(self, agent):
        """Add a delivery agent to the system."""
        self.delivery_agents.append(agent)

    def place_order(self, user_order):
        """Place an order that combines items from different restaurants."""
        order_id = random.randint(1000, 9999)  # Generate a random order ID
        order = {'id': order_id, 'items': user_order, 'status': 'Pending'}
        self.orders.append(order)        unavailable_items = []
        order = {'id': order_id, 'items': user_order, 'status': 'Pending'}
        self.orders.append(order)

        # Send order details to each restaurant
        restaurant_orders = defaultdict(list)
        for item in user_order:
            restaurant_orders[item['restaurant']].append(item)

        for restaurant_name, items in restaurant_orders.items():
            restaurant = next((r for r in self.restaurants if r.name == restaurant_name), None)
            if restaurant and restaurant.is_available():
                restaurant.receive_order(order)
            else:
                unavailable_items.extend(items)
                print(f"Restaurant {restaurant_name} is unavailable for items: {items}")

        if unavailable_items:
            print("Some items are unavailable. Please remove them or cancel the order.")
            return None        # Send order details to each restaurant
        restaurant_orders = defaultdict(list)
        for item in user_order:
            restaurant_orders[item['restaurant']].append(item)

        for restaurant_name, items in restaurant_orders.items():
            restaurant = next((r for r in self.restaurants if r.name == restaurant_name), None)
            if restaurant and restaurant.is_available():
                restaurant.receive_order(order)
            else:
                print(f"Restaurant {restaurant_name} is unavailable.")

        return order

    def assign_delivery(self, order):
        """Assign delivery tasks to delivery agents."""
        available_agents = [agent for agent in self.delivery_agents if len(agent.assigned_orders) < 2]
        if len(available_agents) < 2:
            print("Not enough delivery agents available.")
            return

        # Assign to two different agents
        for agent in available_agents[:2]:
            agent.assign_order(order)

    def update_order_status(self, order_id, status):
        """Update the status of an order."""
        order = next((o for o in self.orders if o['id'] == order_id), None)
        if order:
            order['status'] = status
            print(f"Order {order_id} status updated to {status}.")

# Example usage
if __name__ == "__main__":
    # Create restaurants
    restaurant1 = Restaurant("Pizza Place")
    restaurant1.add_item_to_menu("Margherita Pizza", 10)
    restaurant1.add_item_to_menu("Pepperoni Pizza", 12)

    restaurant2 = Restaurant("Sushi Spot")
    restaurant2.add_item_to_menu("California Roll", 8)
    restaurant2.add_item_to_menu("Tuna Sashimi", 15)

    # Create delivery agents
    agent1 = DeliveryAgent("Alice")
    agent2 = DeliveryAgent("Bob")

    # Initialize MultiServe system
    multi_serve = MultiServe()
    multi_serve.add_restaurant(restaurant1)
    multi_serve.add_restaurant(restaurant2)
    multi_serve.add_delivery_agent(agent1)
    multi_serve.add_delivery_agent(agent2)

    # User places an order
    user_order = [
        {'restaurant': "Pizza Place", 'item': "Margherita Pizza", 'quantity': 1},
        {'restaurant': "Sushi Spot", 'item': "California Roll", 'quantity': 2}
    ]
    order = multi_serve.place_order(user_order)
    print(f"Order placed: {order}")

    # Assign delivery
    multi_serve.assign_delivery(order)

    # Simulate order status updates
    time.sleep(1)  # Simulate time delay
    multi_serve.update_order_status(order['id'], "Ready for pickup")
    time.sleep(1)  # Simulate time delay
    multi_serve.update_order_status(order['id'], "Delivered")