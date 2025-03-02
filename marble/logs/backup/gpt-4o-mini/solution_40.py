# solution.py

# Import necessary libraries
from flask import Flask, request, jsonify, session
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # Secret key for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music_collaboration_hub.db'  # Database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications
db = SQLAlchemy(app)  # Initialize the database
socketio = SocketIO(app)  # Initialize SocketIO for real-time communication

# Database model for User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Database model for Project
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    data = db.Column(db.Text, nullable=False)  # Store project data as JSON
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()  # Create database tables

# User registration endpoint
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    if User.query.filter_by(username=username).first():  # Check for existing username
        return jsonify({"message": "Username already exists!"}), 400
    hashed_password = generate_password_hash(password)  # Hash the password
    new_user = User(username=username, password=hashed_password)  # Create a new user
    db.session.add(new_user)  # Add user to the session
    db.session.commit()  # Commit the session
    return jsonify({"message": "User registered successfully!"}), 201    db.session.commit()  # Commit the session
    return jsonify({"message": "User registered successfully!"}), 201

# User login endpoint
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()  # Find user by username
    if user and check_password_hash(user.password, password):  # Check password
        session['user_id'] = user.id  # Store user ID in session
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"message": "Invalid credentials!"}), 401

# Real-time collaboration endpoint
@socketio.on('join_project')
def handle_join_project(data):
    project_id = data['project_id']
# User logout endpoint
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)  # Clear user ID from session
    return jsonify({"message": "Logout successful!"}), 200
    emit('project_update', {'data': 'User has joined the project.'}, broadcast=True)

# Endpoint to create a new project
@app.route('/projects', methods=['POST'])
def create_project():
    project_name = request.json.get('name')
    user_id = session.get('user_id')
    new_project = Project(name=project_name, data='{}', user_id=user_id)  # Create a new project
    db.session.add(new_project)  # Add project to the session
    db.session.commit()  # Commit the session
    return jsonify({"message": "Project created successfully!"}), 201

# Endpoint to get project data
@app.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = Project.query.get_or_404(project_id)  # Get project by ID
    return jsonify({"name": project.name, "data": project.data}), 200

# Endpoint to update project data
@app.route('/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    project = Project.query.get_or_404(project_id)  # Get project by ID
    project.data = request.json.get('data')  # Update project data
    db.session.commit()  # Commit the session
    return jsonify({"message": "Project updated successfully!"}), 200

# Main entry point for the application
if __name__ == '__main__':
    socketio.run(app, debug=True)  # Run the application with SocketIO