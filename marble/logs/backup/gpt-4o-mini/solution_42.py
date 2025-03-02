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
    """Endpoint for user registration."""
    data = request.get_json()data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"msg": "Missing fields"}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "Username already exists"}), 400
    new_user = User(username=data['username'], password=generate_password_hash(data['password']))
    db.session.add(new_user)    db.session.commit()
    return jsonify({"msg": "User registered successfully"}), 201

# User login endpoint
@app.route('/login', methods=['POST'])
def login():
    """Endpoint for user login."""
    data = request.get_json()user = User.query.filter_by(username=data['username']).first()
if user and check_password_hash(user.password, data['password']):        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401

# Create article endpoint
@app.route('/articles', methods=['POST'])
@jwt_required()
def create_article():
    """Endpoint for creating a new article."""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    new_article = Article(title=data['title'], content=data['content'], author_id=current_user_id)
    db.session.add(new_article)
    db.session.commit()
    return jsonify({"msg": "Article created successfully"}), 201

# Get all articles endpoint
@app.route('/articles', methods=['GET'])
def get_articles():
    """Endpoint for retrieving all articles."""
    articles = Article.query.all()
    return jsonify([{"id": article.id, "title": article.title, "content": article.content, "author_id": article.author_id} for article in articles]), 200

# Update article endpoint
@app.route('/articles/<int:article_id>', methods=['PUT'])
@jwt_required()
def update_article(article_id):
    """Endpoint for updating an existing article."""
    current_user_id = get_jwt_identity()
    article = Article.query.get_or_404(article_id)
    if article.author_id != current_user_id:
        return jsonify({"msg": "Unauthorized"}), 403
    data = request.get_json()
    article.title = data['title']
    article.content = data['content']
    db.session.commit()
    return jsonify({"msg": "Article updated successfully"}), 200

# Delete article endpoint
@app.route('/articles/<int:article_id>', methods=['DELETE'])
@jwt_required()
def delete_article(article_id):
    """Endpoint for deleting an article."""
    current_user_id = get_jwt_identity()
    article = Article.query.get_or_404(article_id)
    if article.author_id != current_user_id:
        return jsonify({"msg": "Unauthorized"}), 403
    db.session.delete(article)
    db.session.commit()
    return jsonify({"msg": "Article deleted successfully"}), 200

# Run the application
if __name__ == '__main__':
    db.create_all()  # Create database tables
    app.run(debug=True)  # Run the Flask application