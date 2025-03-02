# solution.py

# Import necessary libraries
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teamsyncpro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(50), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Communication log model
class CommunicationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# User schema
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

# Task schema
class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task

# Communication log schema
class CommunicationLogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CommunicationLog

# Initialize schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
communication_log_schema = CommunicationLogSchema()
communication_logs_schema = CommunicationLogSchema(many=True)

# Create a new user
@app.route('/users', methods=['POST'])
def add_user():
    username = request.json['username']
    role = request.json['role']
    new_user = User(username=username, role=role)
# Create a new task
@app.route('/tasks', methods=['POST'])
def add_task():
    title = request.json['title']
    description = request.json.get('description', '')
    assigned_to = request.json['assigned_to']
    user = User.query.get(assigned_to)
    if not user:
        return jsonify({'message': 'User not found'}), 400
    new_task = Task(title=title, description=description, assigned_to=assigned_to)
    db.session.add(new_task)
    db.session.commit()
    return task_schema.jsonify(new_task)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()
    return tasks_schema.jsonify(all_tasks)

# Update task status
@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    if task:
        task.status = request.json['status']
        db.session.commit()
        return task_schema.jsonify(task)
    return jsonify({'message': 'Task not found'}), 404

# Log communication
@app.route('/communication', methods=['POST'])
def log_communication():
    user_id = request.json['user_id']
    message = request.json['message']
    new_log = CommunicationLog(user_id=user_id, message=message)
    db.session.add(new_log)
    db.session.commit()
    return communication_log_schema.jsonify(new_log)

# Get all communication logs
@app.route('/communication', methods=['GET'])
def get_communication_logs():
    all_logs = CommunicationLog.query.all()
    return communication_logs_schema.jsonify(all_logs)

# Run the application
if __name__ == '__main__':
    db.create_all()  # Create database tables
    app.run(debug=True)  # Run the Flask application