# database.py
import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, db_file):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)

    def create_tables(self):
        # Create user profiles table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS users
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT NOT NULL, 
            email TEXT NOT NULL, 
            password TEXT NOT NULL)
        ''')

        # Create project metadata table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS projects
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
            title TEXT NOT NULL, 
            description TEXT NOT NULL, 
            created_by INTEGER NOT NULL,
            FOREIGN KEY (created_by) REFERENCES users (id))
        ''')

        # Create content revisions table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS revisions
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
            project_id INTEGER NOT NULL, 
            content TEXT NOT NULL, 
            created_by INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (project_id) REFERENCES projects (id),
            FOREIGN KEY (created_by) REFERENCES users (id))
        ''')

        # Create collaboration logs table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS collaboration_logs
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
            project_id INTEGER NOT NULL, 
            user_id INTEGER NOT NULL, 
            action TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (project_id) REFERENCES projects (id),
            FOREIGN KEY (user_id) REFERENCES users (id))
        ''')

    def insert_user(self, username, email, password):
        self.conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
        self.conn.commit()

    def insert_project(self, title, description, created_by):
        self.conn.execute('INSERT INTO projects (title, description, created_by) VALUES (?, ?, ?)', (title, description, created_by))
        self.conn.commit()

    def insert_revision(self, project_id, content, created_by, created_at):
        self.conn.execute('INSERT INTO revisions (project_id, content, created_by, created_at) VALUES (?, ?, ?, ?)', (project_id, content, created_by, created_at))
        self.conn.commit()

    def insert_collaboration_log(self, project_id, user_id, action, created_at):
        self.conn.execute('INSERT INTO collaboration_logs (project_id, user_id, action, created_at) VALUES (?, ?, ?, ?)', (project_id, user_id, action, created_at))
        self.conn.commit()

    def close_connection(self):
        if self.conn:
            self.conn.close()


# backend.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Revision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

class CollaborationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user)
        return jsonify({'message': 'Logged in successfully'})
    return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@app.route('/create_project', methods=['POST'])
@login_required
def create_project():
    title = request.json['title']
    description = request.json['description']
    project = Project(title=title, description=description, created_by=current_user.id)
    db.session.add(project)
    db.session.commit()
    return jsonify({'message': 'Project created successfully'})

@app.route('/create_revision', methods=['POST'])
@login_required
def create_revision():
    project_id = request.json['project_id']
    content = request.json['content']
    revision = Revision(project_id=project_id, content=content, created_by=current_user.id)
    db.session.add(revision)
    db.session.commit()
    return jsonify({'message': 'Revision created successfully'})

@app.route('/create_collaboration_log', methods=['POST'])
@login_required
def create_collaboration_log():
    project_id = request.json['project_id']
    action = request.json['action']
    collaboration_log = CollaborationLog(project_id=project_id, user_id=current_user.id, action=action)
    db.session.add(collaboration_log)
    db.session.commit()
    return jsonify({'message': 'Collaboration log created successfully'})


# frontend.py
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def connect():
    emit('message', {'data': 'Connected'})

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

@socketio.on('create_project')
def create_project(data):
    # Call backend API to create project
    project = {'title': data['title'], 'description': data['description']}
    # Send project data to backend
    emit('project_created', project)

@socketio.on('create_revision')
def create_revision(data):
    # Call backend API to create revision
    revision = {'project_id': data['project_id'], 'content': data['content']}
    # Send revision data to backend
    emit('revision_created', revision)

@socketio.on('create_collaboration_log')
def create_collaboration_log(data):
    # Call backend API to create collaboration log
    collaboration_log = {'project_id': data['project_id'], 'action': data['action']}
    # Send collaboration log data to backend
    emit('collaboration_log_created', collaboration_log)


# solution.py
from database import Database
from backend import app as backend_app
from frontend import app as frontend_app
from flask import Flask

if __name__ == '__main__':
    # Initialize database
    db = Database('database.db')
    db.create_tables()
    db.close_connection()

    # Run backend and frontend apps
    backend_app.run(port=5000)
    frontend_app.run(port=5001)