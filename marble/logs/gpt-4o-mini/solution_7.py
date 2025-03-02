# solution.py

# Import necessary libraries
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import matplotlib.pyplot as plt
import numpy as np

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
    id = db.Column(db.Integer, primary_key=True)    goal = db.Column(db.Float, default=0.0)
    category = db.Column(db.String(150), nullable=True)    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

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

# Route for creating a budget
@app.route('/create_budget', methods=['POST'])
@login_requirednew_budget = Budget(name=data['name'], goal=data.get('goal', 0.0), category=data.get('category', None), owner_id=current_user.id)    db.session.add(new_budget)
    db.session.commit()
    return jsonify({'message': 'Budget created successfully'}), 201

# Route for adding income or expenses
@app.route('/update_budget/<int:budget_id>', methods=['POST'])
@login_required
def update_budget(budget_id):
    data = request.get_json()
    budget = Budget.query.get(budget_id)
    if 'income' in data:
        budget.total_income += data['income']
    if 'expenses' in data:
        budget.total_expenses += data['expenses']
    db.session.commit()
    return jsonify({'message': 'Budget updated successfully'}), 200

# Route for visualizing budget data
@app.route('/visualize_budget/<int:budget_id>', methods=['GET'])
@login_required
def visualize_budget(budget_id):
    budget = Budget.query.get(budget_id)
    labels = ['Income', 'Expenses']
    sizes = [budget.total_income, budget.total_expenses]
    colors = ['gold', 'lightcoral']
    
    # Create a pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig(f'budget_{budget_id}.png')  # Save the figure
    return jsonify({'message': 'Visualization created', 'image_path': f'budget_{budget_id}.png'}), 200

# Route for user logout
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

# Initialize the database
@app.before_first_request
def create_tables():
    db.create_all()

# Run the application
if __name__ == '__main__':
    app.run(debug=True)