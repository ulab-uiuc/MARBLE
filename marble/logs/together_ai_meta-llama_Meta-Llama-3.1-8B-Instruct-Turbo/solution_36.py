# solution.py
# Importing required libraries
import sqlite3
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from flask import send_file
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
from pyzbar import pyzbar
import qrcode
import base64
from flask import render_template
from flask import redirect, url_for
import random
import string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
import uuid
import json
import requests

# Creating a Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthconnect.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key_here'
CORS(app)

# Initializing the database
db = SQLAlchemy(app)

# Initializing the login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Initializing the bcrypt
bcrypt = Bcrypt(app)

# Initializing the JWT manager
jwt = JWTManager(app)

# Defining the User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    medical_records = db.relationship('MedicalRecord', backref='user', lazy=True)
    medication_schedules = db.relationship('MedicationSchedule', backref='user', lazy=True)
    appointments = db.relationship('Appointment', backref='user', lazy=True)
    consultations = db.relationship('Consultation', backref='user', lazy=True)

# Defining the MedicalRecord model
class MedicalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    record = db.Column(db.String(1000), nullable=False)

# Defining the MedicationSchedule model
class MedicationSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    medication = db.Column(db.String(100), nullable=False)
    schedule = db.Column(db.String(100), nullable=False)

# Defining the Appointment model
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(100), nullable=False)

# Defining the Consultation model
class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(100), nullable=False)
    file = db.Column(db.String(100), nullable=False)

# Defining the login route
@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify({'message': 'Invalid credentials'}), 401

# Defining the register route
@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    email = request.json['email']
    password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

# Defining the medical record route
@app.route('/medical-record', methods=['GET'])
@jwt_required
def get_medical_record():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    medical_record = MedicalRecord.query.filter_by(user_id=user_id).first()
    return jsonify({'medical_record': medical_record.record}), 200

# Defining the medication schedule route
@app.route('/medication-schedule', methods=['GET'])
@jwt_required
def get_medication_schedule():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    medication_schedule = MedicationSchedule.query.filter_by(user_id=user_id).first()
    return jsonify({'medication_schedule': medication_schedule.medication}), 200

# Defining the appointment route
@app.route('/appointment', methods=['GET'])
@jwt_required
def get_appointment():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    appointment = Appointment.query.filter_by(user_id=user_id).first()
    return jsonify({'appointment': appointment.date}), 200

# Defining the consultation route
@app.route('/consultation', methods=['GET'])
@jwt_required
def get_consultation():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    consultation = Consultation.query.filter_by(user_id=user_id).first()
    return jsonify({'consultation': consultation.file}), 200

# Defining the remote consultation route
@app.route('/remote-consultation', methods=['POST'])
@jwt_required
def remote_consultation():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    file = request.files['file']file.save(os.path.join('uploads', file.filename))
# Ensure the 'uploads' directory exists and has proper permissions
# Configure the Flask-Uploads library to handle file uploads securelyconsultation = Consultation(user_id=user_id, file=file.filename)
# Import the Flask-Uploads library
from flask_uploads import UploadManager
# Initialize the UploadManager
uploads = UploadManager(app)
# Configure the file upload settings
uploads.config['UPLOAD_FOLDER'] = 'uploads'
# Validate file types and sizes
if file and allowed_file(file.filename):
    file.save(os.path.join('uploads', file.filename))
    db.session.add(consultation)
    db.session.commit()
    return jsonify({'message': 'Consultation created successfully'}), 201

# Defining the video conferencing route
@app.route('/video-conferencing', methods=['GET'])
@jwt_required
def video_conferencing():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    return render_template('video_conferencing.html')

# Defining the file sharing route
@app.route('/file-sharing', methods=['GET'])
@jwt_required
def file_sharing():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    return render_template('file_sharing.html')

# Defining the logout route
@app.route('/logout', methods=['POST'])
@jwt_required
def logout():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

# Defining the home route
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

# Defining the about route
@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

# Defining the contact route
@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

# Defining the terms route
@app.route('/terms', methods=['GET'])
def terms():
    return render_template('terms.html')

# Defining the privacy route
@app.route('/privacy', methods=['GET'])
def privacy():
    return render_template('privacy.html')

# Defining the FAQ route
@app.route('/faq', methods=['GET'])
def faq():
    return render_template('faq.html')

# Defining the support route
@app.route('/support', methods=['GET'])
def support():
    return render_template('support.html')

# Defining the error handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Not found'}), 404

# Defining the error handler
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'message': 'Internal server error'}), 500

# Running the application
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)