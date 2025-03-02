# solution.py
# Importing required libraries
import os
import uuid
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_cors import CORS
from markdown import markdown
from werkzeug.utils import secure_filename

# Creating a new Flask application
app = Flask(__name__)

# Configuring the application
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book_synergy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a random secret key
app.config['UPLOAD_FOLDER'] = 'uploads'

# Initializing the database, marshmallow, bcrypt, and jwt
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)

# Defining the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    projects = db.relationship('Project', backref='author', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

# Defining the Project model
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    revisions = db.relationship('Revision', backref='project', lazy=True)

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id

# Defining the Revision model
class Revision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, content, project_id, user_id):
        self.content = content
        self.project_id = project_id
        self.user_id = user_id

# Defining the UserSchema
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

# Defining the ProjectSchema
class ProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        load_instance = True

# Defining the RevisionSchema
class RevisionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Revision
        load_instance = True

# Creating the database tables
db.create_all()

# Defining the login route
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    return jsonify({'msg': 'Bad username or password'}), 401

# Defining the register route
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'msg': 'Username already exists'}), 400
    user = User(username, email, password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'User created successfully'}), 201

# Defining the create project route
@app.route('/projects', methods=['POST'])
@jwt_required
def create_project():
    title = request.json.get('title')
    content = request.json.get('content')
    user_id = get_jwt_identity()
    project = Project(title, content, user_id)
    db.session.add(project)
    db.session.commit()
    return jsonify({'msg': 'Project created successfully'}), 201

# Defining the get project route
@app.route('/projects/<int:project_id>', methods=['GET'])
@jwt_required
def get_project(project_id):
    project = Project.query.get(project_id)
    if project:
        return jsonify(ProjectSchema().dump(project))
    return jsonify({'msg': 'Project not found'}), 404

# Defining the update project route
@app.route('/projects/<int:project_id>', methods=['PUT'])
@jwt_required
def update_project(project_id):
    project = Project.query.get(project_id)
    if project:
        title = request.json.get('title')
        content = request.json.get('content')
        project.title = title
        project.content = content
        db.session.commit()
        return jsonify({'msg': 'Project updated successfully'}), 200
    return jsonify({'msg': 'Project not found'}), 404

# Defining the delete project route
@app.route('/projects/<int:project_id>', methods=['DELETE'])
@jwt_required
def delete_project(project_id):
    project = Project.query.get(project_id)
    if project:
        db.session.delete(project)
        db.session.commit()
        return jsonify({'msg': 'Project deleted successfully'}), 200
    return jsonify({'msg': 'Project not found'}), 404

# Defining the create revision route
@app.route('/revisions', methods=['POST'])
@jwt_required
def create_revision():
    project_id = request.json.get('project_id')
    content = request.json.get('content')
    user_id = get_jwt_identity()
    revision = Revision(content, project_id, user_id)
    db.session.add(revision)
    db.session.commit()
    return jsonify({'msg': 'Revision created successfully'}), 201

# Defining the get revision route
@app.route('/revisions/<int:revision_id>', methods=['GET'])
@jwt_required
def get_revision(revision_id):
    revision = Revision.query.get(revision_id)
    if revision:
        return jsonify(RevisionSchema().dump(revision))
    return jsonify({'msg': 'Revision not found'}), 404

# Defining the update revision route
@app.route('/revisions/<int:revision_id>', methods=['PUT'])
@jwt_required
def update_revision(revision_id):
    revision = Revision.query.get(revision_id)
    if revision:
        content = request.json.get('content')
        revision.content = content
        db.session.commit()
        return jsonify({'msg': 'Revision updated successfully'}), 200
    return jsonify({'msg': 'Revision not found'}), 404

# Defining the delete revision route
@app.route('/revisions/<int:revision_id>', methods=['DELETE'])
@jwt_required
def delete_revision(revision_id):
    revision = Revision.query.get(revision_id)
    if revision:
        db.session.delete(revision)
        db.session.commit()
        return jsonify({'msg': 'Revision deleted successfully'}), 200
    return jsonify({'msg': 'Revision not found'}), 404

# Defining the upload file route
@app.route('/upload', methods=['POST'])
@jwt_required
def upload_file():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return jsonify({'msg': 'File uploaded successfully'}), 201

# Running the application
if __name__ == '__main__':
    app.run(debug=True)