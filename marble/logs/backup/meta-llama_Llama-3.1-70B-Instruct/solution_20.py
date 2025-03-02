# music_mashup_battle.py

import asyncio
import json
import os
import sqlite3
from datetime import datetime
import bcrypt
from typing import Dict, List

import websockets

# Database setup
conn = sqlite3.connect('music_mashup_battle.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS rooms (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        creator_id INTEGER NOT NULL,
        FOREIGN KEY (creator_id) REFERENCES users (id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS mashups (
        id INTEGER PRIMARY KEY,
        room_id INTEGER NOT NULL,
        creator_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        data TEXT NOT NULL,
        FOREIGN KEY (room_id) REFERENCES rooms (id),
        FOREIGN KEY (creator_id) REFERENCES users (id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS votes (
        id INTEGER PRIMARY KEY,
        mashup_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        vote INTEGER NOT NULL,
        FOREIGN KEY (mashup_id) REFERENCES mashups (id),
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')

conn.commit()

# User class
class User:password = message['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))user = User(*user_data)
                    await websocket.send(json.dumps({'type': 'login_success', 'user_id': user.id}))
                else:
                    await websocket.send(json.dumps({'type': 'login_failure'}))

            elif message['type'] == 'create_room':
                # Handle create room
                room_name = message['room_name']try: cursor.execute('INSERT INTO rooms (name, creator_id) VALUES (?, ?)', (room_name, user_id)) except sqlite3.Error as e: print(f'Database error: {e}')room_id = cursor.lastrowid
                conn.commit()

                await websocket.send(json.dumps({'type': 'room_created', 'room_id': room_id}))

            elif message['type'] == 'join_room':
                # Handle join room
                room_id = message['room_id']try: cursor.execute('''SELECT m.id, m.name, SUM(v.vote) as total_votes FROM mashups m JOIN votes v ON m.id = v.mashup_id WHERE m.room_id = ? GROUP BY m.id ORDER BY total_votes DESC''', (room_id,)) except sqlite3.Error as e: print(f'Database error: {e}')leaderboard = cursor.fetchall()

                await websocket.send(json.dumps({'type': 'leaderboard', 'leaderboard': leaderboard}))

        except websockets.ConnectionClosed:
            print(f'Connection closed from {path}')
            break

# Start websocket server
async def main():
    async with websockets.serve(handle_connection, 'localhost', 8765):
        print('Websocket server started on port 8765')
        await asyncio.Future()

asyncio.run(main())