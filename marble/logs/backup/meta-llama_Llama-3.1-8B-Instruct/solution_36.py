# solution.py
# Importing required libraries
import sqlite3
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_uploads import UploadManager
from flask_socketio import SocketIO, emit
import os
from datetime import datetime

# Creating a Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthconnect.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
socketio = SocketIO(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Defining the database models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    medical_records = db.relationship('MedicalRecord', backref='user', lazy=True)
    medication_schedules = db.relationship('MedicationSchedule', backref='user', lazy=True)
    appointments = db.relationship('Appointment', backref='user', lazy=True)
    consultations = db.relationship('Consultation', backref='user', lazy=True)

class MedicalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    record = db.Column(db.Text, nullable=False)

class MedicationSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    medication = db.Column(db.String(64), nullable=False)
    dosage = db.Column(db.String(64), nullable=False)
    schedule = db.Column(db.DateTime, nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    time = db.Column(db.Time, nullable=False)
    provider = db.Column(db.String(64), nullable=False)

class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    provider = db.Column(db.String(64), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    time = db.Column(db.Time, nullable=False)
    file = db.Column(db.String(64), nullable=False)

# Defining the forms
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ConsultationForm(FlaskForm):
    provider = StringField('Provider', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    time = StringField('Time', validators=[DataRequired()])
    file = StringField('File', validators=[DataRequired()])
    submit = SubmitField('Schedule Consultation')

# Defining the routes
@app.route('/')
def index():
    return 'Welcome to HealthConnect!'

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        return 'User created successfully!'
    return 'Invalid form data!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return 'Logged in successfully!'
    return 'Invalid email or password!'

@app.route('/consultation', methods=['GET', 'POST'])
@login_required
def consultation():
    form = ConsultationForm()
    if form.validate_on_submit():
        consultation = Consultation(user_id=current_user.id, provider=form.provider.data, date=form.date.data, time=form.time.data, file=form.file.data)
        db.session.add(consultation)
        db.session.commit()
        return 'Consultation scheduled successfully!'
    return 'Invalid form data!'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully!'

# Defining the socket.io routes
@socketio.on('connect')
def connect():
    emit('message', 'Connected to HealthConnect!')

@socketio.on('disconnect')
def disconnect():
    emit('message', 'Disconnected from HealthConnect!')

# Defining the API routes
@app.route('/api/medical_records', methods=['GET'])
@login_required
def get_medical_records():
    medical_records = MedicalRecord.query.filter_by(user_id=current_user.id).all()
    return jsonify([record.record for record in medical_records])

@app.route('/api/medication_schedules', methods=['GET'])
@login_required
def get_medication_schedules():
    medication_schedules = MedicationSchedule.query.filter_by(user_id=current_user.id).all()
    return jsonify([schedule.medication for schedule in medication_schedules])

@app.route('/api/appointments', methods=['GET'])
@login_required
def get_appointments():
    appointments = Appointment.query.filter_by(user_id=current_user.id).all()
    return jsonify([appointment.date for appointment in appointments])

@app.route('/api/consultations', methods=['GET'])
@login_required
def get_consultations():
    consultations = Consultation.query.filter_by(user_id=current_user.id).all()
    return jsonify([consultation.provider for consultation in consultations])

# Running the application
if __name__ == '__main__':
    db.create_all()
    socketio.run(app, host='0.0.0.0', port=5000)