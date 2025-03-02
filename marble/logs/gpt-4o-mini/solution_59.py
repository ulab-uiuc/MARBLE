# solution.py

# Import necessary libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import markdown

# Initialize the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///booksynergy.db'  # Database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Secret key for session management

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)  # Enable CORS for all routes
bcrypt = Bcrypt(app)  # For password hashing
login_manager = LoginManager(app)  # For user session management

# Database models
class User(db.Model, UserMixin):
    """Model for user profiles."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    projects = db.relationship('Project', backref='owner', lazy=True)class Revision(db.Model):
    """Model for content revisions."""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())class Project(db.Model):
    """Model for collaborative book projects."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    revisions = db.relationship('Revision', backref='project', lazy=True)

class Revision(db.Model):
    """Model for content revisions."""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# API routes
@app.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

@app.route('/login', methods=['POST'])
def login():
    """User login."""
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        login_user(user)
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"message": "Invalid credentials!"}), 401

@app.route('/projects', methods=['POST'])
@login_required
def create_project():
    """Create a new project."""
    data = request.get_json()
    new_project = Project(title=data['title'], content=data['content'], owner_id=current_user.id)
    db.session.add(new_project)
    db.session.commit()
    return jsonify({"message": "Project created successfully!"}), 201

@app.route('/projects/<int:project_id>', methods=['GET'])
@login_required
def get_project(project_id):
    """Get project details."""    new_revision = Revision(content=data['content'], project_id=project_id, user_id=current_user.id)
    db.session.add(new_revision)
    db.session.commit()
    return jsonify({"message": "Revision added successfully!"}), 201    new_revision = Revision(content=data['content'], project_id=project_id)
    db.session.add(new_revision)
    db.session.commit()
    return jsonify({"message": "Revision added successfully!"}), 201

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    """User logout."""
    logout_user()
    return jsonify({"message": "Logout successful!"}), 200

# Run the application
if __name__ == '__main__':
    db.create_all()  # Create database tables
    app.run(debug=True)  # Run the Flask application