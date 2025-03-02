# solution.py
import threading
import time
from typing import Dict, List
import networkx as nx
import matplotlib.pyplot as plt

class User:
    """Represents a user with their starting location, destination, and preferred mode of transportation."""
    def __init__(self, user_id: int, start_location: str, destination: str, preferred_mode: str):
        self.user_id = user_id
        self.start_location = start_location
        self.destination = destination
        self.preferred_mode = preferred_mode
        self.route = None

class RoutePlanner:self.G = nx.Graph()
def _initialize_graph(self, start_location, destination):
        self.G.add_edge(start_location, destination, weight=10, time=10, cost=5, eco_friendliness=8)self.users: Dict[int, User] = {}
        self.G = nx.Graph()
        # Initialize the graph with all possible roads and their initial weights
self.initialize_graph = self._initialize_graph
        self.traffic_conditions: Dict[str, int] = {}  # road: congestion_level
        self.lock = threading.Lock()

    def add_user(self, user: User):
        """Adds a new user to the system."""
        with self.lock:
            self.users[user.user_id] = user

    def update_traffic_conditions(self, road: str, congestion_level: int):        if road in self.G.edges:
            self.G[road]['congestion_level'] = congestion_level
            # Update the weights of the edges based on the congestion levelself.traffic_conditions[road] = congestion_level

    def plan_route(self, user_id: int):for road, congestion_level in self.traffic_conditions.items():
                    if road in G.nodes:
                        G.nodes[road]["congestion_level"] = congestion_level

                # Find the shortest path based on the user's preferred mode of transportation                if user.preferred_mode == "fastest":path = nx.shortest_path(self.G, source=user.start_location, target=user.destination, weight="time")
                # Update the weights of the edges based on the current traffic conditions
                for road in self.G.edges:
                    if road in self.traffic_conditions:
                        congestion_level = self.traffic_conditions[road]
                        self.G[road[0]][road[1]]['time'] = self.G[road[0]][road[1]]['time'] * (1 + congestion_level / 100)elif user.preferred_mode == "most cost-effective":path = nx.shortest_path(self.G, source=user.start_location, target=user.destination, weight="cost")
                # Update the weights of the edges based on the current traffic conditions
                for road in self.G.edges:
                    if road in self.traffic_conditions:
                        congestion_level = self.traffic_conditions[road]
                        self.G[road[0]][road[1]]['cost'] = self.G[road[0]][road[1]]['cost'] * (1 + congestion_level / 100)elif user.preferred_mode == "most eco-friendly":path = nx.shortest_path(self.G, source=user.start_location, target=user.destination, weight="eco_friendliness")
                # Update the weights of the edges based on the current traffic conditions
                for road in self.G.edges:
                    if road in self.traffic_conditions:
                        congestion_level = self.traffic_conditions[road]
                        self.G[road[0]][road[1]]['eco_friendliness'] = self.G[road[0]][road[1]]['eco_friendliness'] * (1 + congestion_level / 100)user.route = path

    def get_route(self, user_id: int):
        """Returns the planned route for a user."""
        with self.lock:
            user = self.users.get(user_id)
            if user:
                return user.route

    def display_traffic_updates(self):
        """Displays real-time traffic updates."""
        with self.lock:
            print("Real-time Traffic Updates:")
            for road, congestion_level in self.traffic_conditions.items():
                print(f"{road}: {congestion_level}")

    def display_route_options(self, user_id: int):
        """Displays multiple route options for a user."""
        with self.lock:
            user = self.users.get(user_id)
            if user:
                print("Route Options:")
                print(f"Fastest Route: {nx.shortest_path(nx.Graph(), source=user.start_location, target=user.destination, weight='weight')}")
                print(f"Most Cost-Effective Route: {nx.shortest_path(nx.Graph(), source=user.start_location, target=user.destination, weight='weight')}")
                print(f"Most Eco-Friendly Route: {nx.shortest_path(nx.Graph(), source=user.start_location, target=user.destination, weight='weight')}")

def main():
    route_planner = RoutePlanner()

    # Add users
    user1 = User(1, "Road A", "Road D", "fastest")
    user2 = User(2, "Road B", "Road C", "most cost-effective")
    route_planner.add_user(user1)
    route_planner.add_user(user2)

    # Update traffic conditions
    route_planner.update_traffic_conditions("Road A", 5)
    route_planner.update_traffic_conditions("Road B", 10)

    # Plan routes
    route_planner.plan_route(1)
    route_planner.plan_route(2)

    # Display traffic updates
    route_planner.display_traffic_updates()

    # Display route options
    route_planner.display_route_options(1)
    route_planner.display_route_options(2)

    # Display planned routes
    print("Planned Routes:")
    print(f"User 1: {route_planner.get_route(1)}")
    print(f"User 2: {route_planner.get_route(2)}")

if __name__ == "__main__":
    main()