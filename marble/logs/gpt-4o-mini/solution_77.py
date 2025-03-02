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

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    groups = db.relationship('Group', secondary='user_group', backref='members')

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    alerts = db.relationship('PriceAlert', backref='group')

class UserGroup(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), nullable=False)
    price_threshold = db.Column(db.Float, nullable=False)
    alerts = db.relationship('PriceAlert', backref='product')

class PriceAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=True)
    notified = db.Column(db.Boolean, default=False)

# User registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

# User login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        session['user_id'] = user.id
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

# Create a group
@app.route('/groups', methods=['POST'])
def create_group():
    data = request.json
    new_group = Group(name=data['name'])
    db.session.add(new_group)
    db.session.commit()
    return jsonify({'message': 'Group created successfully'}), 201

# Join a group
@app.route('/groups/join', methods=['POST'])
def join_group():
    data = request.json
    user = User.query.get(session['user_id'])
    group = Group.query.get(data['group_id'])
    if user and group:
        user.groups.append(group)
        db.session.commit()
        return jsonify({'message': 'Joined group successfully'}), 200
    return jsonify({'message': 'Group not found'}), 404

# Add product to watchlist
@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    new_product = Product(url=data['url'], price_threshold=data['price_threshold'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added to watchlist'}), 201

# Set price alert
@app.route('/alerts', methods=['POST'])
def set_price_alert():
    data = request.json
    new_alert = PriceAlert(user_id=session['user_id'], product_id=data['product_id'], group_id=data.get('group_id'))
    db.session.add(new_alert)
    db.session.commit()
    return jsonify({'message': 'Price alert set successfully'}), 201

# Function to check prices and notify users
def check_prices():
    while True:
        alerts = PriceAlert.query.filter_by(notified=False).all()
        for alert in alerts:
            product = Product.query.get(alert.product_id)
            current_price = get_current_price(product.url)  # Function to scrape or fetch current price
            if current_price < product.price_threshold:
                send_notification(alert.user_id, product.url, current_price)  # Function to send email notification
                alert.notified = True
        db.session.commit()
        time.sleep(60)  # Check every minute

# Function to get current price (placeholder)
def get_current_price(url):
    # Here you would implement the logic to scrape or fetch the current price from the URL
    return 100.0  # Placeholder value

# Function to send email notification (placeholder)
def send_notification(user_id, product_url, current_price):
    user = User.query.get(user_id)
    msg = Message('Price Alert', sender='your_email@example.com', recipients=[user.email])
    msg.body = f'The price for {product_url} has dropped to {current_price}.'
    mail.send(msg)

# Start the price checking thread
price_check_thread = threading.Thread(target=check_prices)
price_check_thread.start()

# Run the application
if __name__ == '__main__':
    db.create_all()  # Create database tables
    app.run(debug=True)