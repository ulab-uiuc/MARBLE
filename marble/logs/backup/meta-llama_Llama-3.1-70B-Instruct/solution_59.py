
# templates/index.html
<!DOCTYPE html>
<html>
<head>
    <title>Book Synergy</title>
    <script src="//cdnjs.cloudflare.com/ajax/libs/socket.io/2.2.0/socket.io.js" integrity="sha256-yr4fRk/GU1ehYJPAs8P4JlTgu0Hdsp4ZKrx8bDEDC3I=" crossorigin="anonymous"></script>
    <script>
        var socket = io();

        socket.on('connect', function() {
            console.log('Connected to the server');
        });

        socket.on('disconnect', function() {
            console.log('Disconnected from the server');
        });

        socket.on('project_created', function(data) {
            console.log(data.message);
        });

        socket.on('projects', function(data) {
            console.log(data);
        });

        socket.on('revisions', function(data) {
            console.log(data);
        });

        socket.on('revision_created', function(data) {
            console.log(data.message);
        });

        socket.on('collaborations', function(data) {
            console.log(data);
        });

        socket.on('collaboration_created', function(data) {
            console.log(data.message);
        });

        function createProject() {socket.emit('create_project', {title: 'New Project', description: 'This is a new project'});socket.emit('create_project', {title: 'New Project', description: 'This is a new project'});
        }

        function getProjects() {socket.emit('get_projects');socket.emit('get_projects');
        }

        function getRevisions(projectId) {socket.emit('get_revisions', projectId);socket.emit('get_revisions', projectId);
        }

        function createRevision(projectId, content) {socket.emit('create_revision', projectId, content);socket.emit('create_revision', projectId, content);
        }

        function getCollaborations(projectId) {socket.emit('get_collaborations', projectId);socket.emit('get_collaborations', projectId);
        }

        function createCollaboration(projectId, action) {socket.emit('create_collaboration', projectId, action);socket.emit('create_collaboration', projectId, action);
        }
    </script>
</head>
<body>
    <h1>Book Synergy</h1>
    <button onclick="createProject()">Create Project</button>
    <button onclick="getProjects()">Get Projects</button>
    <button onclick="getRevisions(1)">Get Revisions</button>
    <button onclick="createRevision(1, 'New Revision')">Create Revision</button>
    <button onclick="getCollaborations(1)">Get Collaborations</button>
    <button onclick="createCollaboration(1, 'New Collaboration')">Create Collaboration</button>
</body>
</html>from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emitfrom flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from models import db, User, Project, Revision, CollaborationLog

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book_synergy.db'
db.init_app(app)
CORS(app)
socketio = SocketIO(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@socketio.on('create_project')
def create_project(data):
@login_required
@socketio.on('create_project')
def create_project(data):
    if current_user.id != data['owner_id']:
        return jsonify({'message': 'Unauthorized access'}), 401
    project = Project(title=data['title'], description=data['description'], owner_id=current_user.id)
    db.session.add(project)
    db.session.commit()
    emit('project_created', {'message': 'Project created successfully'})

@socketio.on('create_revision')
def create_revision(data):
@login_required
@socketio.on('create_revision')
def create_revision(data):
    project = Project.query.get(data['project_id'])
    if project and project.owner_id != current_user.id:
        return jsonify({'message': 'Unauthorized access'}), 401
    project = Project.query.get(data['project_id'])
    if project:
        revision = Revision(content=data['content'], project=project)
        db.session.add(revision)
        db.session.commit()
        emit('revision_created', {'message': 'Revision created successfully'})

@socketio.on('create_collaboration')
def create_collaboration(data):
@login_required
@socketio.on('create_collaboration')
def create_collaboration(data):
    project = Project.query.get(data['project_id'])
    if project and project.owner_id != current_user.id:
        return jsonify({'message': 'Unauthorized access'}), 401
    project = Project.query.get(data['project_id'])
    if project:
        collaboration = CollaborationLog(action=data['action'], project=project, user_id=current_user.id)
        db.session.add(collaboration)
        db.session.commit()
        emit('collaboration_created', {'message': 'Collaboration created successfully'})# models.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    """User model for storing user data."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    projects = db.relationship('Project', backref='owner', lazy=True)

    def set_password(self, password):
        """Set password for the user."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check password for the user."""
        return check_password_hash(self.password_hash, password)


class Project(db.Model):
    """Project model for storing project metadata."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    revisions = db.relationship('Revision', backref='project', lazy=True)


class Revision(db.Model):
    """Revision model for storing content revisions."""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())


class CollaborationLog(db.Model):
    """CollaborationLog model for storing collaboration logs."""
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())


# app.py
from flask import Flask, request, jsonify
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from flask_cors import CORS
from models import db, User, Project, Revision, CollaborationLog

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book_synergy.db'
db.init_app(app)
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.query.get(int(user_id))


@app.route('/login', methods=['POST'])
def login():
    """Login user."""
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user)
        return jsonify({'message': 'Logged in successfully'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    """Logout user."""
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200


@app.route('/projects', methods=['GET'])
@login_required
def get_projects():import requests
response = requests.get('http://localhost:5000/projects')
emit('projects', response.json())    # Call the backend API to get all projects
    emit('projects', [{'title': 'Project 1'}, {'title': 'Project 2'}])

@socketio.on('get_revisions')
def get_revisions(project_id):
@login_required
@socketio.on('get_revisions')
def get_revisions(project_id):
    project = Project.query.get(project_id)
    if project and project.owner_id != current_user.id:
        return jsonify({'message': 'Unauthorized access'}), 401import requests
response = requests.get(f'http://localhost:5000/projects/{project_id}/revisions')
emit('revisions', response.json())    # Call the backend API to get all revisions for a project
    emit('revisions', [{'content': 'Revision 1'}, {'content': 'Revision 2'}])

@socketio.on('create_revision')
def create_revision(project_id, content):import requests
response = requests.post(f'http://localhost:5000/projects/{project_id}/revisions', json={'content': content})
emit('revision_created', response.json())    # Call the backend API to create a new revision for a project
    emit('revision_created', {'message': 'Revision created successfully'})

@socketio.on('get_collaborations')
def get_collaborations(project_id):
@login_required
@socketio.on('get_collaborations')
def get_collaborations(project_id):
    project = Project.query.get(project_id)
    if project and project.owner_id != current_user.id:
        return jsonify({'message': 'Unauthorized access'}), 401import requests
response = requests.get(f'http://localhost:5000/projects/{project_id}/collaborations')
emit('collaborations', response.json())    # Call the backend API to get all collaborations for a project
    emit('collaborations', [{'action': 'Collaboration 1'}, {'action': 'Collaboration 2'}])

@socketio.on('create_collaboration')
def create_collaboration(project_id, action):import requests
response = requests.post(f'http://localhost:5000/projects/{project_id}/collaborations', json={'action': action})
emit('collaboration_created', response.json())    # Call the backend API to create a new collaboration for a project
    emit('collaboration_created', {'message': 'Collaboration created successfully'})

if __name__ == '__main__':
    socketio.run(app)

# templates/index.html
<!DOCTYPE html>
<html>
<head>
    <title>Book Synergy</title>
    <script src="//cdnjs.cloudflare.com/ajax/libs/socket.io/2.2.0/socket.io.js" integrity="sha256-yr4fRk/GU1ehYJPAs8P4JlTgu0Hdsp4ZKrx8bDEDC3I=" crossorigin="anonymous"></script>
    <script>
        var socket = io();

        socket.on('connect', function() {
            console.log('Connected to the server');
        });

        socket.on('disconnect', function() {
            console.log('Disconnected from the server');
        });

        socket.on('project_created', function(data) {
            console.log(data.message);
        });

        socket.on('projects', function(data) {
            console.log(data);
        });

        socket.on('revisions', function(data) {
            console.log(data);
        });

        socket.on('revision_created', function(data) {
            console.log(data.message);
        });

        socket.on('collaborations', function(data) {
            console.log(data);
        });

        socket.on('collaboration_created', function(data) {
            console.log(data.message);
        });

        function createProject() {fetch('/projects', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({title: 'New Project', description: 'This is a new project'})}).then(response => response.json()).then(data => console.log(data));
            socket.emit('create_project', {title: 'New Project', description: 'This is a new project'});
        }

        function getProjects() {fetch('/projects').then(response => response.json()).then(data => console.log(data));
            socket.emit('get_projects');
        }

        function getRevisions(projectId) {fetch(`/projects/${projectId}/revisions`).then(response => response.json()).then(data => console.log(data));
            socket.emit('get_revisions', projectId);
        }

        function createRevision(projectId, content) {fetch(`/projects/${projectId}/revisions`, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({content: content})}).then(response => response.json()).then(data => console.log(data));
            socket.emit('create_revision', projectId, content);
        }

        function getCollaborations(projectId) {fetch(`/projects/${projectId}/collaborations`).then(response => response.json()).then(data => console.log(data));
            socket.emit('get_collaborations', projectId);
        }

        function createCollaboration(projectId, action) {fetch(`/projects/${projectId}/collaborations`, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({action: action})}).then(response => response.json()).then(data => console.log(data));
            socket.emit('create_collaboration', projectId, action);
        }
    </script>
</head>
<body>
    <h1>Book Synergy</h1>
    <button onclick="createProject()">Create Project</button>
    <button onclick="getProjects()">Get Projects</button>
    <button onclick="getRevisions(1)">Get Revisions</button>
    <button onclick="createRevision(1, 'New Revision')">Create Revision</button>
    <button onclick="getCollaborations(1)">Get Collaborations</button>
    <button onclick="createCollaboration(1, 'New Collaboration')">Create Collaboration</button>
</body>
</html>