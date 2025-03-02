# solution.py

# Import necessary libraries
import random
from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app and SocketIO for real-time communication
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'  # Database URI
db = SQLAlchemy(app)
socketio = SocketIO(app)

# Database model for Player
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    score = db.Column(db.Integer, default=0)

# Database model for GameState
class GameState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    maze = db.Column(db.String, nullable=False)  # Maze representation
    players = db.relationship('Player', backref='game', lazy=True)

# Initialize the database
db.create_all()

# Define roles for players
ROLES = ['pathfinder', 'blocker', 'swapper']

# Function to generate a random maze (placeholder)
def generate_maze(level):
    # Placeholder for maze generation logic
    return "Maze Level " + str(level)

# Function to start a new game
@app.route('/start_game', methods=['POST'])
def start_game():
    level = request.json.get('level', 1)  # Get level from request
    maze = generate_maze(level)  # Generate maze
    game_state = GameState(maze=maze)  # Create new game state
    db.session.add(game_state)  # Add to database
    db.session.commit()  # Commit changes
    return jsonify({"message": "Game started", "maze": maze}), 200

# SocketIO event for player joining
@socketio.on('join')
def handle_join(data):
    username = data['username']
    role = random.choice(ROLES)  # Assign random role
    player = Player(username=username, role=role)  # Create player
    db.session.add(player)  # Add player to database
    db.session.commit()  # Commit changes
    emit('player_joined', {'username': username, 'role': role}, broadcast=True)  # Notify others

# SocketIO event for player action
@socketio.on('player_action')
def handle_player_action(data):
    action = data['action']
    username = data['username']
    # Logic to handle player actions (e.g., move blocks, create paths)
    emit('action_performed', {'username': username, 'action': action}, broadcast=True)  # Notify others

# Route to get current game state
@app.route('/game_state', methods=['GET'])
def get_game_state():
    game_state = GameState.query.first()  # Get the first game state
    return jsonify({"maze": game_state.maze}), 200  # Return maze

# Route to get player scores
@app.route('/scores', methods=['GET'])
def get_scores():
    players = Player.query.all()  # Get all players
    scores = {player.username: player.score for player in players}  # Create score dictionary
    return jsonify(scores), 200  # Return scores

# Main entry point to run the app
if __name__ == '__main__':
    socketio.run(app, debug=True)  # Run the app with SocketIO