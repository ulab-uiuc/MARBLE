# solution.py

# User Management Module
class User:
    """Class representing a user in the system (coach or player)."""
    
    def __init__(self, user_id, name, role):
        """
        Initialize a new user with an ID, name, and role.
        
        :param user_id: Unique identifier for the user
        :param name: Name of the user
        :param role: Role of the user (e.g., 'coach' or 'player')
        """
        self.user_id = user_id
        self.name = name
        self.role = role

class UserManager:
    """Class to manage user profiles."""
    
    def __init__(self):
        """Initialize the user manager with an empty user list."""
        self.users = {}
    
    def add_user(self, user_id, name, role):
        """Add a new user to the system."""
        if user_id in self.users:
            raise ValueError("User ID already exists.")if role not in ['coach', 'player']:
            raise ValueError("Invalid role. Role must be 'coach' or 'player'.")
        self.users[user_id] = User(user_id, name, role)    def get_user(self, user_id):
        """Retrieve a user by their ID."""
        return self.users.get(user_id, None)
    
    def remove_user(self, user_id):
        """Remove a user from the system."""
        if user_id in self.users:
            del self.users[user_id]

# Scheduling and Communication Module
class Event:
    """Class representing an event in the team schedule."""
    
    def __init__(self, event_id, title, date_time):
        """
        Initialize a new event with an ID, title, and date/time.
        
        :param event_id: Unique identifier for the event
        :param title: Title of the event
        :param date_time: Date and time of the event
        """
        self.event_id = event_id
        self.title = title
        self.date_time = date_time

class ScheduleManager:
    """Class to manage team schedules and communications."""
    
    def __init__(self):
        """Initialize the schedule manager with an empty event list."""
        self.events = {}
    
    def add_event(self, event_id, title, date_time):
        """Add a new event to the schedule."""
        if event_id in self.events:
            raise ValueError("Event ID already exists.")
        self.events[event_id] = Event(event_id, title, date_time)
    
    def get_event(self, event_id):
        """Retrieve an event by its ID."""
        return self.events.get(event_id, None)
    
    def remove_event(self, event_id):
        """Remove an event from the schedule."""
        if event_id in self.events:
            del self.events[event_id]
    
    def send_announcement(self, message):
        """Simulate sending an announcement to all team members."""
        print(f"Announcement to all team members: {message}")

# Performance Tracking Module
class Performance:
    """Class representing a player's performance metrics."""
    
    def __init__(self, player_id):
        """
        Initialize performance metrics for a player.
        
        :param player_id: Unique identifier for the player
        """
        self.player_id = player_id
        self.stats = {}
    
    def add_stat(self, stat_name, value):
        """Add a performance statistic for the player."""
        self.stats[stat_name] = value
    
    def get_stats(self):
        """Retrieve all performance statistics for the player."""
        return self.stats

class PerformanceTracker:
    """Class to track player performance."""
    
    def __init__(self):
        """Initialize the performance tracker with an empty performance records."""
        self.performances = {}
    
    def add_performance(self, player_id):
        """Add a new performance record for a player."""
        if player_id in self.performances:
            raise ValueError("Performance record already exists for this player.")
        self.performances[player_id] = Performance(player_id)
    
    def get_performance(self, player_id):
        """Retrieve performance metrics for a player."""
        return self.performances.get(player_id, None)

# Example usage of the modules
if __name__ == "__main__":
    # Initialize user manager
    user_manager = UserManager()
    user_manager.add_user("1", "Coach John", "coach")
    user_manager.add_user("2", "Player Mike", "player")
    
    # Initialize schedule manager
    schedule_manager = ScheduleManager()
    schedule_manager.add_event("1", "Practice Session", "2023-10-01 10:00")
    schedule_manager.send_announcement("Practice is scheduled for October 1st at 10 AM.")
    
    # Initialize performance tracker
    performance_tracker = PerformanceTracker()
    performance_tracker.add_performance("2")
    performance_tracker.get_performance("2").add_stat("Goals", 5)
    print(performance_tracker.get_performance("2").get_stats())