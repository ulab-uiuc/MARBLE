# quest_hub.py
import sqlite3
# database.py
import sqlite3
class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
    def cursor(self):
        return self.cursor
    def commit(self):
        self.conn.commit()
    def close(self):
        self.conn.close()
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit

# Initialize the Flask app and SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Connect to the SQLite database
conn = sqlite3.connect('quest_hub.db')
c = conn.cursor()

# Create tables in the database
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT, username text, password text)''')

c.execute('''CREATE TABLE IF NOT EXISTS quests
             (id INTEGER PRIMARY KEY AUTOINCREMENT, title text, description text, completed INTEGER)''')

c.execute('''CREATE TABLE IF NOT EXISTS skill_plans
             (id INTEGER PRIMARY KEY AUTOINCREMENT, title text, description text)''')

c.execute('''CREATE TABLE IF NOT EXISTS collaborations
             (id INTEGER PRIMARY KEY AUTOINCREMENT, quest_id INTEGER, user_id INTEGER)''')

conn.commit()
conn.close()

# Define a class for the QuestHub system
class QuestHub:from database import Database
self.db = Database('quest_hub.db')
self.c = self.db.cursorself.c = self.conn.cursor()

    # Method to create a new user
    def create_user(self, username, password):try:self.db.commit()except sqlite3.Error as e:self.db.rollback()self.conn.commit()

    # Method to create a new quest
    def create_quest(self, title, description):try:
    self.c.execute("INSERT INTO quests (title, description, completed) VALUES (?, ?, 0)", (title, description))
except sqlite3.Error as e:
    print(f"Error creating quest: {e}")
    self.conn.rollback()self.conn.commit()

    # Method to update a quest
    def update_quest(self, id, title, description):try:
    self.c.execute("UPDATE quests SET title = ?, description = ? WHERE id = ?", (title, description, id))
except sqlite3.Error as e:
    print(f"Error updating quest: {e}")
    self.conn.rollback()self.conn.commit()

    # Method to complete a quest
    def complete_quest(self, id):try:
    self.c.execute("UPDATE quests SET completed = 1 WHERE id = ?", (id,))
except sqlite3.Error as e:
    print(f"Error completing quest: {e}")
    self.conn.rollback()self.conn.commit()

    # Method to create a new skill plan
    def create_skill_plan(self, title, description):try:
    self.c.execute("INSERT INTO skill_plans (title, description) VALUES (?, ?)", (title, description))
except sqlite3.Error as e:
    print(f"Error creating skill plan: {e}")
    self.conn.rollback()self.conn.commit()

    # Method to collaborate on a quest
    def collaborate_on_quest(self, quest_id, user_id):try:
    self.c.execute("INSERT INTO collaborations (quest_id, user_id) VALUES (?, ?)", (quest_id, user_id))
except sqlite3.Error as e:
    print(f"Error collaborating on quest: {e}")
    self.conn.rollback()self.conn.commit()

    # Method to get all quests
    def get_quests(self):try:
    self.c.execute("SELECT * FROM quests")
except sqlite3.Error as e:
    print(f"Error getting quests: {e}")
    return []return self.c.fetchall()

    # Method to get all skill plans
    def get_skill_plans(self):try:
    self.c.execute("SELECT * FROM skill_plans")
except sqlite3.Error as e:
    print(f"Error getting skill plans: {e}")
    return []return self.c.fetchall()

    # Method to get all collaborations
    def get_collaborations(self):try:
    self.c.execute("SELECT * FROM collaborations")
except sqlite3.Error as e:
    print(f"Error getting collaborations: {e}")
    return []return self.c.fetchall()

# Define routes for the API
@app.route('/create_user', methods=['POST'])
def create_user():
    # Get the username and password from the request
    username = request.json['username']
    password = request.json['password']

    # Create a new user
    quest_hub = QuestHub()
    quest_hub.create_user(username, password)

    # Return a success message
    return jsonify({'message': 'User created successfully'})

@app.route('/create_quest', methods=['POST'])
def create_quest():
    # Get the title and description from the request
    title = request.json['title']
    description = request.json['description']

    # Create a new quest
    quest_hub = QuestHub()
    quest_hub.create_quest(title, description)

    # Return a success message
    return jsonify({'message': 'Quest created successfully'})

@app.route('/update_quest', methods=['POST'])
def update_quest():
    # Get the id, title, and description from the request
    id = request.json['id']
    title = request.json['title']
    description = request.json['description']

    # Update the quest
    quest_hub = QuestHub()
    quest_hub.update_quest(id, title, description)

    # Return a success message
    return jsonify({'message': 'Quest updated successfully'})

@app.route('/complete_quest', methods=['POST'])
def complete_quest():
    # Get the id from the request
    id = request.json['id']

    # Complete the quest
    quest_hub = QuestHub()
    quest_hub.complete_quest(id)

    # Return a success message
    return jsonify({'message': 'Quest completed successfully'})

@app.route('/create_skill_plan', methods=['POST'])
def create_skill_plan():
    # Get the title and description from the request
    title = request.json['title']
    description = request.json['description']

    # Create a new skill plan
    quest_hub = QuestHub()
    quest_hub.create_skill_plan(title, description)

    # Return a success message
    return jsonify({'message': 'Skill plan created successfully'})

@app.route('/collaborate_on_quest', methods=['POST'])
def collaborate_on_quest():
    # Get the quest id and user id from the request
    quest_id = request.json['quest_id']
    user_id = request.json['user_id']

    # Collaborate on the quest
    quest_hub = QuestHub()
    quest_hub.collaborate_on_quest(quest_id, user_id)

    # Return a success message
    return jsonify({'message': 'Collaboration created successfully'})

@app.route('/get_quests', methods=['GET'])
def get_quests():
    # Get all quests
    quest_hub = QuestHub()
    quests = quest_hub.get_quests()

    # Return the quests
    return jsonify(quests)

@app.route('/get_skill_plans', methods=['GET'])
def get_skill_plans():
    # Get all skill plans
    quest_hub = QuestHub()
    skill_plans = quest_hub.get_skill_plans()

    # Return the skill plans
    return jsonify(skill_plans)

@app.route('/get_collaborations', methods=['GET'])
def get_collaborations():
    # Get all collaborations
    quest_hub = QuestHub()
    collaborations = quest_hub.get_collaborations()

    # Return the collaborations
    return jsonify(collaborations)

# Define SocketIO events
@socketio.on('connect')
def connect():
    # Handle the connect event
    emit('connected', {'message': 'Connected to the server'})

@socketio.on('create_quest')
def create_quest_event(data):
    # Create a new quest
    quest_hub = QuestHub()
    quest_hub.create_quest(data['title'], data['description'])

    # Emit the quest to all connected clients
    emit('quest_created', data, broadcast=True)

@socketio.on('update_quest')
def update_quest_event(data):
    # Update the quest
    quest_hub = QuestHub()
    quest_hub.update_quest(data['id'], data['title'], data['description'])

    # Emit the updated quest to all connected clients
    emit('quest_updated', data, broadcast=True)

@socketio.on('complete_quest')
def complete_quest_event(data):
    # Complete the quest
    quest_hub = QuestHub()
    quest_hub.complete_quest(data['id'])

    # Emit the completed quest to all connected clients
    emit('quest_completed', data, broadcast=True)

@socketio.on('create_skill_plan')
def create_skill_plan_event(data):
    # Create a new skill plan
    quest_hub = QuestHub()
    quest_hub.create_skill_plan(data['title'], data['description'])

    # Emit the skill plan to all connected clients
    emit('skill_plan_created', data, broadcast=True)

@socketio.on('collaborate_on_quest')
def collaborate_on_quest_event(data):
    # Collaborate on the quest
    quest_hub = QuestHub()
    quest_hub.collaborate_on_quest(data['quest_id'], data['user_id'])

    # Emit the collaboration to all connected clients
    emit('collaboration_created', data, broadcast=True)

if __name__ == '__main__':
    # Run the Flask app
    socketio.run(app)
finally:
    quest_hub.db.close()