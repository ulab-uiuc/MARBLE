# solution.py
import os
import cv2
import numpy as np
from flask import Flask, request, jsonify, send_filedef calculate_speed(player_positions):
    # Calculate the average distance between consecutive positions
    distances = [((player_positions[i][0] - player_positions[i-1][0])**2 + (player_positions[i][1] - player_positions[i-1][1])**2)**0.5 for i in range(1, len(player_positions))]
    return sum(distances) / len(distances) if distances else 0def calculate_accuracy(player_positions):
    # Calculate the average distance between consecutive positions
    distances = [((player_positions[i][0] - player_positions[i-1][0])**2 + (player_positions[i][1] - player_positions[i-1][1])**2)**0.5 for i in range(1, len(player_positions))]
    return 1 - (sum(distances) / len(distances) if distances else 0) / max(distances) if distances else 0def calculate_agility(player_positions):
    # Calculate the average change in direction
    directions = [(player_positions[i][0] - player_positions[i-1][0], player_positions[i][1] - player_positions[i-1][1]) for i in range(1, len(player_positions))]
    changes_in_direction = [abs(directions[i][0] * directions[i-1][1] - directions[i][1] * directions[i-1][0]) for i in range(1, len(directions))]
    return sum(changes_in_direction) / len(changes_in_direction) if changes_in_direction else 0from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO, emit
import matplotlib.pyplot as plt
from datetime import datetime

# Initialize Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sports_team_syncer.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
socketio = SocketIO(app)

# Define User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(64), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Define Video model
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(128), nullable=False)
    uploaded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Define PerformanceMetric model
class PerformanceMetric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    speed = db.Column(db.Float, nullable=False)
    accuracy = db.Column(db.Float, nullable=False)
    agility = db.Column(db.Float, nullable=False)

# Define CollaborativeWorkspace model
class CollaborativeWorkspace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Load user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User authentication routes
@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user)
        return jsonify({'message': 'Logged in successfully'})
    return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    role = request.json['role']
    user = User(username=username, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'})

# Video analysis route
@app.route('/analyze_video', methods=['POST'])
@login_required
def analyze_video():
    video_file = request.files['video']
    video_filename = video_file.filename
    video_file.save(os.path.join('uploads', video_filename))
    video = Video(filename=video_filename)
    db.session.add(video)
    db.session.commit()
    # Analyze video using OpenCV
    cap = cv2.VideoCapture(os.path.join('uploads', video_filename))
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Detect and track player movements
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
player_positions.append((x, y))
        # Measure key performance metricsplayer_positions = []
speed = calculate_speed(player_positions)
accuracy = calculate_accuracy(player_positions)
agility = calculate_agility(player_positions)# Save performance metrics to databaseperformance_metric = PerformanceMetric(video_id=video.id, player_id=current_user.id, speed=speed, accuracy=accuracy, agility=agility)
# Add error handling to ensure performance metrics are validdb.session.add(performance_metric)
        db.session.commit()
    cap.release()
    cv2.destroyAllWindows()
    return jsonify({'message': 'Video analyzed successfully'})

# Performance dashboard route
@app.route('/performance_dashboard', methods=['GET'])
@login_required
def performance_dashboard():
    performance_metrics = PerformanceMetric.query.filter_by(player_id=current_user.id).all()
    data = []
    for metric in performance_metrics:
        data.append({
            'video_id': metric.video_id,
            'speed': metric.speed,
            'accuracy': metric.accuracy,
            'agility': metric.agility
        })
    return jsonify(data)

# Collaborative workspace route
@app.route('/collaborative_workspace', methods=['POST'])
@login_required
def collaborative_workspace():
    message = request.json['message']
    collaborative_workspace = CollaborativeWorkspace(message=message, user_id=current_user.id)
    db.session.add(collaborative_workspace)
    db.session.commit()
    return jsonify({'message': 'Message sent successfully'})

# SocketIO event handlers
@socketio.on('connect')
def connect():
    emit('connected', {'message': 'Connected to server'})

@socketio.on('disconnect')
def disconnect():
    emit('disconnected', {'message': 'Disconnected from server'})

@socketio.on('send_message')
def send_message(message):
    collaborative_workspace = CollaborativeWorkspace(message=message, user_id=current_user.id)
    db.session.add(collaborative_workspace)
    db.session.commit()
    emit('message_sent', {'message': message}, broadcast=True)

# Test cases
import unittest

class TestSportsTeamSyncer(unittest.TestCase):
    def test_user_authentication(self):
        user = User(username='test_user', email='test@example.com', role='coach')
        user.set_password('test_password')
        db.session.add(user)
        db.session.commit()
        self.assertTrue(user.check_password('test_password'))

    def test_video_analysis(self):
        video_file = open('test_video.mp4', 'rb')
        video_filename = 'test_video.mp4'
        video_file.save(os.path.join('uploads', video_filename))
        video = Video(filename=video_filename)
        db.session.add(video)
        db.session.commit()
        # Analyze video using OpenCV
        cap = cv2.VideoCapture(os.path.join('uploads', video_filename))
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            # Detect and track player movements
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 1000:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cap.release()
        cv2.destroyAllWindows()
        self.assertTrue(os.path.exists(os.path.join('uploads', video_filename)))

    def test_performance_dashboard(self):
        performance_metric = PerformanceMetric(video_id=1, player_id=1, speed=10, accuracy=0.5, agility=5)
        db.session.add(performance_metric)
        db.session.commit()
        performance_metrics = PerformanceMetric.query.filter_by(player_id=1).all()
        self.assertEqual(len(performance_metrics), 1)

    def test_collaborative_workspace(self):
        collaborative_workspace = CollaborativeWorkspace(message='Test message', user_id=1)
        db.session.add(collaborative_workspace)
        db.session.commit()
        collaborative_workspaces = CollaborativeWorkspace.query.filter_by(user_id=1).all()
        self.assertEqual(len(collaborative_workspaces), 1)

if __name__ == '__main__':
    db.create_all()
    socketio.run(app)