# board_game_team_challenge.py
# This is the main implementation of the Board Game Team Challenge system.

import tkinter as tk
from tkinter import ttk
import sqlite3
import json
import threading
import socket
import pickle

class BoardGameTeamChallenge:
    def __init__(self):
        # Initialize the GUI
        self.root = tk.Tk()
        self.root.title("Board Game Team Challenge")

        # Create a notebook with tabs for different game boards
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        # Create a tab for each game board
        self.game_boards = {}
        for i in range(5):
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=f"Game Board {i+1}")
            self.game_boards[i] = tab

        # Create a frame for the chat
        self.chat_frame = tk.Frame(self.root)
        self.chat_frame.pack(pady=10)

        # Create a text box for the chat
        self.chat_text = tk.Text(self.chat_frame)
        self.chat_text.pack(fill="both", expand=True)

        # Create a frame for the game controls
        self.game_controls_frame = tk.Frame(self.root)
        self.game_controls_frame.pack(pady=10)

        # Create buttons for the game controls
        self.join_button = tk.Button(self.game_controls_frame, text="Join Game", command=self.join_game)
        self.join_button.pack(side="left")

        self.start_button = tk.Button(self.game_controls_frame, text="Start Game", command=self.start_game)
        self.start_button.pack(side="left")

        self.end_button = tk.Button(self.game_controls_frame, text="End Game", command=self.end_game)
        self.end_button.pack(side="left")

        # Create a database connection
        self.conn = sqlite3.connect("board_game_team_challenge.db")
        self.cursor = self.conn.cursor()

        # Create tables for the database
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                team_id INTEGER NOT NULL,
                FOREIGN KEY (team_id) REFERENCES teams (id)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS game_progress (
                id INTEGER PRIMARY KEY,
                game_id INTEGER NOT NULL,
                player_id INTEGER NOT NULL,
                turn INTEGER NOT NULL,
                FOREIGN KEY (game_id) REFERENCES games (id),
                FOREIGN KEY (player_id) REFERENCES players (id)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                start_time REAL NOT NULL,
                end_time REAL NOT NULL
            )
        """)
        self.conn.commit()

        # Create a socket for real-time communication
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("localhost", 12345))
        self.socket.listen(5)

        # Create a thread for handling incoming connections
        self.connection_thread = threading.Thread(target=self.handle_incoming_connections)
        self.connection_thread.start()

    def join_game(self):
        # Create a new game
        self.cursor.execute("INSERT INTO games (name, start_time, end_time) VALUES (?, ?, ?)", ("New Game", 0, 0))
        self.conn.commit()
        self.game_id = self.cursor.lastrowid

        # Create a new team
        self.cursor.execute("INSERT INTO teams (name) VALUES (?)", ("New Team",))
        self.conn.commit()
        self.team_id = self.cursor.lastrowid

        # Create a new player
        self.cursor.execute("INSERT INTO players (name, team_id) VALUES (?, ?)", ("New Player", self.team_id))
        self.conn.commit()
        self.player_id = self.cursor.lastrowid

        # Send a message to the chat
        self.chat_text.insert("end", f"Player {self.player_id} joined the game.\n")

    def start_game(self):
        # Start the game
        self.cursor.execute("UPDATE games SET start_time = ? WHERE id = ?", (time.time(), self.game_id))
        self.conn.commit()

        # Send a message to the chat
        self.chat_text.insert("end", "Game started.\n")

    def end_game(self):
        # End the game
        self.cursor.execute("UPDATE games SET end_time = ? WHERE id = ?", (time.time(), self.game_id))
        self.conn.commit()

        # Send a message to the chat
        self.chat_text.insert("end", "Game ended.\n")

    def handle_incoming_connections(self):
        while True:
            # Accept an incoming connection
            connection, address = self.socket.accept()

            # Receive a message from the client
            message = connection.recv(1024)
            message = pickle.loads(message)

            # Handle the message
            if message["type"] == "join_game":
                # Join the game
                self.join_game()
            elif message["type"] == "start_game":
                # Start the game
                self.start_game()
            elif message["type"] == "end_game":
                # End the game
                self.end_game()

            # Send a response back to the client
            response = {"type": "response", "message": "Game updated."}
            connection.send(pickle.dumps(response))

            # Close the connection
            connection.close()

    def run(self):
        # Run the GUI event loop
        self.root.mainloop()

if __name__ == "__main__":
    # Create an instance of the BoardGameTeamChallenge class
    challenge = BoardGameTeamChallenge()

    # Run the challenge
    challenge.run()