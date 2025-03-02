# solution.py

# Import necessary libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///language_collaborator.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model for authentication
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    exercises = db.relationship('Exercise', backref='author', lazy=True)

# Exercise model for language exercises
class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    feedback = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route for user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(username=data['username'], password=generate_password_hash(data['password'], method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        login_user(user)
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"message": "Invalid credentials!"}), 401

# Route for creating a new exercise
@app.route('/exercise', methods=['POST'])
@login_required
def create_exercise():
    data = request.get_json()
    new_exercise = Exercise(title=data['title'], content=data['content'], user_id=current_user.id)
    db.session.add(new_exercise)
    db.session.commit()
    return jsonify({"message": "Exercise created successfully!"}), 201

# Route for providing feedback on an exercise
@app.route('/exercise/<int:exercise_id>/feedback', methods=['POST'])
@login_required
def provide_feedback(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    data = request.get_json()
    exercise.feedback = data['feedback']
    db.session.commit()
    return jsonify({"message": "Feedback submitted successfully!"}), 200

# Route for getting all exercises
@app.route('/exercises', methods=['GET'])
@login_required
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify([{"id": ex.id, "title": ex.title, "content": ex.content, "feedback": ex.feedback} for ex in exercises]), 200

# Route for user logout
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful!"}), 200

# Initialize the database
@app.before_first_request
def create_tables():
    db.create_all()

# Run the application
if __name__ == '__main__':
    app.run(debug=True)

# Test cases can be added here to validate the functionality of the application.
# This can include tests for user registration, login, exercise creation, feedback submission, etc.