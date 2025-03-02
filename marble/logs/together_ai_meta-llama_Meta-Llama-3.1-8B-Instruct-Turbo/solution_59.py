# solution.py
# Importing required libraries
import os
import uuid
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from flask_ckeditor import CKEditor

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book_synergy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key_here'

# Initialize Flask-SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-Ma
ma = Marshmallow(app)

# Initialize Flask-JWT-Extended
jwt = JWTManager(app)

# Initialize Flask-WTF
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(), Length(min=4, max=64)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=128)])

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(), Length(min=4, max=64)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=128)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])

# Initialize Flask-CKEditor
ckeditor = CKEditor(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    projects = db.relationship('Project', backref='author', lazy=True)

    def __init__(self, email, password):
        self.email = email
        self.password = password

# Define Project model
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    revisions = db.relationship('Revision', backref='project', lazy=True)

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id

# Define Revision model
class Revision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __init__(self, content, project_id):
        self.content = content
        self.project_id = project_id

# Define UserSchema
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

# Define ProjectSchema
class ProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        load_instance = True

# Define RevisionSchema
class RevisionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Revision
        load_instance = True

# Create database tables
with app.app_context():
    db.create_all()

# Define routes
@app.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token), 200
    return jsonify(error='Invalid credentials'), 401

@app.route('/register', methods=['POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return jsonify(message='User created successfully'), 201
    return jsonify(error='Invalid form data'), 400

@app.route('/projects', methods=['POST'])
@jwt_required
def create_project():
    title = request.json.get('title')
    content = request.json.get('content')
    user_id = get_jwt_identity()
    project = Project(title=title, content=content, user_id=user_id)
    db.session.add(project)
    db.session.commit()
    return jsonify(message='Project created successfully'), 201

@app.route('/projects/<int:project_id>/revisions', methods=['POST'])
@jwt_required
def create_revision(project_id):
    content = request.json.get('content')
    revision = Revision(content=content, project_id=project_id)
    db.session.add(revision)
    db.session.commit()
    return jsonify(message='Revision created successfully'), 201

# Run the app
if __name__ == '__main__':
    app.run(debug=True)