
from sklearn.externals import joblib
# Load the trained machine learning modelfrom machine_learning_model import train_model
model, accuracy = train_model(data)
joblib.dump(model, 'trained_model.pkl')
model = joblib.load('trained_model.pkl')

# Define a function to train the machine learning model
def train_model(data):
    # Train a machine learning model to verify article credibility
    X = data.drop(['label'], axis=1)
    y = data['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    # Save the trained model
    joblib.dump(model, 'trained_model.pkl')
    return model, accuracy# news_collab.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news_collab.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'

# Initialize extensions
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password, role):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.role = role

# Article model
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('articles', lazy=True))

    def __init__(self, title, content, author_id):
        self.title = title
        self.content = content
        self.author_id = author_id

# Comment model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    article = db.relationship('Article', backref=db.backref('comments', lazy=True))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('comments', lazy=True))

    def __init__(self, content, article_id, author_id):
        self.content = content
        self.article_id = article_id
        self.author_id = author_id

# Verification model
class Verification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    article = db.relationship('Article', backref=db.backref('verifications', lazy=True))
    status = db.Column(db.String(100), nullable=False)

    def __init__(self, article_id, status):
        self.article_id = article_id
        self.status = status

# Schemas
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class ArticleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Article

class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment

class VerificationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Verification

# Routes
@app.route('/register', methods=['POST'])
def register():
    # Register a new user
    username = request.json.get('username')
    password = request.json.get('password')
    role = request.json.get('role')
    user = User(username, password, role)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    # Login a user
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/articles', methods=['GET'])
@jwt_required
def get_articles():
    # Get all articles
    articles = Article.query.all()
    article_schema = ArticleSchema(many=True)
    return jsonify(article_schema.dump(articles)), 200

@app.route('/articles', methods=['POST'])
@jwt_required
def create_article():
    # Create a new articlecurrent_user = User.query.get(get_jwt_identity())
if current_user.role != 'editor':
    article = Article.query.filter_by(author_id=get_jwt_identity()).first()
    if article:
        return jsonify({'message': 'You are not authorized to create an article'}), 401    if article:
        return jsonify({'message': 'You are not authorized to create an article'}), 401    title = request.json.get('title')
    content = request.json.get('content')
    author_id = get_jwt_identity()
    current_user = User.query.get(get_jwt_identity())
    if current_user.role not in ['journalist', 'editor']:
        return jsonify({'message': 'You are not authorized to create an article'}), 401
    article = Article(title, content, author_id)
    db.session.add(article)
    db.session.commit()
    return jsonify({'message': 'Article created successfully'}), 201

@app.route('/articles/<int:article_id>', methods=['GET'])
@jwt_required
def get_article(article_id):
    # Get an article by id
    article = Article.query.get(article_id)
    if article:
        article_schema = ArticleSchema()
        return jsonify(article_schema.dump(article)), 200
    return jsonify({'message': 'Article not found'}), 404

@app.route('/articles/<int:article_id>', methods=['PUT'])
@jwt_required
def update_article(article_id):
    # Update an article
    article = Article.query.get(article_id)
    if article.author_id != get_jwt_identity() and current_user.role != 'editor':
        return jsonify({'message': 'You are not authorized to update this article'}), 401
    if article:
        title = request.json.get('title')
        content = request.json.get('content')
        article.title = title
        article.content = content
        db.session.commit()
        return jsonify({'message': 'Article updated successfully'}), 200
    return jsonify({'message': 'Article not found'}), 404

@app.route('/articles/<int:article_id>', methods=['DELETE'])
@jwt_required
def delete_article(article_id):
    # Delete an article
    article = Article.query.get(article_id)
    if article.author_id != get_jwt_identity() and current_user.role != 'editor':
        return jsonify({'message': 'You are not authorized to delete this article'}), 401
    if article:
        db.session.delete(article)
        db.session.commit()
        return jsonify({'message': 'Article deleted successfully'}), 200
    return jsonify({'message': 'Article not found'}), 404

@app.route('/comments', methods=['POST'])
@jwt_required
def create_comment():
    # Create a new comment
    content = request.json.get('content')
    article_id = request.json.get('article_id')
    author_id = get_jwt_identity()
    comment = Comment(content, article_id, author_id)
    db.session.add(comment)
    db.session.commit()
    return jsonify({'message': 'Comment created successfully'}), 201

@app.route('/verifications', methods=['POST'])
@jwt_required
def create_verification():
    # Create a new verification
    article_id = request.json.get('article_id')
    status = request.json.get('status')
    verification = Verification(article_id, status)
    db.session.add(verification)
    db.session.commit()
    return jsonify({'message': 'Verification created successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)

# notification_service.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_notification(to, subject, message):
    # Send a notification email
    msg = MIMEMultipart()
    msg['From'] = 'news.collab@example.com'
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP('smtp.example.com', 587)
    server.starttls()
    server.login(msg['From'], 'password')
    text = msg.as_string()
    server.sendmail(msg['From'], msg['To'], text)
    server.quit()

# machine_learning_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def train_model(data):
    # Train a machine learning model to verify article credibility
    X = data.drop(['label'], axis=1)
    y = data['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return model, accuracy

# audit_log.py
import logging

def log_activity(activity):
    # Log user activity
    logging.basicConfig(filename='audit.log', level=logging.INFO)
    logging.info(activity)

# main.py
from news_collab import app
from notification_service import send_notification
from machine_learning_model import train_model
from audit_log import log_activity

if __name__ == '__main__':
    app.run(debug=True)