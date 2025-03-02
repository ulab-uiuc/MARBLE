# news_collab.py

# Import required libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import json
import os

# Initialize the Flask application
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news_collab.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'

# Initialize the database
db = SQLAlchemy(app)

# Initialize the Marshmallow
ma = Marshmallow(app)

# Initialize the JWTManager
jwt = JWTManager(app)

# Initialize the API
api = Api(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

# Define the Article model
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('articles', lazy=True))

    def __init__(self, title, content, author_id):
        self.title = title
        self.content = content
        self.author_id = author_id

# Define the Comment model
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

# Define the Verification model
class Verification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    article = db.relationship('Article', backref=db.backref('verifications', lazy=True))
    status = db.Column(db.Boolean, nullable=False)

    def __init__(self, article_id, status):
        self.article_id = article_id
        self.status = status

# Define the User schema
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

# Define the Article schema
class ArticleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Article

# Define the Comment schema
class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment

# Define the Verification schema
class VerificationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Verification

# Create the database tables
db.create_all()

# Define the login function
def login(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify(error='Invalid username or password'), 401

# Define the register function
def register(username, password):
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify(error='Username already exists'), 400
    new_user = User(username, password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message='User created successfully'), 201

# Define the create article function
def create_article(title, content, author_id):
    new_article = Article(title, content, author_id)
    db.session.add(new_article)
    db.session.commit()
    return jsonify(message='Article created successfully'), 201

# Define the get article function
def get_article(article_id):
    article = Article.query.get(article_id)
    if article:
        return jsonify(ArticleSchema().dump(article)), 200
    return jsonify(error='Article not found'), 404

# Define the update article function
def update_article(article_id, title, content):
    article = Article.query.get(article_id)
    if article:
        article.title = title
        article.content = content
        db.session.commit()
        return jsonify(message='Article updated successfully'), 200
    return jsonify(error='Article not found'), 404

# Define the delete article function
def delete_article(article_id):
    article = Article.query.get(article_id)
    if article:
        db.session.delete(article)
        db.session.commit()
        return jsonify(message='Article deleted successfully'), 200
    return jsonify(error='Article not found'), 404

# Define the create comment function
def create_comment(content, article_id, author_id):
    new_comment = Comment(content, article_id, author_id)
    db.session.add(new_comment)
    db.session.commit()
    return jsonify(message='Comment created successfully'), 201

# Define the get comment function
def get_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if comment:
        return jsonify(CommentSchema().dump(comment)), 200
    return jsonify(error='Comment not found'), 404

# Define the update comment function
def update_comment(comment_id, content):
    comment = Comment.query.get(comment_id)
    if comment:
        comment.content = content
        db.session.commit()
        return jsonify(message='Comment updated successfully'), 200
    return jsonify(error='Comment not found'), 404

# Define the delete comment function
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if comment:
        db.session.delete(comment)
        db.session.commit()
        return jsonify(message='Comment deleted successfully'), 200
    return jsonify(error='Comment not found'), 404

# Define the verify article function
def verify_article(article_id, status):
    verification = Verification.query.filter_by(article_id=article_id).first()
    if verification:
        verification.status = status
        db.session.commit()
        return jsonify(message='Article verification updated successfully'), 200
    new_verification = Verification(article_id, status)
    db.session.add(new_verification)
    db.session.commit()
    return jsonify(message='Article verification created successfully'), 201

# Define the get verification function
def get_verification(article_id):
    verification = Verification.query.filter_by(article_id=article_id).first()
    if verification:
        return jsonify(VerificationSchema().dump(verification)), 200
    return jsonify(error='Verification not found'), 404

# Define the notification function
def notification(article_id, message):
    # Send notification to users
    return jsonify(message='Notification sent successfully'), 200

# Define the machine learning model for verification
def machine_learning_model(text):
    # Load the dataset
    dataset = json.load(open('dataset.json'))

    # Preprocess the text
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in stop_words])
    text = ' '.join([lemmatizer.lemmatize(word) for word in text.split()])

    # Create the TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Fit the vectorizer to the dataset
    vectorizer.fit(dataset)

    # Transform the text into a vector
    vector = vectorizer.transform([text])

    # Calculate the cosine similarity
    similarity = cosine_similarity(vector, vectorizer.transform(dataset))

    # Return the verification status
    if similarity > 0.5:
        return True
    else:
        return False

# Define the API endpoints
class Login(Resource):
    def post(self):
        username = request.json['username']
        password = request.json['password']
        return login(username, password)

class Register(Resource):
    def post(self):
        username = request.json['username']
        password = request.json['password']
        return register(username, password)

class CreateArticle(Resource):
    @jwt_required
    def post(self):
        title = request.json['title']
        content = request.json['content']
        author_id = get_jwt_identity()
        return create_article(title, content, author_id)

class GetArticle(Resource):
    def get(self, article_id):
        return get_article(article_id)

class UpdateArticle(Resource):
    @jwt_required
    def put(self, article_id):
        title = request.json['title']
        content = request.json['content']
        return update_article(article_id, title, content)

class DeleteArticle(Resource):
    @jwt_required
    def delete(self, article_id):
        return delete_article(article_id)

class CreateComment(Resource):
    @jwt_required
    def post(self, article_id):
        content = request.json['content']
        author_id = get_jwt_identity()
        return create_comment(content, article_id, author_id)

class GetComment(Resource):
    def get(self, comment_id):
        return get_comment(comment_id)

class UpdateComment(Resource):
    @jwt_required
    def put(self, comment_id):
        content = request.json['content']
        return update_comment(comment_id, content)

class DeleteComment(Resource):
    @jwt_required
    def delete(self, comment_id):
        return delete_comment(comment_id)

class VerifyArticle(Resource):
    @jwt_required
    def post(self, article_id):
        status = machine_learning_model(request.json['text'])
        return verify_article(article_id, status)

class GetVerification(Resource):
    def get(self, article_id):
        return get_verification(article_id)

class Notification(Resource):
    @jwt_required
    def post(self, article_id):
        message = request.json['message']
        return notification(article_id, message)

# Add the API endpoints
api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(CreateArticle, '/article')
api.add_resource(GetArticle, '/article/<int:article_id>')
api.add_resource(UpdateArticle, '/article/<int:article_id>')
api.add_resource(DeleteArticle, '/article/<int:article_id>')
api.add_resource(CreateComment, '/article/<int:article_id>/comment')
api.add_resource(GetComment, '/comment/<int:comment_id>')
api.add_resource(UpdateComment, '/comment/<int:comment_id>')
api.add_resource(DeleteComment, '/comment/<int:comment_id>')
api.add_resource(VerifyArticle, '/article/<int:article_id>/verify')
api.add_resource(GetVerification, '/article/<int:article_id>/verification')
api.add_resource(Notification, '/article/<int:article_id>/notification')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)