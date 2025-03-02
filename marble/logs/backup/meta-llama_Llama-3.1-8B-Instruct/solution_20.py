# music_mashup_battle.py
# This is the main implementation of the MusicMashupBattle application.

import socket
import threading
import json
import time
from datetime import datetime

class MusicMashupBattle:
    def __init__(self):
        # Initialize the server settings
        self.host = '127.0.0.1'
        self.port = 12345
        self.rooms = {}
        self.users = {}
        self.leaderboard = {}

    def start_server(self):
        # Create a socket object
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        # Accept incoming connections
        while True:
            client_socket, address = self.server_socket.accept()
            print(f"Connection from {address} established")

            # Create a new thread for each client
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        # Handle incoming messages from the client
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"Received message: {message}")

                # Parse the message
                data = json.loads(message)
                action = data['action']

                if action == 'join_room':
                    self.join_room(client_socket, data)
                elif action == 'create_room':
                    self.create_room(client_socket, data)
                elif action == 'send_mashup':
                    self.send_mashup(client_socket, data)
                elif action == 'vote':
                    self.vote(client_socket, data)
                elif action == 'get_leaderboard':
                    self.get_leaderboard(client_socket, data)
                elif action == 'chat':
                    self.chat(client_socket, data)
            except json.JSONDecodeError:
                print("Invalid JSON message")
            except Exception as e:
                print(f"Error handling client: {e}")

        # Close the client socket
        client_socket.close()

    def join_room(self, client_socket, data):
        # Join a room
        room_name = data['room_name']
        user_id = data['user_id']

        if room_name not in self.rooms:
            self.rooms[room_name] = {'users': [], 'mashups': []}

        if user_id not in self.users:
            self.users[user_id] = {'socket': client_socket, 'room': room_name}

        self.rooms[room_name]['users'].append(user_id)
        client_socket.send(json.dumps({'action': 'joined_room'}).encode('utf-8'))

    def create_room(self, client_socket, data):
        # Create a new room
        room_name = data['room_name']
        user_id = data['user_id']

        if room_name not in self.rooms:
            self.rooms[room_name] = {'users': [], 'mashups': []}

        self.rooms[room_name]['users'].append(user_id)
        client_socket.send(json.dumps({'action': 'created_room'}).encode('utf-8'))

    def send_mashup(self, client_socket, data):
        # Send a mashup to the room
        room_name = data['room_name']
        mashup = data['mashup']

        if room_name in self.rooms:
            self.rooms[room_name]['mashups'].append(mashup)
            client_socket.send(json.dumps({'action': 'sent_mashup'}).encode('utf-8'))

    def vote(self, client_socket, data):
        # Vote on a mashup
        room_name = data['room_name']
        mashup_id = data['mashup_id']
        vote = data['vote']

        if room_name in self.rooms:
            mashup = self.rooms[room_name]['mashups'][mashup_id]
            mashup['votes'] += vote
            client_socket.send(json.dumps({'action': 'voted'}).encode('utf-8'))

    def get_leaderboard(self, client_socket, data):
        # Get the leaderboard
        room_name = data['room_name']

        if room_name in self.rooms:
            leaderboard = sorted(self.rooms[room_name]['mashups'], key=lambda x: x['votes'], reverse=True)
            client_socket.send(json.dumps({'action': 'leaderboard', 'leaderboard': leaderboard}).encode('utf-8'))

    def chat(self, client_socket, data):
        # Send a chat message to the room
        room_name = data['room_name']
        message = data['message']

        if room_name in self.rooms:
            for user_id in self.rooms[room_name]['users']:
                user_socket = self.users[user_id]['socket']
                user_socket.send(json.dumps({'action': 'chat', 'message': message}).encode('utf-8'))

if __name__ == '__main__':
    music_mashup_battle = MusicMashupBattle()
    music_mashup_battle.start_server()