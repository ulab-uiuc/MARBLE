# solution.py

# Import necessary libraries
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import os

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure the application
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///family_adventure_quest.db'  # Database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)  # Secret key for session management

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect to login page if not authenticated

# Database models
class User(db.Model, UserMixin):
    """User model to store user information."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'))

class Family(db.Model):
    """Family model to store family information."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    members = db.relationship('User', backref='family', lazy=True)

class Quest(db.Model):
    """Quest model to store quest information."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    age_group = db.Column(db.String(50), nullable=False)
    rewards = db.Column(db.String(150), nullable=False)

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# API routes
@app.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/login', methods=['POST'])
def login():
    """Login a user."""
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        login_user(user)
        return jsonify({'message': 'Login successful!'}), 200
    return jsonify({'message': 'Invalid credentials!'}), 401

@app.route('/quests', methods=['GET'])
@login_required
def get_quests():
    """Get all quests."""
    quests = Quest.query.all()
    return jsonify([{'id': quest.id, 'title': quest.title, 'description': quest.description} for quest in quests]), 200

@app.route('/quests', methods=['POST'])
@login_required
def create_quest():
    """Create a new quest."""
    data = request.get_json()
    new_quest = Quest(title=data['title'], description=data['description'], age_group=data['age_group'], rewards=data['rewards'])
    db.session.add(new_quest)
    db.session.commit()
    return jsonify({'message': 'Quest created successfully!'}), 201

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    """Logout a user."""
    logout_user()
    return jsonify({'message': 'Logout successful!'}), 200

# Run the application
if __name__ == '__main__':
    db.create_all()  # Create database tables
    app.run(debug=True)  # Run the Flask application in debug mode