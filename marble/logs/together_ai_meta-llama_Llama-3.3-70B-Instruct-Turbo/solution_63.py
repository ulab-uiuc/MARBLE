# solution.py
import threading
import time
from typing import Dict, List

# Agent class representing a delivery agent
class Agent:
    def __init__(self, agent_id: int, location: str, availability: bool):
class Agent:
    def __init__(self, agent_id: int, location: str, availability: bool, max_load: int = 5):
        self.max_load = max_load
        """
        Initialize an Agent object.

        Args:
        agent_id (int): Unique identifier for the agent.
        location (str): Current location of the agent.
        availability (bool): Availability status of the agent.
        """
        self.agent_id = agent_id
        self.location = location
        self.availability = availability
        self.current_load = 0  # Initialize current load to 0

    def update_location(self, new_location: str):
        """
        Update the agent's location.

        Args:
        new_location (str): New location of the agent.
        """
        self.location = new_location

    def update_availability(self, new_availability: bool):
        """
        Update the agent's availability.

        Args:
        new_availability (bool): New availability status of the agent.
        """
        self.availability = new_availability

    def update_current_load(self, new_load: int):
        """
        Update the agent's current load.

        Args:
        new_load (int): New current load of the agent.
        """
        self.current_load = new_load


# Order class representing a food order
class Order:
    def __init__(self, order_id: int, restaurant: str, customer_location: str, status: str):
        """
        Initialize an Order object.

        Args:
        order_id (int): Unique identifier for the order.
        restaurant (str): Restaurant where the order was placed.
        customer_location (str): Location of the customer.
        status (str): Status of the order (e.g., "pending", "in_transit", "delivered").
        """
        self.order_id = order_id
        self.restaurant = restaurant
        self.customer_location = customer_location
        self.status = status

    def update_status(self, new_status: str):
        """
        Update the order's status.

        Args:
        new_status (str): New status of the order.
        """
        self.status = new_status


# MultiAgentDine class representing the MultiAgentDine system
class MultiAgentDine:
    def __init__(self):
def __retry_assign_agent(self, order_id: int, suitable_agent: Agent):
        # Retry mechanism to handle cases where an agent's availability changes after being assigned to an order
        try:
            suitable_agent.update_current_load(suitable_agent.current_load + 1)
            suitable_agent.update_availability(False)
            # Update order status
            order = self.orders.get(order_id)
            if order:
                order.update_status("in_transit")
                print(f"Agent {suitable_agent.agent_id} assigned to order {order_id}")
        except Exception as e:
            # Retry the assignment
            print(f"Error assigning agent to order: {e}")
            self.__retry_assign_agent(order_id, suitable_agent)
        """
        Initialize a MultiAgentDine object.
        """
        self.agents: Dict[int, Agent] = {}  # Dictionary to store agents
        self.orders: Dict[int, Order] = {}  # Dictionary to store orders
        self.lock = threading.Lock()  # Lock for thread safety

    def add_agent(self, agent_id: int, location: str, availability: bool):
        """
        Add a new agent to the system.

        Args:
        agent_id (int): Unique identifier for the agent.
        location (str): Current location of the agent.
        availability (bool): Availability status of the agent.
        """
        with self.lock:
            self.agents[agent_id] = Agent(agent_id, location, availability)

    def add_order(self, order_id: int, restaurant: str, customer_location: str, status: str):def assign_agent(self, order_id: int):
        with self.lock:
            order = self.orders.get(order_id)
            if order:
                # Find the most suitable agent
                suitable_agent = None
                min_distance = float("inf")
                for agent in self.agents.values():
                    if agent.availability and agent.current_load < agent.max_load:
                        distance = self.calculate_distance(agent.location, order.customer_location)
                        if distance < min_distance:
                            min_distance = distance
                            suitable_agent = agent
                
                if suitable_agent:
                    # Update agent's current load and availability in a single, atomic operation
                    try:
                        suitable_agent.update_current_load(suitable_agent.current_load + 1)
                        suitable_agent.update_availability(False)
                        # Update order status
                        order.update_status("in_transit")
                        print(f"Agent {suitable_agent.agent_id} assigned to order {order_id}")
                    except Exception as e:
                        # Retry mechanism to handle cases where an agent's availability changes after being assigned to an order
                        print(f"Error assigning agent to order: {e}")
                        # Retry the assignment
                        self.assign_agent(order_id)
                else:
                    print(f"No available agents for order {order_id}")def calculate_distance(self, location1: str, location2: str):
        """
        Calculate the distance between two locations (for simplicity, assume locations are points on a 2D plane).

        Args:
        location1 (str): First location.
        location2 (str): Second location.

        Returns:
        float: Distance between the two locations.
        """
        # For simplicity, assume locations are points on a 2D plane
        x1, y1 = map(float, location1.split(","))
        x2, y2 = map(float, location2.split(","))
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def update_agent_location(self, agent_id: int, new_location: str):
        """
        Update an agent's location.

        Args:
        agent_id (int): Unique identifier for the agent.
        new_location (str): New location of the agent.
        """
        with self.lock:
            agent = self.agents.get(agent_id)
            if agent:
                agent.update_location(new_location)

    def update_order_status(self, order_id: int, new_status: str):
        """
        Update an order's status.

        Args:
        order_id (int): Unique identifier for the order.
        new_status (str): New status of the order.
        """
        with self.lock:
            order = self.orders.get(order_id)
            if order:
                order.update_status(new_status)


# Test cases
def test_single_agent_delivery():
    multi_agent_dine = MultiAgentDine()
    multi_agent_dine.add_agent(1, "0,0", True)
    multi_agent_dine.add_order(1, "Restaurant1", "3,4", "pending")
    multi_agent_dine.assign_agent(1)
    print(multi_agent_dine.orders[1].status)  # Should print "in_transit"


def test_multi_agent_coordination():
    multi_agent_dine = MultiAgentDine()
    multi_agent_dine.add_agent(1, "0,0", True)
    multi_agent_dine.add_agent(2, "5,5", True)
    multi_agent_dine.add_order(1, "Restaurant1", "3,4", "pending")
    multi_agent_dine.add_order(2, "Restaurant2", "6,7", "pending")
    multi_agent_dine.assign_agent(1)
    multi_agent_dine.assign_agent(2)
    print(multi_agent_dine.orders[1].status)  # Should print "in_transit"
    print(multi_agent_dine.orders[2].status)  # Should print "in_transit"


def test_edge_cases():
    multi_agent_dine = MultiAgentDine()
    multi_agent_dine.add_agent(1, "0,0", False)
    multi_agent_dine.add_order(1, "Restaurant1", "3,4", "pending")
    multi_agent_dine.assign_agent(1)
    print(multi_agent_dine.orders[1].status)  # Should print "pending" (no available agents)


if __name__ == "__main__":
    test_single_agent_delivery()
    test_multi_agent_coordination()
    test_edge_cases()