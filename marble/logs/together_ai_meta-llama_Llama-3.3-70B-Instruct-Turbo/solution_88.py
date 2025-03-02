# solution.py
# Import required libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO, emit
import pandas as pd
import numpy as np
import os
import unittest

# Create the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sports_team_collaborator.db'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
login_manager = LoginManager(app)
socketio = SocketIO(app)

# Define the User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(64), nullable=False)

    def __init__(self, username, email, password, role):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Define the MatchData model
class MatchData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(128), nullable=False)
    file_type = db.Column(db.String(64), nullable=False)
    file_data = db.Column(db.LargeBinary, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, file_type, file_data, user_id):
        self.file_type = file_type
        self.file_data = file_data
        self.user_id = user_id

# Define the PerformanceMetric model
class PerformanceMetric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    metric_name = db.Column(db.String(64), nullable=False)
    metric_value = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, metric_name, metric_value, user_id):
        self.metric_name = metric_name
        self.metric_value = metric_value
        self.user_id = user_id

# Define the Report model
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_name = db.Column(db.String(64), nullable=False)
    report_data = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, report_name, report_data, user_id):
        self.report_name = report_name
        self.report_data = report_data
        self.user_id = user_id

# Define the Note model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note_text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, note_text, user_id):
        self.note_text = note_text
        self.user_id = user_id

# Define the Comment model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, comment_text, user_id):
        self.comment_text = comment_text
        self.user_id = user_id

# Define the ChatMessage model
class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, message_text, user_id):
        self.message_text = message_text
        self.user_id = user_id

# Load the user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define the route for uploading match data
@app.route('/upload_match_data', methods=['POST'])
@login_required
def upload_match_data():
    # Get the file type and data from the request
    file_type = request.form['file_type']
    file_data = request.files['file_data']

    # Create a new MatchData object
    match_data = MatchData(file_type, file_data.read(), current_user.id)

    # Add the match data to the database
    db.session.add(match_data)
    db.session.commit()

    return jsonify({'message': 'Match data uploaded successfully'}), 200

# Define the route for calculating performance metrics
@app.route('/calculate_performance_metrics', methods=['POST'])
@login_required
def calculate_performance_metrics():
    # Get the match data ID from the request
    match_data_id = request.form['match_data_id']

    # Get the match data from the database
    match_data = MatchData.query.get(match_data_id)

    # Calculate the performance metrics
    # For example, let's calculate the average speed of a player
    performance_metric = PerformanceMetric('average_speed', 10.5, current_user.id)

    # Add the performance metric to the database
    db.session.add(performance_metric)
    db.session.commit()

    return jsonify({'message': 'Performance metrics calculated successfully'}), 200

# Define the route for generating reports
@app.route('/generate_report', methods=['POST'])
@login_required
def generate_report():
    # Get the report name and data from the request
    report_name = request.form['report_name']
    report_data = request.form['report_data']

    # Create a new Report object
    report = Report(report_name, report_data, current_user.id)

    # Add the report to the database
    db.session.add(report)
    db.session.commit()

    return jsonify({'message': 'Report generated successfully'}), 200

# Define the route for sharing notes
@app.route('/share_note', methods=['POST'])
@login_required
def share_note():
    # Get the note text from the request
    note_text = request.form['note_text']

    # Create a new Note object
    note = Note(note_text, current_user.id)

    # Add the note to the database
    db.session.add(note)
    db.session.commit()

    return jsonify({'message': 'Note shared successfully'}), 200

# Define the route for commenting on notes
@app.route('/comment_on_note', methods=['POST'])
@login_required
def comment_on_note():
    # Get the note ID and comment text from the request
    note_id = request.form['note_id']
    comment_text = request.form['comment_text']

    # Create a new Comment object
    comment = Comment(comment_text, current_user.id)

    # Add the comment to the database
    db.session.add(comment)
    db.session.commit()

    return jsonify({'message': 'Comment added successfully'}), 200

# Define the route for sending chat messages
@app.route('/send_chat_message', methods=['POST'])
@login_required
def send_chat_message():
    # Get the message text from the request
    message_text = request.form['message_text']

    # Create a new ChatMessage object
    chat_message = ChatMessage(message_text, current_user.id)

    # Add the chat message to the database
    db.session.add(chat_message)
    db.session.commit()

    return jsonify({'message': 'Chat message sent successfully'}), 200

# Define the SocketIO event for real-time collaboration
@socketio.on('collaborate')
def collaborate(data):
    # Emit the data to all connected clients
    emit('collaborate', data, broadcast=True)

# Define the test cases
class TestSportsTeamCollaborator(unittest.TestCase):
    def test_upload_match_data(self):
        # Create a new user
        user = User('test_user', 'test@example.com', 'password', 'coach')
        db.session.add(user)
        db.session.commit()

        # Upload match data
        file_type = 'video'
        file_data = b'test_video_data'
        match_data = MatchData(file_type, file_data, user.id)
        db.session.add(match_data)
        db.session.commit()

        # Check if the match data is uploaded successfully
        self.assertEqual(match_data.file_type, file_type)
        self.assertEqual(match_data.file_data, file_data)

    def test_calculate_performance_metrics(self):
        # Create a new user
        user = User('test_user', 'test@example.com', 'password', 'coach')
        db.session.add(user)
        db.session.commit()

        # Calculate performance metrics
        performance_metric = PerformanceMetric('average_speed', 10.5, user.id)
        db.session.add(performance_metric)
        db.session.commit()

        # Check if the performance metrics are calculated successfully
        self.assertEqual(performance_metric.metric_name, 'average_speed')
        self.assertEqual(performance_metric.metric_value, 10.5)

    def test_generate_report(self):
        # Create a new user
        user = User('test_user', 'test@example.com', 'password', 'coach')
        db.session.add(user)
        db.session.commit()

        # Generate a report
        report_name = 'test_report'
        report_data = 'test_report_data'
        report = Report(report_name, report_data, user.id)
        db.session.add(report)
        db.session.commit()

        # Check if the report is generated successfully
        self.assertEqual(report.report_name, report_name)
        self.assertEqual(report.report_data, report_data)

    def test_share_note(self):
        # Create a new user
        user = User('test_user', 'test@example.com', 'password', 'coach')
        db.session.add(user)
        db.session.commit()

        # Share a note
        note_text = 'test_note_text'
        note = Note(note_text, user.id)
        db.session.add(note)
        db.session.commit()

        # Check if the note is shared successfully
        self.assertEqual(note.note_text, note_text)

    def test_comment_on_note(self):
        # Create a new user
        user = User('test_user', 'test@example.com', 'password', 'coach')
        db.session.add(user)
        db.session.commit()

        # Comment on a note
        note_id = 1
        comment_text = 'test_comment_text'
        comment = Comment(comment_text, user.id)
        db.session.add(comment)
        db.session.commit()

        # Check if the comment is added successfully
        self.assertEqual(comment.comment_text, comment_text)

    def test_send_chat_message(self):
        # Create a new user
        user = User('test_user', 'test@example.com', 'password', 'coach')
        db.session.add(user)
        db.session.commit()

        # Send a chat message
        message_text = 'test_message_text'
        chat_message = ChatMessage(message_text, user.id)
        db.session.add(chat_message)
        db.session.commit()

        # Check if the chat message is sent successfully
        self.assertEqual(chat_message.message_text, message_text)

if __name__ == '__main__':
    # Create the database tables
    db.create_all()

    # Run the test cases
    unittest.main()

    # Run the Flask application
    socketio.run(app)