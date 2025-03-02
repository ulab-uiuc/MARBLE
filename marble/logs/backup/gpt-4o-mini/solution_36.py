# solution.py

# Import necessary libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import datetime

# Initialize the Flask application
app = Flask(__name__)

# Configure the database and security settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthconnect.db'  # Using SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this in production
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Database models

class User(db.Model):
    """Model for storing user information."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    medical_records = db.relationship('MedicalRecord', backref='user', lazy=True)
    medications = db.relationship('Medication', backref='user', lazy=True)
    consultations = db.relationship('Consultation', backref='user', lazy=True)

class MedicalRecord(db.Model):
    """Model for storing medical records."""
    id = db.Column(db.Integer, primary_key=True)
    record_details = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Medication(db.Model):
    """Model for storing medication details."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(100), nullable=False)
    schedule = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Consultation(db.Model):
    """Model for storing consultation logs."""
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# API Endpoints

@app.route('/register', methods=['POST'])
def register():
    """Endpoint for user registration."""
    username = request.json.get('username')
    password = request.json.get('password')
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    """Endpoint for user login."""
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity={'username': user.username})
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401

@app.route('/medical_records', methods=['GET'])
@jwt_required()
def get_medical_records():
    """Endpoint to retrieve medical records for the logged-in user."""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()
    records = MedicalRecord.query.filter_by(user_id=user.id).all()
    return jsonify([{'id': record.id, 'details': record.record_details} for record in records]), 200

@app.route('/medications', methods=['GET'])
@jwt_required()
def get_medications():
    """Endpoint to retrieve medications for the logged-in user."""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()
    medications = Medication.query.filter_by(user_id=user.id).all()
    return jsonify([{'id': med.id, 'name': med.name, 'dosage': med.dosage, 'schedule': med.schedule} for med in medications]), 200

@app.route('/consultations', methods=['POST'])
@jwt_required()
def create_consultation():
    """Endpoint to create a new consultation."""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()    try:
        date_time = request.json.get('date_time')
        if not date_time:
            return jsonify({"msg": "date_time is required"}), 400
        date_time = datetime.datetime.fromisoformat(date_time)notes = request.json.get('notes')
new_consultation = Consultation(date_time=date_time, notes=notes, user_id=user.id)    db.session.add(new_consultation)
    db.session.commit()
    return jsonify({"msg": "Consultation created successfully"}), 201

# Initialize the database
@app.before_first_request
def create_tables():
    """Create database tables before the first request."""
    db.create_all()

# Run the application
if __name__ == '__main__':
    app.run(debug=True)