# solution.py

# Import necessary libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
import random
import json

# Initialize the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'  # Database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
socketio = SocketIO(app)

# Database models
class Player(db.Model):
    """Model for storing player information."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

class Team(db.Model):
    """Model for storing team information."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    players = db.relationship('Player', backref='team', lazy=True)

class GameState(db.Model):
    """Model for storing the current state of the game."""
    id = db.Column(db.Integer, primary_key=True)
    state_data = db.Column(db.Text, nullable=False)  # JSON string of game state

# Initialize the database
@app.before_first_request
def create_tables():
    db.create_all()

# API endpoint to create a new player
@app.route('/api/player', methods=['POST'])
def create_player():
    """Create a new player and add to the database."""existing_player = Player.query.filter_by(username=data['username']).first()
    if existing_player:
        return jsonify({'message': 'Username already exists'}), 400
    new_player = Player(username=data['username'])
    db.session.add(new_player)
    db.session.commit()    return jsonify({'message': 'Player created', 'player_id': new_player.id}), 201

# API endpoint to create a new team
@app.route('/api/team', methods=['POST'])
def create_team():
    """Create a new team and add to the database."""
    data = request.json
    new_team = Team(name=data['name'])
    db.session.add(new_team)
    db.session.commit()
    return jsonify({'message': 'Team created', 'team_id': new_team.id}), 201

# SocketIO event for player joining a team
@socketio.on('join_team')
def handle_join_team(data):
    """Handle a player joining a team."""
    player = Player.query.get(data['player_id'])
    team = Team.query.get(data['team_id'])
    player.team = team
    db.session.commit()
    emit('team_joined', {'message': f'{player.username} joined {team.name}'}, broadcast=True)

# SocketIO event for game state updates
@socketio.on('update_game_state')
def handle_game_state_update(data):
    """Handle updates to the game state."""
    game_state = GameState.query.first()
    if game_state:
        game_state.state_data = json.dumps(data['state'])
    else:
        game_state = GameState(state_data=json.dumps(data['state']))
        db.session.add(game_state)
    db.session.commit()
    emit('game_state_updated', {'state': data['state']}, broadcast=True)

# API endpoint to get game analytics
@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Provide analytics based on historical gameplay data."""
    # Placeholder for analytics logic
    analytics_data = {
        'total_players': Player.query.count(),
        'total_teams': Team.query.count(),
        'game_states': GameState.query.count()
    }
    return jsonify(analytics_data)

# Main entry point for the application
if __name__ == '__main__':
    socketio.run(app, debug=True)