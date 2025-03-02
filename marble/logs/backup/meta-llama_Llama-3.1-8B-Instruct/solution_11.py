# solution.py
# Importing required libraries
import pymongo
from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import json
from bson import ObjectId
import random

# Creating a Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/culturalconnect'

# Initializing the Flask-PyMongo extension
mongo = PyMongo(app)

# Initializing the Flask-Login extension
login_manager = LoginManager()
login_manager.init_app(app)

# Initializing the Flask-SocketIO extension
socketio = SocketIO(app)

# Defining a User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = generate_password_hash(password)

    @classmethod
    def get(cls, user_id):
        user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        return cls(user['_id'], user['username'], user['password'])

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Loading the user from the user ID
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Defining a route for user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User(None, username, password)
    mongo.db.users.insert_one({'username': username, 'password': user.password})
    return jsonify({'message': 'User created successfully'}), 201

# Defining a route for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = mongo.db.users.find_one({'username': username})
    if user and user['password'] == password:
        user_obj = User(user['_id'], username, user['password'])
        login_user(user_obj)
        return jsonify({'message': 'User logged in successfully'}), 200
    return jsonify({'message': 'Invalid username or password'}), 401

# Defining a route for user logout
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'User logged out successfully'}), 200

# Defining a route for getting user data
@app.route('/user', methods=['GET'])
@login_required
def get_user():
    user = mongo.db.users.find_one({'_id': current_user.id})
    return jsonify({'username': user['username']}), 200

# Defining a route for creating a new cultural content
@app.route('/content', methods=['POST'])
@login_required
def create_content():
    data = request.get_json()
    title = data['title']
    description = data['description']
    cultural_content = {
        'title': title,
        'description': description,
        'user_id': current_user.id
    }
    mongo.db.content.insert_one(cultural_content)
    return jsonify({'message': 'Cultural content created successfully'}), 201

# Defining a route for getting cultural content
@app.route('/content', methods=['GET'])
@login_required
def get_content():
    content = mongo.db.content.find({'user_id': current_user.id})
    return jsonify([{'title': item['title'], 'description': item['description']} for item in content]), 200

# Defining a route for creating a new recommendation
@app.route('/recommendation', methods=['POST'])
@login_required
def create_recommendation():
    data = request.get_json()
    content_id = data['content_id']
    recommendation = {
        'content_id': content_id,
        'user_id': current_user.id
    }
    mongo.db.recommendations.insert_one(recommendation)
    return jsonify({'message': 'Recommendation created successfully'}), 201

# Defining a route for getting recommendations
@app.route('/recommendations', methods=['GET'])
@login_required
def get_recommendations():
    recommendations = mongo.db.recommendations.find({'user_id': current_user.id})
    return jsonify([{'content_id': item['content_id']} for item in recommendations]), 200

# Defining a route for creating a new chat message
@app.route('/chat', methods=['POST'])
@login_required
def create_chat():
    data = request.get_json()
    message = data['message']
    chat_message = {
        'message': message,
        'user_id': current_user.id
    }
    mongo.db.chat.insert_one(chat_message)
    return jsonify({'message': 'Chat message created successfully'}), 201

# Defining a route for getting chat messages
@app.route('/chat', methods=['GET'])
@login_required
def get_chat():
    chat = mongo.db.chat.find({'user_id': current_user.id})
    return jsonify([{'message': item['message']} for item in chat]), 200

# Defining a function for generating recommendations
def generate_recommendations():
    # Get all content
    content = mongo.db.content.find()
    # Get all recommendations
    recommendations = mongo.db.recommendations.find()
    # Create a dictionary to store recommendations
    recommendation_dict = {}
    # Iterate over content
    for item in content:
        # Get all recommendations for the current content
        item_recommendations = [recommendation['content_id'] for recommendation in recommendations if recommendation['content_id'] == item['_id']]
        # Add recommendations to the dictionary
        recommendation_dict[item['_id']] = item_recommendations
    # Return the dictionary
    return recommendation_dict

# Defining a function for sending recommendations to the client
@socketio.on('connect')
def connect():
    # Generate recommendations
    recommendations = generate_recommendations()
    # Emit recommendations to the client
    emit('recommendations', recommendations)

# Running the application
if __name__ == '__main__':
    socketio.run(app, debug=True)