# solution.py
from datetime import datetime

class User:
    """Represents a user in the HealthTeamSync application."""
    def __init__(self, name, email):
        # Initialize user attributes
        self.name = name
        self.email = email
        self.teams = []  # List of teams the user is a part of
        self.goals = []  # List of personal goals
        self.challenges = []  # List of personal challenges
        self.activity_log = []  # List of daily activities

    def join_team(self, team):
        # Add the user to a team
        self.teams.append(team)

    def set_goal(self, goal):
        # Set a personal goal
        self.goals.append(goal)

    def create_challenge(self, challenge):
        # Create a personal challenge
        self.challenges.append(challenge)

    def log_activity(self, activity):
        # Log a daily activity
        self.activity_log.append(activity)


class Team:
    """Represents a team in the HealthTeamSync application."""
    def __init__(self, name, description):
        # Initialize team attributes
        self.name = name
        self.description = description
        self.members = []  # List of team members
        self.goals = []  # List of team goals
self.team_messages = []  # List of team messages
        self.challenges = []  # List of team challenges

    def add_member(self, user):
        # Add a user to the team
        self.members.append(user)

    def set_goal(self, goal):
        # Set a team goal
        self.goals.append(goal)

    def create_challenge(self, challenge):
        # Create a team challenge
        self.challenges.append(challenge)


class Goal:
    """Represents a goal in the HealthTeamSync application."""
    def __init__(self, title, target_value, deadline):
        # Initialize goal attributes
        self.title = title
        self.target_value = target_value
        self.deadline = deadline

    def __str__(self):
        # Return a string representation of the goal
        return f"{self.title}: {self.target_value} by {self.deadline}"


class Challenge:
    """Represents a challenge in the HealthTeamSync application."""
    def __init__(self, title, description, start_date, end_date, activities):
        # Initialize challenge attributes
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.activities = activities

    def __str__(self):
        # Return a string representation of the challenge
        return f"{self.title}: {self.description} from {self.start_date} to {self.end_date}"


class Activity:
    """Represents an activity in the HealthTeamSync application."""
    def __init__(self, date, metric, value):
        # Initialize activity attributes
        self.date = date
        self.metric = metric
        self.value = value

    def __str__(self):
        # Return a string representation of the activity
        return f"{self.date}: {self.metric} = {self.value}"


class Message:
    """Represents a message in the HealthTeamSync application."""
    def __init__(self, sender, content):
        # Initialize message attributes
        self.sender = sender
        self.content = content

    def __str__(self):
        # Return a string representation of the message
        return f"{self.sender}: {self.content}"


class HealthTeamSync:def send_message(self, sender, content, team):
    message = Message(sender, content)
    team.team_messages.append(message)def test_generate_notification():
    app = HealthTeamSync()
    user = app.create_user("John Doe", "john@example.com")
    app.generate_notification(user, "You have a new message!")
    # No assertion, just checking if the notification is printed

def test_display_dashboard():
    app = HealthTeamSync()
    team = app.create_team("Fitness Team", "A team for fitness enthusiasts")
    user = app.create_user("John Doe", "john@example.com")
    team.add_member(user)
    goal = Goal("Weight Loss", 10, datetime(2024, 12, 31))
    team.set_goal(goal)
    challenge = Challenge("Running Challenge", "Run 5 miles every day", datetime(2024, 1, 1), datetime(2024, 1, 31), ["Running"])
    team.create_challenge(challenge)
    activity = Activity(datetime(2024, 1, 1), "Distance", 5)
    user.log_activity(activity)
    app.display_dashboard(team)
    # No assertion, just checking if the dashboard is printed

# Run test cases
test_create_user()
test_create_team()
test_join_team()
test_set_goal()
test_create_challenge()
test_log_activity()
test_send_message()
test_generate_notification()
test_display_dashboard()