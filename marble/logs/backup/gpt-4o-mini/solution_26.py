# solution.py

# Import necessary libraries
from flask import Flask, request, jsonify, session
from flask_socketio import SocketIO, emit
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import os

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SECRET_KEY'] = os.urandom(24)  # Secret key for session management
app.config['MONGO_URI'] = 'mongodb://localhost:27017/artcollab'  # MongoDB URI

# Initialize SocketIO and MongoDB
socketio = SocketIO(app)
mongo = PyMongo(app)

# User registration endpoint
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    if mongo.db.users.find_one({'username': username}):
        return jsonify({'message': 'User already exists!'}), 400
    hashed_password = generate_password_hash(password)
    mongo.db.users.insert_one({'username': username, 'password': hashed_password})
    return jsonify({'message': 'User registered successfully!'}), 201

# User login endpoint
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = mongo.db.users.find_one({'username': username})
    if user and check_password_hash(user['password'], password):
        session['user'] = username  # Store username in session
        return jsonify({'message': 'Login successful!'}), 200
    return jsonify({'message': 'Invalid credentials!'}), 401

# SocketIO event for canvas updates
@socketio.on('canvas_update')
def handle_canvas_update(data):
    # Broadcast the canvas update to all connected clients
    emit('canvas_update', data, broadcast=True)

# SocketIO event for user connection
@socketio.on('connect')
def handle_connect():
    print('User connected')

# SocketIO event for user disconnection
@socketio.on('disconnect')
def handle_disconnect():
    print('User disconnected')

# Main entry point for the application
if __name__ == '__main__':
    socketio.run(app, debug=True)

# Frontend code (React.js) would be in a separate file, but included here for completeness
# index.html
"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ArtCollab</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div id="app"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react/17.0.2/umd/react.production.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/17.0.2/umd/react-dom.production.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.0/socket.io.min.js"></script>
    <script src="app.js"></script>
</body>
</html>
"""

# app.js
"""
const socket = io.connect('http://localhost:5000');

class Canvas extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            canvasData: ''
        };
    }

    componentDidMount() {
        socket.on('canvas_update', (data) => {
            this.setState({ canvasData: data });
        });
    }

    handleCanvasChange = (data) => {
        this.setState({ canvasData: data });
        socket.emit('canvas_update', data);
    }

    render() {
        return (
            <div>
                <canvas onChange={this.handleCanvasChange}></canvas>
            </div>
        );
    }
}

ReactDOM.render(<Canvas />, document.getElementById('app'));
"""

# styles.css
"""
body {
    font-family: Arial, sans-serif;
}

canvas {
    border: 1px solid black;
    width: 100%;
    height: 500px;
}
"""