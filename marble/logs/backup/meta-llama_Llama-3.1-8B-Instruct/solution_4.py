# solution.py
# Importing required libraries
import tkinter as tk
from tkinter import ttk
import sqlite3
import threading
import random
import time

# Database setup
class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                team TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS game_progress (
                id INTEGER PRIMARY KEY,
                player_id INTEGER NOT NULL,
                game_id INTEGER NOT NULL,
                turn INTEGER NOT NULL,
                FOREIGN KEY (player_id) REFERENCES players (id)
            )
        """)
        self.conn.commit()

    def add_player(self, name, team):
        self.cursor.execute("INSERT INTO players (name, team) VALUES (?, ?)", (name, team))
        self.conn.commit()

    def get_player(self, id):
        self.cursor.execute("SELECT * FROM players WHERE id = ?", (id,))
        return self.cursor.fetchone()

    def update_game_progress(self, player_id, game_id, turn):
        self.cursor.execute("INSERT INTO game_progress (player_id, game_id, turn) VALUES (?, ?, ?)", (player_id, game_id, turn))
        self.conn.commit()

# Game logic
class Game:
    def __init__(self):
        self.players = []
        self.game_id = random.randint(1000, 9999)
        self.turn = 0

    def add_player(self, player):
        self.players.append(player)

    def update_turn(self):
        self.turn += 1

# Frontend setup
class Frontend:
    def __init__(self, root):
        self.root = root
        self.root.title("Board Game Team Challenge")
        self.root.geometry("800x600")

        # Create frames
        self.frame_join = tk.Frame(self.root)
        self.frame_game = tk.Frame(self.root)
        self.frame_chat = tk.Frame(self.root)

        # Join frame
        self.label_join = tk.Label(self.frame_join, text="Join a team:")
        self.entry_join_name = tk.Entry(self.frame_join)
        self.entry_join_team = tk.Entry(self.frame_join)
        self.button_join = tk.Button(self.frame_join, text="Join", command=self.join_team)

        # Game frame
        self.label_game = tk.Label(self.frame_game, text="Game board:")
        self.text_game = tk.Text(self.frame_game, height=20, width=80)
        self.button_game_start = tk.Button(self.frame_game, text="Start game", command=self.start_game)

        # Chat frame
        self.label_chat = tk.Label(self.frame_chat, text="Chat:")
        self.text_chat = tk.Text(self.frame_chat, height=10, width=80)
        self.entry_chat = tk.Entry(self.frame_chat)
        self.button_chat = tk.Button(self.frame_chat, text="Send", command=self.send_chat)

        # Layout
        self.frame_join.pack(fill="x")
        self.label_join.pack(side="left")
        self.entry_join_name.pack(side="left")
        self.entry_join_team.pack(side="left")
        self.button_join.pack(side="left")

        self.frame_game.pack(fill="x")
        self.label_game.pack(side="left")
        self.text_game.pack(side="left")
        self.button_game_start.pack(side="left")

        self.frame_chat.pack(fill="x")
        self.label_chat.pack(side="left")
        self.text_chat.pack(side="left")
        self.entry_chat.pack(side="left")
        self.button_chat.pack(side="left")

    def join_team(self):
        name = self.entry_join_name.get()
        team = self.entry_join_team.get()
        db = Database("players.db")
        db.add_player(name, team)
        self.players.append({"name": name, "team": team})

    def start_game(self):
        game = Game()
        for player in self.players:
            game.add_player(player)
        self.text_game.insert("1.0", "Game started!\n")
        self.button_game_start.config(state="disabled")

    def send_chat(self):
        message = self.entry_chat.get()
        self.text_chat.insert("1.0", f"{self.entry_join_name.get()}: {message}\n")
        self.entry_chat.delete(0, "end")

# Backend setup
class Backend:
    def __init__(self, db):
        self.db = db
        self.game = Game()

    def update_game_state(self):
        self.game.update_turn()
        self.db.update_game_progress(self.game.players[0]["id"], self.game.game_id, self.game.turn)

# Main function
def main():
    root = tk.Tk()
    frontend = Frontend(root)
    backend = Backend(Database("players.db"))
    threading.Thread(target=backend.update_game_state).start()
    root.mainloop()

if __name__ == "__main__":
    main()