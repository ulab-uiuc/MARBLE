
# Define the database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

class Quest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)

class SkillPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    quest_id = db.Column(db.Integer, db.ForeignKey('quest.id'), nullable=False)

class Collaboration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quest_id = db.Column(db.Integer, db.ForeignKey('quest.id'), nullable=False)
# Initialize the database
db = SQLAlchemy(app)
# Initialize SocketIO
socketio = SocketIO(app)# Initialize the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quest_hub.db'
app.config['SECRET_KEY'] = 'secret_key'
CORS(app)# quest_hub.py

# Import required libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from datetime import datetimefrom flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return user
    return None
def create_quest(title, description, user_id):
    quest = Quest(title=title, description=description, user_id=user_id)
    db.session.add(quest)
    db.session.commit()
    return quest

# Define a function to update a quest
def update_quest(quest_id, title, description):
    quest = Quest.query.get(quest_id)
    if quest:
        quest.title = title
        quest.description = description
        db.session.commit()
        return quest
    return None
def create_user(username, password):
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

# Define a function to complete a quest
def complete_quest(quest_id):
    quest = Quest.query.get(quest_id)
    if quest:
        quest.completed = True
        db.session.commit()
        return quest
    return None

# Define a function to create a new skill plan
def create_skill_plan(name, description, quest_id):
    skill_plan = SkillPlan(name=name, description=description, quest_id=quest_id)
    db.session.add(skill_plan)
    db.session.commit()
    return skill_plan

# Define a function to update a skill plan
def update_skill_plan(skill_plan_id, name, description):
    skill_plan = SkillPlan.query.get(skill_plan_id)
    if skill_plan:
        skill_plan.name = name
        skill_plan.description = description
        db.session.commit()
        return skill_plan
    return None

# Define a function to handle real-time collaboration
def handle_collaboration(user_id, quest_id):
    collaboration = Collaboration.query.filter_by(user_id=user_id, quest_id=quest_id).first()
    if collaboration:
        return collaboration
    collaboration = Collaboration(user_id=user_id, quest_id=quest_id)
    db.session.add(collaboration)
    db.session.commit()
    return collaboration

# Define API endpoints for quest management
@app.route('/quests', methods=['POST'])
def create_quest_endpoint():
    data = request.json
    user_id = data['user_id']
    title = data['title']
    description = data['description']
    quest = create_quest(title, description, user_id)
    return jsonify({'quest_id': quest.id})

@app.route('/quests/<int:quest_id>', methods=['PUT'])
def update_quest_endpoint(quest_id):
    data = request.json
    title = data['title']
    description = data['description']
    quest = update_quest(quest_id, title, description)
    if quest:
        return jsonify({'quest_id': quest.id})
    return jsonify({'error': 'Quest not found'}), 404

@app.route('/quests/<int:quest_id>/complete', methods=['POST'])
def complete_quest_endpoint(quest_id):
    quest = complete_quest(quest_id)
    if quest:
        return jsonify({'quest_id': quest.id})
    return jsonify({'error': 'Quest not found'}), 404

# Define API endpoints for skill planning
@app.route('/quests/<int:quest_id>/skill-plans', methods=['POST'])
def create_skill_plan_endpoint(quest_id):
    data = request.json
    name = data['name']
    description = data['description']
    skill_plan = create_skill_plan(name, description, quest_id)
    return jsonify({'skill_plan_id': skill_plan.id})

@app.route('/skill-plans/<int:skill_plan_id>', methods=['PUT'])
def update_skill_plan_endpoint(skill_plan_id):
    data = request.json
    name = data['name']
    description = data['description']
    skill_plan = update_skill_plan(skill_plan_id, name, description)
    if skill_plan:
        return jsonify({'skill_plan_id': skill_plan.id})
    return jsonify({'error': 'Skill plan not found'}), 404

# Define SocketIO events for real-time collaboration
@socketio.on('join_quest')
def handle_join_quest(data):
    user_id = data['user_id']
    quest_id = data['quest_id']
    collaboration = handle_collaboration(user_id, quest_id)
    emit('joined_quest', {'quest_id': quest_id}, broadcast=True)

@socketio.on('leave_quest')
def handle_leave_quest(data):
    user_id = data['user_id']
    quest_id = data['quest_id']
    collaboration = Collaboration.query.filter_by(user_id=user_id, quest_id=quest_id).first()
    if collaboration:
        db.session.delete(collaboration)
        db.session.commit()
        emit('left_quest', {'quest_id': quest_id}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)