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

    def add_menu_item(self, item_name, price):
        """Add an item to the restaurant's menu."""
        self.menu[item_name] = price

    def place_order(self, order):
        """Place an order at the restaurant."""
        self.orders.append(order)
        return f"Order received by {self.name}: {order}"

# Define a class to represent a Delivery Agent
class DeliveryAgent:
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def assign_task(self, task):
        """Assign a delivery task to the agent."""
        self.tasks.append(task)

    def update_task_status(self, task_id, status):
        """Update the status of a delivery task."""
        for task in self.tasks:
            if task['id'] == task_id:
                task['status'] = status
                return f"Task {task_id} status updated to {status}"
        return "Task not found."

# Define a class to represent the MultiServe system
class MultiServe:
    def __init__(self):    def place_order(self, user_order):
        """Place an order that may include items from multiple restaurants, handling edge cases."""
        order_details = defaultdict(list)
        unavailable_restaurants = []
        for item, restaurant_name in user_order.items():
            if restaurant_name in self.restaurants:
                order_details[restaurant_name].append(item)
            else:
                unavailable_restaurants.append(restaurant_name)
        if unavailable_restaurants:
            return f"Restaurants not found: {', '.join(unavailable_restaurants)}"

        # Send order details to each restaurant
        for restaurant_name, items in order_details.items():
            order_response = self.restaurants[restaurant_name].place_order(items)
            self.orders.append({'restaurant': restaurant_name, 'items': items})
            print(order_response)

        # Assign delivery tasks to agents
        self.assign_delivery_tasks()        order_details = defaultdict(list)
        unavailable_restaurants = []
        for item, restaurant_name in user_order.items():
            if restaurant_name in self.restaurants:
                order_details[restaurant_name].append(item)
            else:
                unavailable_restaurants.append(restaurant_name)
        if unavailable_restaurants:
            return f"Restaurants not found: {', '.join(unavailable_restaurants)}"

        # Send order details to each restaurant
        for restaurant_name, items in order_details.items():
            order_response = self.restaurants[restaurant_name].place_order(items)
            self.orders.append({'restaurant': restaurant_name, 'items': items})
            print(order_response)        # Assign delivery tasks to agents
        self.assign_delivery_tasks()

    def assign_delivery_tasks(self):
        """Assign delivery tasks to available delivery agents."""
        available_agents = list(self.delivery_agents.values())
        for order in self.orders:
            if available_agents:
                agent = random.choice(available_agents)
                task = {'id': len(agent.tasks) + 1, 'order': order, 'status': 'Assigned'}
                agent.assign_task(task)
                print(f"Assigned task {task['id']} to {agent.name} for order: {order['items']}")
            else:
                print("No available delivery agents.")

# Example usage
if __name__ == "__main__":
    # Create restaurants
    restaurant1 = Restaurant("Pizza Place")
    restaurant1.add_menu_item("Margherita Pizza", 10)
    restaurant1.add_menu_item("Pepperoni Pizza", 12)

    restaurant2 = Restaurant("Sushi Spot")
    restaurant2.add_menu_item("California Roll", 8)
    restaurant2.add_menu_item("Tuna Sashimi", 15)

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
    user_order = {
        "Margherita Pizza": "Pizza Place",
        "California Roll": "Sushi Spot"
    }
    multi_serve.place_order(user_order)

    # Simulate delivery status updates
    time.sleep(1)  # Simulate time delay for delivery
    agent1.update_task_status(1, "Delivered")
    agent2.update_task_status(2, "Delivered")