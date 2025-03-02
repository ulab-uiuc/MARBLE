# solution.py

# Import required libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, emit
import os

# Create the Flask app
app = Flask(__name__)

# Configure the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cultural_exchange_hub.db'
app.config['SECRET_KEY'] = 'secret_key'

# Initialize the database
db = SQLAlchemy(app)

# Initialize the marshmallow
ma = Marshmallow(app)

# Initialize the bcrypt
bcrypt = Bcrypt(app)

# Initialize the login manager
login_manager = LoginManager(app)

# Initialize the socketio
socketio = SocketIO(app)

# Define the User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    profile_picture = db.Column(db.String(120), nullable=True)
    cultural_background = db.Column(db.String(120), nullable=True)
    interests = db.Column(db.String(120), nullable=True)

    def __init__(self, username, email, password, profile_picture=None, cultural_background=None, interests=None):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.profile_picture = profile_picture
        self.cultural_background = cultural_background
        self.interests = interests

# Define the VirtualTour model
class VirtualTour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    model_url = db.Column(db.String(120), nullable=False)
    hotspots = db.relationship('Hotspot', backref='virtual_tour', lazy=True)

    def __init__(self, name, description, model_url):
        self.name = name
        self.description = description
        self.model_url = model_url

# Define the Hotspot model
class Hotspot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    audio_guide = db.Column(db.String(120), nullable=False)
    virtual_tour_id = db.Column(db.Integer, db.ForeignKey('virtual_tour.id'), nullable=False)

    def __init__(self, name, description, audio_guide, virtual_tour_id):
        self.name = name
        self.description = description
        self.audio_guide = audio_guide
        self.virtual_tour_id = virtual_tour_id

# Define the LanguageExchange model
class LanguageExchange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    language1 = db.Column(db.String(120), nullable=False)
    language2 = db.Column(db.String(120), nullable=False)

    def __init__(self, user1_id, user2_id, language1, language2):
        self.user1_id = user1_id
        self.user2_id = user2_id
        self.language1 = language1
        self.language2 = language2

# Define the CulturalWorkshop model
class CulturalWorkshop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    session_url = db.Column(db.String(120), nullable=False)
    expert_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, description, session_url, expert_id):
        self.name = name
        self.description = description
        self.session_url = session_url
        self.expert_id = expert_id

# Define the Feedback model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    virtual_tour_id = db.Column(db.Integer, db.ForeignKey('virtual_tour.id'), nullable=True)
    language_exchange_id = db.Column(db.Integer, db.ForeignKey('language_exchange.id'), nullable=True)
    cultural_workshop_id = db.Column(db.Integer, db.ForeignKey('cultural_workshop.id'), nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(120), nullable=False)

    def __init__(self, user_id, virtual_tour_id=None, language_exchange_id=None, cultural_workshop_id=None, rating=None, review=None):
        self.user_id = user_id
        self.virtual_tour_id = virtual_tour_id
        self.language_exchange_id = language_exchange_id
        self.cultural_workshop_id = cultural_workshop_id
        self.rating = rating
        self.review = review

# Define the schema for the User model
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

# Define the schema for the VirtualTour model
class VirtualTourSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = VirtualTour
        load_instance = True

# Define the schema for the Hotspot model
class HotspotSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Hotspot
        load_instance = True

# Define the schema for the LanguageExchange model
class LanguageExchangeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LanguageExchange
        load_instance = True

# Define the schema for the CulturalWorkshop model
class CulturalWorkshopSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CulturalWorkshop
        load_instance = True

# Define the schema for the Feedback model
class FeedbackSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Feedback
        load_instance = True

# Create the user registration route
@app.route('/register', methods=['POST'])
def register():
    # Get the data from the request
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    profile_picture = data.get('profile_picture')
    cultural_background = data.get('cultural_background')
    interests = data.get('interests')

    # Create a new user
    user = User(username, email, password, profile_picture, cultural_background, interests)
    db.session.add(user)
    db.session.commit()

    # Return a success message
    return jsonify({'message': 'User created successfully'}), 201

# Create the user login route
@app.route('/login', methods=['POST'])
def login():
    # Get the data from the request
    data = request.get_json()
    email = data['email']
    password = data['password']

    # Find the user
    user = User.query.filter_by(email=email).first()

    # Check if the user exists and the password is correct
    if user and bcrypt.check_password_hash(user.password, password):
        # Login the user
        login_user(user)
        return jsonify({'message': 'User logged in successfully'}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

# Create the virtual tour routedef create_virtual_tour():
    # Check if the current user is authorized to create a virtual tour
    if not current_user.is_authenticated:
        return jsonify({'message': 'Unauthorized'}), 401# Get the data from the request
    data = request.get_json()
    name = data['name']
    description = data['description']
    model_url = data['model_url']

    # Create a new virtual tour
    virtual_tour = VirtualTour(name, description, model_url)
    db.session.add(virtual_tour)
    db.session.commit()

    # Return a success message
    return jsonify({'message': 'Virtual tour created successfully'}), 201

# Create the language exchange route
@app.route('/virtual-tours', methods=['POST'])
@login_required
def create_virtual_tour():
    # Check if the current user is authorized to create a virtual tour
    if not current_user.is_authenticated:
        return jsonify({'message': 'Unauthorized'}), 401
    # Get the data from the request
    data = request.get_json()
    name = data['name']
    description = data['description']
    model_url = data['model_url']
    # Create a new virtual tour
    virtual_tour = VirtualTour(name, description, model_url)
    db.session.add(virtual_tour)
    db.session.commit()
    # Return a success message
    return jsonify({'message': 'Virtual tour created successfully'}), 201
@app.route('/language-exchanges', methods=['POST'])
@login_required
def create_language_exchange():data = request.get_json()
user1_id = data['user1_id']
user2_id = data['user2_id']
language1 = data['language1']
language2 = data['language2']
user1 = User.query.get(user1_id)
user2 = User.query.get(user2_id)
if not user1 or not user2 or (user1_id != current_user.id and user2_id != current_user.id):
    return jsonify({'message': 'Unauthorized'}), 401# Create a new language exchange
    language_exchange = LanguageExchange(user1_id, user2_id, language1, language2)
    db.session.add(language_exchange)
    db.session.commit()

    # Return a success message
    return jsonify({'message': 'Language exchange created successfully'}), 201

# Create the cultural workshop routedata = request.get_json()
    name = data['name']
    description = data['description']
    session_url = data['session_url']
    expert_id = data['expert_id']
    # Check if the expert_id exists in the database and if the current user is the expert
    expert = User.query.get(expert_id)
    if not expert or expert_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 401# Create a new cultural workshop
    cultural_workshop = CulturalWorkshop(name, description, session_url, expert_id)
    db.session.add(cultural_workshop)
    db.session.commit()

    # Return a success message
    return jsonify({'message': 'Cultural workshop created successfully'}), 201

# Create the feedback routedata = request.get_json()
    user_id = data['user_id']
    virtual_tour_id = data.get('virtual_tour_id')
    language_exchange_id = data.get('language_exchange_id')
    cultural_workshop_id = data.get('cultural_workshop_id')
    rating = data['rating']
    review = data['review']
    # Check if the user_id exists in the database and if the current user is the one giving feedback
    user = User.query.get(user_id)
    if not user or user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 401# Create a new feedback
    feedback = Feedback(user_id, virtual_tour_id, language_exchange_id, cultural_workshop_id, rating, review)
    db.session.add(feedback)
    db.session.commit()

    # Return a success message
    return jsonify({'message': 'Feedback created successfully'}), 201

# Create the socketio connection
@socketio.on('connect')
def connect():
    emit('message', 'Client connected')

# Create the socketio disconnection
@socketio.on('disconnect')
def disconnect():
    emit('message', 'Client disconnected')

# Run the app
if __name__ == '__main__':
    db.create_all()
    socketio.run(app, host='0.0.0.0', port=5000)