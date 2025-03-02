# solution.py
# Import required libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS
from datetime import datetime

# Create the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///team_sync_pro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'

# Initialize the database, marshmallow, and JWT
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
jwt = JWTManager(app)
CORS(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)

    def __init__(self, username, email, password, role):
        self.username = username
        self.email = email
        self.password = password
        self.role = role

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
class CommunicationLogSchema(ma.SQLAlchemyAutoSchema):from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
class Register(Resource):
    def post(self):
        # Register a new user
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if not data['username'] or not data['password']:
            return jsonify({'message': 'All fields are required'}), 400
        if user:
            return jsonify({'message': 'Username already exists'}), 400
        new_user = User(username=data['username'], email=data['email'], password=bcrypt.generate_password_hash(data['password']).decode('utf-8'), role=data['role'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201    def post(self):
        # Register a new user
        data = request.get_json()user = User.query.filter_by(username=data['username']).first()
        if not data['username'] or not data['password']:
            return jsonify({'message': 'All fields are required'}), 400
        if not user:
            return jsonify({'message': 'Invalid username or password'}), 401if user and bcrypt.check_password_hash(user.password, data['password']):
        if user:
            access_token = create_access_token(identity=user.id)
            return jsonify({'access_token': access_token}), 200
        return jsonify({'message': 'Invalid username or password'}), 401

class TaskAssignment(Resource):
    @jwt_required
    def post(self):
        # Assign a task to a user
        data = request.get_json()
        new_task = Task(title=data['title'], description=data['description'], status='pending', assigned_to=data['assigned_to'])
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task assigned successfully'}), 201

class TaskStatusUpdate(Resource):
    @jwt_required
    def put(self, task_id):
        # Update the status of a task
        data = request.get_json()
        task = Task.query.get(task_id)
        if task:
            task.status = data['status']
            db.session.commit()
            return jsonify({'message': 'Task status updated successfully'}), 200
        return jsonify({'message': 'Task not found'}), 404

class RealTimeCommunication(Resource):
    @jwt_required
    def post(self):
        # Send a message to a user
        data = request.get_json()
        new_message = CommunicationLog(message=data['message'], sender_id=get_jwt_identity(), receiver_id=data['receiver_id'])
        db.session.add(new_message)
        db.session.commit()
        return jsonify({'message': 'Message sent successfully'}), 201

class ReportingModule(Resource):
    @jwt_required
    def get(self):
        # Generate a report
        tasks = Task.query.all()
        report = []
        for task in tasks:
            report.append({
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'assigned_to': task.assigned_to
            })
        return jsonify(report), 200

# Add the API endpoints to the API
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(TaskAssignment, '/assign-task')
api.add_resource(TaskStatusUpdate, '/update-task-status/<int:task_id>')
class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            return jsonify({'message': 'Invalid username or password'}), 401
        if bcrypt.check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.id)
            return jsonify({'access_token': access_token}), 200
        return jsonify({'message': 'Invalid username or password'}), 401
api.add_resource(Login, '/login')
api.add_resource(RealTimeCommunication, '/send-message')
api.add_resource(ReportingModule, '/generate-report')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)