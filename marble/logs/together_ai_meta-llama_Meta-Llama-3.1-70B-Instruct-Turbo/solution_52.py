# photo_collab_editor.py

import os
import json
import socketio
import eventlet
import pymongo
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from PIL import Image
from io import BytesIO
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

# Initialize Flask and SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)
sio = SocketIO(app, cors_allowed_origins='*')

# Initialize MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["photo_collab_editor"]
users_collection = db["users"]
sessions_collection = db["sessions"]

# Load machine learning models
background_removal_model = load_model('background_removal_model.h5')
color_palette_model = load_model('color_palette_model.h5')

# Define a function to handle user authentication
def authenticate_user(username, password):
    user = users_collection.find_one({'username': username, 'password': password})
    if user:
        return user['_id']
    else:
        return None

# Define a function to handle session creation
def create_session(session_name, user_id):
    session = sessions_collection.find_one({'session_name': session_name})
    if session:
        return None
    else:
        sessions_collection.insert_one({'session_name': session_name, 'user_id': user_id, 'users': [user_id]})
        return session_name

# Define a function to handle session joining
def join_session(session_name, user_id):
    session = sessions_collection.find_one({'session_name': session_name})
    if session and user_id not in session['users']:
        sessions_collection.update_one({'session_name': session_name}, {'$push': {'users': user_id}})
        return True
    else:
        return False

# Define a function to handle photo uploading
def upload_photo(photo, session_name):
    # Save the photo to the server
    photo.save('photos/' + session_name + '.jpg')
    return 'photos/' + session_name + '.jpg'

# Define a function to handle photo editing
def edit_photo(photo, session_name, editing_action):
    # Load the photo
    image = Image.open(photo)
    # Apply the editing action
    if editing_action['action'] == 'filter':
        # Apply a filter to the photo
        image = image.filter(ImageFilter.GaussianBlur(radius=5))
    elif editing_action['action'] == 'color_adjustment':
        # Adjust the colors of the photo
        image = image.convert('RGB')
        pixels = image.load()
        for x in range(image.size[0]):
            for y in range(image.size[1]):
                r, g, b = pixels[x, y]
                r = int(r * editing_action['red'])
                g = int(g * editing_action['green'])
                b = int(b * editing_action['blue'])
                pixels[x, y] = (r, g, b)
    elif editing_action['action'] == 'background_removal':
        # Remove the background of the photo using machine learning
        image_array = img_to_array(image)
        image_array = np.expand_dims(image_array, axis=0)
        prediction = background_removal_model.predict(image_array)
        image = Image.fromarray(prediction[0].astype(np.uint8))
    # Save the edited photo
    image.save('photos/' + session_name + '_edited.jpg')
    return 'photos/' + session_name + '_edited.jpg'

# Define a function to handle real-time collaboration
def handle_collaboration(session_name, user_id, editing_action):
    # Get the session
    session = sessions_collection.find_one({'session_name': session_name})
    # Check if the user is in the session
    if user_id in session['users']:
        # Apply the editing action to the photo
        edited_photo = edit_photo('photos/' + session_name + '.jpg', session_name, editing_action)
        # Emit the edited photo to all users in the session
        sio.emit('edited_photo', {'photo': edited_photo}, room=session_name)
    else:
        # The user is not in the session
        sio.emit('error', {'message': 'You are not in this session'}, room=user_id)

# Define SocketIO events
@sio.on('connect')
def connect():
    print('Client connected')

@sio.on('disconnect')
def disconnect():
    print('Client disconnected')

@sio.on('authenticate_user')
def authenticate_user_event(data):
    username = data['username']
    password = data['password']
    user_id = authenticate_user(username, password)
    if user_id:
        sio.emit('authenticated', {'user_id': user_id})
    else:
        sio.emit('error', {'message': 'Invalid username or password'})

@sio.on('create_session')
def create_session_event(data):
    session_name = data['session_name']
    user_id = data['user_id']
    session_name = create_session(session_name, user_id)
    if session_name:
        sio.emit('session_created', {'session_name': session_name})
    else:
        sio.emit('error', {'message': 'Session already exists'})

@sio.on('join_session')
def join_session_event(data):
    session_name = data['session_name']
    user_id = data['user_id']
    if join_session(session_name, user_id):
        sio.emit('session_joined', {'session_name': session_name})
    else:
        sio.emit('error', {'message': 'You are already in this session'})

@sio.on('upload_photo')
def upload_photo_event(data):
    photo = data['photo']
    session_name = data['session_name']
    photo_path = upload_photo(photo, session_name)
    sio.emit('photo_uploaded', {'photo_path': photo_path})

@sio.on('edit_photo')
def edit_photo_event(data):
    photo = data['photo']
    session_name = data['session_name']
    editing_action = data['editing_action']
    edited_photo = edit_photo(photo, session_name, editing_action)
    sio.emit('photo_edited', {'edited_photo': edited_photo})

@sio.on('collaborate')
def collaborate_event(data):
    session_name = data['session_name']
    user_id = data['user_id']
    editing_action = data['editing_action']
    handle_collaboration(session_name, user_id, editing_action)

if __name__ == '__main__':
    sio.run(app, host='localhost', port=5000)