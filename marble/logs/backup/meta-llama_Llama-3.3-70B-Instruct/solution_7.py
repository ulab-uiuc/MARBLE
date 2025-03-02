# solution.py
# Import required libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import matplotlib.pyplot as plt
import numpy as np

# Create the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budgetsync.db'
db = SQLAlchemy(app)

# Define the User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    budgets = db.relationship('Budget', backref='user', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Define the Budget model
class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    income = db.Column(db.Float, nullable=False)
    expenses = db.Column(db.Float, nullable=False)
    goals = db.Column(db.String(128), nullable=False)
    categories = db.Column(db.String(128), nullable=False)

# Define the Expense model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'), nullable=False)
    category = db.Column(db.String(64), nullable=False)
    amount = db.Column(db.Float, nullable=False)

# Define the Income model
class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'), nullable=False)
    source = db.Column(db.String(64), nullable=False)
    amount = db.Column(db.Float, nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Define the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Load the user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define the routes
@app.route('/signup', methods=['POST'])
def signup():
    # Get the request data
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']

    # Create a new user
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    # Get the request data
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Find the user
    user = User.query.filter_by(username=username).first()

    # Check the password
    if user and user.check_password(password):
        login_user(user)
        return jsonify({'message': 'Logged in successfully'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/budgets', methods=['GET'])
@login_required
def get_budgets():
    # Get the user's budgetsbudget = Budget.query.get(budget_id)
        if budget is None:
            return jsonify({'message': 'Budget not found'}), 404
    # Return the budgets
    return jsonify([{'id': budget.id, 'name': budget.name, 'income': budget.income, 'expenses': budget.expenses, 'goals': budget.goals, 'categories': budget.categories} for budget in budgets]), 200

@app.route('/budgets', methods=['POST'])
@login_required
def create_budget():
    # Get the request data
    data = request.get_json()
    name = data['name']
    income = data['income']
    expenses = data['expenses']
    goals = data['goals']
    categories = data['categories']

    # Create a new budget
    budget = Budget(name=name, user_id=current_user.id, income=income, expenses=expenses, goals=goals, categories=categories)
    db.session.add(budget)
    db.session.commit()

    return jsonify({'message': 'Budget created successfully'}), 201

@app.route('/budgets/<int:budget_id>', methods=['GET'])
@login_required
def get_budget(budget_id):
    # Find the budgetbudget = Budget.query.get(budget_id)
        if budget is None:
            return jsonify({'message': 'Budget not found'}), 404
    # Check if the budget belongs to the user
    if budget and budget.user_id == current_user.id:
        return jsonify({'id': budget.id, 'name': budget.name, 'income': budget.income, 'expenses': budget.expenses, 'goals': budget.goals, 'categories': budget.categories}), 200
    else:
        return jsonify({'message': 'Budget not found'}), 404

@app.route('/budgets/<int:budget_id>', methods=['PUT'])
@login_required
def update_budget(budget_id):
    # Find the budgetbudget = Budget.query.get(budget_id)
        if budget is None:
            return jsonify({'message': 'Budget not found'}), 404
    # Check if the budget belongs to the user
    if budget and budget.user_id == current_user.id:
        # Get the request data
        data = request.get_json()
        name = data['name']
        income = data['income']
        expenses = data['expenses']
        goals = data['goals']
        categories = data['categories']

        # Update the budget
        budget.name = name
        budget.income = income
        budget.expenses = expenses
        budget.goals = goals
        budget.categories = categories
        db.session.commit()

        return jsonify({'message': 'Budget updated successfully'}), 200
    else:
        return jsonify({'message': 'Budget not found'}), 404

@app.route('/budgets/<int:budget_id>', methods=['DELETE'])
@login_required
def delete_budget(budget_id):
    # Find the budgetbudget = Budget.query.get(budget_id)
        if budget is None:
            return jsonify({'message': 'Budget not found'}), 404
    # Check if the budget belongs to the user
    if budget and budget.user_id == current_user.id:
        # Delete the budget
        db.session.delete(budget)
        db.session.commit()

        return jsonify({'message': 'Budget deleted successfully'}), 200
    else:
        return jsonify({'message': 'Budget not found'}), 404

@app.route('/expenses', methods=['POST'])
@login_required
def create_expense():
    # Get the request databudget = Budget.query.get(budget_id)
        if budget is None:
            return jsonify({'message': 'Budget not found'}), 404
    # Check if the budget belongs to the user
    if budget and budget.user_id == current_user.id:
        # Create a new expense
        expense = Expense(budget_id=budget_id, category=category, amount=amount)
        db.session.add(expense)
        db.session.commit()

        return jsonify({'message': 'Expense created successfully'}), 201
    else:
        return jsonify({'message': 'Budget not found'}), 404

@app.route('/incomes', methods=['POST'])
@login_required
def create_income():
    # Get the request databudget = Budget.query.get(budget_id)
        if budget is None:
            return jsonify({'message': 'Budget not found'}), 404
    # Check if the budget belongs to the user
    if budget and budget.user_id == current_user.id:
        # Create a new income
        income = Income(budget_id=budget_id, source=source, amount=amount)
        db.session.add(income)
        db.session.commit()

        return jsonify({'message': 'Income created successfully'}), 201
    else:
        return jsonify({'message': 'Budget not found'}), 404

# Define a function to generate a pie chart
def generate_pie_chart(budget_id):import base64
from io import BytesIO

def generate_bar_graph(budget_id):
    # Find the budget
    budget = Budget.query.get(budget_id)
    
    # Check if the budget belongs to the user
    if budget and budget.user_id == current_user.id:
        # Get the expenses
        expenses = Expense.query.filter_by(budget_id=budget_id).all()
        
        # Get the categories and amounts
        categories = [expense.category for expense in expenses]
        amounts = [expense.amount for expense in expenses]
        
        # Generate the bar graph
        plt.bar(categories, amounts)
        plt.title('Expense Breakdown')
        plt.xlabel('Category')
        plt.ylabel('Amount')
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close()
        return imagedef send_notification(budget_id, message):
    # Find the budget
    budget = Budget.query.get(budget_id)

    # Check if the budget belongs to the user
    if budget and budget.user_id == current_user.id:
        # Send the notification
        print(f'Notification: {message}')

# Define a function to get user feedback
def get_feedback():
    # Get the feedback
    feedback = input('Please enter your feedback: ')

    # Save the feedback
    with open('feedback.txt', 'a') as f:
        f.write(feedback + '\n')

    return feedback

# Run the application
if __name__ == '__main__':
    app.run(debug=True)