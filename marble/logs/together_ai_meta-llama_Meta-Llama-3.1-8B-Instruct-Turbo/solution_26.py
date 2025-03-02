# solution.py
# Importing required libraries
import socket
import threading
import json
import random
import string
import hashlib
import hmac
import time
import datetime
from pymongo import MongoClient

# MongoDB connection
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client["ArtCollab"]
users_collection = db["users"]
projects_collection = db["projects"]
collaborations_collection = db["collaborations"]

# Function to generate a random session ID
def generate_session_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

# Function to generate a secure password hash
def generate_password_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to authenticate a user
def authenticate_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and hmac.compare_digest(generate_password_hash(password), user["password"]):
        return user
    return None

# Function to create a new user
def create_user(username, password):
    users_collection.insert_one({"username": username, "password": generate_password_hash(password), "session_id": generate_session_id()})
    return {"username": username, "session_id": generate_session_id()}

# Function to create a new project
def create_project(project_name, creator_session_id):
    projects_collection.insert_one({"project_name": project_name, "creator_session_id": creator_session_id, "collaborators": []})
    return {"project_name": project_name, "creator_session_id": creator_session_id}

# Function to add a collaborator to a project
def add_collaborator(project_id, collaborator_session_id):
    project = projects_collection.find_one({"_id": project_id})
    if project:
        projects_collection.update_one({"_id": project_id}, {"$push": {"collaborators": collaborator_session_id}})
        return {"project_id": project_id, "collaborator_session_id": collaborator_session_id}
    return None

# Function to update the canvas state
def update_canvas_state(project_id, canvas_state):
    project = projects_collection.find_one({"_id": project_id})
    if project:
        projects_collection.update_one({"_id": project_id}, {"$set": {"canvas_state": canvas_state}})
        return {"project_id": project_id, "canvas_state": canvas_state}
    return None

# Function to handle incoming WebSocket connections
def handle_connection(client_socket, address):
    try:
        # Receive the client's session ID
        session_id = client_socket.recv(1024).decode()
        # Authenticate the client
        user = authenticate_user(session_id, "password")
        if user:
            # Create a new project if the client is the creator
            if user["username"] == "creator":
                project = create_project("My Project", user["session_id"])
                projects_collection.insert_one(project)
                # Add the client as a collaborator to the project
                add_collaborator(project["_id"], user["session_id"])
            # Send the project ID to the client
            project_id = projects_collection.find_one({"creator_session_id": user["session_id"]})["_id"]
            client_socket.send(str(project_id).encode())
            # Handle incoming canvas state updates
            while True:
                canvas_state = client_socket.recv(1024).decode()
                update_canvas_state(project_id, canvas_state)
        else:
            # Close the connection if the client is not authenticated
            client_socket.close()
    except Exception as e:
        print(f"Error handling connection: {e}")

# Function to handle incoming WebSocket messages
def handle_message(client_socket, address):
    try:
        # Receive the message from the client
        message = client_socket.recv(1024).decode()
        # Handle the message based on its type
        if message.startswith("CREATE_PROJECT"):
            # Create a new project
            project = create_project("My Project", "creator_session_id")
            projects_collection.insert_one(project)
            # Send the project ID to the client
            client_socket.send(str(project["_id"]).encode())
        elif message.startswith("ADD_COLLABORATOR"):
            # Add a collaborator to the project
            collaborator_session_id = message.split(":")[1]
            add_collaborator(projects_collection.find_one({"creator_session_id": "creator_session_id"})["_id"], collaborator_session_id)
            # Send a success message to the client
            client_socket.send("COLLABORATOR_ADDED".encode())
        elif message.startswith("UPDATE_CANVAS_STATE"):
            # Update the canvas state
            canvas_state = message.split(":")[1]
            update_canvas_state(projects_collection.find_one({"creator_session_id": "creator_session_id"})["_id"], canvas_state)
            # Send a success message to the client
            client_socket.send("CANVAS_STATE_UPDATED".encode())
    except Exception as e:
        print(f"Error handling message: {e}")

# Function to handle incoming WebSocket connections
def handle_connection_thread(client_socket, address):
    threading.Thread(target=handle_connection, args=(client_socket, address)).start()

# Function to handle incoming WebSocket messages
def handle_message_thread(client_socket, address):
    threading.Thread(target=handle_message, args=(client_socket, address)).start()

# Create a WebSocket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 8080))
server_socket.listen(5)

print("WebSocket server listening on port 8080...")

while True:
    client_socket, address = server_socket.accept()
    print(f"Connection from {address}...")
    handle_connection_thread(client_socket, address)
    handle_message_thread(client_socket, address)