# solution.py

# Import required libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Create the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_collaborator.db'
db = SQLAlchemy(app)

# Initialize the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Define the User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Integer, default=1)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    itineraries = db.relationship('Itinerary', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Define the Itinerary model
class Itinerary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Integer, default=1)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    activities = db.relationship('Activity', backref='itinerary', lazy=True)
    accommodations = db.relationship('Accommodation', backref='itinerary', lazy=True)

# Define the Activity model
class Activity(db.Model):class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Integer, default=1)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itinerary.id'), nullable=False)

class Collaborator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itinerary.id'), nullable=False)
    role = db.Column(db.String(100), nullable=False, default='collaborator')
    user = db.relationship('User', backref='collaborations', lazy=True)
    itinerary = db.relationship('Itinerary', backref='collaborators', lazy=True)# Define the Accommodation model
class Accommodation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itinerary.id'), nullable=False)

# Define the Comment model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itinerary.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Define the Message model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Load the user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register a new user
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not email or not password:
        return jsonify({'error': 'Please provide all required fields'}), 400
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'error': 'Username already exists'}), 400
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

# Login a user
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Please provide all required fields'}), 400
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401
    login_user(user)
    return jsonify({'message': 'User logged in successfully'}), 200

# Logout a user
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'User logged out successfully'}), 200

# Create a new itinerary
@app.route('/itineraries', methods=['POST'])
@login_required
def create_itinerary():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    title = data.get('title')
    description = data.get('description')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    if not title or not description or not start_date or not end_date:
        return jsonify({'error': 'Please provide all required fields'}), 400
    new_itinerary = Itinerary(title=title, description=description, start_date=start_date, end_date=end_date, user_id=current_user.id)
    db.session.add(new_itinerary)
    db.session.commit()
    return jsonify({'message': 'Itinerary created successfully'}), 201

# Get all itineraries for a user
@app.route('/itineraries', methods=['GET'])
@app.route('/itineraries/<id>/collaborators', methods=['POST'])
@login_required
def add_collaborator(id):
    itinerary = Itinerary.query.filter_by(id=id, user_id=current_user.id).first()
    if not itinerary:
        return jsonify({'error': 'Itinerary not found'}), 404
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    collaborator_id = data.get('collaborator_id')
    if not collaborator_id:
        return jsonify({'error': 'Please provide all required fields'}), 400
    collaborator = User.query.get(collaborator_id)
    if not collaborator:
        return jsonify({'error': 'Collaborator not found'}), 404
    new_collaborator = Collaborator(user_id=collaborator_id, itinerary_id=id)
    db.session.add(new_collaborator)
    db.session.commit()
    return jsonify({'message': 'Collaborator added successfully'}), 201
@login_required
def get_itineraries():
    itineraries = Itinerary.query.filter_by(user_id=current_user.id).all()
    output = []
    for itinerary in itineraries:
        itinerary_data = {'id': itinerary.id, 'title': itinerary.title, 'description': itinerary.description, 'start_date': itinerary.start_date, 'end_date': itinerary.end_date}
        output.append(itinerary_data)
    return jsonify({'itineraries': output}), 200

# Get a single itinerary
@app.route('/itineraries/<id>', methods=['GET'])itinerary = Itinerary.query.filter_by(id=id).first()if not itinerary:
        return jsonify({'error': 'Itinerary not found'}), 404
    itinerary_data = {'id': itinerary.id, 'title': itinerary.title, 'description': itinerary.description, 'start_date': itinerary.start_date, 'end_date': itinerary.end_date}
    return jsonify({'itinerary': itinerary_data}), 200

# Update an itinerary
@app.route('/itineraries/<id>', methods=['PUT'])def update_itinerary(id):
    itinerary = Itinerary.query.filter_by(id=id, user_id=current_user.id).first()
    if not itinerary:
        return jsonify({'error': 'Itinerary not found'}), 404
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    data = request.get_json()
    if 'version' not in data:
        return jsonify({'error': 'Version not provided'}), 400
    title = data.get('title')
    description = data.get('description')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    if title:
        itinerary.title = title
    if description:
        itinerary.description = description
    if start_date:
        itinerary.start_date = start_date
    if end_date:
        itinerary.end_date = end_dateif itinerary.version != data.get('version'):
    return jsonify({'error': 'Version conflict'}), 409
itinerary.version += 1
try:
    db.session.commit()
except Exception as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), 500
    return jsonify({'message': 'Itinerary updated successfully'}), 200    itinerary = Itinerary.query.filter_by(id=id, user_id=current_user.id).first()
    if not itinerary:
        return jsonify({'error': 'Itinerary not found'}), 404
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    title = data.get('title')
    description = data.get('description')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    if title:
        itinerary.title = title
    if description:
        itinerary.description = description
    if start_date:
        itinerary.start_date = start_date
    if end_date:
        itinerary.end_date = end_date
    db.session.commit()
    return jsonify({'message': 'Itinerary updated successfully'}), 200

# Delete an itinerary
@app.route('/itineraries/<id>', methods=['DELETE'])
@login_required
def delete_itinerary(id):
    itinerary = Itinerary.query.filter_by(id=id, user_id=current_user.id).first()
    if not itinerary:
        return jsonify({'error': 'Itinerary not found'}), 404
    db.session.delete(itinerary)
    db.session.commit()
    return jsonify({'message': 'Itinerary deleted successfully'}), 200

# Create a new activity
@app.route('/itineraries/<id>/activities', methods=['POST'])def create_activity(id):
    itinerary = Itinerary.query.filter_by(id=id, user_id=current_user.id).first()
    if not itinerary:
        return jsonify({'error': 'Itinerary not found'}), 404
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    name = data.get('name')
    description = data.get('description')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    if not name or not description or not start_time or not end_time:
        return jsonify({'error': 'Please provide all required fields'}), 400
    new_activity = Activity(name=name, description=description, start_time=start_time, end_time=end_time, itinerary_id=id)
    db.session.add(new_activity)
    itinerary.version += 1
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Version conflict'}), 409
    return jsonify({'message': 'Activity created successfully'}), 201    itinerary = Itinerary.query.filter_by(id=id, user_id=current_user.id).first()
    if not itinerary:
        return jsonify({'error': 'Itinerary not found'}), 404
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    name = data.get('name')
    description = data.get('description')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    if not name or not description or not start_time or not end_time:
        return jsonify({'error': 'Please provide all required fields'}), 400
    new_activity = Activity(name=name, description=description, start_time=start_time, end_time=end_time, itinerary_id=id)
    db.session.add(new_activity)
    db.session.commit()
    return jsonify({'message': 'Activity created successfully'}), 201

# Get all activities for an itinerary
@app.route('/itineraries/<id>/activities', methods=['GET'])
@login_required
def get_activities(id):
    itinerary = Itinerary.query.filter_by(id=id, user_id=current_user.id).first()
    if not itinerary:
        return jsonify({'error': 'Itinerary not found'}), 404
    activities = Activity.query.filter_by(itinerary_id=id).all()
    output = []
    for activity in activities:
        activity_data = {'id': activity.id, 'name': activity.name, 'description': activity.description, 'start_time': activity.start_time, 'end_time': activity.end_time}
        output.append(activity_data)
    return jsonify({'activities': output}), 200

# Create a new accommodation
@app.route('/itineraries/<id>/accommodations', methods=['POST'])def create_accommodation(id):
    itinerary = Itinerary.query.filter_by(id=id, user_id=current_user.id).first()
    if not itinerary:
        return jsonify({'error': 'Itinerary not found'}), 404
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    name = data.get('name')
    description = data.get('description')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    if not name or not description or not start_date or not end_date:
        return jsonify({'error': 'Please provide all required fields'}), 400
    new_accommodation = Accommodation(name=name, description=description, start_date=start_date, end_date=end_date, itinerary_id=id)
    db.session.add(new_accommodation)
    itinerary.version += 1
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Version conflict'}), 409
    return jsonify({'message': 'Accommodation created successfully'}), 201    itinerary = Itinerary.query.filter_by(id=id, user_id=current_user.id).first()
    if not itinerary:
        return jsonify({'error': 'Itinerary not found'}), 404
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    name = data.get('name')
    description = data.get('description')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    if not name or not description or not start_date or not end_date:
        return jsonify({'error': 'Please provide all required fields'}), 400
    new_accommodation = Accommodation(name=name, description=description, start_date=start_date, end_date=end_date, itinerary_id=id)
    db.session.add(new_accommodation)
    db.session.commit()
    return jsonify({'message': 'Accommodation created successfully'}), 201

# Get all accommodations for an itinerary
@app.route('/itineraries/<id>/accommodations', methods=['GET'])
@login_required
def get_accommodations(id):
    itinerary = Itinerary.query.filter_by(id=id, user_id=current_user.id).first()
    if not itinerary:
        return jsonify({'error': 'Itinerary not found'}), 404
    accommodations = Accommodation.query.filter_by(itinerary_id=id).all()
    output = []
    for accommodation in accommodations:
        accommodation_data = {'id': accommodation.id, 'name': accommodation.name, 'description': accommodation.description, 'start_date': accommodation.start_date, 'end_date': accommodation.end_date}
        output.append(accommodation_data)
    return jsonify({'accommodations': output}), 200

# Create a new comment
@app.route('/itineraries/<id>/comments', methods=['POST'])
    itinerary = Itinerary.query.filter_by(id=id).first()
    if not itinerary:
        return jsonify({'error': 'Itinerary not found'}), 404
    collaborator = Collaborator.query.filter_by(itinerary_id=id, user_id=current_user.id).first()
    if not collaborator:
        return jsonify({'error': 'You are not a collaborator of this itinerary'}), 403
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    text = data.get('text')
    if not text:
        return jsonify({'error': 'Please provide all required fields'}), 400
    new_comment = Comment(text=text, itinerary_id=id, user_id=current_user.id)
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({'message': 'Comment created successfully'}), 201
@login_required
def get_comments(id):
    itinerary = Itinerary.query.filter_by(id=id, user_id=current_user.id).first()
    if not itinerary:
        return jsonify({'error': 'Itinerary not found'}), 404
    comments = Comment.query.filter_by(itinerary_id=id).all()
    output = []
    for comment in comments:
        comment_data = {'id': comment.id, 'text': comment.text, 'user_id': comment.user_id}
        output.append(comment_data)
    return jsonify({'comments': output}), 200

# Create a new message
@app.route('/messages', methods=['POST'])
@login_required
def create_message():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    text = data.get('text')
    receiver_id = data.get('receiver_id')
    if not text or not receiver_id:
        return jsonify({'error': 'Please provide all required fields'}), 400
    new_message = Message(text=text, sender_id=current_user.id, receiver_id=receiver_id)
    db.session.add(new_message)
    db.session.commit()
    return jsonify({'message': 'Message created successfully'}), 201

# Get all messages for a user
@app.route('/messages', methods=['GET'])
@login_required
def get_messages():
    messages = Message.query.filter_by(receiver_id=current_user.id).all()
    output = []
    for message in messages:
        message_data = {'id': message.id, 'text': message.text, 'sender_id': message.sender_id}
        output.append(message_data)
    return jsonify({'messages': output}), 200

if __name__ == '__main__':
    app.run(debug=True)