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
    """Handle a user joining an editing session."""
    session_id = data['session_id']
    username = data['username']
    join_message = f"{username} has joined the session."@socketio.on('join_session')
def handle_join_session(data):
    """Handle a user joining an editing session."""
    session_id = data['session_id']
    username = data['username']
    if session_id not in sessions:
        sessions[session_id] = {'users': []}
    sessions[session_id]['users'].append(username)
    join_message = f"{username} has joined the session."
    emit('user_joined', {'message': join_message, 'users': sessions[session_id]['users']}, room=session_id)    # Notify all users in the session
    emit('user_joined', {'message': join_message}, room=session_id)

@socketio.on('edit_photo')
def handle_edit_photo(data):
    """Handle photo editing actions."""
    session_id = data['session_id']
    edit_action = data['edit_action']
    
    # Broadcast the edit action to all users in the session
    emit('photo_edited', {'edit_action': edit_action}, room=session_id)

# Photo editing tools (placeholder for actual implementation)
@app.route('/apply_filter', methods=['POST'])
def apply_filter():
    """Apply a filter to a photo (placeholder)."""
    # In a real implementation, you would process the image here
    return jsonify({"message": "Filter applied!"}), 200

@app.route('/remove_background', methods=['POST'])
def remove_background():
    """Remove background from a photo (placeholder)."""
    # In a real implementation, you would process the image here
    return jsonify({"message": "Background removed!"}), 200

# Start the server
if __name__ == '__main__':
    socketio.run(app, debug=True)