# solution.py

class User:
    """Class representing a user in the HealthTeamSync application."""
    
    def __init__(self, username):
        self.username = username
        self.teams = []  # List of teams the user has joined
        self.goals = []  # List of personal goals
        self.activities = []  # List of logged activities
        self.messages = []  # List of messages sent by the user

    def join_team(self, team):
        """Allows the user to join a team."""
        self.teams.append(team)
        team.add_member(self)

    def set_goal(self, goal):
        """Allows the user to set a personal health and fitness goal."""
        self.goals.append(goal)

    def log_activity(self, activity):
        """Logs a daily activity for the user."""
        self.activities.append(activity)

    def send_message(self, message):
        """Sends a message to the team."""
        self.messages.append(message)


class Team:
    """Class representing a team in the HealthTeamSync application."""
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.members = []  # List of users in the team
        self.goals = []  # List of team goals
        self.challenges = []  # List of team challenges

    def add_member(self, user):
        """Adds a user to the team."""
        self.members.append(user)

    def set_team_goal(self, goal):
        """Sets a team health and fitness goal."""
        self.goals.append(goal)

    def create_challenge(self, challenge):
        """Creates a new challenge for the team."""
        self.challenges.append(challenge)


class Goal:
    """Class representing a health and fitness goal."""
    
    def __init__(self, title, target_value, deadline):
        self.title = title
        self.target_value = target_value
        self.deadline = deadline


class Challenge:
    """Class representing a challenge in the HealthTeamSync application."""
    
    def __init__(self, title, description, start_date, end_date, activities):
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.activities = activities


class Activity:
    """Class representing a logged activity."""
    
    def __init__(self, date, metric_type, value):
        self.date = date
        self.metric_type = metric_type  # e.g., 'weight', 'distance', 'time', 'calories'
        self.value = value


class HealthTeamSync:
    """Main application class for managing users, teams, goals, and activities."""
    
    def __init__(self):
        self.users = []  # List of all users
        self.teams = []  # List of all teams

    def add_user(self, username):
        """Adds a new user to the application."""
        user = User(username)
        self.users.append(user)
        return user

    def create_team(self, name, description):
        """Creates a new team."""
        team = Team(name, description)
        self.teams.append(team)
        return team

    def get_team_dashboard(self, team):
        """Generates a dashboard for the specified team."""
        dashboard = {
            'team_name': team.name,
            'members': [member.username for member in team.members],
            'goals': [goal.title for goal in team.goals],
            'challenges': [challenge.title for challenge in team.challenges],
        }
        return dashboard


# Example usage
if __name__ == "__main__":
    app = HealthTeamSync()
    
    # Create users
    user1 = app.add_user("Alice")
    user2 = app.add_user("Bob")
    
    # Create a team
    team = app.create_team("Fitness Warriors", "A team dedicated to fitness and health.")
    
    # Users join the team
    user1.join_team(team)
    user2.join_team(team)
    
    # Set personal goals
    user1.set_goal(Goal("Lose 5kg", 5, "2023-12-31"))
    user2.set_goal(Goal("Run a marathon", 42, "2024-05-01"))
    
    # Create a team goal
    team.set_team_goal(Goal("Collectively lose 20kg", 20, "2023-12-31"))
    
    # Create a challenge
    challenge = Challenge("30-Day Fitness Challenge", "Complete a workout every day for 30 days.", "2023-11-01", "2023-11-30", ["Running", "Yoga", "Strength Training"])
    team.create_challenge(challenge)
    
    # Log activities
    user1.log_activity(Activity("2023-10-01", "weight", 70))
    user2.log_activity(Activity("2023-10-01", "distance", 5))
    
    # Get team dashboard
    dashboard = app.get_team_dashboard(team)
    print(dashboard)