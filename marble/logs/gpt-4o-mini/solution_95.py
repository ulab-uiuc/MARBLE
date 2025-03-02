# solution.py

import random
from typing import List, Dict, Any

class Route:
    """Class to represent a transportation route."""
    def __init__(self, mode: str, duration: int, cost: float, environmental_impact: float):
        self.mode = mode  # Mode of transportation (e.g., 'car', 'bus', 'bike')
        self.duration = duration  # Duration in minutes
        self.cost = cost  # Cost of the route
        self.environmental_impact = environmental_impact  # Environmental impact score

    def __repr__(self):
        return f"Route(mode={self.mode}, duration={self.duration}, cost={self.cost}, environmental_impact={self.environmental_impact})"


class User:
    """Class to represent a user of the MATP system."""
    def __init__(self, user_id: str):
        self.user_id = user_id  # Unique identifier for the user
        self.preferences = {}  # User preferences for transportation
        self.feedback = []  # User feedback on routes

    def set_preferences(self, preferences: Dict[str, Any]):
        """Set user preferences for transportation."""
        self.preferences = preferences

    def provide_feedback(self, route: Route, rating: int, issue: str = None):
        """Provide feedback on a route."""
        self.feedback.append({'route': route, 'rating': rating, 'issue': issue})


class MATP:
    """Main class for the Multi-Agent Transport Planner system."""
    def __init__(self):
        self.users = []  # List of users
        self.routes = []  # List of available routes

    def add_user(self, user: User):
        """Add a user to the MATP system."""
        self.users.append(user)

    def generate_routes(self, start: str, destination: str) -> List[Route]:
        """Generate possible routes based on start and destination."""
        # Simulate route generation with random data
        return [
            Route(mode='car', duration=random.randint(20, 60), cost=random.uniform(5, 20), environmental_impact=random.uniform(1, 5)),
            Route(mode='bus', duration=random.randint(30, 90), cost=random.uniform(2, 10), environmental_impact=random.uniform(1, 3)),def suggest_routes(self, user: User, start: str, destination: str) -> List[Route]:
        """Suggest routes to the user based on their preferences."""
        # Generate routes
        routes = self.generate_routes(start, destination)
        # Filter and sort routes based on user preferences
        preferred_routes = []
        for route in routes:
            if (user.preferences.get('mode') is None or user.preferences.get('mode') == route.mode) and 
               (user.preferences.get('cost') is None or user.preferences.get('cost') >= route.cost):
                preferred_routes.append(route)
        # Sort preferred routes based on user-defined criteria
        preferred_routes.sort(key=lambda r: (r.duration if user.preferences.get('priority') == 'fastest' else 0, 
                                               r.cost if user.preferences.get('priority') == 'cheapest' else 0, 
                                               r.environmental_impact if user.preferences.get('priority') == 'environmental' else 0))
        return preferred_routes            Route(mode='walk', duration=random.randint(25, 70), cost=0, environmental_impact=random.uniform(0.1, 0.5)),
        ]

    def suggest_routes(self, user: User, start: str, destination: str) -> List[Route]:
        """Suggest routes to the user based on their preferences."""
        # Generate routes
        routes = self.generate_routes(start, destination)
        # Filter routes based on user preferences (if any)
        preferred_routes = []
        for route in routes:
            if user.preferences.get('mode') == route.mode or user.preferences.get('cost') >= route.cost:
                preferred_routes.append(route)
        return preferred_routes

    def report_issue(self, user: User, route: Route, issue: str):
        """User reports an issue with a route."""
        user.provide_feedback(route, rating=1, issue=issue)  # Assume a low rating for issues

    def get_feedback_summary(self) -> Dict[str, Any]:
        """Get a summary of user feedback for analysis."""
        feedback_summary = {}
        for user in self.users:
            for feedback in user.feedback:
                route = feedback['route']
                if route not in feedback_summary:
                    feedback_summary[route] = {'ratings': [], 'issues': []}
                feedback_summary[route]['ratings'].append(feedback['rating'])
                if feedback['issue']:
                    feedback_summary[route]['issues'].append(feedback['issue'])
        return feedback_summary


# Example usage
if __name__ == "__main__":
    matp = MATP()
    
    # Create users
    user1 = User(user_id="user1")
    user2 = User(user_id="user2")
    
    # Set preferences
    user1.set_preferences({'mode': 'bus', 'cost': 10})
    user2.set_preferences({'mode': 'bike', 'cost': 0})
    
    # Add users to MATP
    matp.add_user(user1)
    matp.add_user(user2)
    
    # Suggest routes for users
    routes_user1 = matp.suggest_routes(user1, "Location A", "Location B")
    routes_user2 = matp.suggest_routes(user2, "Location A", "Location B")
    
    print("Suggested routes for User 1:", routes_user1)
    print("Suggested routes for User 2:", routes_user2)
    
    # User 1 reports an issue
    if routes_user1:
        matp.report_issue(user1, routes_user1[0], "Traffic Jam")
    
    # Get feedback summary
    feedback_summary = matp.get_feedback_summary()
    print("Feedback Summary:", feedback_summary)