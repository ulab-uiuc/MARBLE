class Search:
    def __init__(self, users, projects, group_projects):
        self.users = users
        self.projects = projects
        self.group_projects = group_projects

    def search_group_projects(self, query):
        matching_group_projects = []
        for group_project in self.group_projects:
            if query.lower() in group_project.project_name.lower() or query.lower() in group_project.description.lower():
                matching_group_projects.append(group_project)
        return matching_group_projects

def search_group_projects(group_projects, query, limit=None, sort=None):
    search = Search([], [], group_projects)
    return search.search_group_projects(query)def search_group_projects(group_projects, query, limit=None, sort=None):    search = Search([], [], group_projects)
    return search.search_group_projects(query)


# Test cases
if __name__ == "__main__":
    # Create users
    user1 = create_user("user1", "bio1", "profile_picture1")
    user2 = create_user("user2", "bio2", "profile_picture2")

    # Create projects
    project1 = create_project(user1, "project1", "description1", ["tag1", "tag2"])
    project2 = create_project(user2, "project2", "description2", ["tag3", "tag4"])

    # Create group projects
    group_project1 = create_group_project(user1, "group_project1", "description1", ["tag1", "tag2"])
    group_project2 = create_group_project(user2, "group_project2", "description2", ["tag3", "tag4"])

    # Search users
    users = [user1, user2]
    query = "user1"
    matching_users = search_users(users, query)
    print("Matching users:", [user.username for user in matching_users])

    # Search projects
    projects = [project1, project2]
    query = "project1"
    matching_projects = search_projects(projects, query)
    print("Matching projects:", [project.project_name for project in matching_projects])

    # Search group projects
    group_projects = [group_project1, group_project2]
    query = "group_project1"
    matching_group_projects = search_group_projects(group_projects, query)
    print("Matching group projects:", [group_project.project_name for group_project in matching_group_projects])