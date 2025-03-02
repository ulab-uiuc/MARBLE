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
    savings_goal = db.Column(db.Float, nullable=True)
    transactions = db.relationship('Transaction', backref='user', lazy=True)

# Define the Transaction model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# API endpoint to create a new user
@app.route('/api/users', methods=['POST'])
def create_user():def create_transaction():    data = request.json
    if not all(key in data for key in ['amount', 'category', 'user_id']):if not all(key in data for key in ['username']):        return jsonify({'error': 'Missing fields in request data'}), 400
    try:
        new_transaction = Transaction(amount=data['amount'], category=data['category'], user_id=data['user_id'])
        db.session.add(new_transaction)
        db.session.commit()
        return jsonify({'message': 'Transaction added successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500    return jsonify({'message': 'Transaction added successfully!'}), 201

# API endpoint to get user transactions
@app.route('/api/users/<int:user_id>/transactions', methods=['GET'])
def get_transactions(user_id):
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    return jsonify([{'id': t.id, 'amount': t.amount, 'category': t.category, 'date': t.date} for t in transactions])

# API endpoint to get user savings goal
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({'username': user.username, 'savings_goal': user.savings_goal})

# API endpoint to update savings goal
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_savings_goal(user_id):
    data = request.json
    user = User.query.get_or_404(user_id)
    user.savings_goal = data['savings_goal']
    db.session.commit()
    return jsonify({'message': 'Savings goal updated successfully!'})

# Run the application
if __name__ == '__main__':
    app.run(debug=True)

# The above code implements a simple backend for the BudgetBuddy finance management system.
# It includes user and transaction models, API endpoints for user management, and transaction handling.
# The database is set up using SQLite, and Flask is used as the web framework.
# The application supports CORS for frontend-backend communication.