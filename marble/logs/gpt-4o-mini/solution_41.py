# solution.py

# Import necessary libraries
import random
from collections import defaultdict
from typing import List, Dict, Any

# User class to manage user data and preferences
class User:
    def __init__(self, username: str):
        self.username = username
        self.preferences = []  # User's news preferences
        self.saved_articles = []  # Articles saved by the user
        self.interactions = defaultdict(int)  # Track user interactions with articles

    def set_preferences(self, preferences: List[str]):
        """Set user preferences for news categories."""
        self.preferences = preferences

    def save_article(self, article: 'Article'):
        """Save an article to the user's saved articles."""
        self.saved_articles.append(article)

    def interact_with_article(self, article: 'Article'):
        """Record interaction with an article."""
        self.interactions[article.title] += 1

# Article class to represent news articles
class Article:
    def __init__(self, title: str, content: str, category: str):
        self.title = title
        self.content = content
        self.category = category
        self.summary = self.summarize_article()
        self.sentiment = self.analyze_sentiment()

    def summarize_article(self) -> str:
        """Summarize the article content (mock implementation)."""
        return self.content[:50] + '...'  # Simple truncation for summary

    def analyze_sentiment(self) -> str:
        """Analyze sentiment of the article (mock implementation)."""
        return random.choice(['Positive', 'Neutral', 'Negative'])

# NewsCollaborator class to manage the news aggregation platform
class NewsCollaborator:
    def __init__(self):
        self.users = {}  # Dictionary to store users
        self.articles = []  # List to store articles
        self.article_feedback = defaultdict(list)  # Store feedback for articles

    def register_user(self, username: str) -> User:
        """Register a new user."""
        user = User(username)
        self.users[username] = user
        return user

    def add_article(self, title: str, content: str, category: str):
        """Add a new article to the platform."""
        article = Article(title, content, category)
        self.articles.append(article)def get_personalized_feed(self, user: User) -> List[Article]:
        """Get personalized news feed based on user preferences and interactions."""
        prioritized_articles = sorted(
            [article for article in self.articles if article.category in user.preferences],
            key=lambda article: user.interactions[article.title],
            reverse=True
        )
        return prioritized_articles    def provide_feedback(self, user: User, article: Article, feedback: str):
        """Allow users to provide feedback on articles."""
        self.article_feedback[article.title].append((user.username, feedback))

    def analyze_trends(self) -> Dict[str, Any]:
        """Analyze trends based on article interactions and feedback."""
        trends = defaultdict(int)
        for article_title, feedbacks in self.article_feedback.items():
            trends[article_title] = len(feedbacks)  # Count feedbacks as popularity
        return dict(trends)

# Example usage of the NewsCollaborator system
if __name__ == "__main__":
    # Create an instance of the NewsCollaborator
    news_collaborator = NewsCollaborator()

    # Register users
    user1 = news_collaborator.register_user("Alice")
    user2 = news_collaborator.register_user("Bob")

    # Set user preferences
    user1.set_preferences(["Technology", "Health"])
    user2.set_preferences(["Politics", "Technology"])

    # Add articles to the platform
    news_collaborator.add_article("Tech Innovations 2023", "This year has seen many tech innovations...", "Technology")
    news_collaborator.add_article("Health Tips for 2023", "Staying healthy is important...", "Health")
    news_collaborator.add_article("Political Landscape", "The political landscape is changing...", "Politics")

    # Get personalized feeds
    print("Alice's Feed:", news_collaborator.get_personalized_feed(user1))
    print("Bob's Feed:", news_collaborator.get_personalized_feed(user2))

    # User interactions
    user1.interact_with_article(news_collaborator.articles[0])  # Alice interacts with the first article
    user2.interact_with_article(news_collaborator.articles[2])  # Bob interacts with the third article

    # Provide feedback
    news_collaborator.provide_feedback(user1, news_collaborator.articles[0], "Very informative!")
    news_collaborator.provide_feedback(user2, news_collaborator.articles[2], "Needs more details.")

    # Analyze trends
    print("Article Trends:", news_collaborator.analyze_trends())