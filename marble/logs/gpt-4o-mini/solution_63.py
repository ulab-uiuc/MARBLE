# solution.py

import random
import time
from typing import List, Dict, Optional

# Class to represent a Delivery Agent
class DeliveryAgent:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id  # Unique identifier for the agent
        self.current_location = (0, 0)  # Current location (x, y)
        self.available = True  # Availability status
        self.current_load = 0  # Number of orders currently being delivered

    def update_location(self, new_location: tuple):
        """Update the agent's current location."""
        self.current_location = new_location

    def set_availability(self, status: bool):
        """Set the availability status of the agent."""
        self.available = status

    def update_load(self, load_change: int):
        """Update the current load of the agent."""
        self.current_load += load_change

# Class to represent an Order
class Order:
    def __init__(self, order_id: str, restaurant_location: tuple):
        self.order_id = order_id  # Unique identifier for the order
        self.restaurant_location = restaurant_location  # Location of the restaurant
        self.status = "Pending"  # Current status of the order

    def update_status(self, new_status: str):
        """Update the status of the order."""
        self.status = new_status

# Class to manage the Delivery System
class MultiAgentDine:
    def __init__(self):
        self.agents: List[DeliveryAgent] = []  # List of delivery agents
        self.orders: Dict[str, Order] = {}  # Dictionary of orders

    def add_agent(self, agent: DeliveryAgent):
        """Add a new delivery agent to the system."""
        self.agents.append(agent)

    def place_order(self, order_id: str, restaurant_location: tuple):
        """Place a new order in the system."""
        order = Order(order_id, restaurant_location)
        self.orders[order_id] = order
        self.assign_order(order)

    def assign_order(self, order: Order):
        """Assign the order to the most suitable delivery agent."""
        suitable_agent = None
        min_distance = float('inf')

        for agent in self.agents:
            if agent.available and agent.current_load < 3:  # Check if agent is available and not overloaded
                distance = self.calculate_distance(agent.current_location, order.restaurant_location)
                if distance < min_distance:
                    min_distance = distance
                    suitable_agent = agent

        if suitable_agent:
            suitable_agent.update_load(1)  # Increase the load of the agent
            order.update_status("Assigned to " + suitable_agent.agent_id)
            print(f"Order {order.order_id} assigned to agent {suitable_agent.agent_id}.")
        else:
            print(f"No available agents for order {order.order_id}.")

    @staticmethod
    def calculate_distance(loc1: tuple, loc2: tuple) -> float:
        """Calculate the Euclidean distance between two locations."""
        return ((loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1]) ** 2) ** 0.5

    def update_agent_location(self, agent_id: str, new_location: tuple):
        """Update the location of a specific delivery agent."""
        for agent in self.agents:
            if agent.agent_id == agent_id:
                agent.update_location(new_location)
                print(f"Agent {agent_id} location updated to {new_location}.")
                break

    def update_order_status(self, order_id: str, new_status: str):
        """Update the status of a specific order."""
        if order_id in self.orders:
            self.orders[order_id].update_status(new_status)
            print(f"Order {order_id} status updated to {new_status}.")
        else:
            print(f"Order {order_id} not found.")

# Example usage
if __name__ == "__main__":
    # Create the MultiAgentDine system
    system = MultiAgentDine()

    # Add delivery agents
    for i in range(5):
        agent = DeliveryAgent(agent_id=f"Agent-{i+1}")
        system.add_agent(agent)

    # Simulate placing orders
    system.place_order(order_id="Order-1", restaurant_location=(1, 2))
    system.place_order(order_id="Order-2", restaurant_location=(3, 4))
    system.place_order(order_id="Order-3", restaurant_location=(5, 6))

    # Update agent locations
    system.update_agent_location("Agent-1", (1, 1))
    system.update_agent_location("Agent-2", (2, 2))

    # Update order status
    system.update_order_status("Order-1", "Delivered")