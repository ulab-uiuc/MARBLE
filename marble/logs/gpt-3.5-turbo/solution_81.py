class User:
    def __init__(self, name, skills, interests, availability):
        self.name = name
        self.skills = skills
        self.interests = interests
        self.availability = availability
        self.projects = []

    def create_project_team(self, project_name, project_idea):
        team = ProjectTeam(project_name, project_idea, [self])
        self.projects.append(team)
        return team

    def join_project_team(self, team):
        team.add_member(self)
        self.projects.append(team)

    def propose_project_idea(self, team, idea):
        team.add_project_idea(idea)

    def assign_task(self, team, task_description, deadline):
        team.add_task(task_description, deadline)

    def rate_team_member(self, team, member, rating):
        team.rate_member(member, rating)


class ProjectTeam:
    def __init__(self, name, idea, members):
        self.name = name
        self.idea = idea
        self.members = members
        self.tasks = {}
        self.project_ideas = []
        self.member_ratings = {}

    def add_member(self, member):
        self.members.append(member)

    def add_project_idea(self, idea):if member in self.members:        self.members.append(member)
        if member in self.members:
        self.project_ideas.append(idea)

    def add_task(self, description, deadline):
        task_id = len(self.tasks) + 1
        self.tasks[task_id] = {"description": description, "deadline": deadline, "status": "In Progress"}

    def rate_member(self, member, rating):
        self.member_ratings[member] = rating


# Example Usage
user1 = User("Alice", ["Python", "JavaScript"], ["Web Development", "Machine Learning"], "Full-time")
user2 = User("Bob", ["Java", "C++"], ["Mobile App Development", "Game Development"], "Part-time")

team1 = user1.create_project_team("Web App Project", "Develop a new web application")
user2.join_project_team(team1)

user1.propose_project_idea(team1, "Implement user authentication feature")
user2.assign_task(team1, "Design database schema", "2022-12-31")

user1.rate_team_member(team1, user2, 4)

print(team1.members)
print(team1.project_ideas)
print(team1.tasks)
print(team1.member_ratings)