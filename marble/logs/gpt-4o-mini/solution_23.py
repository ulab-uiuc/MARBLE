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

# Initialize database and migration tools
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt(app)

# Initialize LoginManager for user session management
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect to login page if not authenticated


# User model for authentication
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Quest model to store quest details
class Quest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    age_group = db.Column(db.String(50), nullable=False)
    rewards = db.Column(db.String(150), nullable=False)

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route to register a new user
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

# Route to login a user
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        login_user(user)
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"message": "Invalid credentials!"}), 401

# Route to logout a user
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful!"}), 200

# Route to get all quests
@app.route('/quests', methods=['GET'])
def get_quests():
    quests = Quest.query.all()
    return jsonify([{"id": quest.id, "title": quest.title, "description": quest.description, "age_group": quest.age_group, "rewards": quest.rewards} for quest in quests]), 200

# Route to create a new quest (admin only)
@app.route('/quests', methods=['POST'])
@login_required
def create_quest():
    data = request.get_json()
    new_quest = Quest(title=data['title'], description=data['description'], age_group=data['age_group'], rewards=data['rewards'])    user = User.query.get(current_user.id)
    if user.role != 'admin':
        return jsonify({'message': 'Unauthorized access!'}), 403
    new_quest = Quest(title=data['title'], description=data['description'], age_group=data['age_group'], rewards=data['rewards'])    db.session.add(new_quest)
    db.session.commit()
    return jsonify({"message": "Quest created successfully!"}), 201

# Main entry point to run the application
if __name__ == '__main__':
    db.create_all()  # Create database tables
    app.run(debug=True)  # Run the application in debug mode