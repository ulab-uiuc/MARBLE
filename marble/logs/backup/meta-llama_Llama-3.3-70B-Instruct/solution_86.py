# solution.py

# Import required libraries
import datetime

# User Management Module
class User:
    """Represents a user in the system."""
    def __init__(self, id, name, email):
        """
        Initializes a User object.

        Args:
            id (int): Unique identifier for the user.
            name (str): Name of the user.
            email (str): Email address of the user.
        """
        self.id = id
        self.name = name
        self.email = email

class Player(User):
    """Represents a player in the system."""
    def __init__(self, id, name, email, position):
        """
        Initializes a Player object.

        Args:
            id (int): Unique identifier for the player.
            name (str): Name of the player.
            email (str): Email address of the player.
            position (str): Position of the player in the team.
        """
        super().__init__(id, name, email)
        self.position = position

class Coach(User):
    """Represents a coach in the system."""
    def __init__(self, id, name, email):
        """
        Initializes a Coach object.

        Args:
            id (int): Unique identifier for the coach.
            name (str): Name of the coach.
            email (str): Email address of the coach.
        """
        super().__init__(id, name, email)

class UserManager:self.players = {}self.coaches = {}def add_player(self, player):self.players[player.id] = playerdef add_coach(self, coach):self.coaches[coach.id] = coachdef get_player(self, id):def get_coach(self, id):
    return self.coaches.get(id)class Event:
    """Represents an event in the system."""
    def __init__(self, id, name, date, time):
        """
        Initializes an Event object.

        Args:
            id (int): Unique identifier for the event.
            name (str): Name of the event.
            date (str): Date of the event.
            time (str): Time of the event.
        """
        self.id = id
        self.name = name
        self.date = date
        self.time = time

class Schedule:
    """Manages event scheduling in the system."""
    def __init__(self):
        self.events = []

    def add_event(self, event):
        """
        Adds an event to the schedule.

        Args:
            event (Event): Event object to be added.
        """
        self.events.append(event)

    def get_event(self, id):
        """
        Retrieves an event by its ID.

        Args:
            id (int): ID of the event to retrieve.

        Returns:
            Event: Event object with the specified ID, or None if not found.
        """
        for event in self.events:
            if event.id == id:
                return event
        return None

class Communication:
    """Manages real-time communication in the system."""
    def __init__(self):
        self.announcements = []

    def add_announcement(self, announcement):
        """
        Adds an announcement to the system.

        Args:
            announcement (str): Announcement to be added.
        """
        self.announcements.append(announcement)

    def get_announcements(self):
        """
        Retrieves all announcements in the system.

        Returns:
            list: List of announcements.
        """
        return self.announcements


# Performance Tracking Module
class Performance:
    """Represents a player's performance in the system."""
    def __init__(self, id, player_id, metrics):
        """
        Initializes a Performance object.

        Args:
            id (int): Unique identifier for the performance.
            player_id (int): ID of the player associated with the performance.
            metrics (dict): Dictionary of performance metrics.
        """
        self.id = id
        self.player_id = player_id
        self.metrics = metrics

class PerformanceTracker:
    """Manages performance tracking in the system."""
    def __init__(self):
        self.performances = []

    def add_performance(self, performance):
        """
        Adds a performance to the system.

        Args:
            performance (Performance): Performance object to be added.
        """
        self.performances.append(performance)

    def get_performance(self, id):
        """
        Retrieves a performance by its ID.

        Args:
            id (int): ID of the performance to retrieve.

        Returns:
            Performance: Performance object with the specified ID, or None if not found.
        """
        for performance in self.performances:
            if performance.id == id:
                return performance
        return None


# TeamSync Application
class TeamSync:
    """Represents the TeamSync application."""
    def __init__(self):
        self.user_manager = UserManager()
        self.schedule = Schedule()
        self.communication = Communication()
        self.performance_tracker = PerformanceTracker()

    def create_player(self, id, name, email, position):
        """
        Creates a new player in the system.

        Args:
            id (int): Unique identifier for the player.
            name (str): Name of the player.
            email (str): Email address of the player.
            position (str): Position of the player in the team.
        """
        player = Player(id, name, email, position)
        self.user_manager.add_player(player)

    def create_coach(self, id, name, email):
        """
        Creates a new coach in the system.

        Args:
            id (int): Unique identifier for the coach.
            name (str): Name of the coach.
            email (str): Email address of the coach.
        """
        coach = Coach(id, name, email)
        self.user_manager.add_coach(coach)

    def create_event(self, id, name, date, time):
        """
        Creates a new event in the system.

        Args:
            id (int): Unique identifier for the event.
            name (str): Name of the event.
            date (str): Date of the event.
            time (str): Time of the event.
        """
        event = Event(id, name, date, time)
        self.schedule.add_event(event)

    def create_announcement(self, announcement):
        """
        Creates a new announcement in the system.

        Args:
            announcement (str): Announcement to be added.
        """
        self.communication.add_announcement(announcement)

    def create_performance(self, id, player_id, metrics):
        """
        Creates a new performance in the system.

        Args:
            id (int): Unique identifier for the performance.
            player_id (int): ID of the player associated with the performance.
            metrics (dict): Dictionary of performance metrics.
        """
        performance = Performance(id, player_id, metrics)
        self.performance_tracker.add_performance(performance)


# Example usage
team_sync = TeamSync()

# Create players
team_sync.create_player(1, "John Doe", "john@example.com", "Forward")
team_sync.create_player(2, "Jane Doe", "jane@example.com", "Midfielder")

# Create coaches
team_sync.create_coach(1, "Coach Smith", "coach.smith@example.com")
team_sync.create_coach(2, "Coach Johnson", "coach.johnson@example.com")

# Create events
team_sync.create_event(1, "Practice Session", "2024-09-16", "10:00 AM")
team_sync.create_event(2, "Match", "2024-09-17", "2:00 PM")

# Create announcements
team_sync.create_announcement("Practice session tomorrow at 10:00 AM")
team_sync.create_announcement("Match against Team B on Sunday at 2:00 PM")

# Create performances
team_sync.create_performance(1, 1, {"goals": 2, "assists": 1})
team_sync.create_performance(2, 2, {"goals": 1, "assists": 2})

# Print user data
print("Players:")
for player in team_sync.user_manager.players:
    print(f"ID: {player.id}, Name: {player.name}, Email: {player.email}, Position: {player.position}")

print("\nCoaches:")
for coach in team_sync.user_manager.coaches:
    print(f"ID: {coach.id}, Name: {coach.name}, Email: {coach.email}")

# Print event data
print("\nEvents:")
for event in team_sync.schedule.events:
    print(f"ID: {event.id}, Name: {event.name}, Date: {event.date}, Time: {event.time}")

# Print announcement data
print("\nAnnouncements:")
for announcement in team_sync.communication.announcements:
    print(announcement)

# Print performance data
print("\nPerformances:")
for performance in team_sync.performance_tracker.performances:
    print(f"ID: {performance.id}, Player ID: {performance.player_id}, Metrics: {performance.metrics}")