
# user_registration_resource.py

class UserRegistrationResource(Resource):
    def post(self):
        username = request.json['username']
        password = request.json['password']
        family_id = request.json.get('family_id', None)

        if User.query.filter_by(username=username).first():
            return {'message': 'Username already exists'}, 400

        new_user = User(username, password, family_id)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201# family_adventure_quest.py

# Import required libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

# Create the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///family_adventure_quest.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'

# Initialize the database
db = SQLAlchemy(app)

# Initialize the Marshmallow object
ma = Marshmallow(app)

# Initialize the API
api = Api(app)

# Initialize CORS
CORS(app)

# Initialize Bcrypt
bcrypt = Bcrypt(app)

# Initialize JWTManager
jwt = JWTManager(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'), nullable=True)

    def __init__(self, username, password, family_id=None):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.family_id = family_id

# Define the Family model
class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    users = db.relationship('User', backref='family', lazy=True)

    def __init__(self, name):
        self.name = name

# Define the Quest model
class Quest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    rewards = db.Column(db.Text, nullable=False)

    def __init__(self, name, description, rewards):
        self.name = name
        self.description = description
        self.rewards = rewards

# Define the Progress model
class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quest_id = db.Column(db.Integer, db.ForeignKey('quest.id'), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, user_id, quest_id):
        self.user_id = user_id
        self.quest_id = quest_id

# Define the User schema
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

# Define the Family schema
class FamilySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Family
        load_instance = True

# Define the Quest schema
class QuestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Quest
        load_instance = True

# Define the Progress schema
class ProgressSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Progress
        load_instance = True

# Create the schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
family_schema = FamilySchema()
families_schema = FamilySchema(many=True)
quest_schema = QuestSchema()
quests_schema = QuestSchema(many=True)
progress_schema = ProgressSchema()
progresses_schema = ProgressSchema(many=True)

# Define the User resource
class UserResource(Resource):
    @jwt_required
    def get(self, user_id):
        user = User.query.get(user_id)
        if user is None:
            return {'message': 'User not found'}, 404
        return user_schema.dump(user)

    @jwt_required
    def put(self, user_id):
        user = User.query.get(user_id)
        if user is None:
            return {'message': 'User not found'}, 404
        user.username = request.json['username']
        db.session.commit()
        return user_schema.dump(user)

    @jwt_required
    def delete(self, user_id):
        user = User.query.get(user_id)
        if user is None:
            return {'message': 'User not found'}, 404
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted'}

# Define the Family resource
class FamilyResource(Resource):
    @jwt_required
    def get(self, family_id):
        family = Family.query.get(family_id)
        if family is None:
            return {'message': 'Family not found'}, 404
        return family_schema.dump(family)

    @jwt_required
    def put(self, family_id):
        family = Family.query.get(family_id)
        if family is None:
            return {'message': 'Family not found'}, 404
        family.name = request.json['name']
        db.session.commit()
        return family_schema.dump(family)

    @jwt_required
    def delete(self, family_id):
        family = Family.query.get(family_id)
        if family is None:
            return {'message': 'Family not found'}, 404
        db.session.delete(family)
        db.session.commit()
        return {'message': 'Family deleted'}

# Define the Quest resource
class QuestResource(Resource):
    @jwt_required
    def get(self, quest_id):
        quest = Quest.query.get(quest_id)
        if quest is None:
            return {'message': 'Quest not found'}, 404
        return quest_schema.dump(quest)

    @jwt_required
    def put(self, quest_id):
        quest = Quest.query.get(quest_id)
        if quest is None:
            return {'message': 'Quest not found'}, 404
        quest.name = request.json['name']
        quest.description = request.json['description']
        quest.rewards = request.json['rewards']
        db.session.commit()
        return quest_schema.dump(quest)

    @jwt_required
    def delete(self, quest_id):
        quest = Quest.query.get(quest_id)
        if quest is None:
            return {'message': 'Quest not found'}, 404
        db.session.delete(quest)
        db.session.commit()
        return {'message': 'Quest deleted'}

# Define the Progress resource
class ProgressResource(Resource):
    @jwt_required
    def get(self, progress_id):
        progress = Progress.query.get(progress_id)
        if progress is None:
            return {'message': 'Progress not found'}, 404
        return progress_schema.dump(progress)

    @jwt_required
    def put(self, progress_id):
        progress = Progress.query.get(progress_id)
        if progress is None:
            return {'message': 'Progress not found'}, 404
        progress.completed = request.json['completed']
        db.session.commit()
        return progress_schema.dump(progress)

    @jwt_required
    def delete(self, progress_id):
        progress = Progress.query.get(progress_id)
        if progress is None:
            return {'message': 'Progress not found'}, 404
        db.session.delete(progress)
        db.session.commit()
        return {'message': 'Progress deleted'}

# Define the Login resource
class LoginResource(Resource):
    def post(self):
        username = request.json['username']
        password = request.json['password']
        user = User.query.filter_by(username=username).first()
        if user is None or not bcrypt.check_password_hash(user.password, password):
            return {'message': 'Invalid username or password'}, 401
        access_token = create_access_token(identity=username)
        return {'access_token': access_token}

# Add the resources to the API
api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(FamilyResource, '/families/<int:family_id>')
api.add_resource(QuestResource, '/quests/<int:quest_id>')
api.add_resource(ProgressResource, '/progress/<int:progress_id>')
api.add_resource(LoginResource, '/login')

# Create the database tables
api.add_resource(UserRegistrationResource, '/register')
@app.before_first_request
def create_tables():
    db.create_all()

# Run the application
if __name__ == '__main__':
    app.run(debug=True)