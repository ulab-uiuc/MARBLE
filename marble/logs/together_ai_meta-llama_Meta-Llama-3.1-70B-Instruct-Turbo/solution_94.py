# solution.py

# Import necessary libraries
import threading
import time
import random
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict

# Define an Enum for transportation modes
class TransportationMode(Enum):
    PUBLIC_TRANSPORT = 1
    PRIVATE_VEHICLE = 2
    WALKING = 3

# Define a data class for User
@dataclass
class User:
    id: int
    start_location: str
    destination: str
    preferred_mode: TransportationMode

# Define a data class for Route
@dataclass
class Route:
    user_id: int
    route_id: int
    route: List[str]
    estimated_time: int
    cost: int
    eco_friendliness: int

# Define a class for SmartRoutePlanner
class SmartRoutePlanner:
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.routes: Dict[int, List[Route]] = {}
        self.traffic_conditions: Dict[str, int] = {}
        self.lock = threading.Lock()

    def add_user(self, user: User):
        with self.lock:
            self.users[user.id] = user
            self.routes[user.id] = []

    def update_traffic_conditions(self, location: str, condition: int):
        with self.lock:
            self.traffic_conditions[location] = condition

    def plan_routes(self, user_id: int):
        with self.lock:
            user = self.users[user_id]
            routes = self.routes[user_id]

            # Simulate route planning based on traffic conditions and user preferences
            for i in range(3):
                route_id = i + 1
                route = [user.start_location, user.destination]
                estimated_time = random.randint(30, 60)
                cost = random.randint(10, 20)
                eco_friendliness = random.randint(1, 10)

                # Adjust route based on traffic conditions
                if user.start_location in self.traffic_conditions:
                    estimated_time += self.traffic_conditions[user.start_location]
                if user.destination in self.traffic_conditions:
                    estimated_time += self.traffic_conditions[user.destination]

                # Adjust route based on user preferences
                if user.preferred_mode == TransportationMode.PUBLIC_TRANSPORT:
                    cost -= 5
                    eco_friendliness += 2
                elif user.preferred_mode == TransportationMode.PRIVATE_VEHICLE:
                    cost += 5
                    eco_friendliness -= 2

                routes.append(Route(user_id, route_id, route, estimated_time, cost, eco_friendliness))

    def get_routes(self, user_id: int):
        with self.lock:
            return self.routes[user_id]

    def provide_feedback(self, user_id: int, route_id: int, feedback: str):
        with self.lock:
            # Simulate feedback processing
            print(f"User {user_id} provided feedback on route {route_id}: {feedback}")

    def display_routes(self, user_id: int):
        with self.lock:
            routes = self.get_routes(user_id)
            for route in routes:
                print(f"Route {route.route_id}: {route.route}, Estimated Time: {route.estimated_time} minutes, Cost: ${route.cost}, Eco-Friendliness: {route.eco_friendliness}/10")

# Define a class for CollaborativeFeature
class CollaborativeFeature:
    def __init__(self, smart_route_planner: SmartRoutePlanner):
        self.smart_route_planner = smart_route_planner
        self.collaborative_routes: Dict[str, List[Route]] = {}

    def share_travel_plans(self, user_id: int, destination: str):
        with self.smart_route_planner.lock:
            # Simulate sharing travel plans
            print(f"User {user_id} shared travel plans to {destination}")

            # Update collaborative routes
            if destination not in self.collaborative_routes:
                self.collaborative_routes[destination] = []
            self.collaborative_routes[destination].append(self.smart_route_planner.get_routes(user_id)[0])

    def optimize_routes(self, destination: str):
        with self.smart_route_planner.lock:
            # Simulate optimizing routes
            print(f"Optimizing routes to {destination}")

            # Update routes for users traveling to the same destination
            for route in self.collaborative_routes[destination]:
                user_id = route.user_id
                self.smart_route_planner.routes[user_id] = [route]

# Define a class for UserInterface
class UserInterface:
    def __init__(self, smart_route_planner: SmartRoutePlanner, collaborative_feature: CollaborativeFeature):
        self.smart_route_planner = smart_route_planner
        self.collaborative_feature = collaborative_feature

    def display_traffic_updates(self):
        with self.smart_route_planner.lock:
            # Simulate displaying traffic updates
            print("Traffic Updates:")
            for location, condition in self.smart_route_planner.traffic_conditions.items():
                print(f"{location}: {condition}")

    def display_estimated_travel_times(self, user_id: int):
        with self.smart_route_planner.lock:
            # Simulate displaying estimated travel times
            print(f"Estimated Travel Times for User {user_id}:")
            for route in self.smart_route_planner.get_routes(user_id):
                print(f"Route {route.route_id}: {route.estimated_time} minutes")

    def display_route_options(self, user_id: int):
        with self.smart_route_planner.lock:
            # Simulate displaying route options
            print(f"Route Options for User {user_id}:")
            for route in self.smart_route_planner.get_routes(user_id):
                print(f"Route {route.route_id}: {route.route}, Cost: ${route.cost}, Eco-Friendliness: {route.eco_friendliness}/10")

# Create a SmartRoutePlanner instance
smart_route_planner = SmartRoutePlanner()

# Create a CollaborativeFeature instance
collaborative_feature = CollaborativeFeature(smart_route_planner)

# Create a UserInterface instance
user_interface = UserInterface(smart_route_planner, collaborative_feature)

# Add users
user1 = User(1, "Location A", "Location B", TransportationMode.PUBLIC_TRANSPORT)
user2 = User(2, "Location C", "Location D", TransportationMode.PRIVATE_VEHICLE)
smart_route_planner.add_user(user1)
smart_route_planner.add_user(user2)

# Update traffic conditions
smart_route_planner.update_traffic_conditions("Location A", 10)
smart_route_planner.update_traffic_conditions("Location B", 5)

# Plan routes
smart_route_planner.plan_routes(user1.id)
smart_route_planner.plan_routes(user2.id)

# Display routes
smart_route_planner.display_routes(user1.id)
smart_route_planner.display_routes(user2.id)

# Provide feedback
smart_route_planner.provide_feedback(user1.id, 1, "Good route!")

# Share travel plans
collaborative_feature.share_travel_plans(user1.id, "Location B")
collaborative_feature.share_travel_plans(user2.id, "Location D")

# Optimize routes
collaborative_feature.optimize_routes("Location B")
collaborative_feature.optimize_routes("Location D")

# Display traffic updates
user_interface.display_traffic_updates()

# Display estimated travel times
user_interface.display_estimated_travel_times(user1.id)
user_interface.display_estimated_travel_times(user2.id)

# Display route options
user_interface.display_route_options(user1.id)
user_interface.display_route_options(user2.id)