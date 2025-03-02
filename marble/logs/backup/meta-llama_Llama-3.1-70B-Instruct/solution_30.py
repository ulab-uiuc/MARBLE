# team.py
class Team:
    def __init__(self, name, description):
        """
        Initialize a Team object.

        Args:
            name (str): The name of the team.
            description (str): A brief description of the team.
        """
        self.name = name
        self.description = description
        self.members = []
        self.goals = []
        self.challenges = []

    def add_member(self, member):
        """
        Add a member to the team.

        Args:
            member (User): The member to be added.
        """
        self.members.append(member)

    def remove_member(self, member):
        """
        Remove a member from the team.

        Args:
            member (User): The member to be removed.
        """
        self.members.remove(member)

    def add_goal(self, goal):
        """
        Add a goal to the team.

        Args:
            goal (Goal): The goal to be added.
        """
        self.goals.append(goal)

    def remove_goal(self, goal):
        """
        Remove a goal from the team.

        Args:
            goal (Goal): The goal to be removed.
        """
        self.goals.remove(goal)

    def add_challenge(self, challenge):
        """
        Add a challenge to the team.

        Args:
            challenge (Challenge): The challenge to be added.
        """
        self.challenges.append(challenge)

    def remove_challenge(self, challenge):
        """
        Remove a challenge from the team.

        Args:
            challenge (Challenge): The challenge to be removed.
        """
        self.challenges.remove(challenge)


# user.py
class User:
    def __init__(self, name, email):
        """
        Initialize a User object.

        Args:
            name (str): The name of the user.
            email (str): The email address of the user.
        """
        self.name = name
        self.email = email
        self.teams = []
        self.goals = []
        self.challenges = []
        self.activities = []

    def join_team(self, team):
        """
        Join a team.

        Args:
            team (Team): The team to be joined.
        """
        self.teams.append(team)
        team.add_member(self)

    def leave_team(self, team):
        """
        Leave a team.

        Args:
            team (Team): The team to be left.
        """
        self.teams.remove(team)
        team.remove_member(self)

    def add_goal(self, goal):
        """
        Add a personal goal.

        Args:
            goal (Goal): The goal to be added.
        """
        self.goals.append(goal)

    def remove_goal(self, goal):
        """
        Remove a personal goal.

        Args:
            goal (Goal): The goal to be removed.
        """
        self.goals.remove(goal)

    def add_challenge(self, challenge):
        """
        Add a personal challenge.

        Args:
            challenge (Challenge): The challenge to be added.
        """
        self.challenges.append(challenge)

    def remove_challenge(self, challenge):
        """
        Remove a personal challenge.

        Args:
            challenge (Challenge): The challenge to be removed.
        """
        self.challenges.remove(challenge)

    def log_activity(self, activity):
        """
        Log a daily activity.

        Args:
            activity (Activity): The activity to be logged.
        """
        self.activities.append(activity)


# goal.py
class Goal:
    def __init__(self, target, deadline):
        """
        Initialize a Goal object.

        Args:
            target (float): The target value of the goal.
            deadline (str): The deadline of the goal.
        """
        self.target = target
        self.deadline = deadline

    def update_target(self, target):
        """
        Update the target value of the goal.

        Args:
            target (float): The new target value.
        """
        self.target = target

    def update_deadline(self, deadline):
        """
        Update the deadline of the goal.

        Args:
            deadline (str): The new deadline.
        """
        self.deadline = deadline


# challenge.py
class Challenge:
    def __init__(self, title, description, start_date, end_date):
        """
        Initialize a Challenge object.

        Args:
            title (str): The title of the challenge.
            description (str): A brief description of the challenge.
            start_date (str): The start date of the challenge.
            end_date (str): The end date of the challenge.
        """
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.activities = []

    def add_activity(self, activity):
        """
        Add an activity to the challenge.

        Args:
            activity (Activity): The activity to be added.
        """
        self.activities.append(activity)

    def remove_activity(self, activity):
        """
        Remove an activity from the challenge.

        Args:
            activity (Activity): The activity to be removed.
        """
        self.activities.remove(activity)


# activity.py
class Activity:
    def __init__(self, name, metric, value):
        """
        Initialize an Activity object.

        Args:
            name (str): The name of the activity.
            metric (str): The metric of the activity (e.g., weight, distance, time, calories).
            value (float): The value of the activity.
        """
        self.name = name
        self.metric = metric
        self.value = value


# message.py
class Message:
    def __init__(self, sender, content):
        """
        Initialize a Message object.

        Args:
            sender (User): The sender of the message.
            content (str): The content of the message.
        """
        self.sender = sender
        self.content = content


# notification.py
class Notification:
    def __init__(self, recipient, content):
        """
        Initialize a Notification object.

        Args:
            recipient (User): The recipient of the notification.
            content (str): The content of the notification.
        """
        self.recipient = recipient
        self.content = content


# dashboard.py
class Dashboard:
    def __init__(self, team):
        """
        Initialize a Dashboard object.

        Args:
            team (Team): The team associated with the dashboard.
        """
        self.team = team

    def display_progress(self):
        """
        Display the team's progress.
        """
        print("Team Progress:")
        for member in self.team.members:
            print(f"{member.name}: {member.activities}")

    def display_contributions(self):
        """
        Display the individual contributions of team members.
        """
        print("Individual Contributions:")
        for member in self.team.members:
            print(f"{member.name}: {member.activities}")

    def display_performance_metrics(self):
        """
        Display the team's performance metrics.
        """
        print("Performance Metrics:")
        for goal in self.team.goals:
            print(f"Goal: {goal.target}, Deadline: {goal.deadline}")


# health_team_sync.py
class HealthTeamSync:
    def __init__(self):
        """
        Initialize a HealthTeamSync object.
        """
        self.teams = []
        self.users = []

    def create_team(self, name, description):
        if name in [team.name for team in self.teams]:
            raise ValueError("Team with the same name already exists")
        team = Team(name, description)
        self.teams.append(team)
        return team
    def join_team(self, user, team):
        """
        Join a team.

        Args:
            user (User): The user joining the team.
            team (Team): The team to be joined.
        """
        user.join_team(team)

    def leave_team(self, user, team):
        """
        Leave a team.

        Args:
            user (User): The user leaving the team.
            team (Team): The team to be left.
        """
        user.leave_team(team)

    def set_goal(self, user, goal):
        """
        Set a personal goal.

        Args:
            user (User): The user setting the goal.
            goal (Goal): The goal to be set.
        """
        user.add_goal(goal)

    def log_activity(self, user, activity):
        """
        Log a daily activity.

        Args:
            user (User): The user logging the activity.
            activity (Activity): The activity to be logged.
        """if activity.value <= 0:
            raise ValueError("Activity value must be greater than zero")
        if not isinstance(activity.metric, str):
            raise ValueError("Activity metric must be a string")
        user.log_activity(activity)user.log_activity(activity)
if activity.value <= 0:
            raise ValueError("Activity value must be greater than zero")
        if not isinstance(activity.metric, str):
            raise ValueError("Activity metric must be a string")

    def send_message(self, sender, content, recipient):
        """
        Send a message to a team member.

        Args:
            sender (User): The sender of the message.
            content (str): The content of the message.
            recipient (User): The recipient of the message.
        """
        message = Message(sender, content)
        print(f"{sender.name} sent a message to {recipient.name}: {message.content}")

    def generate_notification(self, recipient, content):
        """
        Generate a notification for a team member.

        Args:
            recipient (User): The recipient of the notification.
            content (str): The content of the notification.
        """
        notification = Notification(recipient, content)
if not isinstance(content, str):
            raise ValueError("Notification content must be a string")
        print(f"Notification sent to {recipient.name}: {notification.content}")


# test_health_team_sync.py
import unittest
from health_team_sync import HealthTeamSync, Team, User, Goal, Activity, Message, Notification

class TestHealthTeamSync(unittest.TestCase):
    def test_create_team(self):
        health_team_sync = HealthTeamSync()
        team = health_team_sync.create_team("Team1", "This is team 1")
        self.assertEqual(team.name, "Team1")
        self.assertEqual(team.description, "This is team 1")

    def test_join_team(self):
        health_team_sync = HealthTeamSync()
        team = health_team_sync.create_team("Team1", "This is team 1")
        user = User("John Doe", "john@example.com")
        health_team_sync.join_team(user, team)
        self.assertIn(user, team.members)

    def test_leave_team(self):
        health_team_sync = HealthTeamSync()
        team = health_team_sync.create_team("Team1", "This is team 1")
        user = User("John Doe", "john@example.com")
        health_team_sync.join_team(user, team)
        health_team_sync.leave_team(user, team)
        self.assertNotIn(user, team.members)

    def test_set_goal(self):
        health_team_sync = HealthTeamSync()
        user = User("John Doe", "john@example.com")
        goal = Goal(10.0, "2024-07-26")
        health_team_sync.set_goal(user, goal)
        self.assertIn(goal, user.goals)

    def test_log_activity(self):
        health_team_sync = HealthTeamSync()
        user = User("John Doe", "john@example.com")
        activity = Activity("Running", "distance", 5.0)
        health_team_sync.log_activity(user, activity)
        self.assertIn(activity, user.activities)

    def test_send_message(self):
        health_team_sync = HealthTeamSync()
        sender = User("John Doe", "john@example.com")
        recipient = User("Jane Doe", "jane@example.com")
        content = "Hello, Jane!"
        health_team_sync.send_message(sender, content, recipient)

    def test_generate_notification(self):
        health_team_sync = HealthTeamSync()
        recipient = User("John Doe", "john@example.com")
        content = "You have a new message!"
        health_team_sync.generate_notification(recipient, content)

if __name__ == "__main__":
    unittest.main()