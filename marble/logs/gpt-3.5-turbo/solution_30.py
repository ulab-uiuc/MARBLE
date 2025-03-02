class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.teams = []
        self.personal_goals = []
        self.team_goals = []
        self.activities = []
        self.messages = []

    def create_team(self, team_name, description):
        team = Team(team_name, description)
        self.teams.append(team)
        return team

    def join_team(self, team):
        self.teams.append(team)

    def set_personal_goal(self, goal_name, target_value, deadline):
        goal = Goal(goal_name, target_value, deadline)
        self.personal_goals.append(goal)

    def set_team_goal(self, team, goal_name, target_value, deadline):
        goal = Goal(goal_name, target_value, deadline)
        team.goals.append(goal)
        self.team_goals.append(goal)

    def log_activity(self, activity_name, metric, value):def send_message(self, goal_name, value, team, message):        for goal in self.personal_goals:
            if goal.name == goal_name:
                goal.progress = value

        for team in self.teams:
            for team_goal in team.goals:
                if team_goal.name == goal_name:
                    team_goal.progress = value
        team.messages.append(f"{self.name}: {message}")


class Team:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.members = []
        self.goals = []
        self.activities = []
        self.messages = []

    def add_member(self, user):
        self.members.append(user)

    def log_activity(self, activity_name, metric, value):
        activity = Activity(activity_name, metric, value)
        self.activities.append(activity)

    def send_message(self, user, message):
        self.messages.append(f"{user.name}: {message}")


class Goal:
    def __init__(self, name, target_value, deadline):
        self.name = name
        self.target_value = target_value
        self.deadline = deadline


class Activity:
    def __init__(self, name, metric, value):
        self.name = name
        self.metric = metric
        self.value = value


# Test cases
# Creating users
user1 = User("Alice", "alice@example.com")
user2 = User("Bob", "bob@example.com")

# Creating teams
team1 = user1.create_team("Fitness Team", "Team for fitness enthusiasts")
user2.join_team(team1)

# Setting goals
user1.set_personal_goal("Weight Loss", 5, "2023-01-01")
user1.set_team_goal(team1, "Muscle Gain", 10, "2023-01-01")

# Logging activities
user1.log_activity("Ran 5 km", "distance", 5)
team1.log_activity("Weightlifting", "reps", 20)

# Sending messages
user1.send_message(team1, "Great workout today!")
team1.send_message(user2, "Let's crush our goals together!")

# Displaying team information
print(f"Team Name: {team1.name}")
print("Team Members:")
for member in team1.members:
    print(f"- {member.name}")
print("Team Goals:")
for goal in team1.goals:
    print(f"- {goal.name}: Target - {goal.target_value}, Deadline - {goal.deadline}")
print("Team Activities:")
for activity in team1.activities:
    print(f"- {activity.name}: {activity.value} {activity.metric}")
print("Team Messages:")
for message in team1.messages:
    print(message)