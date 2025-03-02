# solution.py

# Import necessary libraries
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
import requests
import threading
import time

# Initialize the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///price_tracker.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    groups = db.relationship('Group', backref='user', lazy=True)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    members = db.relationship('User', secondary='group_members', lazy='subquery')

class GroupMembers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), nullable=False)
    price_threshold = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# User registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

# User login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        session['user_id'] = user.id        session['user_email'] = user.email
        return jsonify({'message': 'Login successful'}), 200    return jsonify({'message': 'Invalid credentials'}), 401

# Create a group
@app.route('/group', methods=['POST'])
def create_group():
    data = request.get_json()
    new_group = Group(name=data['name'])
    db.session.add(new_group)
    db.session.commit()
    return jsonify({'message': 'Group created successfully'}), 201

# Add product to watchlist
@app.route('/product', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(url=data['url'], price_threshold=data['price_threshold'], user_id=session['user_id'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added to watchlist'}), 201

# Function to check prices and send notifications
def check_prices():
    while True:
        products = Product.query.all()
        for product in products:
            # Simulate price checking (in a real application, you would scrape or use an API)
            current_price = requests.get(product.url).json().get('current_price')
            if current_price < product.price_threshold:
                send_notification(product)
        time.sleep(60)  # Check every minute

# Send notification via email
def send_notification(product):
    msg = Message('Price Alert', sender='your_email@example.com', recipients=[session['user_email']])
    msg.body = f'The price for {product.url} has dropped below your threshold!'
    mail.send(msg)

# Start price checking in a separate thread
threading.Thread(target=check_prices, daemon=True).start()

# Run the application
if __name__ == '__main__':
    db.create_all()  # Create database tables
    app.run(debug=True)