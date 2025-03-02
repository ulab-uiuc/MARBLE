def plot_budget_breakdown(budget):
    # Plot a pie chart of the budget breakdown
    labels = ['Income', 'Expenses']
    sizes = [budget.income, budget.expenses]
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title('Budget Breakdown')
    plt.show()def suggest_budget_adjustments(budget):
    # Suggest budget adjustments based on spending and income
    if budget.expenses > budget.income * 0.8:
        send_notification(current_user, 'Reduce expenses')
        return 'Reduce expenses'
    elif budget.income > budget.expenses * 1.2:
        send_notification(current_user, 'Increase savings')
        return 'Increase savings'
    else:
        return 'No adjustments needed'# solution.py
# Importing necessary libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import matplotlib.pyplot as plt

# Creating the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budgetsync.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

# User model
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

# Budget model
class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    income = db.Column(db.Float, nullable=False)
    expenses = db.Column(db.Float, nullable=False)
    goals = db.Column(db.String(200), nullable=False)
    categories = db.Column(db.String(200), nullable=False)
    shared_with = db.Column(db.String(200), nullable=False)

# Budget item model
class BudgetItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)

# Notification model
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Feedback model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/signup', methods=['POST'])
def signup():
    # Create a new user
    data = request.get_json()
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
# Budget route
# Budget item route
# Suggest budget adjustments route
# Plot budget breakdown route
@app.route('/budgets/<int:budget_id>/plot', methods=['GET'])
@login_required
def plot_budget_breakdown_route(budget_id):
    budget = Budget.query.get(budget_id)
    if budget is None or budget.user_id != current_user.id:
        return jsonify({'message': 'Budget not found or not authorized'}), 404
    plot_budget_breakdown(budget)
    return jsonify({'message': 'Budget breakdown plotted successfully'}), 200
@app.route('/budgets/<int:budget_id>/suggest', methods=['GET'])
@login_required
def suggest_budget_adjustments_route(budget_id):
    budget = Budget.query.get(budget_id)
    if budget is None or budget.user_id != current_user.id:
        return jsonify({'message': 'Budget not found or not authorized'}), 404
    suggestion = suggest_budget_adjustments(budget)
    return jsonify({'suggestion': suggestion}), 200
@app.route('/budgets/<int:budget_id>/items', methods=['GET', 'POST'])
@login_required
def budget_items(budget_id):
    budget = Budget.query.get(budget_id)
    if budget is None or budget.user_id != current_user.id:
        return jsonify({'message': 'Budget not found or not authorized'}), 404
    if request.method == 'POST':
        # Create a new budget item
        data = request.get_json()
        item = BudgetItem(budget_id=budget_id, name=data['name'], amount=data['amount'], category=data['category'])
        db.session.add(item)
        db.session.commit()
        return jsonify({'message': 'Budget item created successfully'}), 201
    else:
        # Get all budget items for the budget
        items = BudgetItem.query.filter_by(budget_id=budget_id).all()
        return jsonify([{'id': item.id, 'name': item.name, 'amount': item.amount, 'category': item.category} for item in items]), 200
@app.route('/budgets', methods=['GET', 'POST'])
@login_required
def budgets():
    if request.method == 'POST':
        # Create a new budget
        data = request.get_json()
        budget = Budget(name=data['name'], user_id=current_user.id, income=data['income'], expenses=data['expenses'], goals=data['goals'], categories=data['categories'], shared_with=data['shared_with'])
        db.session.add(budget)
        db.session.commit()
        return jsonify({'message': 'Budget created successfully'}), 201
    else:
        # Get all budgets for the current user
        budgets = Budget.query.filter_by(user_id=current_user.id).all()
        return jsonify([{'id': budget.id, 'name': budget.name, 'income': budget.income, 'expenses': budget.expenses, 'goals': budget.goals, 'categories': budget.categories, 'shared_with': budget.shared_with} for budget in budgets]), 200
def login():
    # Login a user
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({'message': 'User logged in successfully'}), 200
    return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    # Logout a user
    logout_user()
    return jsonify({'message': 'User logged out successfully'}), 200

@app.route('/budgets', methods=['GET'])
# Adaptive featuresdef suggest_budget_adjustments(budget):
    # Suggest budget adjustments based on spending and income
    if budget.expenses > budget.income * 0.8:
        send_notification(current_user, 'Reduce expenses')
        return 'Reduce expenses'
    elif budget.income > budget.expenses * 1.2:
        send_notification(current_user, 'Increase savings')
        return 'Increase savings'
    else:
        return 'No adjustments needed'def plot_budget_breakdown(budget):
    # Plot a pie chart of the budget breakdown
    labels = ['Income', 'Expenses']
    sizes = [budget.income, budget.expenses]
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title('Budget Breakdown')
    plt.show()

# Notification system
def send_notification(user, message):
    # Send a notification to a user
    notification = Notification(user_id=user.id, message=message)
    db.session.add(notification)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)