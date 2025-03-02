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
    projects = db.relationship('Project', backref='owner', lazy=True)

class Project(db.Model):
    """Model for collaborative projects."""
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
    """Register a new user."""@app.route('/projects/<int:project_id>', methods=['GET'])
@login_required
def get_project(project_id):
    """Get project details."""
    project = Project.query.get_or_404(project_id)
    if project.owner_id != current_user.id:
        return jsonify({"message": "Forbidden"}), 403    return jsonify({"title": project.title, "content": project.content}), 200

@app.route('/projects/<int:project_id>/revisions', methods=['POST'])
@login_required
def add_revision(project_id):
    """Add a new revision to a project."""
    data = request.get_json()
    new_revision = Revision(content=data['content'], project_id=project_id)
    db.session.add(new_revision)
    db.session.commit()
    return jsonify({"message": "Revision added successfully!"}), 201

@app.route('/projects/<int:project_id>/content', methods=['GET'])
@login_required
def get_project_content(project_id):
    """Get project content in markdown format."""
    project = Project.query.get_or_404(project_id)
    html_content = markdown.markdown(project.content)  # Convert markdown to HTML
    return jsonify({"content": html_content}), 200

# Run the application
if __name__ == '__main__':
    db.create_all()  # Create database tables
    app.run(debug=True)  # Start the Flask application