# multi_agent_dine.py

import threading
import time
import random
from datetime import datetime

# Define a class for Delivery Agents
class DeliveryAgent:
    def __init__(self, agent_id, location):
        self.agent_id = agent_id
        self.location = location
        self.delivery_status = "available"
        self.current_load = 0
        self.lock = threading.Lock()

    def update_status(self, status):
        with self.lock:
            self.delivery_status = status

    def update_load(self, load):
        with self.lock:
            self.current_load = load

    def get_status(self):
        with self.lock:
            return self.delivery_status

    def get_load(self):
        with self.lock:
            return self.current_load


# Define a class for Orders
class Order:
    def __init__(self, order_id, restaurant, customer, location):
        self.order_id = order_id
        self.restaurant = restaurant
        self.customer = customer
        self.location = location
        self.status = "pending"
        self.estimated_delivery_time = None
        self.lock = threading.Lock()

    def update_status(self, status):
        with self.lock:
            self.status = status

    def update_estimated_delivery_time(self, time):
        with self.lock:
            self.estimated_delivery_time = time

    def get_status(self):
        with self.lock:
            return self.status

    def get_estimated_delivery_time(self):
        with self.lock:
            return self.estimated_delivery_time


# Define a class for the MultiAgentDine System
class MultiAgentDine:
    def __init__(self):
        self.agents = []
        self.orders = []
        self.lock = threading.Lock()

    def add_agent(self, agent):
        with self.lock:
            self.agents.append(agent)

    def add_order(self, order):
        with self.lock:
            self.orders.append(order)

    def assign_agent(self, order):
        with self.lock:
            # Find the most suitable agent based on proximity, availability, and current load
            suitable_agents = [agent for agent in self.agents if agent.get_status() == "available"]
            if suitable_agents:
                closest_agent = min(suitable_agents, key=lambda agent: self.calculate_distance(order.location, agent.location))
                closest_agent.update_status("busy")
                closest_agent.update_load(closest_agent.get_load() + 1)
                order.update_status("assigned")
                order.update_estimated_delivery_time(self.calculate_estimated_delivery_time(order.location, closest_agent.location))
                return closest_agent
            else:
                return None

    def calculate_distance(self, location1, location2):
        # Calculate the distance between two locations (simplified for demonstration purposes)
        return abs(location1 - location2)

    def calculate_estimated_delivery_time(self, location1, location2):
        # Calculate the estimated delivery time based on the distance (simplified for demonstration purposes)
        distance = self.calculate_distance(location1, location2)
        return datetime.now() + datetime.timedelta(minutes=distance)

    def update_order_status(self, order_id, status):
        with self.lock:
            for order in self.orders:
                if order.order_id == order_id:
                    order.update_status(status)
                    break

    def get_order_status(self, order_id):
        with self.lock:
            for order in self.orders:
                if order.order_id == order_id:
                    return order.get_status()
            return None

    def get_agent_status(self, agent_id):
        with self.lock:
            for agent in self.agents:
                if agent.agent_id == agent_id:
                    return agent.get_status()
            return None


# Define a class for the Restaurant Staff Interface
class RestaurantStaffInterface:
    def __init__(self, multi_agent_dine):
        self.multi_agent_dine = multi_agent_dine

    def submit_order(self, order_id, restaurant, customer, location):
        order = Order(order_id, restaurant, customer, location)
        self.multi_agent_dine.add_order(order)
        agent = self.multi_agent_dine.assign_agent(order)
        if agent:
            print(f"Order {order_id} assigned to Agent {agent.agent_id}")
        else:
            print(f"No available agents for Order {order_id}")

    def track_order_status(self, order_id):
        status = self.multi_agent_dine.get_order_status(order_id)
        if status:
            print(f"Order {order_id} status: {status}")
        else:
            print(f"Order {order_id} not found")


# Define a class for the Customer Interface
class CustomerInterface:
    def __init__(self, multi_agent_dine):
        self.multi_agent_dine = multi_agent_dine

    def place_order(self, order_id, restaurant, customer, location):
        order = Order(order_id, restaurant, customer, location)
        self.multi_agent_dine.add_order(order)
        agent = self.multi_agent_dine.assign_agent(order)
        if agent:
            print(f"Order {order_id} assigned to Agent {agent.agent_id}")
        else:
            print(f"No available agents for Order {order_id}")

    def track_order_status(self, order_id):
        status = self.multi_agent_dine.get_order_status(order_id)
        if status:
            print(f"Order {order_id} status: {status}")
        else:
            print(f"Order {order_id} not found")


# Test the MultiAgentDine System
def test_multi_agent_dine():
    multi_agent_dine = MultiAgentDine()

    # Create delivery agents
    agent1 = DeliveryAgent(1, 0)
    agent2 = DeliveryAgent(2, 5)
    multi_agent_dine.add_agent(agent1)
    multi_agent_dine.add_agent(agent2)

    # Create restaurant staff interface
    restaurant_staff_interface = RestaurantStaffInterface(multi_agent_dine)

    # Create customer interface
    customer_interface = CustomerInterface(multi_agent_dine)

    # Submit orders
    restaurant_staff_interface.submit_order(1, "Restaurant A", "Customer A", 3)
    customer_interface.place_order(2, "Restaurant B", "Customer B", 7)

    # Track order status
    restaurant_staff_interface.track_order_status(1)
    customer_interface.track_order_status(2)

    # Update order status
    multi_agent_dine.update_order_status(1, "delivered")
    restaurant_staff_interface.track_order_status(1)

    # Get agent status
    print(f"Agent 1 status: {multi_agent_dine.get_agent_status(1)}")


# Run the test
test_multi_agent_dine()