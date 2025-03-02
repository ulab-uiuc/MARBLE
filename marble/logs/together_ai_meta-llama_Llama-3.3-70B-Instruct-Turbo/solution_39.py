# music_collaborator.py
import tkinter as tk
from tkinter import filedialog, messagebox
import midi
import numpy as np
from nltk.sentiment import SentimentIntensityAnalyzer
import threading
import time
import socket
import json

# Constants
HOST = '127.0.0.1'
PORT = 12345

# Music Collaborator class
class MusicCollaborator:def receive_messages(self, client_socket):def send_chat_message(self):
        # Get the chat message
        chat_message = self.chat_entry.get()
        
        # Send the chat message to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        client_socket.sendall(json.dumps({"message": chat_message}).encode())
        
        # Clear the chat entry
        self.chat_entry.delete(0, tk.END)
        
        # Add the chat message to the chat log
        self.chat_log.append(chat_message)
        self.chat_text.insert(tk.END, chat_message + "\n")def start(self):
        # Start the chat thread
        self.start_chat_thread()
        
        # Start the GUI event loop
        self.root.mainloop()if __name__ == "__main__":
def start_chat_thread(self):
        # Create a new socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to the server
        client_socket.connect((HOST, PORT))
        
        # Start the receive messages thread
        threading.Thread(target=self.receive_messages, args=(client_socket,)).start()
    music_collaborator = MusicCollaborator()
    music_collaborator.start()