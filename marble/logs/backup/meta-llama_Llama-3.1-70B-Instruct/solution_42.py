# news_collab.py

# Import required libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import datetime, timedelta
import json

# Initialize the Flask application
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news_collab.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'

# Initialize the database
db = SQLAlchemy(app)

# Initialize the Marshmallow object
ma = Marshmallow(app)

# Initialize the JWTManager object
jwt = JWTManager(app)

# Initialize the Api object
api = Api(app)
# Initialize the Bcrypt object
bcrypt = Bcrypt(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(64), nullable=False)

    def __init__(self, username, password, role):self.password = bcrypt.generate_password_hash(password).decode('utf-8')self.role = role

# Define the Article model
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('articles', lazy=True))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

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
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, content, article_id, author_id):
        self.content = content
        self.article_id = article_id
        self.author_id = author_id

# Define the Verification model
class Verification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    article = db.relationship('Article', backref=db.backref('verifications', lazy=True))
    status = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, article_id, status):
        self.article_id = article_id
        self.status = status

# Define the UserSchema
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

# Define the ArticleSchema
class ArticleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Article
        load_instance = True

# Define the CommentSchema
class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        load_instance = True

# Define the VerificationSchema
class VerificationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Verification
        load_instance = True

# Create the database tables
db.create_all()

# Define the login endpoint
class Login(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        user = User.query.filter_by(username=username).first()if user and bcrypt.check_password_hash(user.password, password):access_token = create_access_token(identity=username, expires_delta=timedelta(minutes=30))
            return jsonify(access_token=access_token)
        return jsonify(error='Invalid credentials'), 401

# Define the register endpoint
class Register(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        role = request.json.get('role')
        user = User(username=username, password=password, role=role)
        db.session.add(user)
        db.session.commit()
        return jsonify(message='User created successfully')

# Define the article endpoint
class ArticleEndpoint(Resource):
    @jwt_required
    def get(self, article_id):
        article = Article.query.get(article_id)
        if article:
            return ArticleSchema().dump(article)
        return jsonify(error='Article not found'), 404

    @jwt_required
    def put(self, article_id):
        article = Article.query.get(article_id)
        if article:
            title = request.json.get('title')
            content = request.json.get('content')
            article.title = title
            article.content = content
            db.session.commit()
            return ArticleSchema().dump(article)
        return jsonify(error='Article not found'), 404

    @jwt_required
    def delete(self, article_id):
        article = Article.query.get(article_id)
        if article:
            db.session.delete(article)
            db.session.commit()
            return jsonify(message='Article deleted successfully')
        return jsonify(error='Article not found'), 404

# Define the comment endpoint
class CommentEndpoint(Resource):
    @jwt_required
    def post(self, article_id):
        content = request.json.get('content')
        author_id = get_jwt_identity()
        comment = Comment(content=content, article_id=article_id, author_id=author_id)
        db.session.add(comment)
        db.session.commit()
        return CommentSchema().dump(comment)

# Define the verification endpoint
class VerificationEndpoint(Resource):
    @jwt_required
    def post(self, article_id):
        status = request.json.get('status')
        verification = Verification(article_id=article_id, status=status)
        db.session.add(verification)
        db.session.commit()
        return VerificationSchema().dump(verification)

# Add the endpoints to the API
api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(ArticleEndpoint, '/article/<int:article_id>')
api.add_resource(CommentEndpoint, '/article/<int:article_id>/comment')
api.add_resource(VerificationEndpoint, '/article/<int:article_id>/verification')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)