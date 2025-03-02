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


class UserRegistrationSystem:
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
                    conflicts[key] = value
                elif key == 'activities':
                    conflicts[key] = value
                elif key == 'budget':
                    conflicts[key] = value
                elif key == 'travel_dates':
                    conflicts[key] = value
            self.conflicts[username] = conflicts

    def get_conflicts(self):
        return self.conflicts


# real_time_collaboration.py
class RealTimeCollaboration:
    def __init__(self):
        self.collaboration = {}

    def collaborate(self, user, changes):
        self.collaboration[user.username] = changes

    def get_collaboration(self):
        return self.collaboration


# notification_system.py
class NotificationSystem:
    def __init__(self):
        self.notifications = {}

    def send_notification(self, user, message):
        self.notifications[user.username] = message

    def get_notifications(self):
        return self.notifications


# solution.py
class CollaborativeTravelPlanner:
    def __init__(self):
        self.user_registration_system = UserRegistrationSystem()
        self.interest_and_preference_collection = InterestAndPreferenceCollection()
        self.itinerary_generator = ItineraryGenerator()
        self.conflict_resolver = ConflictResolver()
        self.real_time_collaboration = RealTimeCollaboration()
        self.notification_system = NotificationSystem()

    def register_user(self, username, email, password):
        return self.user_registration_system.register_user(username, email, password)

    def collect_preferences(self, user):
        self.interest_and_preference_collection.collect_preferences(user)

    def generate_itinerary(self, user):
        self.itinerary_generator.generate_itinerary(user)

    def resolve_conflicts(self, itineraries):
        self.conflict_resolver.resolve_conflicts(itineraries)

    def collaborate(self, user, changes):
        self.real_time_collaboration.collaborate(user, changes)

    def send_notification(self, user, message):
        self.notification_system.send_notification(user, message)

    def get_user(self, username):
        return self.user_registration_system.get_user(username)

    def get_preferences(self, username):
        return self.interest_and_preference_collection.get_preferences().get(username)

    def get_itinerary(self, username):
        return self.itinerary_generator.get_itinerary(username)

    def get_conflicts(self):
        return self.conflict_resolver.get_conflicts()

    def get_collaboration(self):
        return self.real_time_collaboration.get_collaboration()

    def get_notifications(self):
        return self.notification_system.get_notifications()


# Example usage:
planner = CollaborativeTravelPlanner()

# Register users
planner.register_user('user1', 'user1@example.com', 'password1')
planner.register_user('user2', 'user2@example.com', 'password2')

# Collect preferences
user1 = planner.get_user('user1')
user2 = planner.get_user('user2')
user1.add_preference('destinations', ['Paris', 'Rome'])
user1.add_preference('activities', ['sightseeing', 'hiking'])
user1.add_preference('budget', 1000)
user1.add_preference('travel_dates', ['2024-01-01', '2024-01-31'])
user2.add_preference('destinations', ['New York', 'Los Angeles'])
user2.add_preference('activities', ['shopping', 'dining'])
user2.add_preference('budget', 2000)
user2.add_preference('travel_dates', ['2024-02-01', '2024-02-28'])

planner.collect_preferences(user1)
planner.collect_preferences(user2)

# Generate itineraries
planner.generate_itinerary(user1)
planner.generate_itinerary(user2)

# Resolve conflicts
itineraries = {user1.username: planner.get_itinerary(user1.username), user2.username: planner.get_itinerary(user2.username)}
planner.resolve_conflicts(itineraries)

# Collaborate
planner.collaborate(user1, {'destinations': ['Paris', 'Rome', 'New York']})

# Send notifications
planner.send_notification(user1, 'Itinerary updated!')
planner.send_notification(user2, 'Itinerary updated!')

# Get user, preferences, itinerary, conflicts, collaboration, and notifications
print(planner.get_user('user1'))
print(planner.get_preferences('user1'))
print(planner.get_itinerary('user1'))
print(planner.get_conflicts())
print(planner.get_collaboration())
print(planner.get_notifications())