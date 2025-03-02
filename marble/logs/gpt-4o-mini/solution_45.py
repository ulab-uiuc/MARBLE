# solution.py

# Import necessary libraries
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from collections import defaultdict
import json

# Initialize the Flask application and SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Data structure to hold notebook pages and user sessions
notebooks = defaultdict(lambda: {'pages': {}, 'history': {}, 'users': {}})

# User roles
ROLES = ['viewer', 'editor', 'admin']

# Function to create a new page in the notebook
def create_page(notebook_id, page_id):
    notebooks[notebook_id]['pages'][page_id] = {'drawings': [], 'comments': []}
    notebooks[notebook_id]['history'][page_id] = []

# Route to serve the main notebook page
@app.route('/notebook/<notebook_id>')
def notebook(notebook_id):
    # Create a default page if it doesn't exist
    if notebook_id not in notebooks:
        create_page(notebook_id, 'page1')
    return render_template('notebook.html', notebook_id=notebook_id)

# SocketIO event to handle drawing updates
@socketio.on('draw')
def handle_draw(data):@socketio.on('draw')
def handle_draw(data):
    notebook_id = data['notebook_id']
    page_id = data['page_id']
    drawing = data['drawing']
    user_id = data['user_id']
    role = notebooks[notebook_id]['users'].get(user_id, 'viewer')
    if role in ['editor', 'admin']:
        # Append the drawing to the page's drawings
        notebooks[notebook_id]['pages'][page_id]['drawings'].append(drawing)
        # Emit the drawing to all connected clients
        emit('draw', data, broadcast=True)    # Emit the drawing to all connected clients
    emit('draw', data, broadcast=True)

# SocketIO event to handle comments
@socketio.on('comment')
def handle_comment(data):@socketio.on('comment')
def handle_comment(data):
    notebook_id = data['notebook_id']
    page_id = data['page_id']
    comment = data['comment']
    user_id = data['user_id']
    role = notebooks[notebook_id]['users'].get(user_id, 'viewer')
    if role in ['editor', 'admin']:
        # Append the comment to the page's comments
        notebooks[notebook_id]['pages'][page_id]['comments'].append(comment)
        # Emit the comment to all connected clients
        emit('comment', data, broadcast=True)    # Emit the comment to all connected clients
    emit('comment', data, broadcast=True)

# SocketIO event to handle user joining
@socketio.on('join')
def handle_join(data):
    notebook_id = data['notebook_id']
    user_id = data['user_id']
    role = data['role']
    
    # Add user to the notebook's user list
    notebooks[notebook_id]['users'][user_id] = role
    
    # Notify all users in the notebook
    emit('user_joined', {'user_id': user_id, 'role': role}, broadcast=True)

# SocketIO event to handle page switching
@socketio.on('switch_page')
def handle_switch_page(data):
    notebook_id = data['notebook_id']
    page_id = data['page_id']
    
    # Emit the page switch to all connected clients
    emit('switch_page', {'page_id': page_id}, broadcast=True)

# Function to save the notebook state
def save_notebook(notebook_id):
    with open(f'{notebook_id}.json', 'w') as f:
        json.dump(notebooks[notebook_id], f)

# SocketIO event to handle saving the notebook
@socketio.on('save_notebook')
def handle_save_notebook(data):
    notebook_id = data['notebook_id']
    save_notebook(notebook_id)
    emit('notebook_saved', {'notebook_id': notebook_id}, broadcast=True)

# Main entry point to run the application
if __name__ == '__main__':
    socketio.run(app, debug=True)