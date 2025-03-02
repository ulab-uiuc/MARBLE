# solution.py

# This file contains the implementation of the CulturalConnect web application.
# The application consists of a backend built with Flask, which handles user authentication,
# content management, and real-time chat functionality using WebSockets.

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from bson.json_util import dumps
import bcrypt
import jwt
import datetime

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing
app.config["MONGO_URI"] = "mongodb://localhost:27017/culturalconnect"  # MongoDB URI
mongo = PyMongo(app)
socketio = SocketIO(app)

# Secret key for JWT encoding and decoding
app.config['SECRET_KEY'] = 'your_secret_key'

# User registration endpoint
@app.route('/register', methods=['POST'])
def register():
    # Get user data from the request
    username = request.json.get('username')
    password = request.json.get('password')
    
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Store user in the databaseif mongo.db.users.find_one({'username': username}):
        return jsonify({"message": "Username already exists!"}), 400
    
    # Store user in the database
    mongo.db.users.insert_one({
        'username': username,
        'password': hashed_password.decode('utf-8')
    })    return jsonify({"message": "User registered successfully!"}), 201

# User login endpoint
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    # Fetch user from the database
    user = mongo.db.users.find_one({'username': username})
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        # Create JWT token
        token = jwt.encode({
            'user_id': str(user['_id']),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'])
        
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid credentials!"}), 401

# Endpoint to get cultural content
@app.route('/content', methods=['GET'])
def get_content():
    # Fetch cultural content from the database
    content = mongo.db.content.find()
    return dumps(content), 200

# WebSocket for real-time chat
@socketio.on('message')
def handle_message(data):
    # Broadcast the message to all connected clients
    emit('message', data, broadcast=True)

# Run the application
if __name__ == '__main__':
    socketio.run(app, debug=True)

# Note: This is a simplified version of the backend. 
# The frontend should be built using React.js and should handle user authentication,
# display personalized content, and allow users to explore and share cultural content.
# The recommendation system and chat feature should be integrated into the frontend as well.