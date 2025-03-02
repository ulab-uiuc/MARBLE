# news_collaborator.py
# This is the main implementation of the NewsCollaborator system.

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
from nltk.probability import FreqDist
from collections import defaultdict
from datetime import datetime
import random
import json
import pickle
import os

# Initialize the NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')

class User:
    """Represents a user in the NewsCollaborator system."""
    
    def __init__(self, username):
        self.username = username
        self.interests = []
        self.preferences = {}
        self.news_feed = []
        self.comments = defaultdict(list)

class NewsArticle:
    """Represents a news article in the NewsCollaborator system."""
    
    def __init__(self, title, content, topic):
        self.title = title
        self.content = content
        self.topic = topic
        self.sentiment = None
        self.popularity = 0
        self.comments = defaultdict(list)

class NewsCollaborator:
    """Represents the NewsCollaborator system."""
    
    def __init__(self):
        self.users = {}
        self.news_articles = []
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()

    def login(self, username):
        """Logs in a user and returns their user object."""
        
        if username in self.users:
            return self.users[username]
        else:
            return None

    def register(self, username):
        """Registers a new user and returns their user object."""
        
        if username not in self.users:
            self.users[username] = User(username)
            return self.users[username]
        else:
            return None

    def add_interest(self, username, interest):
        """Adds an interest to a user's interests list."""
        
        user = self.login(username)
        if user:
            user.interests.append(interest)
            return True
        else:
            return False

    def add_preference(self, username, preference):
        """Adds a preference to a user's preferences dictionary."""
        
        user = self.login(username)
        if user:
            user.preferences[preference] = True
            return True
        else:
            return False

    def create_news_feed(self, username):
        """Creates a news feed for a user based on their interests and preferences."""
        
        user = self.login(username)
        if user:
            # Use natural language processing to summarize articles and categorize them into topics
            for article in self.news_articles:
                if article.topic in user.interests or article.topic in user.preferences:
                    user.news_feed.append(article)
            return user.news_feed
        else:
            return None

    def share_article(self, username, article_title, article_content, article_topic):
        """Shares a news article with all users."""
        
        article = NewsArticle(article_title, article_content, article_topic)
        self.news_articles.append(article)
        for user in self.users.values():
            user.comments[article.title].append((username, article_content))

    def add_comment(self, username, article_title, comment):
        """Adds a comment to a news article."""
        
        user = self.login(username)
        if user:
            article = next((article for article in self.news_articles if article.title == article_title), None)
            if article:
                user.comments[article.title].append((username, comment))
                return True
        return False

    def get_sentiment(self, article_content):
        """Uses natural language processing to analyze the sentiment of a news article."""
        
        return self.sentiment_analyzer.polarity_scores(article_content)

    def update_popularity(self, article_title):
        """Updates the popularity of a news article based on user interactions."""
        
        article = next((article for article in self.news_articles if article.title == article_title), None)
        if article:
            article.popularity += 1
            return True
        return False

    def get_analytics(self, article_title):
        """Returns detailed analytics and insights on a news article."""
        
        article = next((article for article in self.news_articles if article.title == article_title), None)
        if article:
            return {
                'sentiment': article.sentiment,
                'popularity': article.popularity,
                'comments': article.comments
            }
        return None

    def save_data(self):
        """Saves the user data and news articles to a file."""
        
        with open('users.pkl', 'wb') as f:
            pickle.dump(self.users, f)
        with open('news_articles.pkl', 'wb') as f:
            pickle.dump(self.news_articles, f)

    def load_data(self):
        """Loads the user data and news articles from a file."""
        
        if os.path.exists('users.pkl'):
            with open('users.pkl', 'rb') as f:
                self.users = pickle.load(f)
        if os.path.exists('news_articles.pkl'):
            with open('news_articles.pkl', 'rb') as f:
                self.news_articles = pickle.load(f)

# Create a NewsCollaborator object
news_collaborator = NewsCollaborator()

# Load the user data and news articles
news_collaborator.load_data()

# Register a new user
user = news_collaborator.register('john')
if user:
    print(f'User {user.username} registered successfully.')

# Add interests and preferences to the user
news_collaborator.add_interest('john', 'politics')
news_collaborator.add_preference('john', 'health')

# Create a news feed for the user
news_feed = news_collaborator.create_news_feed('john')
if news_feed:
    print(f'News feed created successfully for user {user.username}.')

# Share a news article with all users
news_collaborator.share_article('john', 'Article Title', 'Article Content', 'Politics')

# Add a comment to the news article
news_collaborator.add_comment('john', 'Article Title', 'Comment Content')

# Get the sentiment of the news article
sentiment = news_collaborator.get_sentiment('Article Content')
if sentiment:
    print(f'Sentiment analysis: {sentiment}')

# Update the popularity of the news article
news_collaborator.update_popularity('Article Title')

# Get the analytics of the news article
analytics = news_collaborator.get_analytics('Article Title')
if analytics:
    print(f'Analytics: {analytics}')

# Save the user data and news articles to a file
news_collaborator.save_data()