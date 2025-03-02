
client = MongoClient('mongodb://localhost:27017/')
db = client['PhotoCollabEditorDB']# PhotoCollabEditor - Real-time collaborative photo editing system

# Import necessary libraries
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

# Store user sessions, photo metadata, and editing actions in memory (for demo purposes)sessions = db['user_sessions']
photos = db['photo_metadata']
editing_actions = db['editing_actions']
from pymongo import MongoClient# Route for the main page
client = MongoClient('mongodb://localhost:27017/')
db = client['PhotoCollabEditorDB']
from pymongo import MongoClient
@app.route('/')
def index():
    return render_template('index.html')

# SocketIO event for handling client connections
@socketio.on('connect')
def handle_connect():
    print('Client connected')

# SocketIO event for handling client disconnections
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# SocketIO event for handling photo upload
@socketio.on('upload_photo')
def handle_upload_photo(data):
    photo_id = data['photo_id']
    photo_data = data['photo_data']
    photos[photo_id] = photo_data
    emit('photo_uploaded', {'photo_id': photo_id}, broadcast=True)

# SocketIO event for handling editing actions
@socketio.on('edit_photo')
def handle_edit_photo(data):
    photo_id = data['photo_id']
    edit_action = data['edit_action']
    if photo_id in editing_actions:
        editing_actions[photo_id].append(edit_action)
    else:
        editing_actions[photo_id] = [edit_action]
    emit('photo_edited', {'photo_id': photo_id, 'edit_action': edit_action}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)