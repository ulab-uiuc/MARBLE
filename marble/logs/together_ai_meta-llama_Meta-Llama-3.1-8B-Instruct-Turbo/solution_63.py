# solution.py

# Import required libraries
import math
import random
import time

# Define a class for DeliveryAgent
class DeliveryAgent:
    def __init__(self, agent_id, location, availability):
        """
        Initialize a DeliveryAgent object.

        Args:
            agent_id (str): Unique identifier for the agent.
            location (tuple): Current location of the agent (x, y coordinates).
            availability (bool): Availability status of the agent.
        """
        self.agent_id = agent_id
        self.location = location
        self.availability = availability
        self.current_load = 0

    def update_availability(self, availability):
        """
        Update the availability status of the agent.

        Args:
            availability (bool): New availability status.
        """
        self.availability = availability

    def update_location(self, new_location):
        """
        Update the location of the agent.

        Args:
            new_location (tuple): New location (x, y coordinates).
        """
        self.location = new_location

    def assign_task(self):
        """
        Assign a task to the agent if available.

        Returns:
            bool: True if task assigned, False otherwise.
        """
        if self.availability:
            self.current_load += 1
            return True
        return False

    def release_task(self):
        """
        Release a task from the agent if available.

        Returns:
            bool: True if task released, False otherwise.
        """
        if self.current_load > 0:
            self.current_load -= 1
            return True
        return False


# Define a class for Restaurant
class Restaurant:
    def __init__(self, restaurant_id, location):
        """
        Initialize a Restaurant object.

        Args:
            restaurant_id (str): Unique identifier for the restaurant.
            location (tuple): Location of the restaurant (x, y coordinates).
        """
        self.restaurant_id = restaurant_id
        self.location = location

    def place_order(self, order_id, customer_location):
        """
        Place an order from the restaurant.

        Args:
            order_id (str): Unique identifier for the order.
            customer_location (tuple): Location of the customer (x, y coordinates).

        Returns:
            tuple: Agent ID and estimated delivery time.
        """
        # Calculate the distance between the restaurant and customer
        distance = math.sqrt((self.location[0] - customer_location[0])**2 + (self.location[1] - customer_location[1])**2)

        # Find the nearest available agent
        nearest_agent = None
        min_distance = float('inf')
        for agent in agents:
            if agent.availability:
                current_distance = math.sqrt((agent.location[0] - customer_location[0])**2 + (agent.location[1] - customer_location[1])**2)
                if current_distance < min_distance:
                    min_distance = current_distance
                    nearest_agent = agent

        # Assign the task to the nearest available agent
        if nearest_agent:
            nearest_agent.assign_task()
            estimated_delivery_time = distance / nearest_agent.current_load
            return nearest_agent.agent_id, estimated_delivery_time
        return None, None


# Define a class for Customer
class Customer:
    def __init__(self, customer_id, location):
        """
        Initialize a Customer object.

        Args:
            customer_id (str): Unique identifier for the customer.
            location (tuple): Location of the customer (x, y coordinates).
        """
        self.customer_id = customer_id
        self.location = location

    def place_order(self, restaurant_id):
        """
        Place an order from the customer.

        Args:
            restaurant_id (str): Unique identifier for the restaurant.

        Returns:
            tuple: Order ID and estimated delivery time.
        """
        # Get the restaurant object
        restaurant = next((r for r in restaurants if r.restaurant_id == restaurant_id), None)

        # Place the order from the restaurant
        order_id, estimated_delivery_time = restaurant.place_order(str(len(orders) + 1), self.location)

        # Update the order status
        orders[order_id] = {'status': 'pending', 'estimated_delivery_time': estimated_delivery_time}

        return order_id, estimated_delivery_time


# Define a class for Order
class Order:
    def __init__(self, order_id, status, estimated_delivery_time):
        """
        Initialize an Order object.

        Args:
            order_id (str): Unique identifier for the order.
            status (str): Status of the order.
            estimated_delivery_time (float): Estimated delivery time.
        """
        self.order_id = order_id
        self.status = status
        self.estimated_delivery_time = estimated_delivery_time

    def update_status(self, new_status):
        """
        Update the status of the order.

        Args:
            new_status (str): New status.
        """
        self.status = new_status


# Define the main function
def main():
    global agents, restaurants, customers, orders

    # Initialize the agents
    agents = [
        DeliveryAgent('A1', (0, 0), True),
        DeliveryAgent('A2', (10, 10), True),
        DeliveryAgent('A3', (20, 20), True)
    ]

    # Initialize the restaurants
    restaurants = [
        Restaurant('R1', (5, 5)),
        Restaurant('R2', (15, 15)),
        Restaurant('R3', (25, 25))
    ]

    # Initialize the customers
    customers = [
        Customer('C1', (3, 3)),
        Customer('C2', (13, 13)),
        Customer('C3', (23, 23))
    ]

    # Initialize the orders
    orders = {}

    # Simulate the order placement process
    for customer in customers:
        order_id, estimated_delivery_time = customer.place_order('R1')
        print(f'Order {order_id} placed by customer {customer.customer_id} with estimated delivery time {estimated_delivery_time}')

    # Simulate the delivery process
    for order_id, order in orders.items():
        print(f'Order {order_id} status: {order.status}')
        time.sleep(order.estimated_delivery_time)
        order.update_status('delivered')
        print(f'Order {order_id} status: {order.status}')


# Run the main function
if __name__ == '__main__':
    main()