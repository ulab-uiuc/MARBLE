# solution.py

# Import necessary libraries
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///photo_collab.db'
db = SQLAlchemy(app)
socketio = SocketIO(app)

# User model for authentication
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Project model for photo projects
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    users = db.relationship('User', secondary='project_user', backref='projects')

# Association table for many-to-many relationship between users and projects
project_user = db.Table('project_user',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'))
)

# Initialize the database
@app.before_first_request
def create_tables():
    db.create_all()

# User registration route
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

# User login route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        session['user_id'] = user.id
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

# Create a new project route
@app.route('/projects', methods=['POST'])
def create_project():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    data = request.json
    new_project = Project(title=data['title'], owner_id=session['user_id'])
    db.session.add(new_project)
    db.session.commit()
    return jsonify({'message': 'Project created successfully'}), 201

# Real-time collaboration using SocketIO
@socketio.on('edit_project')
def handle_edit(data):
    # Broadcast the edit to all users in the project
    emit('project_updated', data, broadcast=True)

# Run the application
if __name__ == '__main__':
    socketio.run(app, debug=True)

# Note: The above code provides a basic structure for user authentication, project creation, and real-time collaboration.
# Additional features such as photo editing tools, version control, and a user interface would need to be implemented separately.