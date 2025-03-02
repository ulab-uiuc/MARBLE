# solution.py

class User:
    """Class representing a user in the travel planner system."""
    
    def __init__(self, username, preferences):
        """Initialize a user with a username and travel preferences."""
        self.username = username
        self.preferences = preferences  # Dictionary to hold user preferences

class CollaborativeTravelPlanner:
    """Class to manage the collaborative travel planning process."""
    
    def __init__(self):
        """Initialize the travel planner with an empty user list and itineraries."""
        self.users = []  # List to hold registered users
        self.individual_itineraries = {}  # Dictionary to hold individual itineraries
        self.group_itinerary = []  # List to hold the final group itinerary

    def register_user(self, username, preferences):
        """Register a new user with their travel preferences."""
        user = User(username, preferences)
        self.users.append(user)  # Add user to the list
        print(f"User {username} registered successfully.")

    def collect_preferences(self):
        """Collect detailed travel preferences from each user."""
        for user in self.users:
            print(f"Collecting preferences for {user.username}: {user.preferences}")

    def generate_individual_itineraries(self):
        """Generate personalized itineraries for each user based on their preferences."""
        for user in self.users:
            itinerary = self.create_itinerary(user.preferences)def create_itinerary(self, preferences):
        """Create an itinerary based on user preferences."""
        itinerary = []
        destinations = preferences['destinations']
        activities = preferences['activities']
        budget = preferences['budget']
        dates = preferences['dates']

        # Simple logic to create an itinerary
        itinerary.append(f"Destinations: {', '.join(destinations)}")
        itinerary.append(f"Activities: {', '.join(activities)}")
        itinerary.append(f"Budget: ${budget}")
        itinerary.append(f"Travel Dates: {', '.join(dates)}")

        return '\n'.join(itinerary)    def integrate_itineraries(self):
        """Integrate individual itineraries into a cohesive group itinerary."""
        for itinerary in self.individual_itineraries.values():
            self.group_itinerary.append(itinerary)
        print(f"Integrated group itinerary: {self.group_itinerary}")

    def resolve_conflicts(self):
        """Resolve conflicts in preferences and ensure a balanced group itinerary."""
        # Placeholder for conflict resolution logic
        print("Resolving conflicts in the group itinerary...")

    def enable_real_time_collaboration(self):
        """Enable real-time collaboration for users to modify the itinerary."""
        print("Real-time collaboration enabled for users.")

    def notify_users(self, message):
        """Notify users about updates and changes in the itinerary."""
        for user in self.users:
            print(f"Notification to {user.username}: {message}")

# Example usage
if __name__ == "__main__":
    planner = CollaborativeTravelPlanner()
    
    # Register users with their preferences
    planner.register_user("Alice", {"destinations": ["Paris", "London"], "activities": ["sightseeing"], "budget": 1500, "dates": ["2023-06-01", "2023-06-10"]})
    planner.register_user("Bob", {"destinations": ["London", "Berlin"], "activities": ["museums"], "budget": 1200, "dates": ["2023-06-05", "2023-06-15"]})
    
    # Collect preferences
    planner.collect_preferences()
    
    # Generate individual itineraries
    planner.generate_individual_itineraries()
    
    # Integrate itineraries into a group itinerary
    planner.integrate_itineraries()
    
    # Resolve conflicts
    planner.resolve_conflicts()
    
    # Enable real-time collaboration
    planner.enable_real_time_collaboration()
    
    # Notify users about the finalized itinerary
    planner.notify_users("The group itinerary has been finalized.")