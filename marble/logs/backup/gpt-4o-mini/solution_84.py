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

# Define the Athlete model
class Athlete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    position = db.Column(db.String(50), nullable=False)
    workout_plans = db.relationship('WorkoutPlan', backref='athlete', lazy=True)

# Define the WorkoutPlan model
class WorkoutPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    athlete_id = db.Column(db.Integer, db.ForeignKey('athlete.id'), nullable=False)

# Define the GameStrategy model
class GameStrategy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# Define the PerformanceMetric model
class PerformanceMetric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    athlete_id = db.Column(db.Integer, db.ForeignKey('athlete.id'), nullable=False)
    metric_name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)
    recorded_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# Create the database tables
@app.before_first_request
def create_tables():
    db.create_all()

# API endpoint to add a new athlete
@app.route('/athletes', methods=['POST'])
def add_athlete():
    data = request.json
    new_athlete = Athlete(name=data['name'], age=data['age'], position=data['position'])
    db.session.add(new_athlete)
    db.session.commit()
    return jsonify({'message': 'Athlete added successfully!'}), 201

# API endpoint to create a workout plan
@app.route('/workout_plans', methods=['POST'])
def create_workout_plan():
    data = request.jsontry:
        parsed_date = datetime.datetime.strptime(data['date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400
    new_plan = WorkoutPlan(date=parsed_date, description=data['description'], athlete_id=data['athlete_id'])    db.session.add(new_plan)
    db.session.commit()
    return jsonify({'message': 'Workout plan created successfully!'}), 201

# API endpoint to add a game strategy
@app.route('/game_strategies', methods=['POST'])
def add_game_strategy():
    data = request.json
    new_strategy = GameStrategy(description=data['description'])
    db.session.add(new_strategy)
    db.session.commit()
    return jsonify({'message': 'Game strategy added successfully!'}), 201

# API endpoint to record performance metrics
@app.route('/performance_metrics', methods=['POST'])
def record_performance_metric():
    data = request.json
    new_metric = PerformanceMetric(athlete_id=data['athlete_id'], metric_name=data['metric_name'], value=data['value'])
    db.session.add(new_metric)
    db.session.commit()
    return jsonify({'message': 'Performance metric recorded successfully!'}), 201

# API endpoint to get all athletes
@app.route('/athletes', methods=['GET'])
def get_athletes():
    athletes = Athlete.query.all()
    return jsonify([{'id': athlete.id, 'name': athlete.name, 'age': athlete.age, 'position': athlete.position} for athlete in athletes]), 200

# API endpoint to get performance metrics for an athlete
@app.route('/performance_metrics/<int:athlete_id>', methods=['GET'])
def get_performance_metrics(athlete_id):
    metrics = PerformanceMetric.query.filter_by(athlete_id=athlete_id).all()
    return jsonify([{'metric_name': metric.metric_name, 'value': metric.value, 'recorded_at': metric.recorded_at} for metric in metrics]), 200

# Run the application
if __name__ == '__main__':
    app.run(debug=True)