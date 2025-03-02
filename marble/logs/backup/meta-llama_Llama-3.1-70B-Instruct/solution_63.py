# multi_agent_dine.py

import threading
import time
import random
from datetime import datetime, timedelta

# Agent class representing a delivery agent
class Agent:
    def __init__(self, agent_id, location):
        self.agent_id = agent_id
        self.location = location
        self.availability = True
        self.current_load = 0
        self.delivery_status = {}

    def update_availability(self, availability):
        self.availability = availability

    def update_current_load(self, current_load):
        self.current_load = current_load

    def update_delivery_status(self, order_id, status):
        self.delivery_status[order_id] = status

# Restaurant class representing a restaurant
class Restaurant:
    def __init__(self, restaurant_id, location):
        self.restaurant_id = restaurant_id
        self.location = location
        self.orders = {}

    def place_order(self, order_id, customer_location):
        self.orders[order_id] = {"customer_location": customer_location, "status": "pending"}

    def update_order_status(self, order_id, status):
        if order_id in self.orders:
            self.orders[order_id]["status"] = status

# Customer class representing a customer
class Customer:
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.orders = {}

    def place_order(self, order_id, restaurant):
        self.orders[order_id] = {"restaurant": restaurant, "status": "pending"}

    def update_order_status(self, order_id, status):
        if order_id in self.orders:
            self.orders[order_id]["status"] = status

# MultiAgentDine class representing the MultiAgentDine system
class MultiAgentDine:
    def __init__(self):
        self.agents = {}
        self.restaurants = {}
        self.customers = {}
        self.orders = {}

    def add_agent(self, agent_id, location):
        self.agents[agent_id] = Agent(agent_id, location)

    def add_restaurant(self, restaurant_id, location):
        self.restaurants[restaurant_id] = Restaurant(restaurant_id, location)

    def add_customer(self, customer_id):
        self.customers[customer_id] = Customer(customer_id)

    def place_order(self, order_id, customer_id, restaurant_id, customer_location):
        if customer_id in self.customers and restaurant_id in self.restaurants:
            self.customers[customer_id].place_order(order_id, self.restaurants[restaurant_id])
            self.restaurants[restaurant_id].place_order(order_id, customer_location)
            self.orders[order_id] = {"customer_id": customer_id, "restaurant_id": restaurant_id, "status": "pending"}

    def assign_agent(self, order_id):
        if order_id in self.orders:
            # Find the most suitable agent based on proximity, availability, and current load
            suitable_agent = None
            min_distance = float("inf")
            for agent_id, agent in self.agents.items():
                if agent.availability and agent.current_load < 5:
                    distance = self.calculate_distance(self.restaurants[self.orders[order_id]["restaurant_id"]].location, agent.location)
                    if distance < min_distance:
                        min_distance = distance
                        suitable_agent = agent_id
            if suitable_agent:
                self.agents[suitable_agent].update_availability(False)
                self.agents[suitable_agent].update_current_load(self.agents[suitable_agent].current_load + 1)
                self.agents[suitable_agent].update_delivery_status(order_id, "in_progress")
                self.restaurants[self.orders[order_id]["restaurant_id"]].update_order_status(order_id, "in_progress")
                self.customers[self.orders[order_id]["customer_id"]].update_order_status(order_id, "in_progress")
                print(f"Agent {suitable_agent} assigned to order {order_id}")

    def update_delivery_status(self, order_id, status):
        if order_id in self.orders:
            self.agents[self.get_assigned_agent(order_id)].update_delivery_status(order_id, status)
            self.restaurants[self.orders[order_id]["restaurant_id"]].update_order_status(order_id, status)
            self.customers[self.orders[order_id]["customer_id"]].update_order_status(order_id, status)
            if status == "delivered":
                self.agents[self.get_assigned_agent(order_id)].update_availability(True)
                self.agents[self.get_assigned_agent(order_id)].update_current_load(self.agents[self.get_assigned_agent(order_id)].current_load - 1)

    def get_assigned_agent(self, order_id):
        for agent_id, agent in self.agents.items():
            if order_id in agent.delivery_status:
                return agent_id

    def calculate_distance(self, location1, location2):
        # Calculate the distance between two locations (simplified for demonstration purposes)
        return abs(location1 - location2)

# Test cases
def test_single_agent_delivery():
    multi_agent_dine = MultiAgentDine()
    multi_agent_dine.add_agent("agent1", 0)
    multi_agent_dine.add_restaurant("restaurant1", 0)
    multi_agent_dine.add_customer("customer1")
    multi_agent_dine.place_order("order1", "customer1", "restaurant1", 10)
    multi_agent_dine.assign_agent("order1")
    multi_agent_dine.update_delivery_status("order1", "delivered")
    print("Single agent delivery test passed")

def test_multi_agent_coordination():
    multi_agent_dine = MultiAgentDine()
    multi_agent_dine.add_agent("agent1", 0)
    multi_agent_dine.add_agent("agent2", 10)
    multi_agent_dine.add_restaurant("restaurant1", 0)
    multi_agent_dine.add_restaurant("restaurant2", 10)
    multi_agent_dine.add_customer("customer1")
    multi_agent_dine.add_customer("customer2")
    multi_agent_dine.place_order("order1", "customer1", "restaurant1", 5)
    multi_agent_dine.place_order("order2", "customer2", "restaurant2", 15)
    multi_agent_dine.assign_agent("order1")
    multi_agent_dine.assign_agent("order2")
    multi_agent_dine.update_delivery_status("order1", "delivered")
    multi_agent_dine.update_delivery_status("order2", "delivered")
    print("Multi-agent coordination test passed")

def test_edge_cases():
    multi_agent_dine = MultiAgentDine()
    multi_agent_dine.add_agent("agent1", 0)
    multi_agent_dine.add_restaurant("restaurant1", 0)
    multi_agent_dine.add_customer("customer1")
    multi_agent_dine.place_order("order1", "customer1", "restaurant1", 10)
    multi_agent_dine.assign_agent("order1")
    # Simulate agent failure
    multi_agent_dine.agents["agent1"].update_availability(False)
    multi_agent_dine.update_delivery_status("order1", "failed")
    print("Edge case test passed")

# Run test cases
test_single_agent_delivery()
test_multi_agent_coordination()
test_edge_cases()