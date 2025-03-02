# solution.py
# Importing necessary libraries
import pymongo
from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import json
from bson import ObjectId
from datetime import datetime, timedelta

# Creating a Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/culturalconnect'
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!

# Initializing the Flask application with extensions
jwt = JWTManager(app)
mongo = PyMongo(app)
socketio = SocketIO(app, cors_allowed_origins='*')
CORS(app)

# Creating a MongoDB client
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Defining a function to create a new user
def create_user(username, email, password):def create_user(form):
    if form.validate():
        user = {
            'username': form.username.data,
            'email': form.email.data,
            'password': bcrypt.generate_password_hash(form.password.data).decode('utf-8'),
            'created_at': datetime.utcnow()
        }
        mongo.db.users.insert_one(user)
        return user
    else:
        return Nonedef create_user(form):
    if form.validate():
        user = {
            'username': form.username.data,
            'email': form.email.data,
            'password': bcrypt.generate_password_hash(form.password.data).decode('utf-8'),
            'created_at': datetime.utcnow()
        }
        mongo.db.users.insert_one(user)
        return user
    else:
        return None    user = {
        'username': username,
        'email': email,
        'password': bcrypt.generate_password_hash(password).decode('utf-8'),
        'created_at': datetime.utcnow()
    }
    mongo.db.users.insert_one(user)
    return user    user = {
        'username': username,
        'email': email,
        'password': password,
        'created_at': datetime.utcnow()
    }
    mongo.db.users.insert_one(user)
    return user

# Defining a function to authenticate a user
def authenticate_user(username, password):
    user = mongo.db.users.find_one({'username': username, 'password': password})
    if user:
        return user
    return None

# Defining a function to get a user's profile
def get_user_profile(username):
    user = mongo.db.users.find_one({'username': username})
    if user:
        return user
    return None

# Defining a function to create a new cultural content item
def create_content(title, description, type):
    content = {
        'title': title,
        'description': description,
        'type': type,
        'created_at': datetime.utcnow()
    }
    mongo.db.content.insert_one(content)
    return content

# Defining a function to get a cultural content item
def get_content(id):
    content = mongo.db.content.find_one({'_id': ObjectId(id)})
    if content:
        return content
    return None

# Defining a function to create a new recommendation
def create_recommendation(user_id, content_id):
    recommendation = {
        'user_id': user_id,
        'content_id': content_id,
        'created_at': datetime.utcnow()
    }
    mongo.db.recommendations.insert_one(recommendation)
    return recommendation

# Defining a function to get a user's recommendations
def get_recommendations(user_id):
    recommendations = mongo.db.recommendations.find({'user_id': user_id})
    if recommendations:
        return recommendations
    return None

# Defining a function to create a new chat message
def create_message(user_id, message):
    message = {
        'user_id': user_id,
        'message': message,
        'created_at': datetime.utcnow()
    }
    mongo.db.messages.insert_one(message)
    return message

# Defining a function to get a user's chat messages
def get_messages(user_id):
    messages = mongo.db.messages.find({'user_id': user_id})
    if messages:
        return messages
    return None

# Defining a route for user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    user = create_user(username, email, password)
    return jsonify({'message': 'User created successfully'}), 201

# Defining a route for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = authenticate_user(username, password)
    if user:
        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

# Defining a route for getting a user's profile
@app.route('/profile', methods=['GET'])
@jwt_required
def get_profile():
    username = get_jwt_identity()
    user = get_user_profile(username)
    if user:
        return jsonify(user), 200
    return jsonify({'message': 'User not found'}), 404

# Defining a route for creating a new cultural content item
@app.route('/content', methods=['POST'])
@jwt_required
def create_content_item():
    data = request.get_json()
    title = data['title']
    description = data['description']
    type = data['type']
    content = create_content(title, description, type)
    return jsonify(content), 201

# Defining a route for getting a cultural content item
@app.route('/content/<id>', methods=['GET'])
def get_content_item(id):
    content = get_content(id)
    if content:
        return jsonify(content), 200
    return jsonify({'message': 'Content not found'}), 404

# Defining a route for creating a new recommendation
@app.route('/recommendation', methods=['POST'])
@jwt_required
def create_recommendation_item():
    data = request.get_json()
    user_id = data['user_id']
    content_id = data['content_id']
    recommendation = create_recommendation(user_id, content_id)
    return jsonify(recommendation), 201

# Defining a route for getting a user's recommendations
@app.route('/recommendations', methods=['GET'])
@jwt_required
def get_recommendations_item():
    user_id = get_jwt_identity()
    recommendations = get_recommendations(user_id)
    if recommendations:
        return jsonify(list(recommendations)), 200
    return jsonify({'message': 'Recommendations not found'}), 404

# Defining a route for creating a new chat message
@app.route('/message', methods=['POST'])
@jwt_required
def create_message_item():
    data = request.get_json()
    user_id = data['user_id']
    message = data['message']
    message = create_message(user_id, message)
    return jsonify(message), 201

# Defining a route for getting a user's chat messages
@app.route('/messages', methods=['GET'])
@jwt_required
def get_messages_item():
    user_id = get_jwt_identity()
    messages = get_messages(user_id)
    if messages:
        return jsonify(list(messages)), 200
    return jsonify({'message': 'Messages not found'}), 404

# Defining a route for real-time chat messages
@socketio.on('message')
def handle_message(data):
    user_id = data['user_id']
    message = data['message']
    message = create_message(user_id, message)
    emit('message', message, broadcast=True)

# Running the Flask application
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)