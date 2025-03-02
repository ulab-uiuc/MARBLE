# solution.py

# Import necessary libraries
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
import os
import pandas as pd

# Initialize the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sports_team_collaborator.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
socketio = SocketIO(app)

# Define User roles
ROLES = {
    'coach': 'full_access',
    'analyst': 'data_analysis',
    'player': 'view_metrics'
}

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)

# Match data model
class MatchData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Initialize the database
@app.before_first_request
def create_tables():
    db.create_all()

# Route to upload match data
@app.route('/upload', methods=['POST'])
def upload_data():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        new_data = MatchData(file_path=file_path, user_id=session['user_id'])
        db.session.add(new_data)
        db.session.commit()
        return jsonify({'message': 'File uploaded successfully'}), 201

# Route to get user role
@app.route('/role', methods=['GET'])
def get_user_role():
    user = User.query.get(session['user_id'])
    return jsonify({'role': user.role}), 200

# Real-time collaboration features
@socketio.on('send_message')
def handle_message(data):
    emit('receive_message', data, broadcast=True)

# Route to get performance metrics
@app.route('/performance/<int:user_id>', methods=['GET'])
def get_performance_metrics(user_id):
    # Placeholder for performance metrics logic
    metrics = {'goals': 10, 'assists': 5}  # Example data
    return jsonify(metrics), 200

# Run the application
if __name__ == '__main__':
    socketio.run(app, debug=True)

# Test cases (to be run separately)
# file_name_1.py
import unittest

class TestSportsTeamCollaborator(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_upload_data(self):
        # Test uploading a file
        with open('test_file.csv', 'w') as f:
            f.write('test data')
        with open('test_file.csv', 'rb') as f:
            response = self.app.post('/upload', data={'file': f})
        self.assertEqual(response.status_code, 201)

    def test_get_user_role(self):
        # Test getting user role
        response = self.app.get('/role')
        self.assertEqual(response.status_code, 200)

    def test_performance_metrics(self):
        # Test getting performance metrics
        response = self.app.get('/performance/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()