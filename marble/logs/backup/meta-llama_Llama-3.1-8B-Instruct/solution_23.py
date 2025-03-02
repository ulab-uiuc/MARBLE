# family_adventure_quest.py
# This is the main implementation of the FamilyAdventureQuest application.

# Importing required libraries
import sqlite3
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_cors import CORS

# Creating a new Flask application
app = Flask(__name__)

# Configuring the application
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///family_adventure_quest.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a random secret key

# Initializing the database, marshmallow, bcrypt, and JWT
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)

# Creating the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'), nullable=False)

    def __init__(self, username, password, family_id):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.family_id = family_id

# Creating the Family model
class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    users = db.relationship('User', backref='family', lazy=True)

    def __init__(self, name):
        self.name = name

# Creating the Quest model
class Quest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    objective = db.Column(db.String(200), nullable=False)
    instructions = db.Column(db.String(200), nullable=False)
    reward = db.Column(db.String(100), nullable=False)
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'), nullable=False)

    def __init__(self, name, description, objective, instructions, reward, family_id):
        self.name = name
        self.description = description
        self.objective = objective
        self.instructions = instructions
        self.reward = reward
        self.family_id = family_id

# Creating the QuestSchema model
class QuestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Quest
        load_instance = True

# Creating the UserSchema model
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

# Creating the FamilySchema model
class FamilySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Family
        load_instance = True

# Creating a new user
@app.route('/user', methods=['POST'])
def create_user():
    username = request.json['username']
    password = request.json['password']
    family_id = request.json['family_id']
    user = User(username, password, family_id)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201def create_user():
    schema = UserSchema()
    data, errors = schema.load(request.json)
    if errors:
        return jsonify({'message': 'Invalid input data', 'errors': errors}), 400
    # Rest of the function remains the same

# Creating a new family
@app.route('/family', methods=['POST'])
def create_family():
    name = request.json['name']
    family = Family(name)
    db.session.add(family)
    db.session.commit()
    return jsonify({'message': 'Family created successfully'}), 201def create_family():
    schema = FamilySchema()
    data, errors = schema.load(request.json)
    if errors:
        return jsonify({'message': 'Invalid input data', 'errors': errors}), 400
    # Rest of the function remains the same

# Creating a new quest
@app.route('/quest', methods=['POST'])
def create_quest():
    name = request.json['name']
    description = request.json['description']
    objective = request.json['objective']
    instructions = request.json['instructions']
    reward = request.json['reward']
    family_id = request.json['family_id']
    quest = Quest(name, description, objective, instructions, reward, family_id)
    db.session.add(quest)
    db.session.commit()
    return jsonify({'message': 'Quest created successfully'}), 201def create_quest():
    schema = QuestSchema()
    data, errors = schema.load(request.json)
    if errors:
        return jsonify({'message': 'Invalid input data', 'errors': errors}), 400
    # Rest of the function remains the same

# Authenticating a user
@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token}), 200
    return jsonify({'message': 'Invalid username or password'}), 401

# Getting all quests for a family
@app.route('/quests', methods=['GET'])
@jwt_required
def get_quests():
    family_id = request.json['family_id']
    quests = Quest.query.filter_by(family_id=family_id).all()
    return jsonify([{'id': quest.id, 'name': quest.name, 'description': quest.description, 'objective': quest.objective, 'instructions': quest.instructions, 'reward': quest.reward} for quest in quests]), 200

# Running the application
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)