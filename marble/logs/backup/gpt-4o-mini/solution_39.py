# solution.py

# Import necessary libraries
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

# Initialize the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music_collaborator.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
socketio = SocketIO(app)

# Database model for User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

# Database model for Project
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    users = db.relationship('User', secondary='project_user', backref='projects')

# Association table for many-to-many relationship between Users and Projects
project_user = db.Table('project_user',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'))
)

# Database model for Composition
class Composition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    version = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint for user login
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
    return jsonify({'user_id': user.id, 'username': user.username})

# API endpoint for creating a new project
@app.route('/projects', methods=['POST'])
def create_project():
    title = request.json.get('title')
    project = Project(title=title)
    db.session.add(project)
    db.session.commit()
    return jsonify({'project_id': project.id, 'title': project.title})

# Socket event for real-time collaboration
@socketio.on('collaborate')
def handle_collaboration(data):
    emit('update', data, broadcast=True)

# API endpoint for saving a composition
@app.route('/compositions', methods=['POST'])
def save_composition():
    project_id = request.json.get('project_id')
    content = request.json.get('content')
    composition = Composition(project_id=project_id, content=content)
    db.session.add(composition)existing_composition = Composition.query.filter_by(project_id=project_id).order_by(Composition.version.desc()).first()
if existing_composition:
    version = existing_composition.version + 1
else:
    version = 1
composition = Composition(project_id=project_id, content=content, version=version)    db.session.commit()
    return jsonify({'composition_id': composition.id})

# API endpoint for retrieving compositions
@app.route('/compositions/<int:project_id>', methods=['GET'])
def get_compositions(project_id):
    compositions = Composition.query.filter_by(project_id=project_id).all()
    return jsonify([{'id': comp.id, 'content': comp.content, 'version': comp.version} for comp in compositions])

# Main entry point for the application
if __name__ == '__main__':
    db.create_all()  # Create database tables
    socketio.run(app, debug=True)  # Run the application with SocketIO support