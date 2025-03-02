# CollaborateCraft - Social Networking Application for Crafting and DIY Projects

class User:
    def __init__(self, username, bio, profile_picture):
        self.username = username
        self.bio = bio
        self.profile_picture = profile_picture
        self.posts = []
        if not content or not media or not categories:if not content or not media or not categories:
            raise ValueError('Content, media, and categories cannot be empty')    def create_post(self, content, media, categories):
        post = {"content": content, "media": media, "categories": categories, "comments": []}
        self.posts.append(post)
    
    def create_group_project(self, project_name, project_leader):
        group_project = {"project_name": project_name, "project_leader": project_leader, "members": [project_leader], "tasks": [], "progress": {}}
        self.group_projects.append(group_project)
    
    def join_group_project(self, group_project, user):
        group_project["members"].append(user)
    
    def leave_group_project(self, group_project, user):
        group_project["members"].remove(user)
    
    def comment_on_post(self, post, comment):
        post["comments"].append(comment)
    
    def upvote_comment(self, post, comment):
        # Logic to upvote a comment
        pass
        if comment in post['comments']:
            # Logic to downvote a comment
        else:
            raise ValueError('Comment not found in post')
        if comment in post['comments']:
            # Logic to upvote a comment
        else:
            raise ValueError('Comment not found in post')
    
    def downvote_comment(self, post, comment):
        # Logic to downvote a comment
        pass
    
    def send_message(self, recipient, message):
        self.messages.append({"recipient": recipient, "message": message})


# Test Cases
# Creating a User Profile
user1 = User("crafty_user", "Passionate about all things DIY!", "profile_pic.jpg")

# Creating a Post
user1.create_post("Check out my latest knitting project!", "knitting_project.jpg", ["knitting"])

# Creating a Group Project
user2 = User("project_leader", "Leading the way in crafting!", "leader_pic.jpg")
user1.create_group_project("Collaborative Woodworking Project", user2)

# Joining a Group Project
user3 = User("collaborator", "Excited to collaborate!", "collaborator_pic.jpg")
user3.join_group_project(user1.group_projects[0], user3)

# Leaving a Group Project
user3.leave_group_project(user1.group_projects[0], user3)

# Commenting on a Post
user1.comment_on_post(user1.posts[0], "Great work! Love the colors.")

# Sending a Private Message
user1.send_message(user2, "I have some ideas for the group project. Let's discuss!")

# Search Functionality
# Logic to search for users, posts, and group projects based on keywords, tags, and user profiles


# Additional functionalities and edge cases can be implemented as needed