# solution.py

class User:
    """Class to represent a user in the travel planning system."""
    
    def __init__(self, username, preferences):
        """Initialize a user with a username and travel preferences."""
        self.username = username
        self.preferences = preferences  # Dictionary to hold user preferences

class CollaborativeTravelPlanner:
    """Class to manage the collaborative travel planning process."""
    
    def __init__(self):
        """Initialize the travel planner with an empty user list and itineraries."""
        self.users = []  # List to hold registered users
        self.individual_itineraries = []  # List to hold individual itineraries
        self.group_itinerary = None  # To hold the final group itinerary

    def register_user(self, username, preferences):
        """Register a new user with their travel preferences."""
        user = User(username, preferences)
        self.users.append(user)  # Add user to the list
        print(f"User {username} registered successfully.")

    def collect_preferences(self):
        """Collect detailed travel preferences from each user."""
        for user in self.users:
            print(f"Collecting preferences for {user.username}: {user.preferences}")def generate_individual_itineraries(self):
        """Generate personalized itineraries for each user based on their preferences."""
        for user in self.users:
            if not all(key in user.preferences for key in ["destinations", "activities", "budget", "dates"]):
                print(f"User {user.username} has incomplete preferences. Skipping itinerary generation.")
                continue
            itinerary = self.create_itinerary(user.preferences)
            self.individual_itineraries.append(itinerary)
            print(f"Generated itinerary for {user.username}: {itinerary}")    def create_itinerary(self, preferences):
        """Create an itinerary based on user preferences."""
        # This is a placeholder for actual itinerary generation logic
        return {"destinations": preferences.get("destinations", []),
                "activities": preferences.get("activities", []),
                "budget": preferences.get("budget", 0),
                "dates": preferences.get("dates", [])}

    def integrate_itineraries(self):
        """Integrate individual itineraries into a single group itinerary."""
        self.group_itinerary = self.merge_itineraries(self.individual_itineraries)
        print(f"Integrated group itinerary: {self.group_itinerary}")

    def merge_itineraries(self, itineraries):
        """Merge individual itineraries into a cohesive group itinerary."""
        # This is a placeholder for actual merging logic
        merged = {
            "destinations": [],
            "activities": [],
            "budget": 0,
            "dates": []
        }
        for itinerary in itineraries:
            merged["destinations"].extend(itinerary["destinations"])
            merged["activities"].extend(itinerary["activities"])
            merged["budget"] += itinerary["budget"]
            merged["dates"].extend(itinerary["dates"])
        return merged

    def resolve_conflicts(self):
        """Resolve conflicts in the group itinerary."""
        # Placeholder for conflict resolution logic
        print("Resolving conflicts in the group itinerary...")

    def enable_real_time_collaboration(self):
        """Enable real-time collaboration for users to modify the itinerary."""
        print("Real-time collaboration enabled for users.")

    def notify_users(self, message):
        """Notify users about updates and changes."""
        for user in self.users:
            print(f"Notification to {user.username}: {message}")

# Example usage
if __name__ == "__main__":
    planner = CollaborativeTravelPlanner()
    
    # Register users
    planner.register_user("Alice", {
        "destinations": ["Paris", "London"],
        "activities": ["sightseeing", "shopping"],
        "budget": 1500,
        "dates": ["2023-06-01", "2023-06-10"]
    })
    
    planner.register_user("Bob", {
        "destinations": ["London", "Berlin"],
        "activities": ["museums", "dining"],
        "budget": 1200,
        "dates": ["2023-06-05", "2023-06-15"]
    })
    
    # Collect preferences
    planner.collect_preferences()
    
    # Generate itineraries
    planner.generate_individual_itineraries()
    
    # Integrate itineraries
    planner.integrate_itineraries()
    
    # Resolve conflicts
    planner.resolve_conflicts()
    
    # Enable collaboration
    planner.enable_real_time_collaboration()
    
    # Notify users
    planner.notify_users("The group itinerary has been finalized.")