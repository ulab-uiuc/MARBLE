# solution.py
# TeamSyncPro: A Comprehensive Project Management System

# Import required librariesfrom flask import Flask, request, jsonify
from flask_bcrypt import Bcryptfrom flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import datetime
import os

# Create the Flask application
app = Flask(__name__)

# Configure the application
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///team_sync_pro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'

# Initialize the database, marshmallow, and JWT manager
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
ma = Marshmallow(app)
api = Api(app)
jwt = JWTManager(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)password_hash = db.Column(db.String(100), nullable=False)role = db.Column(db.String(100), nullable=False)

    def __init__(self, username, email, password, role):
        self.username = username
        self.email = emailself.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')self.role = role

# Define the Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, title, description, status, assigned_to):
        self.title = title
        self.description = description
        self.status = status
        self.assigned_to = assigned_to

# Define the CommunicationLog model
class CommunicationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(200), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, message, sender_id, receiver_id):
        self.message = message
        self.sender_id = sender_id
        self.receiver_id = receiver_id

# Define the schema for the User model
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

# Define the schema for the Task model
class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        load_instance = True

# Define the schema for the CommunicationLog model
class CommunicationLogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CommunicationLog
        load_instance = True

# Create the database tables
with app.app_context():
    db.create_all()

# Define the API endpoints
class Login(Resource):
    def post(self):
        # Get the username and password from the requestusername = request.json.get('username')
password = request.json.get('password')

if not username or not password:
    return {'error': 'Username and password are required'}, 400

# Find the user with the given username and password
user = User.query.filter_by(username=username).first()
if not user:
    return {'error': 'Invalid username or password'}, 401
if user and bcrypt.check_password_hash(user.password_hash, password):# If the user exists, create an access token and return it
        if user:
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}
        else:
            return {'error': 'Invalid username or password'}, 401

class Register(Resource):
    def post(self):
        # Get the username, email, password, and role from the request
        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')
        role = request.json.get('role')

        # Create a new user and add it to the database
        user = User(username, email, password, role)
        db.session.add(user)
        db.session.commit()

        return {'message': 'User created successfully'}

class Tasks(Resource):
    @jwt_required
    def get(self):
        # Get the tasks for the current user
        tasks = Task.query.filter_by(assigned_to=get_jwt_identity()).all()

        # Return the tasks in JSON format
        task_schema = TaskSchema(many=True)
        return task_schema.dump(tasks)

    @jwt_required
    def post(self):
        # Get the title, description, and status from the request
        title = request.json.get('title')
        description = request.json.get('description')
        status = request.json.get('status')

        # Create a new task and add it to the database
        task = Task(title, description, status, get_jwt_identity())
        db.session.add(task)
        db.session.commit()

        return {'message': 'Task created successfully'}

class TaskDetail(Resource):
    @jwt_required
    def get(self, task_id):
        # Get the task with the given ID
        task = Task.query.get(task_id)

        # If the task exists, return it in JSON format
        if task:
            task_schema = TaskSchema()
            return task_schema.dump(task)
        else:
            return {'error': 'Task not found'}, 404

    @jwt_required
    def put(self, task_id):
        # Get the task with the given ID
        task = Task.query.get(task_id)

        # If the task exists, update its status and return a success message
        if task:
            task.status = request.json.get('status')
            db.session.commit()
            return {'message': 'Task updated successfully'}
        else:
            return {'error': 'Task not found'}, 404

    @jwt_required
    def delete(self, task_id):
        # Get the task with the given ID
        task = Task.query.get(task_id)

        # If the task exists, delete it and return a success message
        if task:
            db.session.delete(task)
            db.session.commit()
            return {'message': 'Task deleted successfully'}
        else:
            return {'error': 'Task not found'}, 404

class CommunicationLogs(Resource):
    @jwt_required
    def get(self):
        # Get the communication logs for the current user
        communication_logs = CommunicationLog.query.filter_by(sender_id=get_jwt_identity()).all()

        # Return the communication logs in JSON format
        communication_log_schema = CommunicationLogSchema(many=True)
        return communication_log_schema.dump(communication_logs)

    @jwt_required
    def post(self):
        # Get the message and receiver ID from the request
        message = request.json.get('message')
        receiver_id = request.json.get('receiver_id')

        # Create a new communication log and add it to the database
        communication_log = CommunicationLog(message, get_jwt_identity(), receiver_id)
        db.session.add(communication_log)
        db.session.commit()

        return {'message': 'Communication log created successfully'}

# Add the API endpoints to the API
api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(Tasks, '/tasks')
api.add_resource(TaskDetail, '/tasks/<int:task_id>')
api.add_resource(CommunicationLogs, '/communication-logs')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)