# solution.py

# Import necessary libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from datetime import datetime
import os

# Initialize the Flask application
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///language_learning_hub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize SocketIO for real-time communication
socketio = SocketIO(app)

# Database models

class User(db.Model):
    """Model for storing user information."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # roles: learner, native, admin
    conversations = db.relationship('Conversation', backref='user', lazy=True)

class Conversation(db.Model):
    """Model for storing conversation logs."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class GameScore(db.Model):
    """Model for storing game scores."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    game_date = db.Column(db.DateTime, default=datetime.utcnow)

# Create the database
@app.before_first_request
def create_tables():
    db.create_all()

# API Endpoints

@app.route('/register', methods=['POST'])
def register_user():
    """API endpoint for user registration."""
    data = request.json
    new_user = User(username=data['username'], role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

@app.route('/conversations', methods=['POST'])
def log_conversation():
    """API endpoint for logging conversations."""
    data = request.json
    new_conversation = Conversation(user_id=data['user_id'], message=data['message'])
    db.session.add(new_conversation)
    db.session.commit()
    return jsonify({"message": "Conversation logged successfully!"}), 201

@app.route('/game_score', methods=['POST'])
def log_game_score():
    """API endpoint for logging game scores."""
    data = request.json
    new_score = GameScore(user_id=data['user_id'], score=data['score'])
    db.session.add(new_score)
    db.session.commit()
    return jsonify({"message": "Game score logged successfully!"}), 201

# Real-time communication

@socketio.on('send_message')
def handle_send_message(data):
    """Handle incoming messages for real-time chat."""
    emit('receive_message', data, broadcast=True)

# Run the application
if __name__ == '__main__':
    socketio.run(app, debug=True)

# Note: This is a basic implementation. In a production environment, 
# you would need to implement user authentication, data validation, 
# error handling, and security measures.