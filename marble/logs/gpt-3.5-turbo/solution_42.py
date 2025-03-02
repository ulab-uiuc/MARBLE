# NewsCollab - Collaborative News Application

# Import necessary libraries
import datetime
import uuid

# Define classes for the NewsCollab application

class User:
    def __init__(self, username, email, role):
        self.username = username
        self.email = email
        self.role = role

class Article:
    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author
        self.created_at = datetime.datetime.now()
        self.article_id = uuid.uuid4()

class Comment:self.versions = []self.versions = []
    def __init__(self, user, text):
        self.user = user
        self.text = text
        self.created_at = datetime.datetime.now()

class Notification:
    def __init__(self, message, user):
        self.message = message
        self.user = user
        self.created_at = datetime.datetime.now()

# Define the backend functionality for NewsCollab

class NewsCollabBackend:
    def __init__(self):
        self.users = []
        self.articles = []
        self.comments = []
        self.notifications = []

    def create_user(self, username, email, role):
        new_user = User(username, email, role)
        self.users.append(new_user)
        return new_user

    def create_article(self, title, content, author):
        new_article = Article(title, content, author)
        self.articles.append(new_article)
        return new_article

    def create_comment(self, user, text):
        new_comment = Comment(user, text)
        self.comments.append(new_comment)
        return new_comment

    def create_notification(self, message, user):
        new_notification = Notification(message, user)
        self.notifications.append(new_notification)
        return new_notification

# Sample code to demonstrate the usage of NewsCollab

# Initialize the NewsCollab backend
news_collab_backend = NewsCollabBackend()

# Create users
user1 = news_collab_backend.create_user("journalist1", "journalist1@example.com", "journalist")
user2 = news_collab_backend.create_user("editor1", "editor1@example.com", "editor")

# Create an article
article1 = news_collab_backend.create_article("Breaking News", "This is a breaking news article.", user1)

# Add a comment
comment1 = news_collab_backend.create_comment(user2, "Great article!")

# Create a notification
notification1 = news_collab_backend.create_notification("New comment on your article.", user1)

# Print sample data
print("Users:")
for user in news_collab_backend.users:
    print(user.username, user.email, user.role)

print("\nArticles:")
for article in news_collab_backend.articles:
    print(article.title, article.content, article.author.username)

print("\nComments:")
for comment in news_collab_backend.comments:
    print(comment.user.username, comment.text)

print("\nNotifications:")
for notification in news_collab_backend.notifications:
    print(notification.message, notification.user.username)