# solution.py
# Importing required libraries
import socket
import threading
import json
from pymongo import MongoClient

# Creating a MongoDB client
client = MongoClient('mongodb://localhost:27017/')
db = client['ArtCollab']
users_collection = db['users']
projects_collection = db['projects']
collaborations_collection = db['collaborations']

# Defining a class for the server
class ArtCollabServer:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.clients = []
        self.nicknames = []

    def broadcast(self, message):
        for client in self.clients:try: json.loads(message) except json.JSONDecodeError: print(f"Invalid JSON message: {message}") returnclient.send(message)

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

    def run(self):
        print("Server Started!")
        self.receive()

# Creating a class for the client
class ArtCollabClient:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))

        self.nickname = input("Choose a nickname: ")
        self.client.send(self.nickname.encode('ascii'))

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('ascii')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('ascii'))
                else:
                    print(message)
            except:
                print("An error occurred!")
                self.client.close()
                break

    def write(self):
        while True:
            message = f'{self.nickname}: {input("")}'
            self.client.send(message.encode('ascii'))

    def run(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()

# Creating a class for the user
class ArtCollabUser:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def register(self):
        users_collection.insert_one({
            'username': self.username,
            'password': self.password
        })

    def login(self):
        user = users_collection.find_one({
            'username': self.username,
            'password': self.password
        })
        if user:
            return True
        else:
            return False

# Creating a class for the project
class ArtCollabProject:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def create(self):
        projects_collection.insert_one({
            'name': self.name,
            'description': self.description
        })

    def get(self):
        project = projects_collection.find_one({
            'name': self.name
        })
        if project:
            return project
        else:
            return None

# Creating a class for the collaboration
class ArtCollabCollaboration:
    def __init__(self, project_id, user_id):
        self.project_id = project_id
        self.user_id = user_id

    def create(self):
        collaborations_collection.insert_one({
            'project_id': self.project_id,
            'user_id': self.user_id
        })

    def get(self):
        collaboration = collaborations_collection.find_one({
            'project_id': self.project_id,
            'user_id': self.user_id
        })
        if collaboration:
            return collaboration
        else:
            return None

# Creating an instance of the server
server = ArtCollabServer()

# Creating an instance of the client
client = ArtCollabClient()

# Creating an instance of the user
user = ArtCollabUser('username', 'password')

# Creating an instance of the project
project = ArtCollabProject('project_name', 'project_description')

# Creating an instance of the collaboration
collaboration = ArtCollabCollaboration('project_id', 'user_id')

# Running the server
server.run()

# Running the client
client.run()

# Registering the user
user.register()

# Logging in the user
user.login()

# Creating the project
project.create()

# Getting the project
project.get()

# Creating the collaboration
collaboration.create()

# Getting the collaboration
collaboration.get()