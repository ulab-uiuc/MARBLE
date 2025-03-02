# solution.py

# Importing required libraries
import math
import random
import time

# Agent class representing a delivery agent
class Agent:
    def __init__(self, id, location, availability):
        self.id = id
        self.location = location
        self.availability = availability
        self.current_load = 0
        self.delivery_status = "Available"

    def update_availability(self, status):
        self.availability = status

    def update_current_load(self, load):
        self.current_load = load

    def update_delivery_status(self, status):
        self.delivery_status = status


# Order class representing a food order
class Order:
    def __init__(self, order_id, restaurant, customer_location, order_time):
        self.order_id = order_id
        self.restaurant = restaurant
        self.customer_location = customer_location
        self.order_time = order_time
        self.delivery_status = "Placed"
        self.assigned_agent = None

    def update_delivery_status(self, status):
        self.delivery_status = status

    def assign_agent(self, agent):
        self.assigned_agent = agent


# Restaurant class representing a restaurant
class Restaurant:
    def __init__(self, id, location):
        self.id = id
        self.location = location

    def submit_order(self, order):
        print(f"Order submitted from restaurant {self.id} at {self.location}")


# Customer class representing a customer
class Customer:
    def __init__(self, id, location):
        self.id = id
        self.location = location

    def place_order(self, order):
        print(f"Order placed by customer {self.id} at {self.location}")


# Communication protocol class
class CommunicationProtocol:
    def __init__(self):
        self.agents = []
        self.orders = []
        self.restaurants = []
        self.customers = []

    def add_agent(self, agent):
        self.agents.append(agent)

    def add_order(self, order):
        self.orders.append(order)

    def add_restaurant(self, restaurant):
        self.restaurants.append(restaurant)

    def add_customer(self, customer):
        self.customers.append(customer)

    def update_agent_availability(self, agent_id, status):
        for agent in self.agents:
            if agent.id == agent_id:
                agent.update_availability(status)

    def update_agent_current_load(self, agent_id, load):
        for agent in self.agents:
            if agent.id == agent_id:
                agent.update_current_load(load)

    def update_agent_delivery_status(self, agent_id, status):
        for agent in self.agents:
            if agent.id == agent_id:
                agent.update_delivery_status(status)

    def assign_order_to_agent(self, order_id, agent_id):
        for order in self.orders:
            if order.order_id == order_id:
                order.assign_agent(self.agents[agent_id])
                print(f"Order {order_id} assigned to agent {agent_id}")

    def get_nearest_agent(self, customer_location):
        nearest_agent = None
        min_distance = float("inf")
        for agent in self.agents:
            distance = math.sqrt((agent.location[0] - customer_location[0]) ** 2 + (agent.location[1] - customer_location[1]) ** 2)
            if distance < min_distance and agent.availability == "Available":
                min_distance = distance
                nearest_agent = agent
        return nearest_agent


# Coordination algorithm class
class CoordinationAlgorithm:
    def __init__(self, communication_protocol):
        self.communication_protocol = communication_protocol

    def assign_orders_to_agents(self):
        for order in self.communication_protocol.orders:
            nearest_agent = self.communication_protocol.get_nearest_agent(order.customer_location)
            if nearest_agent:
                self.communication_protocol.assign_order_to_agent(order.order_id, self.communication_protocol.agents.index(nearest_agent))
            else:
                print(f"No available agent found for order {order.order_id}")


# User interface class
class UserInterface:
    def __init__(self, communication_protocol):
        self.communication_protocol = communication_protocol

    def submit_order(self, order):
        self.communication_protocol.add_order(order)
        self.communication_protocol.add_restaurant(order.restaurant)
        self.communication_protocol.add_customer(order.customer)
        self.communication_protocol.add_agent(order.assigned_agent)

    def track_delivery_status(self, order_id):
        for order in self.communication_protocol.orders:
            if order.order_id == order_id:
                print(f"Delivery status for order {order_id}: {order.delivery_status}")
                return
        print(f"Order {order_id} not found")


# Main function
def main():
    communication_protocol = CommunicationProtocol()
    coordination_algorithm = CoordinationAlgorithm(communication_protocol)
    user_interface = UserInterface(communication_protocol)

    # Create agents
    agent1 = Agent(1, (0, 0), "Available")
    agent2 = Agent(2, (10, 10), "Available")
    communication_protocol.add_agent(agent1)
    communication_protocol.add_agent(agent2)

    # Create orders
    order1 = Order(1, Restaurant(1, (5, 5)), Customer(1, (15, 15)), time.time())
    order2 = Order(2, Restaurant(2, (20, 20)), Customer(2, (25, 25)), time.time())
    user_interface.submit_order(order1)
    user_interface.submit_order(order2)

    # Assign orders to agents
    coordination_algorithm.assign_orders_to_agents()

    # Track delivery status
    user_interface.track_delivery_status(1)
    user_interface.track_delivery_status(2)


if __name__ == "__main__":
    main()