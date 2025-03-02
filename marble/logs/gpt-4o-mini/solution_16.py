# solution.py

# Import necessary libraries
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import git
import os

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)
login_manager = LoginManager(app)

# In-memory user storage for demonstration purposes
users = {}

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

# Load user for Flask-Login
@login_manager.user_loader
def load_user(username):
    return users.get(username)

# Route for the main dashboard
@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Route for user registration
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if username not in users:
        users[username] = User(username, password)
        return jsonify({'message': 'User registered successfully!'}), 201
    return jsonify({'message': 'User already exists!'}), 400

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = load_user(username)
    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({'message': 'Logged in successfully!'}), 200
    return jsonify({'message': 'Invalid credentials!'}), 401

# Route for user logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully!'}), 200

# Real-time code sharing and annotation
@socketio.on('code_update')
def handle_code_update(data):
    username = current_user.username if current_user.is_authenticated else 'Anonymous'
    data['username'] = username# Real-time chat functionality
@socketio.on('chat_message')
def handle_chat_message(data):
    username = current_user.username if current_user.is_authenticated else 'Anonymous'
    data['username'] = username# Version control integration (Git)
@app.route('/git/pull', methods=['POST'])
@login_required
def git_pull():
    repo_path = request.form['repo_path']
    try:
        repo = git.Repo(repo_path)
        repo.git.pull()
        return jsonify({'message': 'Repository pulled successfully!'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/git/push', methods=['POST'])
@login_required
def git_push():
    repo_path = request.form['repo_path']
    try:
        repo = git.Repo(repo_path)
        repo.git.add(A=True)
        repo.git.commit(m='Code changes')
        repo.git.push()
        return jsonify({'message': 'Changes pushed successfully!'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Run the application
if __name__ == '__main__':
    socketio.run(app, debug=True)