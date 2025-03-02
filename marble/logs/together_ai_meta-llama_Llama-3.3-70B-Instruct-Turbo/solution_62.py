# solution.py
# Import required libraries
from abc import ABC, abstractmethod
from typing import Dict, List

# Define a class for Restaurant
class Restaurant:
    def __init__(self, name: str, menu: Dict[str, float]):
        """
        Initialize a Restaurant object.

        Args:
        name (str): The name of the restaurant.
        menu (Dict[str, float]): A dictionary of menu items and their prices.
        """
        self.name = name
        self.menu = menu

    def get_menu(self) -> Dict[str, float]:
        """
        Get the menu of the restaurant.

        Returns:
        Dict[str, float]: A dictionary of menu items and their prices.
        """
        return self.menu

# Define a class for DeliveryAgent
class DeliveryAgent:def update_status(self, task: str, status: str):
        for i, t in enumerate(self.tasks):
            if t == task:
                self.tasks[i] = f"{task} - {status}"
                self.workload -= 1class Order:
    def __init__(self, order_id: int, items: Dict[str, List[str]]):
        """
        Initialize an Order object.

        Args:
        order_id (int): The ID of the order.
        items (Dict[str, List[str]]): A dictionary of restaurant names and their corresponding order items.
        """
        self.order_id = order_id
        self.items = items
        self.status = "pending"

    def update_status(self, status: str):
        """
        Update the status of the order.

        Args:
        status (str): The status of the order.
        """
        self.status = status

# Define a class for MultiServe
class MultiServe:
    def __init__(self):
        """
        Initialize a MultiServe object.
        """
        self.restaurants = {}
        self.delivery_agents = {}
        self.orders = {}

    def add_restaurant(self, restaurant: Restaurant):
        """
        Add a restaurant to the system.

        Args:
        restaurant (Restaurant): The restaurant to add.
        """
        self.restaurants[restaurant.name] = restaurant

    def add_delivery_agent(self, delivery_agent: DeliveryAgent):
        """
        Add a delivery agent to the system.

        Args:
        delivery_agent (DeliveryAgent): The delivery agent to add.
        """
        self.delivery_agents[delivery_agent.name] = delivery_agent

    def place_order(self, order_id: int, items: Dict[str, List[str]]):
        """
        Place an order.

        Args:
        order_id (int): The ID of the order.
        items (Dict[str, List[str]]): A dictionary of restaurant names and their corresponding order items.
        """
        order = Order(order_id, items)
        self.orders[order_id] = order
        for restaurant, items in items.items():
            # Send order details to the restaurant
            print(f"Sending order details to {restaurant}...")
            for item in items:
                print(f"Item: {item}")

    def assign_delivery_tasks(self, order_id: int):
        """
        Assign delivery tasks to delivery agents.

        Args:
        order_id (int): The ID of the order.
        """
        order = self.orders[order_id]for i, (restaurant, items) in enumerate(order.items.items()):delivery_agent = list(self.delivery_agents.values())[i % len(self.delivery_agents)]; delivery_agent.assign_task(f"Deliver {', '.join(items)} from {restaurant}")print(f"Assigned delivery task to {delivery_agent.name}...")

    def update_delivery_status(self, order_id: int, task: str, status: str):
        """
        Update the status of a delivery task.

        Args:
        order_id (int): The ID of the order.
        task (str): The delivery task.
        status (str): The status of the task.
        """
        order = self.orders[order_id]
        for delivery_agent in self.delivery_agents.values():
            delivery_agent.update_status(task, status)
        order.update_status(status)
        print(f"Updated delivery status for order {order_id}...")

# Define a class for UserInterface
class UserInterface:
    def __init__(self, multi_serve: MultiServe):
        """
        Initialize a UserInterface object.

        Args:
        multi_serve (MultiServe): The MultiServe object.
        """
        self.multi_serve = multi_serve

    def browse_menus(self):
        """
        Browse menus from multiple restaurants.
        """
        for restaurant in self.multi_serve.restaurants.values():
            print(f"Menu for {restaurant.name}:")
            for item, price in restaurant.get_menu().items():
                print(f"{item}: ${price}")

    def add_to_cart(self, restaurant: str, item: str):
        """
        Add an item to the cart.

        Args:
        restaurant (str): The name of the restaurant.
        item (str): The name of the item.
        """
        # Add item to cart
        print(f"Added {item} from {restaurant} to cart...")

    def place_order(self, order_id: int, items: Dict[str, List[str]]):
        """
        Place an order.

        Args:
        order_id (int): The ID of the order.
        items (Dict[str, List[str]]): A dictionary of restaurant names and their corresponding order items.
        """
        self.multi_serve.place_order(order_id, items)

# Define a class for DeliveryAgentInterface
class DeliveryAgentInterface:
    def __init__(self, multi_serve: MultiServe):
        """
        Initialize a DeliveryAgentInterface object.

        Args:
        multi_serve (MultiServe): The MultiServe object.
        """
        self.multi_serve = multi_serve

    def log_in(self, delivery_agent: DeliveryAgent):
        """
        Log in as a delivery agent.

        Args:
        delivery_agent (DeliveryAgent): The delivery agent.
        """
        # Log in as delivery agent
        print(f"Logged in as {delivery_agent.name}...")

    def receive_tasks(self):
        """
        Receive assigned delivery tasks.
        """
        for delivery_agent in self.multi_serve.delivery_agents.values():
            print(f"Tasks for {delivery_agent.name}:")
            for task in delivery_agent.tasks:
                print(task)

    def update_status(self, task: str, status: str):
        """
        Update the status of a delivery task.

        Args:
        task (str): The delivery task.
        status (str): The status of the task.
        """
        self.multi_serve.update_delivery_status(1, task, status)

# Test cases
def test_place_order():
    multi_serve = MultiServe()
    restaurant1 = Restaurant("Restaurant 1", {"Item 1": 10.99, "Item 2": 9.99})
    restaurant2 = Restaurant("Restaurant 2", {"Item 3": 12.99, "Item 4": 11.99})
    multi_serve.add_restaurant(restaurant1)
    multi_serve.add_restaurant(restaurant2)
    multi_serve.place_order(1, {"Restaurant 1": ["Item 1", "Item 2"], "Restaurant 2": ["Item 3", "Item 4"]})

def test_assign_delivery_tasks():
    multi_serve = MultiServe()
    restaurant1 = Restaurant("Restaurant 1", {"Item 1": 10.99, "Item 2": 9.99})
    restaurant2 = Restaurant("Restaurant 2", {"Item 3": 12.99, "Item 4": 11.99})
    multi_serve.add_restaurant(restaurant1)
    multi_serve.add_restaurant(restaurant2)
    delivery_agent = DeliveryAgent("Delivery Agent 1")
    multi_serve.add_delivery_agent(delivery_agent)
    multi_serve.place_order(1, {"Restaurant 1": ["Item 1", "Item 2"], "Restaurant 2": ["Item 3", "Item 4"]})
    multi_serve.assign_delivery_tasks(1)

def test_update_delivery_status():
    multi_serve = MultiServe()
    restaurant1 = Restaurant("Restaurant 1", {"Item 1": 10.99, "Item 2": 9.99})
    restaurant2 = Restaurant("Restaurant 2", {"Item 3": 12.99, "Item 4": 11.99})
    multi_serve.add_restaurant(restaurant1)
    multi_serve.add_restaurant(restaurant2)
    delivery_agent = DeliveryAgent("Delivery Agent 1")
    multi_serve.add_delivery_agent(delivery_agent)
    multi_serve.place_order(1, {"Restaurant 1": ["Item 1", "Item 2"], "Restaurant 2": ["Item 3", "Item 4"]})
    multi_serve.assign_delivery_tasks(1)
    multi_serve.update_delivery_status(1, "Deliver Item 1, Item 2 from Restaurant 1", "delivered")

# Run test cases
test_place_order()
test_assign_delivery_tasks()
test_update_delivery_status()

# Create a MultiServe object
multi_serve = MultiServe()

# Create restaurants
restaurant1 = Restaurant("Restaurant 1", {"Item 1": 10.99, "Item 2": 9.99})
restaurant2 = Restaurant("Restaurant 2", {"Item 3": 12.99, "Item 4": 11.99})

# Add restaurants to MultiServe
multi_serve.add_restaurant(restaurant1)
multi_serve.add_restaurant(restaurant2)

# Create a user interface
user_interface = UserInterface(multi_serve)

# Browse menus
user_interface.browse_menus()

# Add items to cart
user_interface.add_to_cart("Restaurant 1", "Item 1")
user_interface.add_to_cart("Restaurant 2", "Item 3")

# Place an order
user_interface.place_order(1, {"Restaurant 1": ["Item 1", "Item 2"], "Restaurant 2": ["Item 3", "Item 4"]})

# Create a delivery agent
delivery_agent = DeliveryAgent("Delivery Agent 1")

# Add delivery agent to MultiServe
multi_serve.add_delivery_agent(delivery_agent)

# Assign delivery tasks
multi_serve.assign_delivery_tasks(1)

# Create a delivery agent interface
delivery_agent_interface = DeliveryAgentInterface(multi_serve)

# Log in as delivery agent
delivery_agent_interface.log_in(delivery_agent)

# Receive tasks
delivery_agent_interface.receive_tasks()

# Update status
delivery_agent_interface.update_status("Deliver Item 1, Item 2 from Restaurant 1", "delivered")