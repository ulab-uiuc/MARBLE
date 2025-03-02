# solution.py
# Importing necessary libraries
from abc import ABC, abstractmethod
from typing import List, Dict
from enum import Enum
import bcrypt
import hashlib
import hmac
import json

# Defining an Enum for order status
class OrderStatus(Enum):
    """Enum for order status"""
    PENDING = 1
    ACCEPTED = 2
    REJECTED = 3
    DELIVERED = 4

# Defining an abstract class for users
class User(ABC):
# Defining a class for customers
class Customer(User):
    def __init__(self, id: int, name: str, email: str, password: str):
        self.id = id
        self.name = name
        self.email = email
        self.password = self._hash_password(password)
        self.orders = []

    def login(self, email: str, password: str) -> bool:
        if self.email == email and self._check_password(password):
            return True
        return False

    def _hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password.decode()

    def _check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password.encode())def place_order(self, restaurant_id: int, order_details: Dict) -> None:
        # Placing an order
        self.orders.append({"restaurant_id": restaurant_id, "order_details": order_details})

# Defining a class for restaurants
class Restaurant(User):def login(self, email: str, password: str) -> bool:
        if self.email == email and self._check_password(password):
            return True
        return False

    def _hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password.decode()

    def _check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password.encode())def add_menu_item(self, item: Dict) -> None:    def accept_order(self, order_id: int, delivery_personnel_id: int) -> None:
        # Accepting an order and notifying the FoodChain system
        for order in self.orders:
            if order['id'] == order_id:
                # Notify the FoodChain system to assign a delivery personnel
                food_chain = FoodChain()
                food_chain.assign_delivery_personnel(order_id, delivery_personnel_id)
                order['status'] = OrderStatus.ACCEPTED
                break        order['status'] = OrderStatus.ACCEPTED
                    break
        # Initializing FoodChain attributes
        self.customers = []
        self.restaurants = []
        self.delivery_personnel = []

    def add_customer(self, customer: Customer) -> None:
        # Adding a customer
        self.customers.append(customer)

    def add_restaurant(self, restaurant: Restaurant) -> None:
        # Adding a restaurant
        self.restaurants.append(restaurant)

    def add_delivery_personnel(self, delivery_personnel: DeliveryPersonnel) -> None:    def accept_order(self, restaurant_id: int, order_id: int, delivery_personnel_id: int) -> None:
        # Accepting an order and assigning a delivery personnel
        restaurant = next((r for r in self.restaurants if r.id == restaurant_id), None)
        if restaurant:
            self.assign_delivery_personnel(order_id, delivery_personnel_id)
            restaurant.accept_order(order_id)        restaurant.accept_order(order_id)

    def reject_order(self, restaurant_id: int, order_id: int) -> None:
        # Rejecting an order
        restaurant = next((r for r in self.restaurants if r.id == restaurant_id), None)
        if restaurant:
            restaurant.reject_order(order_id)

    def update_delivery_status(self, delivery_personnel_id: int, delivery_id: int, status: OrderStatus) -> None:
        # Updating delivery status
        delivery_personnel = next((dp for dp in self.delivery_personnel if dp.id == delivery_personnel_id), None)
        if delivery_personnel:
            delivery_personnel.update_delivery_status(delivery_id, status)

# Defining a function to simulate the FoodChain system
def simulate_food_chain() -> None:
    # Creating a FoodChain instance
    food_chain = FoodChain()

    # Creating customers
    customer1 = Customer(1, "John Doe", "john@example.com", "password123")
    customer2 = Customer(2, "Jane Doe", "jane@example.com", "password123")

    # Creating restaurants
    restaurant1 = Restaurant(1, "Restaurant 1", "restaurant1@example.com", "password123")
    restaurant2 = Restaurant(2, "Restaurant 2", "restaurant2@example.com", "password123")

    # Creating delivery personnel
    delivery_personnel1 = DeliveryPersonnel(1, "Delivery Person 1", "delivery1@example.com", "password123")
    delivery_personnel2 = DeliveryPersonnel(2, "Delivery Person 2", "delivery2@example.com", "password123")

    # Adding customers, restaurants, and delivery personnel to the FoodChain
    food_chain.add_customer(customer1)
    food_chain.add_customer(customer2)
    food_chain.add_restaurant(restaurant1)
    food_chain.add_restaurant(restaurant2)
    food_chain.add_delivery_personnel(delivery_personnel1)
    food_chain.add_delivery_personnel(delivery_personnel2)

    # Getting nearby restaurants for a customer
    nearby_restaurants = food_chain.get_nearby_restaurants(customer1.id)
    print("Nearby restaurants for customer 1:")
    for restaurant in nearby_restaurants:
        print(restaurant.name)

    # Placing an order
    food_chain.place_order(customer1.id, restaurant1.id, {"item": "Burger", "quantity": 2})
    print("Order placed successfully!")

    # Accepting an order
    food_chain.accept_order(restaurant1.id, 1)
    print("Order accepted successfully!")

    # Updating delivery status
    food_chain.update_delivery_status(delivery_personnel1.id, 1, OrderStatus.DELIVERED)
    print("Delivery status updated successfully!")

# Simulating the FoodChain system
simulate_food_chain()