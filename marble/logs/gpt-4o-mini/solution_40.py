# solution.py

# Import necessary libraries
from flask import Flask, request, jsonify, session
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # Secret key for session management
from flask_socketio import join_room, leave_room
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music_collaboration_hub.db'  # Database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
db = SQLAlchemy(app)  # Initialize the database
socketio = SocketIO(app)  # Initialize SocketIO for real-time communication

# Database models
class User(db.Model):
    """Model for storing user information."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

class Project(db.Model):
    """Model for storing music project data."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Collaboration(db.Model):
    """Model for storing collaboration history."""
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# User authentication routes
@app.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.json
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    """Log in a user."""
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        session['user_id'] = user.id  # Store user ID in session
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    """Log out a user."""
    session.pop('user_id', None)  # Remove user ID from session
    return jsonify({'message': 'Logout successful'}), 200

# Project management routes
@app.route('/projects', methods=['POST'])
def create_project():
    """Create a new music project."""
    data = request.json
    new_project = Project(name=data['name'], user_id=session['user_id'])
    db.session.add(new_project)
    db.session.commit()
    return jsonify({'message': 'Project created successfully'}), 201

@app.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """Get project details."""
    project = Project.query.get_or_404(project_id)
    return jsonify({'id': project.id, 'name': project.name}), 200

# Real-time collaboration using SocketIO
@socketio.on('join')
def handle_join(data):
    """Handle user joining a project."""
    project_id = data['project_id']
    join_room(project_id)  # Join the room corresponding to the project
    emit('message', {'msg': f'User has joined project {project_id}'}, room=project_id)

@socketio.on('leave')
def handle_leave(data):
    """Handle user leaving a project."""
    project_id = data['project_id']
    leave_room(project_id)  # Leave the room corresponding to the project
    emit('message', {'msg': f'User has left project {project_id}'}, room=project_id)

@socketio.on('update_project')
def handle_update(data):
    """Handle project updates."""
    project_id = data['project_id']
    emit('project_updated', data, room=project_id)  # Broadcast the update to all users in the project

# Main entry point
if __name__ == '__main__':
    db.create_all()  # Create database tables
    socketio.run(app, debug=True)  # Run the application with SocketIO