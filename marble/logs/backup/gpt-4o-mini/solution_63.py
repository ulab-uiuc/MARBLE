# solution.py

import random
import time
from typing import List, Dict, Optional

# Class to represent a Delivery Agent
class DeliveryAgent:
    def __init__(self, agent_id: int):
        self.agent_id = agent_id
        self.current_location = (0, 0)  # (x, y) coordinates
        self.available = True
        self.current_load = 0  # Number of orders currently being delivered

    def update_location(self, new_location: tuple):
        """Update the agent's current location."""
        self.current_location = new_location

    def set_availability(self, available: bool):
        """Set the availability status of the agent."""
        self.available = available

    def assign_order(self):
        """Assign an order to the agent."""
        self.current_load += 1

    def complete_order(self):
        """Complete an order and reduce the load."""
        if self.current_load > 0:
            self.current_load -= 1

# Class to represent an Order
class Order:
    def __init__(self, order_id: int, restaurant_location: tuple):
        self.order_id = order_id
        self.restaurant_location = restaurant_location
        self.status = "Pending"  # Order status
        self.assigned_agent: Optional[DeliveryAgent] = None

    def assign_agent(self, agent: DeliveryAgent):
        """Assign a delivery agent to the order."""
        self.assigned_agent = agent
        self.status = "Assigned"

    def update_status(self, new_status: str):
        """Update the order status."""
        self.status = new_status

# Class to manage the Delivery System
class MultiAgentDine:
    def __init__(self):
        self.agents: List[DeliveryAgent] = []
        self.orders: List[Order] = []

    def add_agent(self, agent: DeliveryAgent):
        """Add a new delivery agent to the system."""
        self.agents.append(agent)

    def place_order(self, restaurant_location: tuple) -> Order:
        """Place a new order and return the order object."""
        order_id = len(self.orders) + 1
        new_order = Order(order_id, restaurant_location)
        self.orders.append(new_order)
        return new_order    def assign_orders(self):
        """Assign orders to the most suitable delivery agents."""
        for order in self.orders:
            if order.status == "Pending":
                suitable_agent = self.find_suitable_agent(order)
                if suitable_agent:
                    order.assign_agent(suitable_agent)
                    suitable_agent.assign_order()
                else:
                    self.handle_unassignable_order(order)

    def handle_unassignable_order(self, order: Order):
        """Handle orders that cannot be assigned to any agent."""

        self.check_agent_availability()
        print(f"Warning: Order ID {order.order_id} cannot be assigned to any agent.")
        # Additional logic for notifying restaurant staff or retrying can be added here.    def find_suitable_agent(self, order: Order) -> Optional[DeliveryAgent]:
        """Find the most suitable delivery agent for the order."""
        suitable_agents = [
            agent for agent in self.agents
            if agent.available and agent.current_load < 2  # Example load limit
        ]
        if not suitable_agents:
            return None

        # Sort agents by proximity to the restaurant location
        suitable_agents.sort(key=lambda agent: self.calculate_distance(agent.current_location, order.restaurant_location))
        return suitable_agents[0]  # Return the closest agent

    @staticmethod
    def calculate_distance(loc1: tuple, loc2: tuple) -> float:
        """Calculate the Euclidean distance between two locations."""
        return ((loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1]) ** 2) ** 0.5

    def update_agent_status(self, agent_id: int, available: bool):
        """Update the availability status of a delivery agent."""
        for agent in self.agents:
            if agent.agent_id == agent_id:
                agent.set_availability(available)

# Example usage
if __name__ == "__main__":
    # Create the MultiAgentDine system
    system = MultiAgentDine()

    # Add delivery agents
    for i in range(5):
        system.add_agent(DeliveryAgent(agent_id=i + 1))

    # Simulate placing orders
    order1 = system.place_order((5, 5))
    order2 = system.place_order((1, 1))
    order3 = system.place_order((3, 3))

    # Assign orders to agents
    system.assign_orders()

    # Print order statuses
    for order in system.orders:
        print(f"Order ID: {order.order_id}, Status: {order.status}, Assigned Agent: {order.assigned_agent.agent_id if order.assigned_agent else 'None'}")

    # Simulate agent completing an order
    if order1.assigned_agent:
        order1.assigned_agent.complete_order()
        order1.update_status("Delivered")
        print(f"Order ID: {order1.order_id} has been delivered.")