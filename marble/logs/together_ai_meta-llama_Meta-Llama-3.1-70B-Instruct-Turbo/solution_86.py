# team_sync.py

class User:
    """Represents a user in the TeamSync system."""
    
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

    def __str__(self):
        """Returns a string representation of the User object."""
        return f"User {self.id}: {self.name} ({self.email})"


class Player(User):
    """Represents a player in the TeamSync system."""
    
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

    def __str__(self):
        """Returns a string representation of the Player object."""
        return f"Player {self.id}: {self.name} ({self.email}) - {self.position}"


class Coach(User):
    """Represents a coach in the TeamSync system."""
    
    def __init__(self, id, name, email):
        """
        Initializes a Coach object.

        Args:
            id (int): Unique identifier for the coach.
            name (str): Name of the coach.
            email (str): Email address of the coach.
        """
        super().__init__(id, name, email)

    def __str__(self):
        """Returns a string representation of the Coach object."""
        return f"Coach {self.id}: {self.name} ({self.email})"


class TeamSync:
    """Represents the TeamSync system."""
    
    def __init__(self):
        """Initializes the TeamSync system."""
        self.players = []
        self.coaches = []
        self.schedules = []
        self.performance_data = {}

    def add_player(self, player):
        """
        Adds a player to the TeamSync system.

        Args:
            player (Player): Player object to add.
        """
        self.players.append(player)

    def add_coach(self, coach):
        """
        Adds a coach to the TeamSync system.

        Args:
            coach (Coach): Coach object to add.
        """
        self.coaches.append(coach)

    def create_schedule(self, event_name, event_date, event_time):
        """
        Creates a new schedule event in the TeamSync system.

        Args:
            event_name (str): Name of the event.
            event_date (str): Date of the event.
            event_time (str): Time of the event.
        """
        self.schedules.append({"event_name": event_name, "event_date": event_date, "event_time": event_time})

    def send_announcement(self, announcement):
        """
        Sends an announcement to all team members in the TeamSync system.

        Args:
            announcement (str): Announcement message to send.
        """
        print(f"Announcement: {announcement}")

    def track_performance(self, player_id, performance_data):
        """
        Tracks the performance of a player in the TeamSync system.

        Args:
            player_id (int): Unique identifier of the player.
            performance_data (dict): Performance data to track.
        """
        self.performance_data[player_id] = performance_data


# Example usage:
team_sync = TeamSync()

# Create players
player1 = Player(1, "John Doe", "john.doe@example.com", "Forward")
player2 = Player(2, "Jane Doe", "jane.doe@example.com", "Defender")

# Create coaches
coach1 = Coach(1, "Coach Smith", "coach.smith@example.com")

# Add players and coaches to the TeamSync system
team_sync.add_player(player1)
team_sync.add_player(player2)
team_sync.add_coach(coach1)

# Create schedule events
team_sync.create_schedule("Practice Session", "2024-03-01", "10:00 AM")
team_sync.create_schedule("Match Day", "2024-03-08", "2:00 PM")

# Send announcements
team_sync.send_announcement("Practice session tomorrow at 10:00 AM!")
team_sync.send_announcement("Match day this Saturday at 2:00 PM!")

# Track player performance
team_sync.track_performance(1, {"goals_scored": 5, "assists": 3})
team_sync.track_performance(2, {"goals_scored": 2, "assists": 1})

# Print player performance data
print("Player Performance Data:")
for player_id, performance_data in team_sync.performance_data.items():
    print(f"Player {player_id}: {performance_data}")