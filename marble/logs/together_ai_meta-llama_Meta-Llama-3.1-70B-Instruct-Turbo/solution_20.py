# music_mashup_battle.py

import asyncio
import json
import os
import sqlite3
from datetime import datetime
from typing import Dict, List

import websockets

# Database
class Database:
    def __init__(self, db_name: str):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                creator_id INTEGER NOT NULL,
                FOREIGN KEY (creator_id) REFERENCES users (id)
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS mashups (
                id INTEGER PRIMARY KEY,
                room_id INTEGER NOT NULL,
                creator_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                FOREIGN KEY (room_id) REFERENCES rooms (id),
                FOREIGN KEY (creator_id) REFERENCES users (id)
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS votes (
                id INTEGER PRIMARY KEY,
                mashup_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                vote INTEGER NOT NULL,
                FOREIGN KEY (mashup_id) REFERENCES mashups (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            """
        )
        self.conn.commit()

    def add_user(self, username: str, password: str):
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.conn.commit()

    def get_user(self, username: str):
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return self.cursor.fetchone()

    def add_room(self, name: str, creator_id: int):
        self.cursor.execute("INSERT INTO rooms (name, creator_id) VALUES (?, ?)", (name, creator_id))
        self.conn.commit()

    def get_room(self, room_id: int):
        self.cursor.execute("SELECT * FROM rooms WHERE id = ?", (room_id,))
        return self.cursor.fetchone()

    def add_mashup(self, room_id: int, creator_id: int, name: str):
        self.cursor.execute("INSERT INTO mashups (room_id, creator_id, name) VALUES (?, ?, ?)", (room_id, creator_id, name))
        self.conn.commit()

    def get_mashup(self, mashup_id: int):
        self.cursor.execute("SELECT * FROM mashups WHERE id = ?", (mashup_id,))
        return self.cursor.fetchone()

    def add_vote(self, mashup_id: int, user_id: int, vote: int):
        self.cursor.execute("INSERT INTO votes (mashup_id, user_id, vote) VALUES (?, ?, ?)", (mashup_id, user_id, vote))
        self.conn.commit()

    def get_votes(self, mashup_id: int):
        self.cursor.execute("SELECT * FROM votes WHERE mashup_id = ?", (mashup_id,))
        return self.cursor.fetchall()

# Backend
class Backend:
    def __init__(self, db: Database):
        self.db = db
        self.rooms = {}
        self.mashups = {}

    async def handle_connection(self, websocket, path):
        async for message in websocket:
            data = json.loads(message)
            if data["type"] == "join_room":
                await self.join_room(websocket, data["room_id"])
            elif data["type"] == "create_room":
                await self.create_room(websocket, data["room_name"])
            elif data["type"] == "create_mashup":
                await self.create_mashup(websocket, data["room_id"], data["mashup_name"])
            elif data["type"] == "vote":
                await self.vote(websocket, data["mashup_id"], data["vote"])

    async def join_room(self, websocket, room_id: int):async def create_room(self, websocket, room_name: str, username: str):async def create_mashup(self, websocket, room_id: int, mashup_name: str, username: str):user = self.db.get_user(username); if user: user_id = user[0]; else: await websocket.send(json.dumps({"type": "error", "message": "User not found"})); returnself.db.add_mashup(room_id, user_id, mashup_name)
        mashup_id = self.db.cursor.lastrowid
        self.mashups[mashup_id] = {"room_id": room_id, "creator_id": user_id, "name": mashup_name}
        await websocket.send(json.dumps({"type": "mashup_created", "mashup_id": mashup_id}))

    async def vote(self, websocket, mashup_id: int, vote: int):user_id = self.db.get_user(username)[0]self.db.add_vote(mashup_id, user_id, vote)
        await websocket.send(json.dumps({"type": "voted"}))

# Frontend
class Frontend:
    def __init__(self):
        self.rooms = {}
        self.mashups = {}

    def render_room(self, room_id: int):
        # Render room UI
        pass

    def render_mashup(self, mashup_id: int):
        # Render mashup UI
        pass

    def handle_user_input(self, user_input: str):
        # Handle user input
        pass

# Main
async def main():
    db = Database("music_mashup_battle.db")
    backend = Backend(db)
    frontend = Frontend()

    async with websockets.serve(backend.handle_connection, "localhost", 8765):
        print("Server started on port 8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())