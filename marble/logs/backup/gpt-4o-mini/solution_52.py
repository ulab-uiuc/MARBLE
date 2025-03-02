# solution.py

# Import necessary libraries
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import os

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure MongoDB
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb://localhost:27017/photo_collab")
mongo = PyMongo(app)

# Initialize SocketIO for real-time communication
socketio = SocketIO(app)

# User authentication and session management
@app.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    username = request.json.get('username')
    password = request.json.get('password')
    hashed_password = generate_password_hash(password)
    
    # Store user in the database
    mongo.db.users.insert_one({'username': username, 'password': hashed_password})
    return jsonify({"message": "User registered successfully!"}), 201

@app.route('/login', methods=['POST'])
def login():
    """Authenticate a user."""
    username = request.json.get('username')
    password = request.json.get('password')
    user = mongo.db.users.find_one({'username': username})
    
    if user and check_password_hash(user['password'], password):
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"message": "Invalid credentials!"}), 401

# Real-time collaboration features
@socketio.on('join_session')
def handle_join_session(data):
    """Handle a user joining an editing session."""    # Check if the session exists
    session = mongo.db.sessions.find_one({'_id': session_id})
    if not session:
        emit('error', {'message': 'Session does not exist.'})
        return
    join_message = f"{username} has joined the session."
    # Notify all users in the session
    emit('user_joined', {'message': join_message}, room=session_id)
    join_room(session_id)    # Notify all users in the session
    emit('user_joined', {'message': join_message}, room=session_id)
    join_room(session_id)

@socketio.on('edit_photo')
def handle_edit_photo(data):
    """Handle photo editing actions."""
    session_id = data['session_id']
    edit_action = data['edit_action']
    
    # Broadcast the edit action to all users in the session
    emit('photo_edited', {'edit_action': edit_action}, room=session_id)

# Photo metadata and editing actions storage
@app.route('/photos', methods=['POST'])
def upload_photo():
    """Upload a photo and store its metadata."""
    file = request.files['photo']
    session_id = request.form['session_id']
    
    # Save the photo to a directory (for simplicity, not implemented here)
    # file.save(os.path.join('uploads', file.filename))
    
    # Store photo metadata in the database
    mongo.db.photos.insert_one({
        'session_id': session_id,
        'filename': file.filename,
        'metadata': {}  # Placeholder for additional metadata
    })
    return jsonify({"message": "Photo uploaded successfully!"}), 201

# Start the Flask application
if __name__ == '__main__':
    socketio.run(app, debug=True)