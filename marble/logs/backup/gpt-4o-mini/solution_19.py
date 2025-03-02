# solution.py

# Import necessary libraries
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stories.db'
db = SQLAlchemy(app)
socketio = SocketIO(app)

# Database models

# User model for user registration and authentication
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

# Story model for story creation and editing
class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)author_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

# Initialize the database
@app.before_first_request
def create_tables():
    db.create_all()

# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        session['user_id'] = user.id
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

# Story Creation
@app.route('/stories', methods=['POST'])
def create_story():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 403
    data = request.json
    new_story = Story(title=data['title'], content=data['content'], author_id=session['user_id'])
    db.session.add(new_story)
    db.session.commit()
    return jsonify({'message': 'Story created successfully'}), 201

# Real-Time Collaboration
@socketio.on('edit_story')
def handle_edit(data):
    # Broadcast the edit to all connected clients
    emit('story_edited', data, broadcast=True)

# Version Control (simplified)
@app.route('/stories/<int:story_id>/versions', methods=['GET'])
def get_story_versions(story_id):
    # This would normally return a list of versions for the story
    return jsonify({'message': 'Version control not implemented yet'}), 501

# Community Gallery (simplified)
@app.route('/gallery', methods=['GET'])
def get_gallery():
    stories = Story.query.all()
    return jsonify([{'id': story.id, 'title': story.title} for story in stories]), 200

# Notification System (simplified)
@app.route('/notifications', methods=['GET'])
def get_notifications():
    # This would normally return notifications for the logged-in user
    return jsonify({'message': 'Notification system not implemented yet'}), 501

# Run the application
if __name__ == '__main__':
    socketio.run(app, debug=True)