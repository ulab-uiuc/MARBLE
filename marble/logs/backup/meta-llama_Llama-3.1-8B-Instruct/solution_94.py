# solution.py
# Importing required libraries
import networkx as nx
import matplotlib.pyplot as plt
import random
import time
from threading import Thread

# Class to represent a user
class User:
    def __init__(self, name, start_location, destination, preferred_mode):
        self.name = name
        self.start_location = start_location
        self.destination = destination
        self.preferred_mode = preferred_mode
        self.route = None

# Class to represent the SmartRoutePlanner system
class SmartRoutePlanner:
    def __init__(self):
        self.users = []
        self.graph = nx.Graph()
        self.traffic_conditions = {}

    # Method to add a user to the system
    def add_user(self, user):
        self.users.append(user)

    # Method to update traffic conditions
    def update_traffic_conditions(self, location, condition):
        self.traffic_conditions[location] = condition

    # Method to calculate the shortest path between two locations
    def calculate_shortest_path(self, start, end):
        try:
            return nx.shortest_path(self.graph, start, end)
        except nx.NetworkXNoPath:
            return None

    # Method to calculate the fastest route for a user
    def calculate_fastest_route(self, user):
        if user.route:
            return user.route
        shortest_path = self.calculate_shortest_path(user.start_location, user.destination)
        if shortest_path:
            user.route = shortest_path
            return shortest_path
        return None

    # Method to calculate the most cost-effective route for a user
    def calculate_cost_effective_route(self, user):
        # For simplicity, assume cost-effective route is the same as the fastest route
        return self.calculate_fastest_route(user)

    # Method to calculate the most eco-friendly route for a user
    def calculate_eco_friendly_route(self, user):
        # For simplicity, assume eco-friendly route is the same as the fastest route
        return self.calculate_fastest_route(user)

    # Method to display the routes for all users
    def display_routes(self):
        for user in self.users:
            print(f"User: {user.name}")
            print(f"Route: {user.route}")
            print()

    # Method to update routes for all users based on traffic conditions
    def update_routes(self):
        for user in self.users:
            self.calculate_fastest_route(user)
            self.calculate_cost_effective_route(user)
            self.calculate_eco_friendly_route(user)

    # Method to display real-time traffic updates
    def display_traffic_updates(self):
        for location, condition in self.traffic_conditions.items():
            print(f"Location: {location}, Condition: {condition}")

# Class to represent a traffic condition
class TrafficCondition:
    def __init__(self, location, condition):
        self.location = location
        self.condition = condition

# Function to simulate real-time traffic updates
def simulate_traffic_updates(smart_route_planner):
    while True:
        location = random.choice(list(smart_route_planner.graph.nodes))
        condition = random.choice(["congested", "accident", "road_closure"])
        smart_route_planner.update_traffic_conditions(location, condition)
        print(f"Simulating traffic update: Location: {location}, Condition: {condition}")
        time.sleep(1)

# Function to display user feedback
def display_user_feedback(smart_route_planner):
    while True:
        user_name = input("Enter user name: ")
        user_feedback = input("Enter user feedback: ")
        for user in smart_route_planner.users:
            if user.name == user_name:
                print(f"User: {user.name}, Feedback: {user_feedback}")
                break
        else:
            print("User not found.")
        time.sleep(1)

# Main function
def main():
    smart_route_planner = SmartRoutePlanner()

    # Create users
    user1 = User("User1", "A", "D", "car")
    user2 = User("User2", "B", "C", "bus")
    user3 = User("User3", "C", "A", "bike")

    # Add users to the system
    smart_route_planner.add_user(user1)
    smart_route_planner.add_user(user2)
    smart_route_planner.add_user(user3)

    # Create graph
    smart_route_planner.graph.add_node("A")
    smart_route_planner.graph.add_node("B")
    smart_route_planner.graph.add_node("C")
    smart_route_planner.graph.add_node("D")
    smart_route_planner.graph.add_edge("A", "B")
    smart_route_planner.graph.add_edge("B", "C")
    smart_route_planner.graph.add_edge("C", "D")
    smart_route_planner.graph.add_edge("D", "A")

    # Simulate real-time traffic updates
    traffic_thread = Thread(target=simulate_traffic_updates, args=(smart_route_planner,))
    traffic_thread.daemon = True
    traffic_thread.start()

    # Display user feedback
    feedback_thread = Thread(target=display_user_feedback, args=(smart_route_planner,))
    feedback_thread.daemon = True
    feedback_thread.start()

    # Update routes for all users
    while True:
        smart_route_planner.update_routes()
        smart_route_planner.display_routes()
        smart_route_planner.display_traffic_updates()
        time.sleep(2)

if __name__ == "__main__":
    main()