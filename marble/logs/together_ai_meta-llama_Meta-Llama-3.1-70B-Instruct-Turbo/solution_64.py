# questhub.py

# Import required libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from datetime import datetime

# Create a Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questhub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Initialize the SocketIO instance
socketio = SocketIO(app, cors_allowed_origins='*')

# Enable CORS
CORS(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    quests = db.relationship('Quest', backref='user', lazy=True)

# Define the Quest model
class Quest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    skill_plans = db.relationship('SkillPlan', backref='quest', lazy=True)

# Define the SkillPlan model
class SkillPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    quest_id = db.Column(db.Integer, db.ForeignKey('quest.id'), nullable=False)

# Define the Collaboration model
class Collaboration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quest_id = db.Column(db.Integer, db.ForeignKey('quest.id'), nullable=False)
    user = db.relationship('User', backref='collaborations', lazy=True)
    quest = db.relationship('Quest', backref='collaborations', lazy=True)

# Create the database tables
@app.before_first_request
def create_tables():
    db.create_all()

# Define the API endpoint to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(username=data['username'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

# Define the API endpoint to create a new quest
@app.route('/quests', methods=['POST'])
def create_quest():
    data = request.get_json()
    quest = Quest(title=data['title'], description=data['description'], user_id=data['user_id'])
    db.session.add(quest)
    db.session.commit()
    return jsonify({'message': 'Quest created successfully'}), 201

# Define the API endpoint to create a new skill plan
@app.route('/skill-plans', methods=['POST'])
def create_skill_plan():
    data = request.get_json()
    skill_plan = SkillPlan(name=data['name'], description=data['description'], quest_id=data['quest_id'])
    db.session.add(skill_plan)
    db.session.commit()
    return jsonify({'message': 'Skill plan created successfully'}), 201

# Define the API endpoint to create a new collaboration
@app.route('/collaborations', methods=['POST'])
def create_collaboration():
    data = request.get_json()
    collaboration = Collaboration(user_id=data['user_id'], quest_id=data['quest_id'])
    db.session.add(collaboration)
    db.session.commit()
    return jsonify({'message': 'Collaboration created successfully'}), 201

# Define the SocketIO event to update a quest in real-time
@socketio.on('update_quest')
def update_quest(data):
    quest = Quest.query.get(data['quest_id'])
    quest.title = data['title']
    quest.description = data['description']
    db.session.commit()
    emit('quest_updated', {'quest_id': quest.id, 'title': quest.title, 'description': quest.description}, broadcast=True)

# Define the SocketIO event to update a skill plan in real-time
@socketio.on('update_skill_plan')
def update_skill_plan(data):
    skill_plan = SkillPlan.query.get(data['skill_plan_id'])
    skill_plan.name = data['name']
    skill_plan.description = data['description']
    db.session.commit()
    emit('skill_plan_updated', {'skill_plan_id': skill_plan.id, 'name': skill_plan.name, 'description': skill_plan.description}, broadcast=True)

# Run the application
if __name__ == '__main__':
    socketio.run(app)