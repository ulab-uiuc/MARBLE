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

class Route:
    """Represents a route with its estimated travel time, cost, and eco-friendliness."""
    def __init__(self, route_id: int, travel_time: float, cost: float, eco_friendliness: float):
        self.route_id = route_id
        self.travel_time = travel_time
        self.cost = cost
        self.eco_friendliness = eco_friendliness

class SmartRoutePlanner:
    """The main class that manages users, routes, and traffic conditions."""
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.routes: Dict[int, List[Route]] = {}
        self.traffic_conditions: Dict[str, float] = {}  # congestion level (0-1)
        self.lock = threading.Lock()

    def add_user(self, user: User):
        """Adds a new user to the system."""
        with self.lock:
            self.users[user.user_id] = user

    def update_traffic_conditions(self, location: str, congestion_level: float):
        """Updates the traffic conditions for a given location."""
        with self.lock:
            self.traffic_conditions[location] = congestion_level

    def get_route_options(self, user_id: int):
        """Gets the route options for a given user."""
        with self.lock:
            user = self.users.get(user_id)
            if user:
                # Create a graph with the user's start location and destination
                G = nx.Graph()
                G.add_node(user.start_location)
                G.add_node(user.destination)
                # Add edges with estimated travel times based on traffic conditions
                for location in self.traffic_conditions:
                    if location == user.start_location:
                        G.add_edge(user.start_location, user.destination, weight=self.traffic_conditions[location])G.add_edge(user.start_location, location, weight={'travel_time': self.traffic_conditions[location], 'cost': self.traffic_conditions[location], 'eco_friendliness': self.traffic_conditions[location]})G.add_edge(location, user.destination, weight=self.traffic_conditions[location])
                # Calculate the shortest paths using Dijkstra's algorithm
                try:fastest_route = nx.shortest_path(G, source=user.start_location, target=user.destination, weight='travel_time')most_cost_effective_route = nx.dijkstra_path(G, source=user.start_location, target=user.destination)most_eco_friendly_route = nx.shortest_path(G, source=user.start_location, target=user.destination, weight='eco_friendliness');
return [Route(1, nx.shortest_path_length(G, source=user.start_location, target=user.destination, weight='travel_time'), nx.shortest_path_length(G, source=user.start_location, target=user.destination, weight='cost'), nx.shortest_path_length(G, source=user.start_location, target=user.destination, weight='eco_friendliness')), Route(2, nx.shortest_path_length(G, source=user.start_location, target=user.destination, weight='travel_time'), nx.shortest_path_length(G, source=user.start_location, target=user.destination, weight='cost'), nx.shortest_path_length(G, source=user.start_location, target=user.destination, weight='eco_friendliness')), Route(3, nx.shortest_path_length(G, source=user.start_location, target=user.destination, weight='travel_time'), nx.shortest_path_length(G, source=user.start_location, target=user.destination, weight='cost'), nx.shortest_path_length(G, source=user.start_location, target=user.destination, weight='eco_friendliness'))]except nx.NetworkXNoPath:
                    return []

    def display_route_options(self, user_id: int):
        """Displays the route options for a given user."""
        route_options = self.get_route_options(user_id)
        if route_options:
            print("Route Options:")
            for route in route_options:
                print(f"Route {route.route_id}: Travel Time = {route.travel_time} minutes, Cost = ${route.cost}, Eco-Friendliness = {route.eco_friendliness}")
        else:
            print("No route options available.")

    def get_user_feedback(self, user_id: int):
        """Gets feedback from a user about their current route."""
        # Simulate user feedback
        return "Good"

    def update_routes(self, user_id: int, feedback: str):
        """Updates the routes for a given user based on their feedback."""
        # Simulate route update
        print("Routes updated.")

    def display_traffic_updates(self):
        """Displays real-time traffic updates."""
        print("Real-time Traffic Updates:")
        for location, congestion_level in self.traffic_conditions.items():
            print(f"{location}: {congestion_level*100}% congested")

    def display_estimated_travel_times(self, user_id: int):
        """Displays estimated travel times for a given user."""
        route_options = self.get_route_options(user_id)
        if route_options:
            print("Estimated Travel Times:")
            for route in route_options:
                print(f"Route {route.route_id}: {route.travel_time} minutes")
        else:
            print("No estimated travel times available.")

    def display_route_options_visually(self, user_id: int):
        """Displays route options visually for a given user."""
        route_options = self.get_route_options(user_id)
        if route_options:
            # Create a graph with the user's start location and destination
            G = nx.Graph()
            G.add_node(self.users[user_id].start_location)
            G.add_node(self.users[user_id].destination)
            # Add edges with estimated travel times based on traffic conditions
            for location in self.traffic_conditions:
                if location == self.users[user_id].start_location:
                    G.add_edge(self.users[user_id].start_location, self.users[user_id].destination, weight=self.traffic_conditions[location])
                else:
                    G.add_edge(self.users[user_id].start_location, location, weight=self.traffic_conditions[location])
                    G.add_edge(location, self.users[user_id].destination, weight=self.traffic_conditions[location])
            # Draw the graph
            pos = nx.spring_layout(G)
            nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, edge_color='black', linewidths=1, font_size=12)
            labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
            plt.show()
        else:
            print("No route options available.")

def main():
    # Create a SmartRoutePlanner instance
    planner = SmartRoutePlanner()

    # Add users
    user1 = User(1, "Home", "Work", "Driving")
    user2 = User(2, "School", "Library", "Walking")
    planner.add_user(user1)
    planner.add_user(user2)

    # Update traffic conditions
    planner.update_traffic_conditions("Home", 0.5)
    planner.update_traffic_conditions("Work", 0.8)
    planner.update_traffic_conditions("School", 0.2)
    planner.update_traffic_conditions("Library", 0.6)

    # Display route options
    planner.display_route_options(1)
    planner.display_route_options(2)

    # Get user feedback
    feedback = planner.get_user_feedback(1)
    print(f"User {1} feedback: {feedback}")

    # Update routes
    planner.update_routes(1, feedback)

    # Display traffic updates
    planner.display_traffic_updates()

    # Display estimated travel times
    planner.display_estimated_travel_times(1)
    planner.display_estimated_travel_times(2)

    # Display route options visually
    planner.display_route_options_visually(1)
    planner.display_route_options_visually(2)

if __name__ == "__main__":
    main()