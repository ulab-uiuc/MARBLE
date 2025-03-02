# solution.py
# Import required libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import pandas as pd
from sklearn.model_selection import train_test_splitfrom sklearn.ensemble import RandomForestRegressorfrom sklearn.metrics import mean_squared_error

# Create a Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sport_team_coordinator.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Define the database schema
class Athlete(db.Model):
    """Athlete model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, name, email):
        self.name = name
        self.email = email

class WorkoutPlan(db.Model):
    """Workout plan model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    athlete_id = db.Column(db.Integer, db.ForeignKey('athlete.id'), nullable=False)

    def __init__(self, name, description, athlete_id):
        self.name = name
        self.description = description
        self.athlete_id = athlete_id

class GameStrategy(db.Model):
    """Game strategy model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    athlete_id = db.Column(db.Integer, db.ForeignKey('athlete.id'), nullable=False)

    def __init__(self, name, description, athlete_id):
        self.name = name
        self.description = description
        self.athlete_id = athlete_id

class PerformanceMetric(db.Model):
    """Performance metric model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)
    athlete_id = db.Column(db.Integer, db.ForeignKey('athlete.id'), nullable=False)

    def __init__(self, name, value, athlete_id):
        self.name = name
        self.value = value
        self.athlete_id = athlete_id

# Create the database tables
db.create_all()

# Define the API endpoints
@app.route('/athletes', methods=['GET', 'POST'])
def athletes():
    """Athlete API endpoint"""
    if request.method == 'GET':
        athletes = Athlete.query.all()
        return jsonify([{'id': athlete.id, 'name': athlete.name, 'email': athlete.email} for athlete in athletes])
    elif request.method == 'POST':
        data = request.get_json()
        athlete = Athlete(data['name'], data['email'])
        db.session.add(athlete)
        db.session.commit()
        return jsonify({'id': athlete.id, 'name': athlete.name, 'email': athlete.email})

@app.route('/workout-plans', methods=['GET', 'POST'])
def workout_plans():
    """Workout plan API endpoint"""
    if request.method == 'GET':
        workout_plans = WorkoutPlan.query.all()
        return jsonify([{'id': workout_plan.id, 'name': workout_plan.name, 'description': workout_plan.description, 'athlete_id': workout_plan.athlete_id} for workout_plan in workout_plans])
    elif request.method == 'POST':
        data = request.get_json()
        workout_plan = WorkoutPlan(data['name'], data['description'], data['athlete_id'])
        db.session.add(workout_plan)
        db.session.commit()
        return jsonify({'id': workout_plan.id, 'name': workout_plan.name, 'description': workout_plan.description, 'athlete_id': workout_plan.athlete_id})

@app.route('/game-strategies', methods=['GET', 'POST'])
def game_strategies():
    """Game strategy API endpoint"""
    if request.method == 'GET':
        game_strategies = GameStrategy.query.all()
        return jsonify([{'id': game_strategy.id, 'name': game_strategy.name, 'description': game_strategy.description, 'athlete_id': game_strategy.athlete_id} for game_strategy in game_strategies])
    elif request.method == 'POST':
        data = request.get_json()
        game_strategy = GameStrategy(data['name'], data['description'], data['athlete_id'])
        db.session.add(game_strategy)
        db.session.commit()
        return jsonify({'id': game_strategy.id, 'name': game_strategy.name, 'description': game_strategy.description, 'athlete_id': game_strategy.athlete_id})

@app.route('/performance-metrics', methods=['GET', 'POST'])
def performance_metrics():
    """Performance metric API endpoint"""
    if request.method == 'GET':
        performance_metrics = PerformanceMetric.query.all()
        return jsonify([{'id': performance_metric.id, 'name': performance_metric.name, 'value': performance_metric.value, 'athlete_id': performance_metric.athlete_id} for performance_metric in performance_metrics])
    elif request.method == 'POST':
        data = request.get_json()
        performance_metric = PerformanceMetric(data['name'], data['value'], data['athlete_id'])
        db.session.add(performance_metric)
        db.session.commit()
        return jsonify({'id': performance_metric.id, 'name': performance_metric.name, 'value': performance_metric.value, 'athlete_id': performance_metric.athlete_id})

# Define the analytics functions
def predict_performance(athlete_id):
    """Predict athlete performance"""
    # Get the athlete's performance metrics
    performance_metrics = PerformanceMetric.query.filter_by(athlete_id=athlete_id).all()
    # Create a pandas dataframe
    df = pd.DataFrame([{'name': metric.name, 'value': metric.value} for metric in performance_metrics])
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(df[['value']], df['name'], test_size=0.2, random_state=42)y_train, y_test = df['value'], df['value']model.fit(X_train, y_train)
    # Make predictions
    predictions = model.predict(X_test)mse = mean_squared_error(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)
return mse, mae, r2return mse

def get_athlete_performance(athlete_id):
    """Get athlete performance"""
    # Get the athlete's performance metrics
    performance_metrics = PerformanceMetric.query.filter_by(athlete_id=athlete_id).all()
    # Create a pandas dataframe
    df = pd.DataFrame([{'name': metric.name, 'value': metric.value} for metric in performance_metrics])
    # Calculate the mean and standard deviation of the performance metrics
    mean = df['value'].mean()
    std = df['value'].std()
    return mean, std

# Define the dashboard API endpoint
@app.route('/dashboard', methods=['GET'])
def dashboard():
    """Dashboard API endpoint"""
    # Get the athlete's performance metrics
    performance_metrics = PerformanceMetric.query.all()
    # Create a pandas dataframe
    df = pd.DataFrame([{'name': metric.name, 'value': metric.value, 'athlete_id': metric.athlete_id} for metric in performance_metrics])
    # Calculate the mean and standard deviation of the performance metrics
    mean = df['value'].mean()
    std = df['value'].std()
    # Predict the athlete's performance
    predictions = predict_performance(1)
    return jsonify({'mean': mean, 'std': std, 'predictions': predictions})

if __name__ == '__main__':
    app.run(debug=True)

# frontend.py
# Import required libraries
import tkinter as tk
from tkinter import ttk

# Create a tkinter application
class SportTeamCoordinator:
    def __init__(self, root):
        self.root = root
        self.root.title('Sport Team Coordinator')
        # Create a notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)
        # Create frames for each tab
        self.athletes_frame = tk.Frame(self.notebook)
        self.workout_plans_frame = tk.Frame(self.notebook)
        self.game_strategies_frame = tk.Frame(self.notebook)
        self.performance_metrics_frame = tk.Frame(self.notebook)
        self.dashboard_frame = tk.Frame(self.notebook)
        # Add the frames to the notebook
        self.notebook.add(self.athletes_frame, text='Athletes')
        self.notebook.add(self.workout_plans_frame, text='Workout Plans')
        self.notebook.add(self.game_strategies_frame, text='Game Strategies')
        self.notebook.add(self.performance_metrics_frame, text='Performance Metrics')
        self.notebook.add(self.dashboard_frame, text='Dashboard')
        # Create the athlete tab
        self.create_athlete_tab()
        # Create the workout plan tab
        self.create_workout_plan_tab()
        # Create the game strategy tab
        self.create_game_strategy_tab()
        # Create the performance metric tab
        self.create_performance_metric_tab()
        # Create the dashboard tab
        self.create_dashboard_tab()

    def create_athlete_tab(self):
        # Create a label and entry for the athlete's name
        tk.Label(self.athletes_frame, text='Name:').pack()
        self.athlete_name_entry = tk.Entry(self.athletes_frame)
        self.athlete_name_entry.pack()
        # Create a label and entry for the athlete's email
        tk.Label(self.athletes_frame, text='Email:').pack()
        self.athlete_email_entry = tk.Entry(self.athletes_frame)
        self.athlete_email_entry.pack()
        # Create a button to add the athlete
        tk.Button(self.athletes_frame, text='Add Athlete', command=self.add_athlete).pack()

    def create_workout_plan_tab(self):
        # Create a label and entry for the workout plan's name
        tk.Label(self.workout_plans_frame, text='Name:').pack()
        self.workout_plan_name_entry = tk.Entry(self.workout_plans_frame)
        self.workout_plan_name_entry.pack()
        # Create a label and entry for the workout plan's description
        tk.Label(self.workout_plans_frame, text='Description:').pack()
        self.workout_plan_description_entry = tk.Entry(self.workout_plans_frame)
        self.workout_plan_description_entry.pack()
        # Create a label and entry for the athlete's id
        tk.Label(self.workout_plans_frame, text='Athlete ID:').pack()
        self.workout_plan_athlete_id_entry = tk.Entry(self.workout_plans_frame)
        self.workout_plan_athlete_id_entry.pack()
        # Create a button to add the workout plan
        tk.Button(self.workout_plans_frame, text='Add Workout Plan', command=self.add_workout_plan).pack()

    def create_game_strategy_tab(self):
        # Create a label and entry for the game strategy's name
        tk.Label(self.game_strategies_frame, text='Name:').pack()
        self.game_strategy_name_entry = tk.Entry(self.game_strategies_frame)
        self.game_strategy_name_entry.pack()
        # Create a label and entry for the game strategy's description
        tk.Label(self.game_strategies_frame, text='Description:').pack()
        self.game_strategy_description_entry = tk.Entry(self.game_strategies_frame)
        self.game_strategy_description_entry.pack()
        # Create a label and entry for the athlete's id
        tk.Label(self.game_strategies_frame, text='Athlete ID:').pack()
        self.game_strategy_athlete_id_entry = tk.Entry(self.game_strategies_frame)
        self.game_strategy_athlete_id_entry.pack()
        # Create a button to add the game strategy
        tk.Button(self.game_strategies_frame, text='Add Game Strategy', command=self.add_game_strategy).pack()

    def create_performance_metric_tab(self):
        # Create a label and entry for the performance metric's name
        tk.Label(self.performance_metrics_frame, text='Name:').pack()
        self.performance_metric_name_entry = tk.Entry(self.performance_metrics_frame)
        self.performance_metric_name_entry.pack()
        # Create a label and entry for the performance metric's value
        tk.Label(self.performance_metrics_frame, text='Value:').pack()
        self.performance_metric_value_entry = tk.Entry(self.performance_metrics_frame)
        self.performance_metric_value_entry.pack()
        # Create a label and entry for the athlete's id
        tk.Label(self.performance_metrics_frame, text='Athlete ID:').pack()
        self.performance_metric_athlete_id_entry = tk.Entry(self.performance_metrics_frame)
        self.performance_metric_athlete_id_entry.pack()
        # Create a button to add the performance metric
        tk.Button(self.performance_metrics_frame, text='Add Performance Metric', command=self.add_performance_metric).pack()

    def create_dashboard_tab(self):
        # Create a label to display the dashboard
        tk.Label(self.dashboard_frame, text='Dashboard').pack()
        # Create a button to view the dashboard
        tk.Button(self.dashboard_frame, text='View Dashboard', command=self.view_dashboard).pack()

    def add_athlete(self):
        # Get the athlete's name and email
        name = self.athlete_name_entry.get()
        email = self.athlete_email_entry.get()
        # Add the athlete to the database
        athlete = Athlete(name, email)
        db.session.add(athlete)
        db.session.commit()

    def add_workout_plan(self):
        # Get the workout plan's name, description, and athlete's id
        name = self.workout_plan_name_entry.get()
        description = self.workout_plan_description_entry.get()
        athlete_id = self.workout_plan_athlete_id_entry.get()
        # Add the workout plan to the database
        workout_plan = WorkoutPlan(name, description, athlete_id)
        db.session.add(workout_plan)
        db.session.commit()

    def add_game_strategy(self):
        # Get the game strategy's name, description, and athlete's id
        name = self.game_strategy_name_entry.get()
        description = self.game_strategy_description_entry.get()
        athlete_id = self.game_strategy_athlete_id_entry.get()
        # Add the game strategy to the database
        game_strategy = GameStrategy(name, description, athlete_id)
        db.session.add(game_strategy)
        db.session.commit()

    def add_performance_metric(self):
        # Get the performance metric's name, value, and athlete's id
        name = self.performance_metric_name_entry.get()
        value = self.performance_metric_value_entry.get()
        athlete_id = self.performance_metric_athlete_id_entry.get()
        # Add the performance metric to the database
        performance_metric = PerformanceMetric(name, value, athlete_id)
        db.session.add(performance_metric)
        db.session.commit()

    def view_dashboard(self):
        # Get the dashboard data
        dashboard_data = self.get_dashboard_data()
        # Display the dashboard data
        tk.Label(self.dashboard_frame, text=dashboard_data).pack()

    def get_dashboard_data(self):
        # Get the athlete's performance metrics
        performance_metrics = PerformanceMetric.query.all()
        # Create a pandas dataframe
        df = pd.DataFrame([{'name': metric.name, 'value': metric.value, 'athlete_id': metric.athlete_id} for metric in performance_metrics])
        # Calculate the mean and standard deviation of the performance metrics
        mean = df['value'].mean()
        std = df['value'].std()
        # Predict the athlete's performance
        predictions = predict_performance(1)
        return f'Mean: {mean}, Standard Deviation: {std}, Predictions: {predictions}'

if __name__ == '__main__':
    root = tk.Tk()
    app = SportTeamCoordinator(root)
    root.mainloop()