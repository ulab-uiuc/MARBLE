# solution.py

# Import necessary libraries
from typing import List, Dict, Optional
import uuid

# Define a class to represent a Restaurant
class Restaurant:
    def __init__(self, name: str, menu: Dict[str, float]):
        self.name = name  # Name of the restaurant
        self.menu = menu  # Menu items with prices
        self.orders = []  # List to hold orders

    def view_menu(self) -> Dict[str, float]:
        """Return the restaurant's menu."""
        return self.menu

    def accept_order(self, order: 'Order'):
        """Accept an incoming order."""
        self.orders.append(order)

    def reject_order(self, order: 'Order'):
        """Reject an incoming order."""
        if order in self.orders:
            self.orders.remove(order)

# Define a class to represent a Customer
class Customer:
    def __init__(self, name: str):
        self.name = name  # Name of the customer
        self.orders = []  # List to hold orders

    def place_order(self, restaurant: Restaurant, items: List[str]) -> 'Order':
        """Place an order at a restaurant."""
        order = Order(customer=self, restaurant=restaurant, items=items)
        restaurant.accept_order(order)
        self.orders.append(order)
        return order

# Define a class to represent an Order
class Order:
    def __init__(self, customer: Customer, restaurant: Restaurant, items: List[str]):
        self.id = uuid.uuid4()  # Unique identifier for the order
        self.customer = customer  # Customer who placed the order
        self.restaurant = restaurant  # Restaurant fulfilling the order
        self.items = items  # Items in the order
        self.status = 'Pending'  # Initial status of the order

    def update_status(self, status: str):
        """Update the status of the order."""
        self.status = status

# Define a class to represent Delivery Personnel
class DeliveryPersonnel:
    def __init__(self, name: str):
        self.name = name  # Name of the delivery personnel
        self.deliveries = []  # List to hold deliveries

    def track_delivery(self, order: Order):
        """Track a delivery order."""
        self.deliveries.append(order)

    def update_delivery_status(self, order: Order, status: str):
        """Update the delivery status of an order."""
        order.update_status(status)

# Define a class to represent the FoodChain system
class FoodChain:
    def __init__(self):
        self.restaurants = []  # List of restaurants
        self.customers = []  # List of customers
        self.delivery_personnel = []  # List of delivery personnel

    def add_restaurant(self, restaurant: Restaurant):
        """Add a restaurant to the system."""
        self.restaurants.append(restaurant)

    def add_customer(self, customer: Customer):
        """Add a customer to the system."""
        self.customers.append(customer)

    def add_delivery_personnel(self, personnel: DeliveryPersonnel):
        """Add delivery personnel to the system."""
        self.delivery_personnel.append(personnel)

    def notify(self, message: str):
        """Notify all parties about updates."""
        print(f"Notification: {message}")

# Example usage
if __name__ == "__main__":
    # Create an instance of FoodChain
    food_chain = FoodChain()

    # Create a restaurant and add it to the system
    restaurant = Restaurant("Pizza Place", {"Margherita": 8.99, "Pepperoni": 9.99})
    food_chain.add_restaurant(restaurant)

    # Create a customer and place an order
    customer = Customer("John Doe")
    food_chain.add_customer(customer)
    order = customer.place_order(restaurant, ["Margherita"])

    # Create delivery personnel and track the order
    delivery_person = DeliveryPersonnel("Jane Smith")
    food_chain.add_delivery_personnel(delivery_person)
    delivery_person.track_delivery(order)

    # Update order and delivery status
    order.update_status("Accepted")
    delivery_person.update_delivery_status(order, "Picked Up")
    food_chain.notify(f"Order {order.id} has been picked up.")

    # Customer feedback mechanism (not fully implemented)
    # This can be expanded to include rating and comments