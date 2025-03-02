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


class Team:
    """Represents a team in the TeamSync system."""
    
    def __init__(self, id, name, coach):
        """
        Initializes a Team object.
        
        Args:
        id (int): Unique identifier for the team.
        name (str): Name of the team.
        coach (Coach): Coach of the team.
        """
        self.id = id
        self.name = name
        self.coach = coach
        self.players = []
        
    def add_player(self, player):
        """
        Adds a player to the team.
        
        Args:
        player (Player): Player to be added to the team.
        """
        self.players.append(player)


class Schedule:
    """Represents a schedule in the TeamSync system."""
    
    def __init__(self, id, team, event_type, date, time):
        """
        Initializes a Schedule object.
        
        Args:
        id (int): Unique identifier for the schedule.
        team (Team): Team associated with the schedule.
        event_type (str): Type of event (e.g., practice, match).
        date (str): Date of the event.
        time (str): Time of the event.
        """
        self.id = id
        self.team = team
        self.event_type = event_type
        self.date = date
        self.time = time


class PerformanceTracker:
    """Represents a performance tracker in the TeamSync system."""
    
    def __init__(self, id, player):
        """
        Initializes a PerformanceTracker object.
        
        Args:
        id (int): Unique identifier for the performance tracker.
        player (Player): Player associated with the performance tracker.
        """
        self.id = id
        self.player = player
        self.metrics = {}
        
    def add_metric(self, name, value):
        """
        Adds a performance metric to the tracker.
        
        Args:
        name (str): Name of the metric.
        value (float): Value of the metric.
        """
        self.metrics[name] = value


class TeamSync:def create_team(self, id, name, coach):def create_player(self, id, name, email, position):def create_coach(self, id, name, email):def create_schedule(self, id, team, event_type, date, time):def create_performance_tracker(self, id, player):
        if any(tracker.id == id for tracker in self.performance_trackers):
            raise ValueError(f"Performance tracker with ID {id} already exists")tracker = PerformanceTracker(id, player)
        self.performance_trackers.append(tracker)
        return tracker


# Example usage:

team_sync = TeamSync()

# Create a coach
coach = team_sync.create_coach(1, "John Doe", "john.doe@example.com")

# Create a team
team = team_sync.create_team(1, "Team A", coach)

# Create players
player1 = team_sync.create_player(1, "Jane Doe", "jane.doe@example.com", "Forward")
player2 = team_sync.create_player(2, "Bob Smith", "bob.smith@example.com", "Defender")

# Add players to the team
team.add_player(player1)
team.add_player(player2)

# Create a schedule
schedule = team_sync.create_schedule(1, team, "Practice", "2024-07-26", "10:00 AM")

# Create performance trackers
tracker1 = team_sync.create_performance_tracker(1, player1)
tracker2 = team_sync.create_performance_tracker(2, player2)

# Add performance metrics
tracker1.add_metric("Goals", 10)
tracker2.add_metric("Goals", 5)

print("Team:", team.name)
print("Coach:", team.coach.name)
print("Players:")
for player in team.players:
    print(player.name)
print("Schedule:")
print(schedule.event_type, "on", schedule.date, "at", schedule.time)
print("Performance Metrics:")
for tracker in team_sync.performance_trackers:
    print(tracker.player.name, ":", tracker.metrics)