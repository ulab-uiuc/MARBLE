# solution.py

# Import required libraries
import datetime

# Define a class for Restaurant
class Restaurant:
    def __init__(self, name, menu):
        """
        Initialize a Restaurant object.

        Args:
        name (str): The name of the restaurant.
        menu (dict): A dictionary of menu items with their prices.
        """
        self.name = name
        self.menu = menu
        self.orders = []

    def add_order(self, order):
        """
        Add an order to the restaurant's orders list.

        Args:
        order (dict): A dictionary containing the order details.
        """
        self.orders.append(order)

    def update_order_status(self, order_id, status):
        """
        Update the status of an order.

        Args:
        order_id (int): The ID of the order.
        status (str): The new status of the order.
        """
        for order in self.orders:
            if order['id'] == order_id:
                order['status'] = status
                break


# Define a class for DeliveryAgent
class DeliveryAgent:
    def __init__(self, name):
        """
        Initialize a DeliveryAgent object.

        Args:
        name (str): The name of the delivery agent.
        """
        self.name = name
        self.tasks = []

    def add_task(self, task):
        """
        Add a delivery task to the agent's tasks list.

        Args:
        task (dict): A dictionary containing the task details.
        """
        self.tasks.append(task)

    def update_task_status(self, task_id, status):
        """
        Update the status of a delivery task.

        Args:
        task_id (int): The ID of the task.
        status (str): The new status of the task.
        """
        for task in self.tasks:
            if task['id'] == task_id:
                task['status'] = status
                break


# Define a class for User
class User:
    def __init__(self, name):
        """
        Initialize a User object.

        Args:
        name (str): The name of the user.
        """
        self.name = name
        self.cart = []
        self.orders = []

    def add_to_cart(self, item):
        """
        Add an item to the user's cart.

        Args:
        item (dict): A dictionary containing the item details.
        """
        self.cart.append(item)

    def place_order(self, restaurants):
        """
        Place an order with the items in the user's cart.

        Args:
        restaurants (list): A list of Restaurant objects.
        """
        order_id = len(self.orders) + 1
        order = {'id': order_id, 'status': 'pending', 'items': self.cart}
        self.orders.append(order)

        # Send order details to each restaurant
        for item in self.cart:
            for restaurant in restaurants:
                if item['restaurant'] == restaurant.name:
                    restaurant.add_order({'id': order_id, 'item': item['name'], 'status': 'pending'})

        # Assign delivery tasks to delivery agents
        delivery_agents = [DeliveryAgent('Agent 1'), DeliveryAgent('Agent 2')]
        for i, item in enumerate(self.cart):
            task_id = i + 1
            task = {'id': task_id, 'order_id': order_id, 'item': item['name'], 'status': 'pending'}
            delivery_agents[i % len(delivery_agents)].add_task(task)

        # Update the user's cart
        self.cart = []

    def cancel_order(self, order_id):
        """
        Cancel an order.

        Args:
        order_id (int): The ID of the order.
        """
        for order in self.orders:
            if order['id'] == order_id:
                order['status'] = 'canceled'
                break


# Define a class for MultiServe
class MultiServe:
    def __init__(self):
        """
        Initialize a MultiServe object.
        """
        self.restaurants = []
        self.users = []
        self.delivery_agents = []

    def add_restaurant(self, restaurant):
        """
        Add a restaurant to the system.

        Args:
        restaurant (Restaurant): A Restaurant object.
        """
        self.restaurants.append(restaurant)

    def add_user(self, user):
        """
        Add a user to the system.

        Args:
        user (User): A User object.
        """
        self.users.append(user)

    def add_delivery_agent(self, delivery_agent):
        """
        Add a delivery agent to the system.

        Args:
        delivery_agent (DeliveryAgent): A DeliveryAgent object.
        """
        self.delivery_agents.append(delivery_agent)

    def display_menu(self, restaurant):
        """
        Display the menu of a restaurant.

        Args:
        restaurant (Restaurant): A Restaurant object.
        """
        print(f"Menu for {restaurant.name}:")
        for item, price in restaurant.menu.items():
            print(f"{item}: ${price}")

    def display_cart(self, user):
        """
        Display the cart of a user.

        Args:
        user (User): A User object.
        """
        print(f"Cart for {user.name}:")
        for item in user.cart:
            print(f"{item['name']} from {item['restaurant']}")

    def display_orders(self, user):
        """
        Display the orders of a user.

        Args:
        user (User): A User object.
        """
        print(f"Orders for {user.name}:")
        for order in user.orders:
            print(f"Order {order['id']}: {order['status']}")


# Test the system
if __name__ == "__main__":
    # Create restaurants
    restaurant1 = Restaurant('Restaurant 1', {'item1': 10.99, 'item2': 9.99})
    restaurant2 = Restaurant('Restaurant 2', {'item3': 12.99, 'item4': 11.99})

    # Create users
    user1 = User('User 1')

    # Create a MultiServe object
    multiserve = MultiServe()

    # Add restaurants and users to the system
    multiserve.add_restaurant(restaurant1)
    multiserve.add_restaurant(restaurant2)
    multiserve.add_user(user1)

    # Display menus
    multiserve.display_menu(restaurant1)
    multiserve.display_menu(restaurant2)

    # Add items to cart
    user1.add_to_cart({'name': 'item1', 'restaurant': 'Restaurant 1'})
    user1.add_to_cart({'name': 'item3', 'restaurant': 'Restaurant 2'})

    # Display cart
    multiserve.display_cart(user1)

    # Place order
    user1.place_order(multiserve.restaurants)

    # Display orders
    multiserve.display_orders(user1)

    # Cancel order
    user1.cancel_order(1)

    # Display orders
    multiserve.display_orders(user1)