# solution.py

# Import necessary libraries
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO, emit
from datetime import datetime
import os

# Initialize the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_collaborator.db'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
socketio = SocketIO(app)

# User model for authentication and profile management
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    itineraries = db.relationship('Itinerary', backref='owner', lazy=True)

# Itinerary model for itinerary creation and management
class Itinerary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    activities = db.relationship('Activity', backref='itinerary', lazy=True)

# Activity model for managing activities within itineraries
class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itinerary.id'), nullable=False)

# Initialize the database
@app.before_first_request
def create_tables():
    db.create_all()

# User registration endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({"message": "Username already taken!"}), 400
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()    return jsonify({"message": "User registered successfully!"}), 201

# User login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        session['user_id'] = user.id
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"message": "Invalid credentials!"}), 401

# Itinerary creation endpoint
@app.route('/itinerary', methods=['POST'])
def create_itinerary():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized!"}), 401
    data = request.get_json()
    new_itinerary = Itinerary(title=data['title'], user_id=session['user_id'])
    db.session.add(new_itinerary)
    db.session.commit()
    return jsonify({"message": "Itinerary created successfully!"}), 201

# Activity addition endpoint
@app.route('/itinerary/<int:itinerary_id>/activity', methods=['POST'])
def add_activity(itinerary_id):
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized!"}), 401
    data = request.get_json()
    new_activity = Activity(name=data['name'], date_time=datetime.strptime(data['date_time'], '%Y-%m-%d %H:%M:%S'), itinerary_id=itinerary_id)
    db.session.add(new_activity)
    db.session.commit()
    return jsonify({"message": "Activity added successfully!"}), 201

# SocketIO for real-time communication
@socketio.on('message')
def handle_message(data):
    emit('message', data, broadcast=True)

# Run the application
if __name__ == '__main__':
    socketio.run(app, debug=True)