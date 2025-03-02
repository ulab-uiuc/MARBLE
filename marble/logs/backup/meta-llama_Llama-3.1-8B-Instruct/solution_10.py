# team_sync_pro.py
# This is the main implementation of TeamSyncPro

# Importing required libraries
import sqlite3
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from datetime import datetime, timedelta

# Creating a Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'  # Change this to a random secret key
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a random secret key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Creating a JWT manager
jwt = JWTManager(app)

# Creating a RESTful API
api = Api(app)

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
        message TEXT NOT NULL,
        sender INTEGER NOT NULL,
        receiver INTEGER NOT NULL,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (sender) REFERENCES users (id),
        FOREIGN KEY (receiver) REFERENCES users (id)
    )
''')

# Committing changes to the database
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
    def __init__(self, id, message, sender, receiver, timestamp):
        self.id = id
        self.message = message
        self.sender = sender
        self.receiver = receiver
        self.timestamp = timestamp

# Creating a login endpoint
class Login(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        if user:
            access_token = create_access_token(identity=username)
            return {'access_token': access_token}
        return {'error': 'Invalid username or password'}, 401

# Creating a task endpoint
class TaskEndpoint(Resource):
    @jwt_required
    def get(self):
        cursor.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()
        return [Task(*task) for task in tasks]

    @jwt_required
    def post(self):
        title = request.json.get('title')
        description = request.json.get('description')
        assigned_to = request.json.get('assigned_to')
        status = request.json.get('status')
        cursor.execute('INSERT INTO tasks (title, description, assigned_to, status) VALUES (?, ?, ?, ?)', (cursor.execute('INSERT INTO tasks (title, description, assigned_to, status) VALUES (?, ?, ?, ?)', (task_data['title'], task_data['description'], task_data['assigned_to'], task_data['status'])), status))conn.commit()
    return {'message': 'Task created successfully'}return {'message': 'Task created successfully'}

# Creating a communication log endpoint
class CommunicationLogEndpoint(Resource):
    @jwt_required
    def post(self):
        message = request.json.get('message')
        sender = request.json.get('sender')
        receiver = request.json.get('receiver')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('INSERT INTO communication_logs (message, sender, receiver, timestamp) VALUES (?, ?, ?, ?)', (message, sender, receiver, timestamp))
        conn.commit()
        return {'message': 'Communication log created successfully'}

# Adding endpoints to the API
api.add_resource(Login, '/login')
api.add_resource(TaskEndpoint, '/tasks')
api.add_resource(CommunicationLogEndpoint, '/communication_logs')

# Running the application
if __name__ == '__main__':
    app.run(debug=True)