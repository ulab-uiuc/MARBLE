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
    # This function would generate a maze based on the level
    return f"Maze Level {level}: " + ''.join(random.choices('X O', k=20))

# Route to create a new game
@app.route('/new_game', methods=['POST'])
def new_game():
    level = request.json.get('level', 1)  # Get level from request
    maze = generate_maze(level)  # Generate maze
    game_state = GameState(maze=maze)  # Create new game state
    db.session.add(game_state)  # Add to database
    db.session.commit()  # Commit changes
    return jsonify({'maze': maze}), 201  # Return maze

# Socket event for player joining
@socketio.on('join')
def handle_join(data):
    username = data['username']
    role = data['role']
    player = Player(username=username, role=role)  # Create new player
    db.session.add(player)  # Add player to database
    db.session.commit()  # Commit changes
    emit('player_joined', {'username': username, 'role': role}, broadcast=True)  # Notify others

# Socket event for player action
@socketio.on('player_action')
def handle_player_action(data):
    action = data['action']
    username = data['username']
    # Here we would handle the action and update the game state accordingly
    emit('action_performed', {'username': username, 'action': action}, broadcast=True)  # Notify others

# Route to get current game state
@app.route('/game_state', methods=['GET'])
def get_game_state():
    game_state = GameState.query.first()  # Get the first game state
    return jsonify({'maze': game_state.maze}), 200  # Return maze

# Main route to serve the frontend
@app.route('/')
def index():
    return render_template('index.html')  # Render the main game page

# Run the app
if __name__ == '__main__':
    socketio.run(app, debug=True)  # Start the server with SocketIO