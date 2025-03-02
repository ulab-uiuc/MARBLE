# solution.py

# Import necessary libraries
from flask import Flask, request, jsonify, session
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # Secure session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music_mashup_battle.db'  # Database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

# Initialize the database
with app.app_context():
    db.create_all()

# SocketIO for real-time communication
socketio = SocketIO(app)

# Routes for user management
@app.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    username = request.json.get('username')
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/mashups', methods=['POST'])
def create_mashup():
    """Create a new mashup."""
    title = request.json.get('title')
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 403
    new_mashup = Mashup(title=title, creator_id=user_id)
    db.session.add(new_mashup)
    db.session.commit()
    return jsonify({'message': 'Mashup created successfully'}), 201

@app.route('/vote', methods=['POST'])
def vote():
    """Vote for a mashup."""
    mashup_id = request.json.get('mashup_id')
    user_id = session.get('user_id')
    score = request.json.get('score')
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 403
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
    room = data['room']
    join_room(room)
    emit('user_joined', {'message': f'User has joined the room: {room}'}, room=room)

@socketio.on('send_message')
def handle_send_message(data):
    """Handle sending messages in the chat."""
    room = data['room']
    message = data['message']
    emit('receive_message', {'message': message}, room=room)

@socketio.on('create_mashup')
def handle_create_mashup(data):
    """Handle mashup creation in real-time."""
    room = data['room']
    mashup_data = data['mashup']
    emit('mashup_created', {'mashup': mashup_data}, room=room)

# Run the application
if __name__ == '__main__':
    socketio.run(app, debug=True)