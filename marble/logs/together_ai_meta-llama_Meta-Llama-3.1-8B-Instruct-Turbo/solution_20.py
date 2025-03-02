# music_mashup_battle.py
# This script implements the MusicMashupBattle application.

import socket
import threading
import json
import random
import time

# Define a class for the MusicMashupBattle application
class MusicMashupBattle:
    def __init__(self):
        # Initialize the server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 12345))
        self.server_socket.listen(5)

        # Initialize the user dictionary
        self.users = {}

        # Initialize the room dictionary
        self.rooms = {}

        # Initialize the leaderboard
        self.leaderboard = {}

        # Initialize the voting dictionary
        self.voting = {}

        # Initialize the chat dictionary
        self.chat = {}

        # Start the server thread
        self.server_thread = threading.Thread(target=self.server_loop)
        self.server_thread.start()

    def server_loop(self):
        # Continuously listen for incoming connections
        while True:
            # Accept an incoming connection
            client_socket, address = self.server_socket.accept()

            # Handle the client connection in a separate thread
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        # Receive data from the client
        data = client_socket.recv(1024).decode('utf-8')

        # Parse the received data
        parsed_data = json.loads(data)

        # Handle the client request
        if parsed_data['request'] == 'join_room':
            self.join_room(client_socket, parsed_data['room_name'], parsed_data['username'])
        elif parsed_data['request'] == 'create_room':
            self.create_room(client_socket, parsed_data['room_name'], parsed_data['username'])
        elif parsed_data['request'] == 'send_mashup':
            self.send_mashup(client_socket, parsed_data['mashup'])
        elif parsed_data['request'] == 'vote_mashup':
            self.vote_mashup(client_socket, parsed_data['mashup_id'])
        elif parsed_data['request'] == 'send_message':
            self.send_message(client_socket, parsed_data['message'])

        # Close the client socket
        client_socket.close()

    def join_room(self, client_socket, room_name, username):
        # Check if the room exists
        if room_name in self.rooms:
            # Add the user to the room
            self.rooms[room_name].append(username)

            # Send a confirmation message to the client
            client_socket.send(json.dumps({'message': 'Joined room successfully'}).encode('utf-8'))
        else:
            # Create a new room
            self.rooms[room_name] = [username]

            # Send a confirmation message to the client
            client_socket.send(json.dumps({'message': 'Room created successfully'}).encode('utf-8'))

    def create_room(self, client_socket, room_name, username):
        # Check if the room already exists
        if room_name in self.rooms:
            # Send an error message to the client
            client_socket.send(json.dumps({'message': 'Room already exists'}).encode('utf-8'))
        else:
            # Create a new room
            self.rooms[room_name] = [username]

            # Send a confirmation message to the client
            client_socket.send(json.dumps({'message': 'Room created successfully'}).encode('utf-8'))

    def send_mashup(self, client_socket, mashup):
        # Add the mashup to the room
        room_name = self.get_room_name(client_socket)
        self.rooms[room_name].append(mashup)

        # Send a confirmation message to the client
        client_socket.send(json.dumps({'message': 'Mashup sent successfully'}).encode('utf-8'))

    def vote_mashup(self, client_socket, mashup_id):
        # Get the room name
        room_name = self.get_room_name(client_socket)

        # Get the mashup ID
        mashup_id = int(mashup_id)

        # Check if the mashup ID is valid
        if mashup_id < len(self.rooms[room_name]):
            # Increment the vote count
            self.voting[mashup_id] = self.voting.get(mashup_id, 0) + 1

            # Send a confirmation message to the client
            client_socket.send(json.dumps({'message': 'Voted successfully'}).encode('utf-8'))
        else:
            # Send an error message to the client
            client_socket.send(json.dumps({'message': 'Invalid mashup ID'}).encode('utf-8'))

    def send_message(self, client_socket, message):
        # Get the room name
        room_name = self.get_room_name(client_socket)

        # Add the message to the chat
        self.chat[room_name].append(message)

        # Send a confirmation message to the client
        client_socket.send(json.dumps({'message': 'Message sent successfully'}).encode('utf-8'))

    def get_room_name(self, client_socket):
        # Get the room name from the client
        data = client_socket.recv(1024).decode('utf-8')
        parsed_data = json.loads(data)
        return parsed_data['room_name']

    def update_leaderboard(self):
        # Get the top mashups
        top_mashups = sorted(self.voting.items(), key=lambda x: x[1], reverse=True)

        # Update the leaderboard
        self.leaderboard = {i: mashup_id for i, (mashup_id, _) in enumerate(top_mashups)}

        # Send the leaderboard to all clients
        for client_socket in self.users.values():
            client_socket.send(json.dumps({'leaderboard': self.leaderboard}).encode('utf-8'))

    def run(self):
        # Continuously update the leaderboard
        while True:
            self.update_leaderboard()
            time.sleep(1)

if __name__ == '__main__':
    # Create an instance of the MusicMashupBattle application
    app = MusicMashupBattle()

    # Run the application
    app.run()