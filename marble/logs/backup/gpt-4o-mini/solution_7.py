# solution.py

# Import necessary libraries
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import json

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budgetsync.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model for the database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    budgets = db.relationship('Budget', backref='owner', lazy=True)

# Budget model for the database
class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Associate budget with user
    users = db.relationship('BudgetUser', backref='budget', lazy=True)
    name = db.Column(db.String(150), nullable=False)

# BudgetUser model to manage user access to budgets
class BudgetUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    access_level = db.Column(db.String(50), nullable=False)  # e.g., 'view', 'edit'

# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route for user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        login_user(user)
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

# Route for creating a new budget
@app.route('/create_budget', methods=['POST'])
@login_required
def create_budget():    new_budget = Budget(name=data['name'], user_id=current_user.id)  # Associate budget with the current user
    db.session.commit()
    return jsonify({'message': 'Budget created successfully'}), 201
    data = request.get_json()

# Route for adding income and expenses
@app.route('/update_budget/<int:budget_id>', methods=['POST'])
@login_required
def update_budget(budget_id):
    data = request.get_json()
    budget = Budget.query.get(budget_id)
    if budget:
        budget.total_income += data.get('income', 0)
        budget.total_expenses += data.get('expenses', 0)
        db.session.commit()
        return jsonify({'message': 'Budget updated successfully'}), 200
    return jsonify({'message': 'Budget not found'}), 404

# Route for getting budget details
@app.route('/budget/<int:budget_id>', methods=['GET'])
@login_required
def get_budget(budget_id):
    budget = Budget.query.get(budget_id)
    if budget:
        return jsonify({
            'name': budget.name,
            'total_income': budget.total_income,
            'total_expenses': budget.total_expenses
        }), 200
    return jsonify({'message': 'Budget not found'}), 404

# Route for logging out
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

# Main function to run the application
if __name__ == '__main__':
    db.create_all()  # Create database tables
    app.run(debug=True)  # Run the application in debug mode