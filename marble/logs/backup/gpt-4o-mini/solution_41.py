# solution.py

# Import necessary libraries
import random
from collections import defaultdict
from typing import List, Dict, Any

# User class to manage user information and preferences
class User:
    def __init__(self, username: str, interests: List[str]):
        self.username = username  # Unique username for the user
        self.interests = interests  # List of interests for personalized news feed
        self.saved_articles = []  # List to store saved articles
        self.feedback = defaultdict(list)  # Store user feedback on articles

# Article class to represent news articles
class Article:
    def __init__(self, title: str, content: str, category: str):
        self.title = title  # Title of the article
        self.content = content  # Content of the article
        self.category = category  # Category of the article (e.g., politics, technology)

    def summarize(self) -> str:
        # Simple summarization by taking the first 30 characters
        return self.content[:30] + '...' if len(self.content) > 30 else self.content

# NewsCollaborator class to manage the news aggregation and user interactions
class NewsCollaborator:
    def __init__(self):
        self.users = {}  # Dictionary to store users by username
        self.articles = []  # List to store articles
        self.article_views = defaultdict(int)  # Track views for articles

    def register_user(self, username: str, interests: List[str]) -> User:
        # Register a new user
        if username in self.users:
            raise ValueError("Username already exists.")
        user = User(username, interests)
        self.users[username] = user
        return user

    def add_article(self, title: str, content: str, category: str):
        # Add a new article to the platform
        article = Article(title, content, category)
        self.articles.append(article)

    def get_personalized_feed(self, username: str) -> List[Dict[str, Any]]:
        # Generate a personalized news feed based on user interests
        user = self.users.get(username)
        if not user:
            raise ValueError("User not found.")        # Track article scores based on user interactions
        article_scores = defaultdict(int)
        for article in self.articles:
            if article.category in user.interests:
                article_scores[article.title] += self.article_views[article.title]  # Increase score by views
                if article.title in user.saved_articles:
                    article_scores[article.title] += 10  # Boost score for saved articles

        # Sort articles by score and get top recommendations
        sorted_articles = sorted(article_scores.items(), key=lambda x: x[1], reverse=True)
        personalized_articles = [        personalized_articles = [
            {
                'title': title,
                'summary': next(article.summarize() for article in self.articles if article.title == title),
                'category': next(article.category for article in self.articles if article.title == title)
            }
            for title, score in sorted_articles if score > 0
        ]        return personalized_articles        # Filter articles based on user interests
        personalized_articles = [
            {
                'title': article.title,
                'summary': article.summarize(),
                'category': article.category
            }
            for article in self.articles if article.category in user.interests
        ]
        return personalized_articles

    def share_article(self, username: str, article_title: str):
        # Allow users to share articles
        user = self.users.get(username)
        if not user:
            raise ValueError("User not found.")
        
        # Simulate sharing by increasing the view count
        for article in self.articles:
            if article.title == article_title:
                self.article_views[article_title] += 1
                return f"{username} shared the article: {article_title}"
        return "Article not found."

    def provide_feedback(self, username: str, article_title: str, rating: int):
        # Allow users to provide feedback on articles
        user = self.users.get(username)
        if not user:
            raise ValueError("User not found.")
        
        user.feedback[article_title].append(rating)

    def analyze_article_sentiment(self, article_title: str) -> str:
        # Dummy sentiment analysis based on random choice
        sentiments = ['Positive', 'Neutral', 'Negative']
        return random.choice(sentiments)

    def get_article_trends(self) -> Dict[str, int]:
        # Get popularity trends based on article views
        return dict(self.article_views)

# Example usage of the NewsCollaborator system
if __name__ == "__main__":
    # Create an instance of NewsCollaborator
    news_collaborator = NewsCollaborator()

    # Register users
    user1 = news_collaborator.register_user("alice", ["technology", "health"])
    user2 = news_collaborator.register_user("bob", ["politics", "technology"])

    # Add articles
    news_collaborator.add_article("Tech Innovations", "New tech innovations are emerging...", "technology")
    news_collaborator.add_article("Health Tips", "Here are some health tips...", "health")
    news_collaborator.add_article("Political Debate", "The political debate was intense...", "politics")

    # Get personalized feeds
    print(news_collaborator.get_personalized_feed("alice"))
    print(news_collaborator.get_personalized_feed("bob"))

    # Share an article
    print(news_collaborator.share_article("alice", "Tech Innovations"))

    # Provide feedback
    news_collaborator.provide_feedback("bob", "Political Debate", 5)

    # Analyze article sentiment
    print(news_collaborator.analyze_article_sentiment("Health Tips"))

    # Get article trends
    print(news_collaborator.get_article_trends())