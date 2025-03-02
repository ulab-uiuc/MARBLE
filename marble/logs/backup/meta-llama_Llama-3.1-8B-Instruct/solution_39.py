# music_collaborator.py
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import socket
import json
import os
import numpy as np
from pydub import AudioSegment
from pydub.playback import play
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class MusicCollaborator:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Collaborator")
        self.project_name = tk.StringVar()
        self.project_name.set("New Project")
        self.project_path = tk.StringVar()
        self.project_path.set("")
        self.user_name = tk.StringVar()
        self.user_name.set("Guest")
        self.users = {}
        self.project_data = {}
        self.version_control = {}
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.create_widgets()

    def create_widgets(self):
        # Project Name
        tk.Label(self.root, text="Project Name:").grid(row=0, column=0)
        tk.Entry(self.root, textvariable=self.project_name).grid(row=0, column=1)

        # Project Path
        tk.Label(self.root, text="Project Path:").grid(row=1, column=0)
        tk.Entry(self.root, textvariable=self.project_path).grid(row=1, column=1)

        # User Name
        tk.Label(self.root, text="User Name:").grid(row=2, column=0)
        tk.Entry(self.root, textvariable=self.user_name).grid(row=2, column=1)

        # Login Button
        tk.Button(self.root, text="Login", command=self.login).grid(row=3, column=0)

        # Create Project Button
        tk.Button(self.root, text="Create Project", command=self.create_project).grid(row=3, column=1)

        # Project Data
        self.project_data_text = tk.Text(self.root)
        self.project_data_text.grid(row=4, column=0, columnspan=2)

        # Version Control
        self.version_control_text = tk.Text(self.root)
        self.version_control_text.grid(row=5, column=0, columnspan=2)

        # Chat
        self.chat_text = tk.Text(self.root)
        self.chat_text.grid(row=6, column=0, columnspan=2)

        # Send Button
        tk.Button(self.root, text="Send", command=self.send_message).grid(row=7, column=0)

        # Audio Playback
        self.audio_button = tk.Button(self.root, text="Play Audio", command=self.play_audio)
        self.audio_button.grid(row=7, column=1)

    def login(self):
        # Get user name and project name
        user_name = self.user_name.get()
        project_name = self.project_name.get()

        # Check if user exists
        if user_name in self.users:
            # Check if project exists
            if project_name in self.project_data:
                # Login successful
                messagebox.showinfo("Login Successful", "You have logged in successfully.")
            else:
                # Project does not exist
                messagebox.showerror("Error", "Project does not exist.")
        else:
            # User does not exist
            messagebox.showerror("Error", "User does not exist.")

    def create_project(self):
        # Get project name and path
        project_name = self.project_name.get()
        project_path = self.project_path.get()

        # Check if project name is valid
        if project_name:
            # Create project directory
            project_dir = os.path.join(project_path, project_name)
            os.makedirs(project_dir, exist_ok=True)

            # Create project data file
            project_data_file = os.path.join(project_dir, "project_data.json")
            with open(project_data_file, "w") as f:
                json.dump({}, f)

            # Create version control file
            version_control_file = os.path.join(project_dir, "version_control.json")
            with open(version_control_file, "w") as f:
                json.dump({}, f)

            # Create chat log file
            chat_log_file = os.path.join(project_dir, "chat_log.txt")
            with open(chat_log_file, "w") as f:
                f.write("")

            # Create audio file
            audio_file = os.path.join(project_dir, "audio.mp3")
            AudioSegment.from_wav(audio_file).export(audio_file, format="mp3")

            # Create project data
            self.project_data[project_name] = {"melody": [], "harmony": [], "lyrics": []}

            # Update project data text
            self.project_data_text.delete(1.0, tk.END)
            self.project_data_text.insert(tk.END, json.dumps(self.project_data[project_name], indent=4))

            # Update version control text
            self.version_control_text.delete(1.0, tk.END)
            self.version_control_text.insert(tk.END, json.dumps({}, indent=4))

            # Update chat text
            self.chat_text.delete(1.0, tk.END)

            # Update user name
            self.user_name.set(project_name)

            # Update project name
            self.project_name.set(project_name)

            # Update project path
            self.project_path.set(project_dir)

            # Login successful
            messagebox.showinfo("Project Created", "Project created successfully.")
        else:
            # Project name is invalid
            messagebox.showerror("Error", "Project name is invalid.")

    def send_message(self):
        # Get message
        message = self.chat_text.get("1.0", tk.END)

        # Send message to server
        self.send_message_to_server(message)

    def send_message_to_server(self, message):
        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to server
        sock.connect(("localhost", 12345))

        # Send message to server
        sock.sendall(message.encode())

        # Close socket
        sock.close()

    def play_audio(self):
        # Get audio file path
        audio_file_path = os.path.join(self.project_path.get(), "audio.mp3")

        # Play audio
        play(AudioSegment.from_mp3(audio_file_path))

    def analyze_lyrics(self):
        # Get lyrics
        lyrics = self.project_data[self.project_name.get()]["lyrics"]

        # Analyze lyrics
        sentiment = self.sentiment_analyzer.polarity_scores(" ".join(lyrics))
        lemmatized_lyrics = [self.lemmatizer.lemmatize(word) for word in word_tokenize(" ".join(lyrics)) if word not in self.stop_words]
        print("Sentiment:", sentiment)
        print("Lemmatized Lyrics:", lemmatized_lyrics)

def main():
    root = tk.Tk()
    app = MusicCollaborator(root)
    root.mainloop()

if __name__ == "__main__":
    main()