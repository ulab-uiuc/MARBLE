# solution.py

# Import necessary libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import datetime

# Initialize Flask application
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthhub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model for User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    symptoms = db.relationship('SymptomLog', backref='user', lazy=True)

# Database model for SymptomLog
class SymptomLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    symptom = db.Column(db.String(100), nullable=False)
    severity = db.Column(db.Integer, nullable=False)  # Severity on a scale of 1-10
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# Initialize the database
with app.app_context():
    db.create_all()

# Endpoint to log symptoms
@app.route('/log_symptom', methods=['POST'])
def log_symptom():
    data = request.json
    # Data validation
    if 'user_id' not in data or 'symptom' not in data or 'severity' not in data or 'duration' not in data:
        return jsonify({'error': 'Missing required fields.'}), 400
    if not (1 <= data['severity'] <= 10):
        return jsonify({'error': 'Severity must be between 1 and 10.'}), 400
    if data['duration'] <= 0:
        return jsonify({'error': 'Duration must be a positive integer.'}), 400

    new_symptom = SymptomLog(
        user_id=data['user_id'],
        symptom=data['symptom'],
        severity=data['severity'],
        duration=data['duration']
    )    db.session.add(new_symptom)
    db.session.commit()
    return jsonify({"message": "Symptom logged successfully!"}), 201

# Endpoint to get user symptoms
@app.route('/get_symptoms/<int:user_id>', methods=['GET'])
def get_symptoms(user_id):
    symptoms = SymptomLog.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "symptom": s.symptom,
        "severity": s.severity,
        "duration": s.duration,
        "timestamp": s.timestamp
    } for s in symptoms]), 200

# Recommendation engine based on symptom data
def generate_recommendations(user_id):
    # Fetch user's symptom logs
    logs = SymptomLog.query.filter_by(user_id=user_id).all()
    if not logs:
        return "No data available for recommendations."

    # Prepare data for analysis
    data = pd.DataFrame([{
        "severity": log.severity,
        "duration": log.duration
    } for log in logs])    # Check if there are enough data points for analysis
    if len(data) < 2:
        return "Insufficient data for recommendations. Please log more symptoms."

    # Prepare data for analysis
    X = np.array(data[['severity', 'duration']])  # Severity and duration as independent variables
    y = data.index.values  # Time as dependent variable
    model = LinearRegression().fit(X, y)

    # Generate recommendations based on the model
    if model.coef_[0] > 0 and model.coef_[1] > 0:
        return "Consider consulting a healthcare provider as symptoms are worsening."
    else:
        return "Your symptoms seem to be stable. Keep monitoring your health."    # Generate recommendations based on the model
    if model.coef_[0] > 0:
        return "Consider consulting a healthcare provider as symptoms are worsening."
    else:
        return "Your symptoms seem to be stable. Keep monitoring your health."

# Endpoint to get recommendations
@app.route('/get_recommendations/<int:user_id>', methods=['GET'])
def get_recommendations_endpoint(user_id):
    recommendations = generate_recommendations(user_id)
    return jsonify({"recommendations": recommendations}), 200

# Run the application
if __name__ == '__main__':
    app.run(debug=True)