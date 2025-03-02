# user_registration.py
class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.preferences = {}

    def add_preference(self, key, value):
        self.preferences[key] = value

    def get_preferences(self):
        return self.preferences


class UserRegistration:
    def __init__(self):
        self.users = {}

    def register_user(self, username, email, password):
        if username not in self.users:
            self.users[username] = User(username, email, password)
            return True
        return False

    def get_user(self, username):
        return self.users.get(username)


# interest_and_preference_collection.py
class InterestAndPreferenceCollection:
    def __init__(self):
        self.preferences = {}

    def collect_preferences(self, user):
        preferences = user.get_preferences()
        self.preferences[user.username] = preferences

    def get_preferences(self):
        return self.preferences


# itinerary_generation.py
class ItineraryGenerator:
    def __init__(self):
        self.itineraries = {}

    def generate_itinerary(self, user):
        preferences = user.get_preferences()
        itinerary = {}
        for key, value in preferences.items():
            if key == 'destinations':
                itinerary['destinations'] = value
            elif key == 'activities':
                itinerary['activities'] = value
            elif key == 'budget':
                itinerary['budget'] = value
            elif key == 'travel_dates':
                itinerary['travel_dates'] = value
        self.itineraries[user.username] = itinerary

    def get_itinerary(self, username):
        return self.itineraries.get(username)


# conflict_resolution_and_synchronization.py
class ConflictResolver:
    def __init__(self):
        self.conflicts = {}

    def resolve_conflicts(self, itineraries):
        for username, itinerary in itineraries.items():
            conflicts = {}
            for key, value in itinerary.items():
                if key == 'destinations':
                    conflicts[key] = self.resolve_destination_conflicts(value)
                elif key == 'activities':
                    conflicts[key] = self.resolve_activity_conflicts(value)
                elif key == 'budget':
                    conflicts[key] = self.resolve_budget_conflicts(value)
                elif key == 'travel_dates':
                    conflicts[key] = self.resolve_travel_date_conflicts(value)
            self.conflicts[username] = conflicts

    def resolve_destination_conflicts(self, destinations):
        # Simple conflict resolution for destinations
        return destinations[:3]

    def resolve_activity_conflicts(self, activities):
        # Simple conflict resolution for activities
        return activities[:2]

    def resolve_budget_conflicts(self, budget):
        # Simple conflict resolution for budget
        return budget * 0.8

    def resolve_travel_date_conflicts(self, travel_dates):
        # Simple conflict resolution for travel dates
        return travel_dates[:2]

    def get_conflicts(self, username):
        return self.conflicts.get(username)


# real_time_collaboration.py
class RealTimeCollaboration:
    def __init__(self):
        self.collaboration_status = False

    def enable_collaboration(self):
        self.collaboration_status = True

    def disable_collaboration(self):
        self.collaboration_status = False

    def is_collaboration_enabled(self):
        return self.collaboration_status


# notification_system.py
class NotificationSystem:
    def __init__(self):
        self.notifications = {}

    def send_notification(self, user, message):
        self.notifications[user.username] = message

    def get_notifications(self, username):
        return self.notifications.get(username)


# solution.py
class CollaborativeTravelPlanner:
    def __init__(self):
        self.user_registration = UserRegistration()
        self.interest_and_preference_collection = InterestAndPreferenceCollection()
        self.itinerary_generator = ItineraryGenerator()
        self.conflict_resolver = ConflictResolver()
        self.real_time_collaboration = RealTimeCollaboration()
        self.notification_system = NotificationSystem()

    def register_user(self, username, email, password):
        return self.user_registration.register_user(username, email, password)

    def collect_preferences(self, user):
        self.interest_and_preference_collection.collect_preferences(user)

    def generate_itinerary(self, user):
        self.itinerary_generator.generate_itinerary(user)

    def resolve_conflicts(self, itineraries):
        self.conflict_resolver.resolve_conflicts(itineraries)

    def enable_real_time_collaboration(self):
        self.real_time_collaboration.enable_collaboration()

    def send_notification(self, user, message):
        self.notification_system.send_notification(user, message)


# Example usage
if __name__ == "__main__":
    planner = CollaborativeTravelPlanner()

    # Register users
    planner.register_user('user1', 'user1@example.com', 'password1')
    planner.register_user('user2', 'user2@example.com', 'password2')

    # Collect preferences
    user1 = planner.user_registration.get_user('user1')
    user1.add_preference('destinations', ['Paris', 'Rome', 'London'])
    user1.add_preference('activities', ['Hiking', 'Cycling', 'Swimming'])
    user1.add_preference('budget', 1000)
    user1.add_preference('travel_dates', ['2024-01-01', '2024-01-31'])

    user2 = planner.user_registration.get_user('user2')
    user2.add_preference('destinations', ['Tokyo', 'Seoul', 'Hong Kong'])
    user2.add_preference('activities', ['Shopping', 'Dining', 'Entertainment'])
    user2.add_preference('budget', 800)
    user2.add_preference('travel_dates', ['2024-02-01', '2024-02-28'])

    planner.collect_preferences(user1)
    planner.collect_preferences(user2)

    # Generate itineraries
    planner.generate_itinerary(user1)
    planner.generate_itinerary(user2)

    # Resolve conflicts
    itineraries = {user1.username: planner.itinerary_generator.get_itinerary(user1.username), user2.username: planner.itinerary_generator.get_itinerary(user2.username)}
    planner.resolve_conflicts(itineraries)

    # Enable real-time collaboration
    planner.enable_real_time_collaboration()

    # Send notifications
    planner.send_notification(user1, 'Itinerary updated!')
    planner.send_notification(user2, 'Itinerary updated!')