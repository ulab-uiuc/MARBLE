class Database:from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def connect(self):self.conn = sqlite3.connect('language_learning_hub.db', timeout=10)self.cursor = self.conn.cursor()# models.py
from enum import Enum
from typing import List, Dict

class UserRole(Enum):
    LEARNER = 1
    NATIVE_SPEAKER = 2
    ADMINISTRATOR = 3

class User:
    def __init__(self, id: int, name: str, role: UserRole):
        self.id = id
        self.name = name
        self.role = role

class Conversation:
    def __init__(self, id: int, user1: User, user2: User, language: str):
        self.id = id
        self.user1 = user1
        self.user2 = user2
        self.language = language
        self.messages = []

    def add_message(self, message: str, sender: User):
        self.messages.append((message, sender))

class VocabularyGame:
    def __init__(self, id: int, user: User, language: str):
        self.id = id
        self.user = user
        self.language = language
        self.score = 0

    def update_score(self, score: int):
        self.score += score

class GrammarCorrection:
    def __init__(self, id: int, user: User, language: str):
        self.id = id
        self.user = user
        self.language = language
        self.corrections = []

    def add_correction(self, correction: str):
        self.corrections.append(correction)


# database.py
from typing import List, Dict
from models import User, Conversation, VocabularyGame, GrammarCorrection

class Database:
def __del__(self):
    self.conn.close()import sqlite3
self.conn = sqlite3.connect('language_learning_hub.db')
self.cursor = self.conn.cursor()
self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, role TEXT)''')
try:
    self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, role TEXT)''')
except sqlite3.Error as e:
    print(f"Error creating table: {e}")
self.users = self.cursor.execute('SELECT * FROM users').fetchall()self.conversations: Dict[int, Conversation] = {}self.cursor.execute('''CREATE TABLE IF NOT EXISTS vocabulary_games (id INTEGER PRIMARY KEY, user_id INTEGER, language TEXT, score INTEGER)''')
self.vocabulary_games = self.cursor.execute('SELECT * FROM vocabulary_games').fetchall()self.grammar_corrections: Dict[int, GrammarCorrection] = {}

    def add_user(self, user: User):def add_user(self, user: User):
    try:
        self.cursor.execute('INSERT INTO users VALUES (?, ?, ?)', (user.id, user.name, user.role.value))
        self.conn.commit()
        return self.cursor.lastrowid
    except sqlite3.Error as e:
        self.conn.rollback()
        print(f"An error occurred: {e}")
        return Nonedef add_conversation(self, conversation: Conversation):def add_conversation(self, conversation: Conversation):
    try:
        self.cursor.execute('INSERT INTO conversations VALUES (?, ?, ?, ?)', (conversation.id, conversation.user1.id, conversation.user2.id, conversation.language))
        self.conn.commit()
        return self.cursor.lastrowid
    except sqlite3.Error as e:
        self.conn.rollback()
        print(f"An error occurred: {e}")
        return Nonedef add_vocabulary_game(self, game: VocabularyGame):def add_vocabulary_game(self, game: VocabularyGame):
    try:
        self.cursor.execute('INSERT INTO vocabulary_games VALUES (?, ?, ?, ?)', (game.id, game.user.id, game.language, game.score))
        self.conn.commit()
        return self.cursor.lastrowid
    except sqlite3.Error as e:
        self.conn.rollback()
        print(f"An error occurred: {e}")
        return Nonedef add_grammar_correction(self, correction: GrammarCorrection):def add_grammar_correction(self, correction: GrammarCorrection):
    try:
        self.cursor.execute('INSERT INTO grammar_corrections VALUES (?, ?, ?, ?)', (correction.id, correction.user.id, correction.language, correction.corrections))
        self.conn.commit()
        return self.cursor.lastrowid
    except sqlite3.Error as e:
        self.conn.rollback()
        print(f"An error occurred: {e}")
        return Noneself.cursor.execute('INSERT INTO grammar_corrections VALUES (?, ?, ?, ?)', (correction.id, correction.user.id, correction.language, correction.corrections))
self.conn.commit()return self.grammar_corrections.get(id)


# backend.py
from flask import Flask, request, jsonify
from models import User, Conversation, VocabularyGame, GrammarCorrection
from database import Database

app = Flask(__name__)
db = Database()

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = User(id=data['id'], name=data['name'], role=UserRole[data['role']])
    db.add_user(user)
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/conversations', methods=['POST'])
def create_conversation():
    data = request.json
    user1 = db.get_user(data['user1_id'])
    user2 = db.get_user(data['user2_id'])
    conversation = Conversation(id=data['id'], user1=user1, user2=user2, language=data['language'])
    db.add_conversation(conversation)
    return jsonify({'message': 'Conversation created successfully'}), 201

@app.route('/vocabulary_games', methods=['POST'])
def create_vocabulary_game():
    data = request.json
    user = db.get_user(data['user_id'])
    game = VocabularyGame(id=data['id'], user=user, language=data['language'])
    db.add_vocabulary_game(game)
    return jsonify({'message': 'Vocabulary game created successfully'}), 201

@app.route('/grammar_corrections', methods=['POST'])
def create_grammar_correction():
    data = request.json
    user = db.get_user(data['user_id'])
    correction = GrammarCorrection(id=data['id'], user=user, language=data['language'])
    db.add_grammar_correction(correction)
    return jsonify({'message': 'Grammar correction created successfully'}), 201

@app.route('/conversations/<int:conversation_id>/messages', methods=['POST'])
def add_message(conversation_id: int):
    data = request.json
    conversation = db.get_conversation(conversation_id)
    if conversation:
        conversation.add_message(data['message'], db.get_user(data['sender_id']))
        return jsonify({'message': 'Message added successfully'}), 201
    else:
        return jsonify({'message': 'Conversation not found'}), 404

@app.route('/vocabulary_games/<int:game_id>/score', methods=['PUT'])
def update_score(game_id: int):
    data = request.json
    game = db.get_vocabulary_game(game_id)
    if game:
        game.update_score(data['score'])
        return jsonify({'message': 'Score updated successfully'}), 200
    else:
        return jsonify({'message': 'Vocabulary game not found'}), 404

@app.route('/grammar_corrections/<int:correction_id>/corrections', methods=['POST'])
def add_correction(correction_id: int):
    data = request.json
    correction = db.get_grammar_correction(correction_id)
    if correction:
        correction.add_correction(data['correction'])
        return jsonify({'message': 'Correction added successfully'}), 201
    else:
        return jsonify({'message': 'Grammar correction not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)


# frontend.py
from flask import Flask, render_template, request, jsonify
from backend import app as backend_app

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    # Authenticate user
    return jsonify({'message': 'User logged in successfully'}), 200

@app.route('/conversations', methods=['GET'])
def get_conversations():
    # Get conversations from backend
    conversations = backend_app.test_client().get('/conversations').json
    return jsonify(conversations), 200

@app.route('/conversations/<int:conversation_id>/messages', methods=['GET'])
def get_messages(conversation_id: int):
    # Get messages from backend
    messages = backend_app.test_client().get(f'/conversations/{conversation_id}/messages').json
    return jsonify(messages), 200

@app.route('/vocabulary_games', methods=['GET'])
def get_vocabulary_games():
    # Get vocabulary games from backend
    games = backend_app.test_client().get('/vocabulary_games').json
    return jsonify(games), 200

@app.route('/grammar_corrections', methods=['GET'])
def get_grammar_corrections():
    # Get grammar corrections from backend
    corrections = backend_app.test_client().get('/grammar_corrections').json
    return jsonify(corrections), 200

if __name__ == '__main__':
    app.run(debug=True)