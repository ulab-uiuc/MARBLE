# music_mashup_battle.py
import os
import json
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask appfrom flask import Flask, render_template, request, jsonify
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_userapp = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
login_manager = LoginManager(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music_mashup_battle.db'
db = SQLAlchemy(app)
socketio = SocketIO(app)

# Define database models
class User(db.Model):
class MashupVote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mashup_id = db.Column(db.Integer, db.ForeignKey('mashup.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __init__(self, mashup_id, user_id):
        self.mashup_id = mashup_id
        self.user_id = user_id
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    mashups = db.relationship('Mashup', backref='user', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Mashup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    tracks = db.Column(db.String(120), nullable=False)
    effects = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    votes = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, name, tracks, effects, user_id):
        self.name = name
        self.tracks = tracks
        self.effects = effects
        self.user_id = user_id

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    users = db.relationship('User', secondary='room_user', backref='rooms', lazy=True)

class RoomUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

# Frontend routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False})
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'success': True})
    return render_template('register.html')

# Backend routes@app.route('/vote_mashup', methods=['POST'])def vote_mashup():
    if not current_user.is_authenticated:
        return jsonify({'error': 'You must be logged in to vote for a mashup'}), 401mashup_id = request.json['mashup_id']mashup = Mashup.query.get(mashup_id)
if mashup is None:
    return jsonify({'error': 'Mashup not found'}), 404
    mashup.votes += 1
    db.session.commit()
    return jsonify({'success': True})

# SocketIO events@socketio.on('vote_mashup')def vote_mashup_event(data):
    if not current_user.is_authenticated:
        emit('error', {'message': 'You must be logged in to vote for a mashup'}), 401mashup_id = data['mashup_id']mashup = Mashup.query.get(mashup_id)
if mashup is None:
    emit('error', {'message': 'Mashup not found'}), 404existing_vote = MashupVote.query.filter_by(mashup_id=mashup_id, user_id=current_user.id).first()
if existing_vote is None:
    new_vote = MashupVote(mashup_id, current_user.id)
    db.session.add(new_vote)
    mashup.votes += 1
    db.session.commit()
    emit('mashup_voted', {'mashup_id': mashup_id, 'votes': mashup.votes}, broadcast=True)
else:
    emit('error', {'message': 'You have already voted for this mashup'}), 400emit('mashup_voted', {'mashup_id': mashup_id, 'votes': mashup.votes}, broadcast=True)

# Run the app
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)

# index.html
# <html>
#   <head>
#     <title>Music Mashup Battle</title>
#   </head>
#   <body>
#     <h1>Music Mashup Battle</h1>
#     <button id="create-room-btn">Create Room</button>
#     <button id="join-room-btn">Join Room</button>
#     <script src="https://cdn.jsdelivr.net/npm/socket.io@2.3.0/dist/socket.io.js"></script>
#     <script>
#       var socket = io();
#       document.getElementById('create-room-btn').addEventListener('click', function() {
#         socket.emit('create_room', { room_name: 'My Room' });
#       });
#       document.getElementById('join-room-btn').addEventListener('click', function() {
#         socket.emit('join_room', { room_id: 1, user_id: 1 });
#       });
#     </script>
#   </body>
# </html>

# login.html
# <html>
#   <head>
#     <title>Login</title>
#   </head>
#   <body>
#     <h1>Login</h1>
#     <form id="login-form">
#       <input type="text" id="username" placeholder="Username">
#       <input type="password" id="password" placeholder="Password">
#       <button id="login-btn">Login</button>
#     </form>
#     <script>
#       document.getElementById('login-btn').addEventListener('click', function() {
#         var username = document.getElementById('username').value;
#         var password = document.getElementById('password').value;
#         fetch('/login', {
#           method: 'POST',
#           headers: { 'Content-Type': 'application/json' },
#           body: JSON.stringify({ username: username, password: password })
#         })
#         .then(response => response.json())
#         .then(data => console.log(data));
#       });
#     </script>
#   </body>
# </html>

# register.html
# <html>
#   <head>
#     <title>Register</title>
#   </head>
#   <body>
#     <h1>Register</h1>
#     <form id="register-form">
#       <input type="text" id="username" placeholder="Username">
#       <input type="password" id="password" placeholder="Password">
#       <button id="register-btn">Register</button>
#     </form>
#     <script>
#       document.getElementById('register-btn').addEventListener('click', function() {
#         var username = document.getElementById('username').value;
#         var password = document.getElementById('password').value;
#         fetch('/register', {
#           method: 'POST',
#           headers: { 'Content-Type': 'application/json' },
#           body: JSON.stringify({ username: username, password: password })
#         })
#         .then(response => response.json())
#         .then(data => console.log(data));
#       });
#     </script>
#   </body>
# </html>