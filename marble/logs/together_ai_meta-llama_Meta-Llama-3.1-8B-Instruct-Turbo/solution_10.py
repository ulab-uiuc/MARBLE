# team_sync_pro.py
# This is the main implementation file for TeamSyncPro

# Importing required libraries
import sqlite3
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_cors import CORS
import pandas as pd
import calendar
import datetime

# Creating a Flask application
app = Flask(__name__)
CORS(app)
api = Api(app)

# Configuring the application
app.config['SECRET_KEY'] = 'super-secret'  # Change this to a random secret key
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a random secret key
jwt = JWTManager(app)

# Creating a SQLite database connection
conn = sqlite3.connect('team_sync_pro.db')
cursor = conn.cursor()

# Creating tables in the database
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        assigned_to INTEGER NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (assigned_to) REFERENCES users (id)
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS communication_logs (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')
conn.commit()

# Creating a user class
class User:
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

# Creating a task class
class Task:
    def __init__(self, id, title, description, assigned_to, status):
        self.id = id
        self.title = title
        self.description = description
        self.assigned_to = assigned_to
        self.status = status

# Creating a communication log class
class CommunicationLog:
    def __init__(self, id, user_id, message, timestamp):
        self.id = id
        self.user_id = user_id
        self.message = message
        self.timestamp = timestamp

# Creating a RESTful API endpoint for user registration
class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        role = data['role']
        cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
        conn.commit()
        return {'message': 'User registered successfully'}, 201

# Creating a RESTful API endpoint for user login
class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        if user:
            access_token = create_access_token(identity=username)
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Invalid username or password'}, 401

# Creating a RESTful API endpoint for task creation
class TaskCreation(Resource):
    @jwt_required
    def post(self):
        data = request.get_json()
        title = data['title']
        description = data['description']
        assigned_to = data['assigned_to']
        status = data['status']
        cursor.execute('INSERT INTO tasks (title, description, assigned_to, status) VALUES (?, ?, ?, ?)', (title, description, assigned_to, status))
        conn.commit()
        return {'message': 'Task created successfully'}, 201

# Creating a RESTful API endpoint for task retrieval
class TaskRetrieval(Resource):
    @jwt_required
    def get(self):
        cursor.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()
        return {'tasks': tasks}, 200

# Creating a RESTful API endpoint for communication log creation
class CommunicationLogCreation(Resource):
    @jwt_required
    def post(self):
        data = request.get_json()
        user_id = data['user_id']
        message = data['message']
        timestamp = data['timestamp']
        cursor.execute('INSERT INTO communication_logs (user_id, message, timestamp) VALUES (?, ?, ?)', (user_id, message, timestamp))
        conn.commit()
        return {'message': 'Communication log created successfully'}, 201

# Creating a RESTful API endpoint for communication log retrieval
class CommunicationLogRetrieval(Resource):
    @jwt_required
    def get(self):
        cursor.execute('SELECT * FROM communication_logs')
        communication_logs = cursor.fetchall()
        return {'communication_logs': communication_logs}, 200

# Adding RESTful API endpoints to the application
api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(TaskCreation, '/tasks')
api.add_resource(TaskRetrieval, '/tasks/retrieve')
api.add_resource(CommunicationLogCreation, '/communication_logs')
api.add_resource(CommunicationLogRetrieval, '/communication_logs/retrieve')

# Running the application
if __name__ == '__main__':
    app.run(debug=True)