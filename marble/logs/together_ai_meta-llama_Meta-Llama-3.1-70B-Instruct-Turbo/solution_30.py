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
            member (User): The member to add.
        """
        self.members.append(member)

    def add_goal(self, goal):
        """
        Add a goal to the team.

        Args:
            goal (Goal): The goal to add.
        """
        self.goals.append(goal)

    def add_challenge(self, challenge):
        """
        Add a challenge to the team.

        Args:
            challenge (Challenge): The challenge to add.
        """
        self.challenges.append(challenge)


# user.py
class User:
    def __init__(self, name):
        """
        Initialize a User object.

        Args:
            name (str): The name of the user.
        """
        self.name = name
        self.goals = []
        self.challenges = []
        self.activities = []

    def add_goal(self, goal):
        """
        Add a goal to the user.

        Args:
            goal (Goal): The goal to add.
        """
        self.goals.append(goal)

    def add_challenge(self, challenge):
        """
        Add a challenge to the user.

        Args:
            challenge (Challenge): The challenge to add.
        """
        self.challenges.append(challenge)

    def log_activity(self, activity):
        """
        Log an activity for the user.

        Args:
            activity (Activity): The activity to log.
        """
        self.activities.append(activity)


# goal.py
class Goal:
    def __init__(self, target, deadline):
        """
        Initialize a Goal object.

        Args:
            target (float): The target value of the goal.
            deadline (str): The deadline for the goal.
        """
        self.target = target
        self.deadline = deadline

    def __str__(self):
        return f"Target: {self.target}, Deadline: {self.deadline}"


# challenge.py
class Challenge:
    def __init__(self, title, description, start_date, end_date, activities):
        """
        Initialize a Challenge object.

        Args:
            title (str): The title of the challenge.
            description (str): A brief description of the challenge.
            start_date (str): The start date of the challenge.
            end_date (str): The end date of the challenge.
            activities (list): A list of activities for the challenge.
        """
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.activities = activities

    def __str__(self):
        return f"Title: {self.title}, Description: {self.description}, Start Date: {self.start_date}, End Date: {self.end_date}, Activities: {self.activities}"


# activity.py
class Activity:
    def __init__(self, metric, value):
        """
        Initialize an Activity object.

        Args:
            metric (str): The metric of the activity (e.g. weight, distance, time, calories).
            value (float): The value of the activity.
        """
        self.metric = metric
        self.value = value

    def __str__(self):
        return f"Metric: {self.metric}, Value: {self.value}"


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

    def __str__(self):
        return f"Sender: {self.sender.name}, Content: {self.content}"


# health_team_sync.py
class HealthTeamSync:
    def __init__(self):
    def display_dashboard(self, team):
        # Calculate and display team progress
        total_activities = sum(len(member.activities) for member in team.members)
        print(f"Total activities logged: {total_activities}")

        # Calculate and display individual contributions
        for member in team.members:
            print(f"{member.name}'s contributions: {len(member.activities)} activities")

        # Calculate and display overall performance metrics
        total_progress = sum(goal.target for goal in team.goals)
        print(f"Total progress towards goals: {total_progress}")

        # Calculate and display team member rankings
        rankings = sorted(team.members, key=lambda member: len(member.activities), reverse=True)
        print("Team member rankings:")
        for i, member in enumerate(rankings):
            print(f"{i+1}. {member.name} - {len(member.activities)} activities")
        """
        Initialize a HealthTeamSync object.
        """
        self.teams = []
        self.users = []

    def create_team(self, name, description):
        """
        Create a new team.

        Args:
            name (str): The name of the team.
            description (str): A brief description of the team.

        Returns:
            Team: The newly created team.
        """
        team = Team(name, description)
        self.teams.append(team)
        return team

    def create_user(self, name):
        """
        Create a new user.

        Args:
            name (str): The name of the user.

        Returns:
            User: The newly created user.
        """
        user = User(name)
        self.users.append(user)
        return user

    def join_team(self, user, team):
        """
        Join a team.

        Args:
            user (User): The user to join the team.
            team (Team): The team to join.
        """
        team.add_member(user)

    def set_goal(self, user, target, deadline):
        """
        Set a goal for a user.

        Args:
            user (User): The user to set the goal for.
            target (float): The target value of the goal.
            deadline (str): The deadline for the goal.
        """
        goal = Goal(target, deadline)
        user.add_goal(goal)

    def set_challenge(self, team, title, description, start_date, end_date, activities):
        """
        Set a challenge for a team.

        Args:
            team (Team): The team to set the challenge for.
            title (str): The title of the challenge.
            description (str): A brief description of the challenge.
            start_date (str): The start date of the challenge.
            end_date (str): The end date of the challenge.
            activities (list): A list of activities for the challenge.
        """
        challenge = Challenge(title, description, start_date, end_date, activities)
        team.add_challenge(challenge)

    def log_activity(self, user, metric, value):
        """
        Log an activity for a user.

        Args:
            user (User): The user to log the activity for.
            metric (str): The metric of the activity (e.g. weight, distance, time, calories).
            value (float): The value of the activity.
        """
        activity = Activity(metric, value)
        user.log_activity(activity)

    def send_message(self, sender, content):
        """
        Send a message.

        Args:
            sender (User): The sender of the message.
            content (str): The content of the message.

        Returns:
            Message: The newly sent message.
        """
        message = Message(sender, content)
        return message


# test_health_team_sync.py
import unittest
from health_team_sync import HealthTeamSync, Team, User, Goal, Challenge, Activity, Message

class TestHealthTeamSync(unittest.TestCase):
    def test_create_team(self):
        health_team_sync = HealthTeamSync()
        team = health_team_sync.create_team("Team1", "This is team 1")
        self.assertEqual(team.name, "Team1")
        self.assertEqual(team.description, "This is team 1")

    def test_create_user(self):
        health_team_sync = HealthTeamSync()
        user = health_team_sync.create_user("User1")
        self.assertEqual(user.name, "User1")

    def test_join_team(self):
        health_team_sync = HealthTeamSync()
        team = health_team_sync.create_team("Team1", "This is team 1")
        user = health_team_sync.create_user("User1")
        health_team_sync.join_team(user, team)
        self.assertIn(user, team.members)

    def test_set_goal(self):
        health_team_sync = HealthTeamSync()
        user = health_team_sync.create_user("User1")
        health_team_sync.set_goal(user, 10.0, "2024-01-01")
        self.assertEqual(user.goals[0].target, 10.0)
        self.assertEqual(user.goals[0].deadline, "2024-01-01")

    def test_set_challenge(self):
        health_team_sync = HealthTeamSync()
        team = health_team_sync.create_team("Team1", "This is team 1")
        health_team_sync.set_challenge(team, "Challenge1", "This is challenge 1", "2024-01-01", "2024-01-31", ["Activity1", "Activity2"])
        self.assertEqual(team.challenges[0].title, "Challenge1")
        self.assertEqual(team.challenges[0].description, "This is challenge 1")
        self.assertEqual(team.challenges[0].start_date, "2024-01-01")
        self.assertEqual(team.challenges[0].end_date, "2024-01-31")
        self.assertEqual(team.challenges[0].activities, ["Activity1", "Activity2"])

    def test_log_activity(self):
        health_team_sync = HealthTeamSync()
        user = health_team_sync.create_user("User1")
        health_team_sync.log_activity(user, "weight", 70.0)
        self.assertEqual(user.activities[0].metric, "weight")
        self.assertEqual(user.activities[0].value, 70.0)

    def test_send_message(self):
        health_team_sync = HealthTeamSync()
        user = health_team_sync.create_user("User1")
        message = health_team_sync.send_message(user, "Hello, team!")
        self.assertEqual(message.sender.name, "User1")
        self.assertEqual(message.content, "Hello, team!")

if __name__ == "__main__":
    unittest.main()