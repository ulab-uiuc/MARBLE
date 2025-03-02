# solution.py
# Importing necessary libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

# Creating the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///family_adventure_quest.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'

# Initializing the database, marshmallow, CORS, Bcrypt, and JWTManager
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Defining the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'), nullable=True)

    def __init__(self, username, email, password, family_id=None):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.family_id = family_id

# Defining the Family model
class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    users = db.relationship('User', backref='family', lazy=True)

    def __init__(self, name):
        self.name = namedef create_family():
    data = request.get_json()
    name = data['name']
    existing_family = Family.query.filter_by(name=name).first()
    if existing_family:
        return jsonify({'message': 'Family with the same name already exists'}), 400
    family = Family(name)
    db.session.add(family)
    db.session.commit()
    return jsonify({'message': 'Family created successfully'}), 201

@app.route('/family', methods=['POST'])
def create_family_route():
    return create_family()@app.route('/quest', methods=['POST'])
def create_quest_route():
    data = request.get_json()
    name = data['name']
    description = data['description']
    age_group = data['age_group']
    educational_standard = data['educational_standard']
    rewards = data['rewards']
    existing_quest = Quest.query.filter_by(name=name).first()
    if existing_quest:
        return jsonify({'message': 'Quest with the same name already exists'}), 400
    quest = Quest(name, description, age_group, educational_standard, rewards)
    db.session.add(quest)
    db.session.commit()
    return jsonify({'message': 'Quest created successfully'}), 201@app.route('/progress', methods=['POST'])
@jwt_required
def create_progress():
    # Getting the data from the request
    data = request.get_json()
    user_id = data['user_id']
    quest_id = data['quest_id']
    progress = data['progress']

    # Creating a new progress record
    progress_record = Progress(user_id, quest_id, progress)
    db.session.add(progress_record)
    db.session.commit()

    # Returning a success message
    return jsonify({'message': 'Progress record created successfully'}), 201

# Defining the route for getting all progress records
@app.route('/progress', methods=['GET'])
@jwt_required
def get_progress():
    # Getting all progress records
    progress_records = Progress.query.all()
    progress_schema = ProgressSchema(many=True)
    return jsonify(progress_schema.dump(progress_records)), 200

if __name__ == '__main__':
    app.run(debug=True)