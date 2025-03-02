# solution.py

# Import necessary libraries
from typing import List, Dict, Optional
import uuid
import json

# Define a class to represent a Restaurant
class Restaurant:
    def __init__(self, name: str, menu: Dict[str, float]):
        self.name = name  # Name of the restaurant
        self.menu = menu  # Menu items with prices
        self.orders = []  # List to hold incoming orders

    def accept_order(self, order_id: str):
        """Accept an incoming order by its ID."""
        self.orders.append(order_id)

    def reject_order(self, order_id: str):
        """Reject an incoming order by its ID."""
        if order_id in self.orders:
            self.orders.remove(order_id)

    def modify_order(self, order_id: str, new_items: Dict[str, float]):
        """Modify an existing order with new items."""def modify_order(self, order_id: str, new_items: Dict[str, float]):
        """Modify an existing order with new items."""
        if order_id in self.orders:
            available_items = {item: price for item, price in self.menu.items() if item in new_items}
            if available_items:
                self.orders.remove(order_id)  # Remove the old order
                new_order_id = str(uuid.uuid4())  # Generate a new unique order ID
                self.orders.append(new_order_id)  # Add the modified order with new ID
                # Logic to handle updated order details (not implemented for simplicity)
            else:
                print('Some items are not available in the menu.')                print('Some items are not available in the menu.')            # Logic to modify the order (not implemented for simplicity)
            pass

# Define a class to represent a Customer
class Customer:
    def __init__(self, name: str):
        self.name = name  # Name of the customer
        self.orders = []  # List to hold customer's orders

    def place_order(self, restaurant: Restaurant, items: Dict[str, int]):
        """Place an order at a restaurant."""
        order_id = str(uuid.uuid4())  # Generate a unique order ID
        self.orders.append(order_id)  # Add order ID to customer's orders
        restaurant.accept_order(order_id)  # Notify restaurant of the new order
        # Logic to handle order details (not implemented for simplicity)
        return order_id

# Define a class to represent Delivery Personnel
class DeliveryPersonnel:
    def __init__(self, name: str):
        self.name = name  # Name of the delivery personnel
        self.deliveries = []  # List to hold deliveries

    def update_delivery_status(self, order_id: str, status: str):
        """Update the status of a delivery."""
        # Logic to update delivery status (not implemented for simplicity)
        self.deliveries.append((order_id, status))

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

    def get_nearby_restaurants(self) -> List[str]:
        """Return a list of nearby restaurants."""
        return [restaurant.name for restaurant in self.restaurants]

    def get_restaurant_menu(self, restaurant_name: str) -> Optional[Dict[str, float]]:
        """Get the menu of a specific restaurant."""
        for restaurant in self.restaurants:
            if restaurant.name == restaurant_name:
                return restaurant.menu
        return None

    def send_notification(self, message: str):
        """Send a notification to all parties."""
        # Logic to send notifications (not implemented for simplicity)
        print(f"Notification: {message}")

# Example usage of the FoodChain system
if __name__ == "__main__":
    # Create an instance of FoodChain
    food_chain = FoodChain()

    # Create some restaurants
    restaurant1 = Restaurant("Pizza Place", {"Margherita": 8.99, "Pepperoni": 9.99})
    restaurant2 = Restaurant("Sushi Spot", {"California Roll": 12.99, "Nigiri": 15.99})

    # Add restaurants to the system
    food_chain.add_restaurant(restaurant1)
    food_chain.add_restaurant(restaurant2)

    # Create a customer
    customer = Customer("John Doe")
    food_chain.add_customer(customer)

    # Customer places an order
    order_id = customer.place_order(restaurant1, {"Margherita": 2})
    print(f"Order placed with ID: {order_id}")

    # Delivery personnel
    delivery_person = DeliveryPersonnel("Jane Smith")
    food_chain.add_delivery_personnel(delivery_person)

    # Update delivery status
    delivery_person.update_delivery_status(order_id, "Picked Up")
    food_chain.send_notification(f"Order {order_id} has been picked up.")

    # Display nearby restaurants
    print("Nearby Restaurants:", food_chain.get_nearby_restaurants())
    # Display menu for a specific restaurant
    print("Menu for Pizza Place:", food_chain.get_restaurant_menu("Pizza Place"))