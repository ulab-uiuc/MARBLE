# board_game_team_challenge.py

import sqlite3
import threading
from datetime import datetime
import random
import string
import json
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Database setup
conn = sqlite3.connect('board_game_team_challenge.db')
c = conn.cursor()

# Create tables
c.execute('''CREATE TABLE IF NOT EXISTS players
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, email text)''')

c.execute('''CREATE TABLE IF NOT EXISTS teams
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, player_id INTEGER, FOREIGN KEY (player_id) REFERENCES players (id))''')

c.execute('''CREATE TABLE IF NOT EXISTS games
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, team_id INTEGER, FOREIGN KEY (team_id) REFERENCES teams (id))''')

c.execute('''CREATE TABLE IF NOT EXISTS game_progress
             (id INTEGER PRIMARY KEY AUTOINCREMENT, game_id INTEGER, player_id INTEGER, progress text, FOREIGN KEY (game_id) REFERENCES games (id), FOREIGN KEY (player_id) REFERENCES players (id))''')

c.execute('''CREATE TABLE IF NOT EXISTS game_challenges
             (id INTEGER PRIMARY KEY AUTOINCREMENT, game_id INTEGER, challenge text, difficulty INTEGER, FOREIGN KEY (game_id) REFERENCES games (id))''')

conn.commit()
conn.close()

# Game logic
class Game:
    def __init__(self, id, name, team_id):
        self.id = id
        self.name = name
        self.team_id = team_id
        self.players = []
        self.challenges = []
        self.progress = {}

    def add_player(self, player):
        self.players.append(player)

    def add_challenge(self, challenge):
        self.challenges.append(challenge)

    def update_progress(self, player, progress):
        self.progress[player] = progress

# Player class
class Player:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

# Team class
class Team:
    def __init__(self, id, name, player_id):
        self.id = id
        self.name = name
        self.player_id = player_id

# Challenge class
class Challenge:
    def __init__(self, id, game_id, challenge, difficulty):
        self.id = id
        self.game_id = game_id
        self.challenge = challenge
        self.difficulty = difficulty

# Function to generate random string
def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# Function to create a new game
def create_game(name, team_id):
    conn = sqlite3.connect('board_game_team_challenge.db')
    c = conn.cursor()
    c.execute("INSERT INTO games (name, team_id) VALUES (?, ?)", (name, team_id))
    game_id = c.lastrowid
    conn.commit()
    conn.close()
    return Game(game_id, name, team_id)

# Function to create a new player
def create_player(name, email):
    conn = sqlite3.connect('board_game_team_challenge.db')
    c = conn.cursor()
    c.execute("INSERT INTO players (name, email) VALUES (?, ?)", (name, email))
    player_id = c.lastrowid
    conn.commit()
    conn.close()
    return Player(player_id, name, email)

# Function to create a new team
def create_team(name, player_id):
    conn = sqlite3.connect('board_game_team_challenge.db')
    c = conn.cursor()
    c.execute("INSERT INTO teams (name, player_id) VALUES (?, ?)", (name, player_id))
    team_id = c.lastrowid
    conn.commit()
    conn.close()
    return Team(team_id, name, player_id)

# Function to create a new challenge
def create_challenge(game_id, challenge, difficulty):
    conn = sqlite3.connect('board_game_team_challenge.db')
    c = conn.cursor()
    c.execute("INSERT INTO game_challenges (game_id, challenge, difficulty) VALUES (?, ?, ?)", (game_id, challenge, difficulty))
    challenge_id = c.lastrowid
    conn.commit()
    conn.close()
    return Challenge(challenge_id, game_id, challenge, difficulty)

# Function to update game progress
def update_game_progress(game_id, player_id, progress):
    conn = sqlite3.connect('board_game_team_challenge.db')
    c = conn.cursor()
    c.execute("INSERT INTO game_progress (game_id, player_id, progress) VALUES (?, ?, ?)", (game_id, player_id, progress))
    conn.commit()
    conn.close()

# SocketIO events
@socketio.on('connect')
def connect():
    emit('connected', {'data': 'Connected'})

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

@socketio.on('create_game')
def create_game_event(data):
    game = create_game(data['name'], data['team_id'])
    emit('game_created', {'data': game.name})

@socketio.on('create_player')
def create_player_event(data):
    player = create_player(data['name'], data['email'])
    emit('player_created', {'data': player.name})

@socketio.on('create_team')
def create_team_event(data):
    team = create_team(data['name'], data['player_id'])
    emit('team_created', {'data': team.name})

@socketio.on('create_challenge')
def create_challenge_event(data):
    challenge = create_challenge(data['game_id'], data['challenge'], data['difficulty'])
    emit('challenge_created', {'data': challenge.challenge})

@socketio.on('update_game_progress')
def update_game_progress_event(data):
    update_game_progress(data['game_id'], data['player_id'], data['progress'])
    emit('game_progress_updated', {'data': 'Game progress updated'})

# API endpoints
@app.route('/games', methods=['GET'])
def get_games():
    conn = sqlite3.connect('board_game_team_challenge.db')
    c = conn.cursor()
    c.execute("SELECT * FROM games")
    games = c.fetchall()
    conn.close()
    return jsonify(games)

@app.route('/players', methods=['GET'])
def get_players():
    conn = sqlite3.connect('board_game_team_challenge.db')
    c = conn.cursor()
    c.execute("SELECT * FROM players")
    players = c.fetchall()
    conn.close()
    return jsonify(players)

@app.route('/teams', methods=['GET'])
def get_teams():
    conn = sqlite3.connect('board_game_team_challenge.db')
    c = conn.cursor()
    c.execute("SELECT * FROM teams")
    teams = c.fetchall()
    conn.close()
    return jsonify(teams)

@app.route('/challenges', methods=['GET'])
def get_challenges():
    conn = sqlite3.connect('board_game_team_challenge.db')
    c = conn.cursor()
    c.execute("SELECT * FROM game_challenges")
    challenges = c.fetchall()
    conn.close()
    return jsonify(challenges)

@app.route('/game_progress', methods=['GET'])
def get_game_progress():
    conn = sqlite3.connect('board_game_team_challenge.db')
    c = conn.cursor()
    c.execute("SELECT * FROM game_progress")
    game_progress = c.fetchall()
    conn.close()
    return jsonify(game_progress)

if __name__ == '__main__':
    socketio.run(app)