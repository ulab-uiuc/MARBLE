# solution.py

# Import necessary libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
import logging

# Initialize the Flask application
app = Flask(__name__)


# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news_collab.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a random secret key
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Database models
class User(db.Model):
    """Model for storing user information."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    articles = db.relationship('Article', backref='author', lazy=True)

class Article(db.Model):
    """Model for storing news articles."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# User registration endpoint
@app.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    username = request.json.get('username')
    password = request.json.get('password')
    if User.query.filter_by(username=username).first():from werkzeug.security import generate_password_hash
new_user = User(username=username, password=generate_password_hash(password))    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User registered successfully"}), 201

# User login endpoint
@app.route('/login', methods=['POST'])
def login():
    """Authenticate a user and return a JWT token."""
    username = request.json.get('username')
    password = request.json.get('password')user = User.query.filter_by(username=username).first()
if user and check_password_hash(user.password, password):        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401

# Create a new article
@app.route('/articles', methods=['POST'])
@jwt_required()
def create_article():
    """Create a new article."""
    current_user_id = get_jwt_identity()
    title = request.json.get('title')
    content = request.json.get('content')
    new_article = Article(title=title, content=content, author_id=current_user_id)
    db.session.add(new_article)
    db.session.commit()
    return jsonify({"msg": "Article created", "article_id": new_article.id}), 201

# Get all articles
@app.route('/articles', methods=['GET'])
def get_articles():
    """Retrieve all articles."""
    articles = Article.query.all()
    return jsonify([{"id": article.id, "title": article.title, "content": article.content} for article in articles]), 200

# Update an article
@app.route('/articles/<int:article_id>', methods=['PUT'])
@jwt_required()
def update_article(article_id):
    """Update an existing article."""
    current_user_id = get_jwt_identity()
    article = Article.query.get_or_404(article_id)
    if article.author_id != current_user_id:
        return jsonify({"msg": "Unauthorized"}), 403
    title = request.json.get('title')
    content = request.json.get('content')
    article.title = title
    article.content = content
    db.session.commit()
    return jsonify({"msg": "Article updated"}), 200

# Delete an article
@app.route('/articles/<int:article_id>', methods=['DELETE'])
@jwt_required()
def delete_article(article_id):
    """Delete an article."""
    current_user_id = get_jwt_identity()
    article = Article.query.get_or_404(article_id)
    if article.author_id != current_user_id:
        return jsonify({"msg": "Unauthorized"}), 403
    db.session.delete(article)
    db.session.commit()
    return jsonify({"msg": "Article deleted"}), 200

# Run the application
if __name__ == '__main__':
    db.create_all()  # Create database tables
    app.run(debug=True)  # Run the Flask application