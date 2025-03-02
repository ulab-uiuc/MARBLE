# solution.py

# Import necessary libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budgetbuddy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    savings_goals = db.relationship('SavingsGoal', backref='user', lazy=True)
    transactions = db.relationship('Transaction', backref='user', lazy=True)

# Define the SavingsGoal model
class SavingsGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal_name = db.Column(db.String(120), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Define the Transaction model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# API endpoint to create a new user
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
existing_user = User.query.filter((User.username == data['username']) | (User.email == data['email'])).first()    if existing_user:
        return jsonify({'message': 'Username or email already exists!'}), 400
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()    return jsonify({'message': 'User created successfully!'}), 201

# API endpoint to add a savings goal
@app.route('/api/users/<int:user_id>/savings_goals', methods=['POST'])
def add_savings_goal(user_id):
    data = request.json
    new_goal = SavingsGoal(goal_name=data['goal_name'], target_amount=data['target_amount'], user_id=user_id)
    db.session.add(new_goal)
    db.session.commit()
    return jsonify({'message': 'Savings goal added successfully!'}), 201

# API endpoint to add a transaction
@app.route('/api/users/<int:user_id>/transactions', methods=['POST'])
def add_transaction(user_id):
    data = request.json
    new_transaction = Transaction(amount=data['amount'], category=data['category'], user_id=user_id)
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction added successfully!'}), 201

# API endpoint to get user transactions
@app.route('/api/users/<int:user_id>/transactions', methods=['GET'])
def get_transactions(user_id):
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    return jsonify([{'id': t.id, 'amount': t.amount, 'category': t.category, 'date': t.date} for t in transactions]), 200

# API endpoint to get savings goals
@app.route('/api/users/<int:user_id>/savings_goals', methods=['GET'])
def get_savings_goals(user_id):
    goals = SavingsGoal.query.filter_by(user_id=user_id).all()
    return jsonify([{'id': g.id, 'goal_name': g.goal_name, 'target_amount': g.target_amount, 'current_amount': g.current_amount} for g in goals]), 200

# Run the application
if __name__ == '__main__':
    app.run(debug=True)