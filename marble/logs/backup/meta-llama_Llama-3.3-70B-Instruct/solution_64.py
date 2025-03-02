# quest_hub.py
import sqlite3
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit

# Initialize the Flask application
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

# Define a class for the QuestHub application
class QuestHub:def create_user(self, username, password):
self.database = Database()self.database.insert_user(username, password)self.conn.commit()return "Collaboration created successfully!"

# Define routes for the API
@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    quest_hub = QuestHub()
    return quest_hub.create_user(data['username'], data['password'])

@app.route('/create_quest', methods=['POST'])
def create_quest():
    data = request.get_json()
    quest_hub = QuestHub()
    return quest_hub.create_quest(data['title'], data['description'])

@app.route('/create_skill_plan', methods=['POST'])
def create_skill_plan():
    data = request.get_json()
    quest_hub = QuestHub()
    return quest_hub.create_skill_plan(data['title'], data['description'])

@app.route('/collaborate_on_quest', methods=['POST'])
def collaborate_on_quest():
    data = request.get_json()
    quest_hub = QuestHub()
    return quest_hub.collaborate_on_quest(data['quest_id'], data['user_id'])

# Define SocketIO events for real-time collaboration
@socketio.on('join_quest')
def join_quest(data):
    # Handle user joining a quest
    emit('user_joined', data, broadcast=True)

@socketio.on('leave_quest')
def leave_quest(data):
    # Handle user leaving a quest
    emit('user_left', data, broadcast=True)

@socketio.on('update_quest')
def update_quest(data):
    # Handle quest updates
    emit('quest_updated', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)

# database.py
import sqlite3

class Database:
    def __init__(self):
self.database = Database()
        self.conn = sqlite3.connect('quest_hub.db')
        self.c = self.conn.cursor()

    def create_tables(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS users
                         (id INTEGER PRIMARY KEY AUTOINCREMENT, username text, password text)''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS quests
                         (id INTEGER PRIMARY KEY AUTOINCREMENT, title text, description text, completed INTEGER)''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS skill_plans
                         (id INTEGER PRIMARY KEY AUTOINCREMENT, title text, description text)''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS collaborations
                         (id INTEGER PRIMARY KEY AUTOINCREMENT, quest_id INTEGER, user_id INTEGER)''')

        self.conn.commit()

    def insert_user(self, username, password):self.c.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {'username': username, 'password': password})self.conn.commit()

    def insert_quest(self, title, description):self.c.execute("INSERT INTO quests (title, description, completed) VALUES (:title, :description, 0)", {'title': title, 'description': description})self.conn.commit()

    def insert_skill_plan(self, title, description):self.c.execute("INSERT INTO skill_plans (title, description) VALUES (:title, :description)", {'title': title, 'description': description})self.conn.commit()

    def insert_collaboration(self, quest_id, user_id):self.c.execute("INSERT INTO collaborations (quest_id, user_id) VALUES (:quest_id, :user_id)", {'quest_id': quest_id, 'user_id': user_id})self.conn.commit()

# frontend.py
import tkinter as tk
from tkinter import messagebox

class Frontend:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("QuestHub")

        # Create frames for different sections
        self.login_frame = tk.Frame(self.root)
        self.quest_frame = tk.Frame(self.root)
        self.skill_plan_frame = tk.Frame(self.root)
        self.collaboration_frame = tk.Frame(self.root)

        # Create login frame
        self.login_label = tk.Label(self.login_frame, text="Login")
        self.login_label.pack()

        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack()

        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.pack()

        # Create quest frame
        self.quest_label = tk.Label(self.quest_frame, text="Quests")
        self.quest_label.pack()

        self.quest_title_entry = tk.Entry(self.quest_frame)
        self.quest_title_entry.pack()

        self.quest_description_entry = tk.Entry(self.quest_frame)
        self.quest_description_entry.pack()

        self.create_quest_button = tk.Button(self.quest_frame, text="Create Quest", command=self.create_quest)
        self.create_quest_button.pack()

        # Create skill plan frame
        self.skill_plan_label = tk.Label(self.skill_plan_frame, text="Skill Plans")
        self.skill_plan_label.pack()

        self.skill_plan_title_entry = tk.Entry(self.skill_plan_frame)
        self.skill_plan_title_entry.pack()

        self.skill_plan_description_entry = tk.Entry(self.skill_plan_frame)
        self.skill_plan_description_entry.pack()

        self.create_skill_plan_button = tk.Button(self.skill_plan_frame, text="Create Skill Plan", command=self.create_skill_plan)
        self.create_skill_plan_button.pack()

        # Create collaboration frame
        self.collaboration_label = tk.Label(self.collaboration_frame, text="Collaborations")
        self.collaboration_label.pack()

        self.collaboration_quest_id_entry = tk.Entry(self.collaboration_frame)
        self.collaboration_quest_id_entry.pack()

        self.collaboration_user_id_entry = tk.Entry(self.collaboration_frame)
        self.collaboration_user_id_entry.pack()

        self.create_collaboration_button = tk.Button(self.collaboration_frame, text="Create Collaboration", command=self.create_collaboration)
        self.create_collaboration_button.pack()

    def login(self):
        # Handle login functionality
        pass

    def create_quest(self):
        # Handle create quest functionality
        pass

    def create_skill_plan(self):
        # Handle create skill plan functionality
        pass

    def create_collaboration(self):
        # Handle create collaboration functionality
        pass

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    frontend = Frontend()
    frontend.run()