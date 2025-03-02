# solution.py
# Importing required libraries
import tkinter as tk
from tkinter import ttk
import sqlite3
import threading
import socket
import json

# Database setup
class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS quests (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS skill_plans (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        self.conn.commit()

    def insert_user(self, username, password):
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.conn.commit()

    def get_user(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return self.cursor.fetchone()

    def insert_quest(self, title, description, user_id):
        self.cursor.execute("INSERT INTO quests (title, description, user_id) VALUES (?, ?, ?)", (title, description, user_id))
        self.conn.commit()

    def get_quests(self, user_id):
        self.cursor.execute("SELECT * FROM quests WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()

    def insert_skill_plan(self, name, description, user_id):
        self.cursor.execute("INSERT INTO skill_plans (name, description, user_id) VALUES (?, ?, ?)", (name, description, user_id))
        self.conn.commit()

    def get_skill_plans(self, user_id):
        self.cursor.execute("SELECT * FROM skill_plans WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()

# Backend setup
class Backend:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.clients = []
        self.nicknames = []

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.nicknames.remove(nickname)
                self.broadcast(f'{nickname} left the chat!'.encode('ascii'))
                break

    def receive(self):
        while True:
            client, address = self.server.accept()
            print(f"Connected with {str(address)}")

            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            self.nicknames.append(nickname)
            self.clients.append(client)

            print(f'Nickname of the client is {nickname}!')
            self.broadcast(f'{nickname} joined the chat!'.encode('ascii'))
            client.send('Connected to the server!'.encode('ascii'))

            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

# Frontend setup
class Frontend:
    def __init__(self, root):
        self.root = root
        self.root.title('QuestHub')
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        self.frame1 = tk.Frame(self.notebook)
        self.frame2 = tk.Frame(self.notebook)
        self.frame3 = tk.Frame(self.notebook)

        self.notebook.add(self.frame1, text='Quests')
        self.notebook.add(self.frame2, text='Skill Plans')
        self.notebook.add(self.frame3, text='Chat')

        self.create_widgets()

    def create_widgets(self):
        # Quests frame
        self.quest_label = tk.Label(self.frame1, text='Quests:')
        self.quest_label.pack()

        self.quest_entry = tk.Entry(self.frame1)
        self.quest_entry.pack()

        self.quest_button = tk.Button(self.frame1, text='Create Quest', command=self.create_quest)
        self.quest_button.pack()

        self.quests_listbox = tk.Listbox(self.frame1)
        self.quests_listbox.pack()

        # Skill Plans frame
        self.skill_plan_label = tk.Label(self.frame2, text='Skill Plans:')
        self.skill_plan_label.pack()

        self.skill_plan_entry = tk.Entry(self.frame2)
        self.skill_plan_entry.pack()

        self.skill_plan_button = tk.Button(self.frame2, text='Create Skill Plan', command=self.create_skill_plan)
        self.skill_plan_button.pack()

        self.skill_plans_listbox = tk.Listbox(self.frame2)
        self.skill_plans_listbox.pack()

        # Chat frame
        self.chat_label = tk.Label(self.frame3, text='Chat:')
        self.chat_label.pack()

        self.chat_text = tk.Text(self.frame3)
        self.chat_text.pack()

        self.chat_entry = tk.Entry(self.frame3)
        self.chat_entry.pack()

        self.chat_button = tk.Button(self.frame3, text='Send', command=self.send_message)
        self.chat_button.pack()

    def create_quest(self):
        title = self.quest_entry.get()
        description = self.quests_listbox.get(tk.ACTIVE)
        user_id = 1  # Replace with actual user ID
        db = Database('questhub.db')
        db.insert_quest(title, description, user_id)
        self.quests_listbox.insert(tk.END, title)

    def create_skill_plan(self):
        name = self.skill_plan_entry.get()
        description = self.skill_plans_listbox.get(tk.ACTIVE)
        user_id = 1  # Replace with actual user ID
        db = Database('questhub.db')
        db.insert_skill_plan(name, description, user_id)
        self.skill_plans_listbox.insert(tk.END, name)

    def send_message(self):
        message = self.chat_entry.get()
        self.chat_text.insert(tk.END, f'You: {message}\n')
        self.chat_entry.delete(0, tk.END)
        backend = Backend('127.0.0.1', 55555)
        backend.broadcast(message.encode('ascii'))

# Main function
def main():
    root = tk.Tk()
    root.geometry('800x600')
    frontend = Frontend(root)
    root.mainloop()

if __name__ == '__main__':
    main()