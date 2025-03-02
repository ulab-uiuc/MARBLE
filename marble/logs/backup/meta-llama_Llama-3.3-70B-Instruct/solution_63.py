# solution.py
import threading
import time
from typing import Dict, List

# Define a class for DeliveryAgent
class DeliveryAgent:
    def __init__(self, agent_id: str, location: str, availability: bool = True):
        """
        Initialize a DeliveryAgent object.

        Args:
        - agent_id (str): Unique identifier for the agent.
        - location (str): Current location of the agent.
        - availability (bool): Availability status of the agent. Defaults to True.
        """
        self.agent_id = agent_id
        self.location = location
        self.availability = availability
        self.current_load = 0  # Initialize current load to 0

    def update_location(self, new_location: str):
        """
        Update the location of the agent.

        Args:
        - new_location (str): New location of the agent.
        """
        self.location = new_location

    def update_availability(self, new_availability: bool):
        """
        Update the availability status of the agent.

        Args:
        - new_availability (bool): New availability status of the agent.
        """
        self.availability = new_availability

    def update_current_load(self, new_load: int):
        """
        Update the current load of the agent.

        Args:
        - new_load (int): New current load of the agent.
        """
        self.current_load = new_load


# Define a class for Order
class Order:
    def __init__(self, order_id: str, restaurant: str, customer_location: str, status: str = "pending"):
        """
        Initialize an Order object.

        Args:
        - order_id (str): Unique identifier for the order.
        - restaurant (str): Restaurant where the order was placed.
        - customer_location (str): Location of the customer.
        - status (str): Status of the order. Defaults to "pending".
        """
        self.order_id = order_id
        self.restaurant = restaurant
        self.customer_location = customer_location
        self.status = status
        self.assigned_agent = None  # Initialize assigned agent to None

    def update_status(self, new_status: str):
        """
        Update the status of the order.

        Args:
        - new_status (str): New status of the order.
        """
        self.status = new_status

    def assign_agent(self, agent: DeliveryAgent):
        """
        Assign a delivery agent to the order.

        Args:
        - agent (DeliveryAgent): Delivery agent to be assigned.
        """
        self.assigned_agent = agent


# Define a class for MultiAgentDine
class MultiAgentDine:
    def __init__(self):
        """
        Initialize a MultiAgentDine object.
        """
        self.agents: Dict[str, DeliveryAgent] = {}  # Dictionary to store delivery agents
        self.orders: Dict[str, Order] = {}  # Dictionary to store orders

    def add_agent(self, agent: DeliveryAgent):
        """
        Add a delivery agent to the system.

        Args:
        - agent (DeliveryAgent): Delivery agent to be added.
        """
        self.agents[agent.agent_id] = agent

    def add_order(self, order: Order):
        """
        Add an order to the system.

        Args:
        - order (Order): Order to be added.
        """
        self.orders[order.order_id] = order

    def assign_order_to_agent(self, order_id: str):
        """
        Assign an order to the most suitable delivery agent.

        Args:
        - order_id (str): Unique identifier for the order.
        """
        order = self.orders.get(order_id)
        if order:
            # Find the most suitable agent based on proximity, availability, and current load
            suitable_agent = self.find_suitable_agent(order)
            if suitable_agent:
                order.assign_agent(suitable_agent)
                suitable_agent.update_current_load(suitable_agent.current_load + 1)
                order.update_status("assigned")
                print(f"Order {order_id} assigned to agent {suitable_agent.agent_id}")
            else:
                print(f"No suitable agent found for order {order_id}")
        else:
            print(f"Order {order_id} not found")

    def find_suitable_agent(self, order: Order) -> DeliveryAgent:
        """
        Find the most suitable delivery agent for an order.

        Args:
        - order (Order): Order to be assigned.

        Returns:
        - DeliveryAgent: Most suitable delivery agent.
        """
        suitable_agent = None
        min_distance = float("inf")
        for agent in self.agents.values():
            if agent.availability and agent.current_load < 5:  # Assume maximum load per agent is 5
                # Calculate distance between agent and customer location
                distance = self.calculate_distance(agent.location, order.customer_location)
                if distance < min_distance:
                    min_distance = distance
                    suitable_agent = agent
        return suitable_agent

    def calculate_distance(self, location1: str, location2: str) -> float:
        """
        Calculate the distance between two locations.

        Args:
        - location1 (str): First location.
        - location2 (str): Second location.

        Returns:
        - float: Distance between the two locations.
        """
        # For simplicity, assume locations are points on a 2D plane and distance is Euclidean distance
        x1, y1 = map(float, location1.split(","))
        x2, y2 = map(float, location2.split(","))
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def update_agent_location(self, agent_id: str, new_location: str):
        """
        Update the location of a delivery agent.

        Args:
        - agent_id (str): Unique identifier for the agent.
        - new_location (str): New location of the agent.
        """
        agent = self.agents.get(agent_id)
        if agent:
            agent.update_location(new_location)
            print(f"Agent {agent_id} location updated to {new_location}")
        else:
            print(f"Agent {agent_id} not found")

    def update_agent_availability(self, agent_id: str, new_availability: bool):
        """
        Update the availability status of a delivery agent.

        Args:
        - agent_id (str): Unique identifier for the agent.
        - new_availability (bool): New availability status of the agent.
        """
        agent = self.agents.get(agent_id)
        if agent:
            agent.update_availability(new_availability)
            print(f"Agent {agent_id} availability updated to {new_availability}")
        else:
            print(f"Agent {agent_id} not found")


# Define a function to simulate order placement and assignment
def simulate_order_placement(multi_agent_dine: MultiAgentDine, order_id: str, restaurant: str, customer_location: str):
    order = Order(order_id, restaurant, customer_location)
    multi_agent_dine.add_order(order)
    multi_agent_dine.assign_order_to_agent(order_id)


# Define a function to simulate agent location updates
def simulate_agent_location_update(multi_agent_dine: MultiAgentDine, agent_id: str, new_location: str):
    multi_agent_dine.update_agent_location(agent_id, new_location)


# Define a function to simulate agent availability updates
def simulate_agent_availability_update(multi_agent_dine: MultiAgentDine, agent_id: str, new_availability: bool):
    multi_agent_dine.update_agent_availability(agent_id, new_availability)


# Create a MultiAgentDine object
multi_agent_dine = MultiAgentDine()

# Create delivery agents
agent1 = DeliveryAgent("agent1", "0,0")
agent2 = DeliveryAgent("agent2", "3,4")
agent3 = DeliveryAgent("agent3", "6,8")

# Add agents to the system
multi_agent_dine.add_agent(agent1)
multi_agent_dine.add_agent(agent2)
multi_agent_dine.add_agent(agent3)

# Simulate order placement and assignment
simulate_order_placement(multi_agent_dine, "order1", "restaurant1", "1,1")
simulate_order_placement(multi_agent_dine, "order2", "restaurant2", "4,5")
simulate_order_placement(multi_agent_dine, "order3", "restaurant3", "7,9")

# Simulate agent location updates
simulate_agent_location_update(multi_agent_dine, "agent1", "1,1")
simulate_agent_location_update(multi_agent_dine, "agent2", "4,5")

# Simulate agent availability updates
simulate_agent_availability_update(multi_agent_dine, "agent1", False)
simulate_agent_availability_update(multi_agent_dine, "agent2", True)

# Test cases
def test_single_agent_delivery():
    multi_agent_dine = MultiAgentDine()
    agent = DeliveryAgent("agent1", "0,0")
    multi_agent_dine.add_agent(agent)
    order = Order("order1", "restaurant1", "1,1")
    multi_agent_dine.add_order(order)
    multi_agent_dine.assign_order_to_agent("order1")
    assert order.assigned_agent == agent

def test_multi_agent_coordination():
    multi_agent_dine = MultiAgentDine()
    agent1 = DeliveryAgent("agent1", "0,0")
    agent2 = DeliveryAgent("agent2", "3,4")
    multi_agent_dine.add_agent(agent1)
    multi_agent_dine.add_agent(agent2)
    order1 = Order("order1", "restaurant1", "1,1")
    order2 = Order("order2", "restaurant2", "4,5")
    multi_agent_dine.add_order(order1)
    multi_agent_dine.add_order(order2)
    multi_agent_dine.assign_order_to_agent("order1")
    multi_agent_dine.assign_order_to_agent("order2")
    assert order1.assigned_agent == agent1
    assert order2.assigned_agent == agent2

def test_edge_cases():
    multi_agent_dine = MultiAgentDine()
    agent = DeliveryAgent("agent1", "0,0")
    multi_agent_dine.add_agent(agent)
    order = Order("order1", "restaurant1", "1,1")
    multi_agent_dine.add_order(order)
    multi_agent_dine.assign_order_to_agent("order1")
    agent.update_availability(False)
    order2 = Order("order2", "restaurant2", "4,5")
    multi_agent_dine.add_order(order2)
    multi_agent_dine.assign_order_to_agent("order2")
    assert order2.assigned_agent is None

test_single_agent_delivery()
test_multi_agent_coordination()
test_edge_cases()