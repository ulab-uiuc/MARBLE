# solution.py
# Importing required libraries
import socketio
import eventlet
import pymongo
from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import base64
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import json

# Creating a Flask application
app = Flask(__name__)

# Configuring MongoDB
app.config['MONGO_URI'] = 'mongodb://localhost:27017/photo-collab-editor'
mongo = PyMongo(app)

# Creating a Socket.IO application
sio = socketio.Server()
app.wsgi_app = sio

# Creating a MongoDB client
client = MongoClient('mongodb://localhost:27017/')

# Creating a database and a collection
db = client['photo-collab-editor']
collection = db['sessions']

# Function to generate a unique session ID
def generate_session_id():
    return base64.b64encode(np.random.bytes(16)).decode('utf-8')

# Function to authenticate a user
def authenticate_user(username, password):
    user = mongo.db.users.find_one({'username': username})
    if user and check_password_hash(user['password'], password):
        return user
    return None

# Function to create a new user
def create_user(username, password):
    user = mongo.db.users.find_one({'username': username})
    if user:
        return None
    hashed_password = generate_password_hash(password)
    mongo.db.users.insert_one({'username': username, 'password': hashed_password})
    return username

# Function to create a new session
def create_session(username):
    session_id = generate_session_id()
    mongo.db.sessions.insert_one({'session_id': session_id, 'username': username})
    return session_id

# Function to join a session
def join_session(session_id, username):
    session = mongo.db.sessions.find_one({'session_id': session_id})
    if session and session['username'] != username:
        return session_id
    return None

# Function to get the current session
def get_current_session(username):
    session = mongo.db.sessions.find_one({'username': username})
    if session:
        return session['session_id']
    return None

# Function to update the session
def update_session(session_id, username, photo):
    mongo.db.sessions.update_one({'session_id': session_id}, {'$set': {'photo': photo, 'username': username}})

# Function to get the current photo
def get_current_photo(session_id):
    session = mongo.db.sessions.find_one({'session_id': session_id})
    if session:
        return session['photo']
    return None

# Function to apply a filter to the photo
def apply_filter(photo, filter_name):
    # This function applies a filter to the photo using OpenCV
    # For simplicity, we will just apply a grayscale filter
    gray = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
    return gray

# Function to remove the background from the photo
def remove_background(photo):
    # This function removes the background from the photo using OpenCV
    # For simplicity, we will just remove the background by setting all pixels to white
    white = np.full(photo.shape, 255, dtype=np.uint8)
    return white

# Function to get the color palette of the photo
def get_color_palette(photo):
    # This function gets the color palette of the photo using OpenCV
    # For simplicity, we will just get the top 5 colors
    hsv = cv2.cvtColor(photo, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0], None, [180], [0, 180])
    colors = []
    for i in range(5):
        max_index = np.argmax(hist)
        colors.append((max_index, hist[max_index]))
        hist[max_index] = 0
    return colors

# Socket.IO event handlers
@sio.on('connect')
def connect(sid, environ):
    print('Client connected:', sid)

@sio.on('disconnect')
def disconnect(sid):
    print('Client disconnected:', sid)

@sio.on('create_session')
def create_session(sid, data):
    username = data['username']
    session_id = create_session(username)
    sio.emit('session_created', {'session_id': session_id}, room=sid)

@sio.on('join_session')
def join_session(sid, data):
    session_id = data['session_id']
    username = data['username']
    joined_session_id = join_session(session_id, username)
    if joined_session_id:
        sio.emit('session_joined', {'session_id': joined_session_id}, room=sid)

@sio.on('get_current_session')
def get_current_session(sid, data):
    username = data['username']
    session_id = get_current_session(username)
    if session_id:
        sio.emit('current_session', {'session_id': session_id}, room=sid)

@sio.on('update_session')
def update_session(sid, data):
    session_id = data['session_id']
    username = data['username']
    photo = data['photo']
    update_session(session_id, username, photo)
    sio.emit('session_updated', {'photo': photo}, room=sid)

@sio.on('get_current_photo')
def get_current_photo(sid, data):
    session_id = data['session_id']
    photo = get_current_photo(session_id)
    if photo:
        sio.emit('current_photo', {'photo': photo}, room=sid)

@sio.on('apply_filter')
def apply_filter(sid, data):
    session_id = data['session_id']
    filter_name = data['filter_name']
    photo = get_current_photo(session_id)
    if photo:
        filtered_photo = apply_filter(photo, filter_name)
        sio.emit('filtered_photo', {'photo': filtered_photo}, room=sid)

@sio.on('remove_background')
def remove_background(sid, data):
    session_id = data['session_id']
    photo = get_current_photo(session_id)
    if photo:
        background_removed_photo = remove_background(photo)
        sio.emit('background_removed_photo', {'photo': background_removed_photo}, room=sid)

@sio.on('get_color_palette')
def get_color_palette(sid, data):
    session_id = data['session_id']
    photo = get_current_photo(session_id)
    if photo:
        color_palette = get_color_palette(photo)
        sio.emit('color_palette', {'color_palette': color_palette}, room=sid)

# Running the application
if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)