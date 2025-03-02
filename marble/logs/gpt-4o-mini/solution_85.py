# solution.py

# Import necessary libraries
import json
import threading
from collections import defaultdict
from flask import Flask, request, jsonify, render_template

# Initialize Flask application
app = Flask(__name__)

# In-memory storage for users and game data
users = {}
game_data = defaultdict(lambda: defaultdict(list))  # game_data[game_id][player_name] = [metrics]
lock = threading.Lock()  # Lock for thread-safe operations

# User class to handle user accounts
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

# Function to create a new user account
def create_user(username, password):
    if username in users:
        return False  # User already exists
    users[username] = User(username, password)
    return True

# Function to authenticate a user
def authenticate(username, password):
    user = users.get(username)
    return user is not None and user.password == password

# Route to create a new user account
@app.route('/create_user', methods=['POST'])
def register_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if create_user(username, password):
        return jsonify({"message": "User created successfully"}), 201
    return jsonify({"message": "User already exists"}), 400

# Route to authenticate a user
@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if authenticate(username, password):
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# Route to input game data
@app.route('/input_data', methods=['POST'])
def input_game_data():
    data = request.json
    game_id = data.get('game_id')
    player_name = data.get('player_name')
    metrics = data.get('metrics')  # e.g., {'score': 10, 'assists': 2}

    with lock:  # Ensure thread-safe access to game data
        game_data[game_id][player_name].append(metrics)

    return jsonify({"message": "Data input successful"}), 200

# Route to get game data
@app.route('/get_data/<game_id>', methods=['GET'])
def get_game_data(game_id):
    with lock:
        return jsonify(game_data[game_id]), 200

# Route to generate reports
@app.route('/generate_report/<game_id>', methods=['GET'])
def generate_report(game_id):
    with lock:
        report = {}
        for player, metrics in game_data[game_id].items():
            report[player] = {
                "total_scores": sum(m['score'] for m in metrics),
                "total_assists": sum(m['assists'] for m in metrics),
                "games_played": len(metrics)
            }
    return jsonify(report), 200

# Function to run the application
if __name__ == '__main__':
    app.run(debug=True)

# Test cases for the application
# These would typically be in a separate test file, but included here for completeness
def test_create_user():
    assert create_user("analyst1", "password123") == True
    assert create_user("analyst1", "password123") == False  # User already exists

def test_authenticate():
    create_user("analyst2", "password123")
    assert authenticate("analyst2", "password123") == True
    assert authenticate("analyst2", "wrongpassword") == False

def test_input_game_data():
    create_user("analyst3", "password123")
    authenticate("analyst3", "password123")
    input_game_data({"game_id": "game1", "player_name": "Player1", "metrics": {"score": 10, "assists": 2}})
    assert len(game_data["game1"]["Player1"]) == 1

def test_generate_report():
    input_game_data({"game_id": "game1", "player_name": "Player1", "metrics": {"score": 10, "assists": 2}})
    report = generate_report("game1")
    assert report["Player1"]["total_scores"] == 10
    assert report["Player1"]["total_assists"] == 2
    assert report["Player1"]["games_played"] == 1