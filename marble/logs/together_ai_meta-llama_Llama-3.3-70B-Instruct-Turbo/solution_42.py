# news_collab.pyfrom flask import Flask, request, jsonify
from flask_bcrypt import Bcryptfrom flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS
import os
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news_collab.db'
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'

# Initialize the database
db = SQLAlchemy(app)

# Initialize the Marshmallow serializer
ma = Marshmallow(app)

# Initialize the JWT manager
jwt = JWTManager(app)

# Initialize CORS
CORS(app)

# Define the User model
class User(db.Model):def __init__(self, username, password, role):
    self.username = username
    self.password = bcrypt.generate_password_hash(password).decode('utf-8')self.username = username
        self.password = password
        self.role = role

# Define the Article model
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('articles', lazy=True))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

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
    status = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, article_id, status):
        self.article_id = article_id
        self.status = status

# Define the schema for the User model
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

# Define the schema for the Article model
class ArticleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Article
        load_instance = True

# Define the schema for the Comment model
class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        load_instance = True

# Define the schema for the Verification model
class VerificationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Verification
        load_instance = True

# Create the database tables
with app.app_context():
    db.create_all()

# Define the login route
@app.route('/login', methods=['POST'])
def login():username = request.json.get('username')
password = request.json.get('password')
user = User.query.filter_by(username=username).first()
if user and bcrypt.check_password_hash(user.password, password):
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)
return jsonify(message='Invalid username or password'), 401# Define the create article route
@app.route('/articles', methods=['POST'])
@jwt_required
def create_article():
    title = request.json.get('title')
    content = request.json.get('content')
    author_id = get_jwt_identity()
    article = Article(title, content, author_id)
    db.session.add(article)
    db.session.commit()
    return jsonify(message='Article created successfully')

# Define the get articles route
@app.route('/articles', methods=['GET'])
@jwt_required
def get_articles():
    articles = Article.query.all()
    schema = ArticleSchema(many=True)
    return jsonify(schema.dump(articles))

# Define the get article route
@app.route('/articles/<int:article_id>', methods=['GET'])
@jwt_required
def get_article(article_id):
    article = Article.query.get(article_id)
    schema = ArticleSchema()
    return jsonify(schema.dump(article))

# Define the update article route
@app.route('/articles/<int:article_id>', methods=['PUT'])
@jwt_required
def update_article(article_id):
    article = Article.query.get(article_id)
    title = request.json.get('title')
    content = request.json.get('content')
    article.title = title
    article.content = content
    db.session.commit()
    return jsonify(message='Article updated successfully')

# Define the delete article route
@app.route('/articles/<int:article_id>', methods=['DELETE'])
@jwt_required
def delete_article(article_id):
    article = Article.query.get(article_id)
    db.session.delete(article)
    db.session.commit()
    return jsonify(message='Article deleted successfully')

# Define the create comment route
@app.route('/comments', methods=['POST'])
@jwt_required
def create_comment():
    content = request.json.get('content')
    article_id = request.json.get('article_id')
    author_id = get_jwt_identity()
    comment = Comment(content, article_id, author_id)
    db.session.add(comment)
    db.session.commit()
    return jsonify(message='Comment created successfully')

# Define the get comments route
@app.route('/comments', methods=['GET'])
@jwt_required
def get_comments():
    comments = Comment.query.all()
    schema = CommentSchema(many=True)
    return jsonify(schema.dump(comments))

# Define the get comment route
@app.route('/comments/<int:comment_id>', methods=['GET'])
@jwt_required
def get_comment(comment_id):
    comment = Comment.query.get(comment_id)
    schema = CommentSchema()
    return jsonify(schema.dump(comment))

# Define the update comment route
@app.route('/comments/<int:comment_id>', methods=['PUT'])
@jwt_required
def update_comment(comment_id):
    comment = Comment.query.get(comment_id)
    content = request.json.get('content')
    comment.content = content
    db.session.commit()
    return jsonify(message='Comment updated successfully')

# Define the delete comment route
@app.route('/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify(message='Comment deleted successfully')

# Define the create verification route
@app.route('/verifications', methods=['POST'])
@jwt_required
def create_verification():
    article_id = request.json.get('article_id')
    status = request.json.get('status')
    verification = Verification(article_id, status)
    db.session.add(verification)
    db.session.commit()
    return jsonify(message='Verification created successfully')

# Define the get verifications route
@app.route('/verifications', methods=['GET'])
@jwt_required
def get_verifications():
    verifications = Verification.query.all()
    schema = VerificationSchema(many=True)
    return jsonify(schema.dump(verifications))

# Define the get verification route
@app.route('/verifications/<int:verification_id>', methods=['GET'])
@jwt_required
def get_verification(verification_id):
    verification = Verification.query.get(verification_id)
    schema = VerificationSchema()
    return jsonify(schema.dump(verification))

# Define the update verification route
@app.route('/verifications/<int:verification_id>', methods=['PUT'])
@jwt_required
def update_verification(verification_id):
    verification = Verification.query.get(verification_id)
    status = request.json.get('status')
    verification.status = status
    db.session.commit()
    return jsonify(message='Verification updated successfully')

# Define the delete verification route
@app.route('/verifications/<int:verification_id>', methods=['DELETE'])
@jwt_required
def delete_verification(verification_id):
    verification = Verification.query.get(verification_id)
    db.session.delete(verification)
    db.session.commit()
    return jsonify(message='Verification deleted successfully')

if __name__ == '__main__':
    app.run(debug=True)