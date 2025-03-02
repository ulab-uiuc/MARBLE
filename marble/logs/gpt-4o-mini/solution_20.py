# solution.py

# Import necessary libraries
from flask import Flask, request, jsonify, session
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # Secret key for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music_mashup_battle.db'  # Database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications
CORS(app)  # Enable Cross-Origin Resource Sharing
db = SQLAlchemy(app)  # Initialize the database

# Database models
class User(db.Model):
    """Model for storing user profiles."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    mashups = db.relationship('Mashup', backref='creator', lazy=True)

class Mashup(db.Model):
    """Model for storing mashup creations."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    votes = db.relationship('Vote', backref='mashup', lazy=True)

class Vote(db.Model):
    """Model for storing votes on mashups."""
    id = db.Column(db.Integer, primary_key=True)
    mashup_id = db.Column(db.Integer, db.ForeignKey('mashup.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

# Initialize SocketIO for real-time communication
socketio = SocketIO(app)

# Routes for user management
@app.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    username = request.json.get('username')
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400
    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/create_mashup', methods=['POST'])
def create_mashup():
    """Create a new mashup."""
    title = request.json.get('title')
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'User not logged in'}), 403    title = request.json.get('title')
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'User not logged in'}), 403
    if not title or title.strip() == '':
        return jsonify({'message': 'Mashup title is required and cannot be empty'}), 400
    new_mashup = Mashup(title=title, creator_id=user_id)    db.session.add(new_mashup)
    db.session.commit()
    return jsonify({'message': 'Mashup created successfully'}), 201

@app.route('/vote', methods=['POST'])
def vote():
    """Vote for a mashup."""
    mashup_id = request.json.get('mashup_id')
    user_id = session.get('user_id')
    score = request.json.get('score')
    if not user_id:
        return jsonify({'message': 'User not logged in'}), 403
    existing_vote = Vote.query.filter_by(mashup_id=mashup_id, user_id=user_id).first()
    if existing_vote:
        existing_vote.score = score  # Update existing vote
    else:
        new_vote = Vote(mashup_id=mashup_id, user_id=user_id, score=score)
        db.session.add(new_vote)
    db.session.commit()
    return jsonify({'message': 'Vote recorded successfully'}), 200

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    """Get the leaderboard of mashups based on votes."""
    results = db.session.query(Mashup.title, db.func.count(Vote.id).label('vote_count')) \
        .outerjoin(Vote) \
        .group_by(Mashup.id) \
        .order_by(db.func.count(Vote.id).desc()) \
        .all()
    return jsonify([{'title': title, 'vote_count': vote_count} for title, vote_count in results]), 200

# SocketIO events for real-time collaboration
@socketio.on('join_room')
def handle_join_room(data):
    """Handle user joining a room."""

def validate_user_and_title(user_id, title):
    if not user_id:
        return jsonify({'message': 'User not logged in'}), 403
    if not title or title.strip() == '':
        return jsonify({'message': 'Mashup title is required and cannot be empty'}), 400
    return None
    room = data['room']
    join_room(room)
    emit('user_joined', {'message': f'User has joined the room: {room}'}, room=room)

@socketio.on('send_message')
def handle_send_message(data):
    """Handle sending messages in the chat."""
    room = data['room']
    message = data['message']
    emit('receive_message', {'message': message}, room=room)

@socketio.on('create_mashup_event')
def handle_create_mashup_event(data):
    """Handle mashup creation event."""
    emit('mashup_created', data, broadcast=True)

# Main entry point for the application
if __name__ == '__main__':
    db.create_all()  # Create database tables
    socketio.run(app, debug=True)  # Run the application with SocketIO