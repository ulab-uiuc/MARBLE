# solution.py

# Import necessary libraries
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from PIL import Image, ImageEnhance
import io
import base64
import json

# Initialize Flask application and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Global variable to store the current state of the photo and its history
photo_state = None
photo_history = []
comments = []

# Function to load the initial photo
def load_initial_photo():
    global photo_state
    # Load a sample image (you can replace this with your own image)
    img = Image.new('RGB', (800, 600), color='white')
    photo_state = img

# Route to serve the main page
@app.route('/')
def index():
    return render_template('index.html')

# SocketIO event to handle photo edits
@socketio.on('edit_photo')
def handle_edit(data):
    global photo_state
    # Apply edits based on user input
    if data['action'] == 'brightness':
        enhancer = ImageEnhance.Brightness(photo_state)
        photo_state = enhancer.enhance(data['value'])
    elif data['action'] == 'contrast':
        enhancer = ImageEnhance.Contrast(photo_state)
        photo_state = enhancer.enhance(data['value'])
    
    # Save the current state to history
    save_to_history()
    
    # Emit the updated photo to all clients
    emit('photo_updated', {'photo': encode_image(photo_state)}, broadcast=True)

# Function to encode image to base64
def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Function to save the current state to history
def save_to_history():
    global photo_history
    photo_history.append(encode_image(photo_state))

# SocketIO event to handle comments
@socketio.on('add_comment')
def handle_comment(data):
    comments.append(data)
    emit('comment_added', data, broadcast=True)

# SocketIO event to handle version control
    suggestions = generate_suggestions(data['comment'])
    emit('suggestions', {'suggestions': suggestions}, broadcast=True)
@socketio.on('revert_photo')
def handle_revert(data):
    global photo_state
    if data['version'] < len(photo_history):
        photo_state = decode_image(photo_history[data['version']])
        emit('photo_updated', {'photo': encode_image(photo_state)}, broadcast=True)

# Function to decode base64 image
def decode_image(data):
    image_data = base64.b64decode(data)
    return Image.open(io.BytesIO(image_data))

# Load the initial photo when the application starts

load_initial_photo()

# Run the application
if __name__ == '__main__':
    socketio.run(app, debug=True)