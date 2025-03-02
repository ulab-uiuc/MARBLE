# language_learning_hub.py
# This is the main implementation file for the Language Learning Hub project.

# Importing required libraries
import tkinter as tk
from tkinter import ttk
import sqlite3
import threading
import socket
import json

# Database schema
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
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY,
                user1 INTEGER NOT NULL,
                user2 INTEGER NOT NULL,
                message TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS game_scores (
                id INTEGER PRIMARY KEY,
                user INTEGER NOT NULL,
                score INTEGER NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def insert_user(self, username, password, role):
        self.cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        self.conn.commit()

    def get_user(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return self.cursor.fetchone()

    def insert_conversation(self, user1, user2, message, timestamp):
        self.cursor.execute("INSERT INTO conversations (user1, user2, message, timestamp) VALUES (?, ?, ?, ?)", (user1, user2, message, timestamp))
        self.conn.commit()

    def get_conversations(self, user):
        self.cursor.execute("SELECT * FROM conversations WHERE user1 = ? OR user2 = ?", (user, user))
        return self.cursor.fetchall()

    def insert_game_score(self, user, score, timestamp):
        self.cursor.execute("INSERT INTO game_scores (user, score, timestamp) VALUES (?, ?, ?)", (user, score, timestamp))
        self.conn.commit()

    def get_game_scores(self, user):
        self.cursor.execute("SELECT * FROM game_scores WHERE user = ?", (user,))
        return self.cursor.fetchall()

# Real-time chat and voice communication
class Chat:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Learning Hub")
        self.root.geometry("800x600")
        self.chat_frame = tk.Frame(self.root)
        self.chat_frame.pack(fill="both", expand=True)
        self.text_box = tk.Text(self.chat_frame)
        self.text_box.pack(fill="both", expand=True)
        self.entry = tk.Entry(self.chat_frame)
        self.entry.pack(fill="x")
        self.send_button = tk.Button(self.chat_frame, text="Send", command=self.send_message)
        self.send_button.pack(fill="x")
        self.receive_thread = threading.Thread(target=self.receive_message)
        self.receive_thread.start()

    def send_message(self):
        message = self.entry.get()
        self.entry.delete(0, "end")
        self.text_box.insert("end", "You: " + message + "\n")
        self.text_box.see("end")
        self.send_socket(message)

    def receive_message(self):
        while True:
            message = self.receive_socket()
            self.text_box.insert("end", "Other: " + message + "\n")
            self.text_box.see("end")

    def send_socket(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 12345))
        sock.sendall(message.encode())
        sock.close()

    def receive_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("localhost", 12345))
        sock.listen(1)
        conn, addr = sock.accept()
        message = conn.recv(1024).decode()
        conn.close()
        sock.close()
        return message

# Vocabulary games
class VocabularyGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Vocabulary Game")
        self.root.geometry("800x600")
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(fill="both", expand=True)
        self.word_label = tk.Label(self.game_frame, text="Word:")
        self.word_label.pack(fill="x")
        self.word_entry = tk.Entry(self.game_frame)
        self.word_entry.pack(fill="x")
        self.definition_label = tk.Label(self.game_frame, text="Definition:")
        self.definition_label.pack(fill="x")
        self.definition_entry = tk.Entry(self.game_frame)
        self.definition_entry.pack(fill="x")
        self.submit_button = tk.Button(self.game_frame, text="Submit", command=self.submit_word)
        self.submit_button.pack(fill="x")

    def submit_word(self):
        word = self.word_entry.get()
        definition = self.definition_entry.get()
        self.word_entry.delete(0, "end")
        self.definition_entry.delete(0, "end")
        self.game_frame.destroy()
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(fill="both", expand=True)
        self.result_label = tk.Label(self.game_frame, text="Result:")
        self.result_label.pack(fill="x")
        self.result_text = tk.Text(self.game_frame)
        self.result_text.pack(fill="both", expand=True)
        self.result_text.insert("end", "Word: " + word + "\nDefinition: " + definition + "\n")
        self.result_text.see("end")

# Grammar correction
class GrammarCorrection:
    def __init__(self, root):
        self.root = root
        self.root.title("Grammar Correction")
        self.root.geometry("800x600")
        self.correction_frame = tk.Frame(self.root)
        self.correction_frame.pack(fill="both", expand=True)
        self.text_box = tk.Text(self.correction_frame)
        self.text_box.pack(fill="both", expand=True)
        self.submit_button = tk.Button(self.correction_frame, text="Submit", command=self.submit_text)
        self.submit_button.pack(fill="x")

    def submit_text(self):
        text = self.text_box.get("1.0", "end")
        self.text_box.delete("1.0", "end")
        self.correction_frame.destroy()
        self.correction_frame = tk.Frame(self.root)
        self.correction_frame.pack(fill="both", expand=True)
        self.result_label = tk.Label(self.correction_frame, text="Result:")
        self.result_label.pack(fill="x")
        self.result_text = tk.Text(self.correction_frame)
        self.result_text.pack(fill="both", expand=True)
        self.result_text.insert("end", "Corrected text: " + text + "\n")
        self.result_text.see("end")

# Main application
class LanguageLearningHub:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Learning Hub")
        self.root.geometry("800x600")
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)
        self.chat_frame = tk.Frame(self.root)
        self.notebook.add(self.chat_frame, text="Chat")
        self.vocabulary_game_frame = tk.Frame(self.root)
        self.notebook.add(self.vocabulary_game_frame, text="Vocabulary Game")
        self.grammar_correction_frame = tk.Frame(self.root)
        self.notebook.add(self.grammar_correction_frame, text="Grammar Correction")
        self.database = Database("language_learning_hub.db")
        self.database.insert_user("admin", "password", "admin")
        self.chat = Chat(self.chat_frame)
        self.vocabulary_game = VocabularyGame(self.vocabulary_game_frame)
        self.grammar_correction = GrammarCorrection(self.grammar_correction_frame)

# Create the main application
root = tk.Tk()
app = LanguageLearningHub(root)
root.mainloop()