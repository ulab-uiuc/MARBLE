# solution.py

# Import necessary libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sports_team_coordinator.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database models

class Athlete(db.Model):
    """Model to represent an athlete."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    position = db.Column(db.String(50), nullable=False)
    workout_plans = db.relationship('WorkoutPlan', backref='athlete', lazy=True)

class WorkoutPlan(db.Model):
    """Model to represent a workout plan."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    athlete_id = db.Column(db.Integer, db.ForeignKey('athlete.id'), nullable=False)

class GameStrategy(db.Model):
    """Model to represent a game strategy."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class PerformanceMetric(db.Model):
    """Model to represent performance metrics."""
    id = db.Column(db.Integer, primary_key=True)
    athlete_id = db.Column(db.Integer, db.ForeignKey('athlete.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    score = db.Column(db.Float, nullable=False)

# API routes

@app.route('/athletes', methods=['POST'])
def add_athlete():
    """Add a new athlete."""
    data = request.json
    new_athlete = Athlete(name=data['name'], age=data['age'], position=data['position'])
    db.session.add(new_athlete)
    db.session.commit()
    return jsonify({'message': 'Athlete added successfully!'}), 201

@app.route('/workout_plans', methods=['POST'])
def add_workout_plan():
    """Add a new workout plan."""
    data = request.json    if 'title' not in data or 'athlete_id' not in data:
        return jsonify({'error': 'Title and athlete_id are required fields.'}), 400
    new_plan = WorkoutPlan(title=data['title'], description=data['description'], athlete_id=data['athlete_id'])
    db.session.add(new_plan)
    db.session.commit()    return jsonify({'message': 'Workout plan added successfully!'}), 201

@app.route('/game_strategies', methods=['POST'])
def add_game_strategy():
    """Add a new game strategy."""
    data = request.json    if 'title' not in data:
        return jsonify({'error': 'Title is a required field.'}), 400
    new_strategy = GameStrategy(title=data['title'], description=data['description'])
    db.session.add(new_strategy)
    db.session.commit()    return jsonify({'message': 'Game strategy added successfully!'}), 201

@app.route('/performance_metrics', methods=['POST'])
def add_performance_metric():
    """Add a new performance metric."""
    data = request.json    if 'athlete_id' not in data or 'score' not in data:
        return jsonify({'error': 'athlete_id and score are required fields.'}), 400
    new_metric = PerformanceMetric(athlete_id=data['athlete_id'], score=data['score'])
    db.session.add(new_metric)
    db.session.commit()    return jsonify({'message': 'Performance metric added successfully!'}), 201

@app.route('/athletes', methods=['GET'])
def get_athletes():
    """Get all athletes."""
    athletes = Athlete.query.all()
    return jsonify([{'id': athlete.id, 'name': athlete.name, 'age': athlete.age, 'position': athlete.position} for athlete in athletes]), 200

@app.route('/workout_plans', methods=['GET'])
def get_workout_plans():
    """Get all workout plans."""
    plans = WorkoutPlan.query.all()
    return jsonify([{'id': plan.id, 'title': plan.title, 'description': plan.description, 'athlete_id': plan.athlete_id} for plan in plans]), 200

@app.route('/game_strategies', methods=['GET'])
def get_game_strategies():
    """Get all game strategies."""
    strategies = GameStrategy.query.all()
    return jsonify([{'id': strategy.id, 'title': strategy.title, 'description': strategy.description} for strategy in strategies]), 200

@app.route('/performance_metrics', methods=['GET'])
def get_performance_metrics():
    """Get all performance metrics."""
    metrics = PerformanceMetric.query.all()
    return jsonify([{'id': metric.id, 'athlete_id': metric.athlete_id, 'date': metric.date, 'score': metric.score} for metric in metrics]), 200

# Initialize the database
with app.app_context():
    db.create_all()

# Run the application
if __name__ == '__main__':
    app.run(debug=True)