# solution.py

# User Registration and Profile Management Module
class User:
    def __init__(self, username, profile_picture, cultural_background, interests):
        self.username = username  # User's unique username
        self.profile_picture = profile_picture  # URL or path to the user's profile picture
        self.cultural_background = cultural_background  # User's cultural background
        self.interests = interests  # List of user's interests

class UserManager:
    def __init__(self):
        self.users = []  # List to store registered users

    def register_user(self, username, profile_picture, cultural_background, interests):
        """Register a new user and add them to the user list."""
        for user in self.users:
            if user.username == username:
                raise ValueError('Username already taken.')
        new_user = User(username, profile_picture, cultural_background, interests)        self.users.append(new_user)
        return new_user        return new_user

    def get_user(self, username):
        """Retrieve a user by their username."""
        for user in self.users:
            if user.username == username:
                return user
        return None

# Virtual Tour Module
class VirtualTour:
    def __init__(self, landmark_name, description):
        self.landmark_name = landmark_name  # Name of the cultural landmark
        self.description = description  # Description of the landmark
        self.hotspots = []  # List to store interactive hotspots

    def add_hotspot(self, hotspot):
        """Add an interactive hotspot to the virtual tour."""
        self.hotspots.append(hotspot)

class Hotspot:
    def __init__(self, title, info, audio_guide):
        self.title = title  # Title of the hotspot
        self.info = info  # Information about the hotspot
        self.audio_guide = audio_guide  # URL or path to the audio guide

# Language Learning Module
class LanguageExchange:
    def __init__(self):
        self.pairs = []  # List to store user pairs for language exchange

    def pair_users(self, user1, user2):
        """Pair two users for language exchange."""
        self.pairs.append((user1, user2))

    def translate(self, text, target_language):
        """Simulate a translation tool (placeholder for actual translation logic)."""
        return f"Translated '{text}' to {target_language}"

# Cultural Workshop Module
class CulturalWorkshop:
    def __init__(self, title, expert, session_type):
        self.title = title  # Title of the workshop
        self.expert = expert  # Name of the cultural expert
        self.session_type = session_type  # Live or pre-recorded

    def join_session(self):
        """Simulate joining a workshop session."""
        return f"Joined the workshop: {self.title} by {self.expert}"

# User Feedback and Rating System
class Feedback:
    def __init__(self):
        self.reviews = []  # List to store user feedback

    def add_review(self, user, rating, comment):
        """Add a review from a user."""
        review = {
            'user': user.username,
            'rating': rating,
            'comment': comment
        }
        self.reviews.append(review)

    def get_reviews(self):
        """Retrieve all reviews."""
        return self.reviews

# Main Application Class
class CulturalExchangeHub:
    def __init__(self):
        self.user_manager = UserManager()  # User management system
        self.virtual_tours = []  # List of virtual tours
        self.language_exchange = LanguageExchange()  # Language exchange system
        self.workshops = []  # List of cultural workshops
        self.feedback_system = Feedback()  # Feedback system

    def add_virtual_tour(self, tour):
        """Add a virtual tour to the platform."""
        self.virtual_tours.append(tour)

    def add_workshop(self, workshop):
        """Add a cultural workshop to the platform."""
        self.workshops.append(workshop)

# Example usage
if __name__ == "__main__":
    hub = CulturalExchangeHub()

    # Register a user
    user1 = hub.user_manager.register_user("Alice", "alice_pic.jpg", "American", ["Art", "Travel"])
    user2 = hub.user_manager.register_user("Bob", "bob_pic.jpg", "French", ["Cuisine", "History"])

    # Create a virtual tour
    tour = VirtualTour("Eiffel Tower", "A famous landmark in Paris.")
    hotspot1 = Hotspot("Viewpoint", "A great place to see the city.", "audio_guide1.mp3")
    tour.add_hotspot(hotspot1)
    hub.add_virtual_tour(tour)

    # Pair users for language exchange
    hub.language_exchange.pair_users(user1, user2)

    # Create a cultural workshop
    workshop = CulturalWorkshop("French Cooking", "Chef Pierre", "Live")
    hub.add_workshop(workshop)

    # Add feedback
    hub.feedback_system.add_review(user1, 5, "Amazing experience!")
    hub.feedback_system.add_review(user2, 4, "Very informative.")

    # Print feedback
    print(hub.feedback_system.get_reviews())