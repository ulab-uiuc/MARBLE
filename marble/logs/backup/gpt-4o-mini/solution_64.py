# solution.py

# Import necessary libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questhub.db'  # Database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # Initialize the database
socketio = SocketIO(app)  # Initialize SocketIO for real-time communication

# Database models
class User(db.Model):
    """Model for user profiles."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Quest(db.Model):
    """Model for quests."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    completed = db.Column(db.Boolean, default=False)

class SkillPlan(db.Model):
    """Model for character skill plans."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    skill_name = db.Column(db.String(120), nullable=False)
    level = db.Column(db.Integer, default=1)

# User authentication routes
@app.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    """Login a user."""
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

# Quest management routes
@app.route('/quests', methods=['POST'])
def create_quest():
    """Create a new quest."""
    data = request.get_json()
    new_quest = Quest(title=data['title'], description=data['description'])
    db.session.add(new_quest)
    db.session.commit()
    return jsonify({'message': 'Quest created successfully'}), 201

@app.route('/quests/<int:quest_id>', methods=['PUT'])
def update_quest(quest_id):
    """Update an existing quest."""
    data = request.get_json()
    quest = Quest.query.get(quest_id)
    if quest:
        quest.title = data['title']
        quest.description = data['description']
        db.session.commit()
        return jsonify({'message': 'Quest updated successfully'}), 200
    return jsonify({'message': 'Quest not found'}), 404

@app.route('/quests/<int:quest_id>', methods=['DELETE'])
def complete_quest(quest_id):
    """Complete a quest."""
    quest = Quest.query.get(quest_id)
    if quest:
        quest.completed = True
        db.session.commit()
        return jsonify({'message': 'Quest completed successfully'}), 200
    return jsonify({'message': 'Quest not found'}), 404

# Skill plan management routes
@app.route('/skillplans', methods=['POST'])
def create_skill_plan():
    """Create a new skill plan."""
    data = request.get_json()
    new_skill_plan = SkillPlan(user_id=data['user_id'], skill_name=data['skill_name'], level=data['level'])
    db.session.add(new_skill_plan)
    db.session.commit()
    return jsonify({'message': 'Skill plan created successfully'}), 201

# Real-time collaboration using SocketIO
@socketio.on('join')
def handle_join(data):
    """Handle a user joining a quest or skill plan."""
    room = data['room']
    join_room(room)
    emit('message', {'msg': f"{data['username']} has joined the room."}, room=room)

@socketio.on('send_message')
def handle_message(data):
    """Handle sending messages in a room."""
    emit('message', {'msg': data['msg']}, room=data['room'])

# Main entry point
if __name__ == '__main__':
    db.create_all()  # Create database tables
    socketio.run(app, debug=True)  # Run the application with SocketIO