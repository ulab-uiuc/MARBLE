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
class User(db.Model):
    """Model for User."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

class Story(db.Model):
    """Model for Story."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Version(db.Model):
    """Model for Story Version."""
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# User Registration and Authentication
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
        session['user_id'] = user.id
        return jsonify({'message': 'Logged in successfully'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    """Log out a user."""
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200

# Story Creation and Editing
@app.route('/stories', methods=['POST'])
def create_story():
    """Create a new story."""
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 403
    data = request.json
    new_story = Story(title=data['title'], content=data['content'], user_id=session['user_id'])
    db.session.add(new_story)
    db.session.commit()
    return jsonify({'message': 'Story created successfully'}), 201

@app.route('/stories/<int:story_id>', methods=['PUT'])
def edit_story(story_id):
    """Edit an existing story."""
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 403
    story = Story.query.get_or_404(story_id)
    if story.user_id != session['user_id']:
        return jsonify({'message': 'Forbidden'}), 403
    data = request.json
    # Save the current version before editing
    new_version = Version(story_id=story.id, content=story.content)
    db.session.add(new_version)
    story.content = data['content']
    db.session.commit()
    return jsonify({'message': 'Story updated successfully'}), 200

# Real-Time Collaboration
@socketio.on('edit_story')
def handle_edit(data):
    """Handle real-time story editing."""
    story = Story.query.get(data['story_id'])
    if story:
        story.content = data['content']
        db.session.commit()
        emit('story_updated', {'story_id': story.id, 'content': story.content}, broadcast=True)

# Version Control
@app.route('/stories/<int:story_id>/versions', methods=['GET'])
def get_versions(story_id):
    """Get all versions of a story."""
    versions = Version.query.filter_by(story_id=story_id).all()
    return jsonify([{'id': v.id, 'content': v.content, 'created_at': v.created_at} for v in versions]), 200

@app.route('/stories/<int:story_id>/versions/<int:version_id>', methods=['POST'])
def revert_to_version(story_id, version_id):
    """Revert a story to a previous version."""
    story = Story.query.get_or_404(story_id)
    version = Version.query.get_or_404(version_id)
    story.content = version.content
    db.session.commit()
    return jsonify({'message': 'Story reverted to previous version'}), 200

# Community Gallery
@app.route('/gallery', methods=['GET'])
def gallery():
    """Get all completed stories."""
    stories = Story.query.all()
    return jsonify([{'id': s.id, 'title': s.title, 'content': s.content} for s in stories]), 200

# Notification System
@app.route('/notifications', methods=['GET'])
def notifications():
    """Get notifications for the logged-in user."""
    # Placeholder for notifications logic
    return jsonify({'message': 'No new notifications'}), 200

# Run the application
if __name__ == '__main__':
    db.create_all()  # Create database tables
    socketio.run(app, debug=True)  # Run the Flask application with SocketIO