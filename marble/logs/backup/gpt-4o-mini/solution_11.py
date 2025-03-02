// This file contains the implementation of the CulturalConnect web application.
// The application consists of a backend built with Node.js and Express, which handles user authentication,
// content management, and real-time chat functionality.

const express = require('express');
const mongoose = require('mongoose');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');
const bcrypt = require('bcrypt');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

app.use(cors());
app.use(express.json());

// Connect to MongoDB
mongoose.connect(process.env.MONGO_URI || 'mongodb://localhost:27017/culturalconnect', { useNewUrlParser: true, useUnifiedTopology: true });

const userSchema = new mongoose.Schema({
    username: String,
    password: String
});
const User = mongoose.model('User', userSchema);

const contentSchema = new mongoose.Schema({
    title: String,
    description: String
});
const Content = mongoose.model('Content', contentSchema);

// User registration endpoint
app.post('/register', async (req, res) => {
    const { username, password } = req.body;
    const hashedPassword = await bcrypt.hash(password, 10);
    const user = new User({ username, password: hashedPassword });
    await user.save();
    res.status(201).json({ message: 'User registered successfully!' });
});

// User login endpoint
app.post('/login', async (req, res) => {
    const { username, password } = req.body;
    const user = await User.findOne({ username });
    if (user && await bcrypt.compare(password, user.password)) {
        res.status(200).json({ message: 'Login successful!' });
    } else {
        res.status(401).json({ message: 'Invalid credentials!' });
    }
});

// Endpoint to get cultural content
app.get('/content', async (req, res) => {
    const content = await Content.find();
    res.status(200).json(content);
});

// Endpoint to add cultural content
app.post('/content', async (req, res) => {
    const { title, description } = req.body;
    const content = new Content({ title, description });
    await content.save();
    res.status(201).json({ message: 'Content added successfully!' });
});

// WebSocket event for chat
io.on('connection', (socket) => {
    socket.on('message', (data) => {
        io.emit('message', data);
    });
});

// Run the application
const PORT = process.env.PORT || 5000;
server.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

// Note: This is a simplified version of the backend. 
// The frontend would be built using React.js and would interact with these endpoints.
// The recommendation system and additional features would require further implementation.# solution.py

# This file contains the implementation of the CulturalConnect web application.
# The application consists of a backend built with Flask, which handles user authentication,
# content management, and real-time chat functionality.

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure MongoDB
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/culturalconnect")
mongo = PyMongo(app)

# Initialize SocketIO for real-time communication
socketio = SocketIO(app)

# User registration endpoint
@app.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    username = request.json.get('username')
    password = request.json.get('password')
    
    # Hash the password for security
    hashed_password = generate_password_hash(password)
    
    # Store user in the database
    mongo.db.users.insert_one({
        'username': username,
        'password': hashed_password
    })
    
    return jsonify({"message": "User registered successfully!"}), 201

# User login endpoint
@app.route('/login', methods=['POST'])
def login():
    """Authenticate a user."""
    username = request.json.get('username')
    password = request.json.get('password')
    
    user = mongo.db.users.find_one({'username': username})
    
    if user and check_password_hash(user['password'], password):
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"message": "Invalid credentials!"}), 401

# Endpoint to get cultural content
@app.route('/content', methods=['GET'])
def get_content():
    """Retrieve cultural content from the database."""
    content = list(mongo.db.content.find())
    return jsonify(content), 200

# Endpoint to add cultural content
@app.route('/content', methods=['POST'])
def add_content():
    """Add new cultural content."""
    title = request.json.get('title')
    description = request.json.get('description')
    
    mongo.db.content.insert_one({
        'title': title,
        'description': description
    })
    
    return jsonify({"message": "Content added successfully!"}), 201

# WebSocket event for chat
@socketio.on('message')
def handle_message(data):
    """Handle incoming chat messages."""
    emit('message', data, broadcast=True)

# Run the application
if __name__ == '__main__':
    socketio.run(app, debug=True)

# Note: This is a simplified version of the backend. 
# The frontend would be built using React.js and would interact with these endpoints.
# The recommendation system and additional features would require further implementation.