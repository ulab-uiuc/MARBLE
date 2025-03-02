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
    password = db.Column(db.String(200), nullable=False)

class Conversation(db.Model):
    """Model for storing conversation logs."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class GameScore(db.Model):
    """Model for storing game scores."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    game_name = db.Column(db.String(50), nullable=False)

class GrammarCorrection(db.Model):
    """Model for storing grammar correction feedback."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    correction = db.Column(db.Text, nullable=False)

# API Endpoints

@app.route('/register', methods=['POST'])
def register():
    """API endpoint for user registration."""
    data = request.json
    new_user = User(username=data['username'], role=data['role'], password=data['password'])    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "Username already taken!"}), 400
    if len(data['password']) < 8 or not any(char in '!@#$%^&*()_+' for char in data['password']):
        return jsonify({"message": "Password must be at least 8 characters long and include a special character!"}), 400
    new_user = User(username=data['username'], role=data['role'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()    return jsonify({"message": "User registered successfully!"}), 201

@app.route('/login', methods=['POST'])
def login():
    """API endpoint for user login."""
    data = request.json
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if user:
        return jsonify({"message": "Login successful!", "user_id": user.id}), 200
    return jsonify({"message": "Invalid credentials!"}), 401

@app.route('/send_message', methods=['POST'])
def send_message():
    """API endpoint for sending messages in conversations."""
    data = request.json
    new_message = Conversation(user_id=data['user_id'], message=data['message'])
    db.session.add(new_message)
    db.session.commit()
    socketio.emit('new_message', {'user_id': data['user_id'], 'message': data['message']})
    return jsonify({"message": "Message sent!"}), 200

@app.route('/submit_score', methods=['POST'])
def submit_score():
    """API endpoint for submitting game scores."""
    data = request.json
    new_score = GameScore(user_id=data['user_id'], score=data['score'], game_name=data['game_name'])
    db.session.add(new_score)
    db.session.commit()
    return jsonify({"message": "Score submitted!"}), 200

@app.route('/submit_correction', methods=['POST'])
def submit_correction():
    """API endpoint for submitting grammar corrections."""
    data = request.json
    new_correction = GrammarCorrection(user_id=data['user_id'], text=data['text'], correction=data['correction'])
    db.session.add(new_correction)
    db.session.commit()
    return jsonify({"message": "Correction submitted!"}), 200

# Real-time communication

@socketio.on('connect')
def handle_connect():
    """Handle user connection for real-time chat."""
    emit('response', {'message': 'Connected to the chat!'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle user disconnection."""
    print('User disconnected')

# Main function to run the application
if __name__ == '__main__':
    # Create the database tables
    db.create_all()
    # Run the application with SocketIO
    socketio.run(app, debug=True)