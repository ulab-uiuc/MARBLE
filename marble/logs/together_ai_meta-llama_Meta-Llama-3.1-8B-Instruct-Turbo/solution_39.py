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
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import download

# Download required NLTK data
download('stopwords')
download('wordnet')
download('punkt')

class MusicCollaborator:
    def __init__(self, root):
        self.root = root
        self.root.title('Music Collaborator')
        self.project_name = tk.StringVar()
        self.project_name.set('New Project')
        self.project_path = tk.StringVar()
        self.project_path.set('Select Project Path')
        self.user_name = tk.StringVar()
        self.user_name.set('Enter User Name')
        self.lyrics = tk.Text(self.root)
        self.melody = tk.Text(self.root)
        self.harmony = tk.Text(self.root)
        self.audio = tk.Label(self.root, text='Audio')
        self.audio_button = tk.Button(self.root, text='Upload Audio', command=self.upload_audio)
        self.sentiment_label = tk.Label(self.root, text='Sentiment Analysis')
        self.sentiment_text = tk.Text(self.root)
        self.chat_log = tk.Text(self.root)
        self.chat_entry = tk.Entry(self.root)
        self.chat_button = tk.Button(self.root, text='Send', command=self.send_chat)
        self.version_control_button = tk.Button(self.root, text='Save Version', command=self.save_version)
        self.revert_button = tk.Button(self.root, text='Revert to Previous Version', command=self.revert_version)
        self.suggest_button = tk.Button(self.root, text='Suggest Musical Adjustments', command=self.suggest_adjustments)
        self.project_frame = tk.Frame(self.root)
        self.project_frame.pack()
        self.project_name_label = tk.Label(self.project_frame, text='Project Name:')
        self.project_name_label.pack(side=tk.LEFT)
        self.project_name_entry = tk.Entry(self.project_frame, textvariable=self.project_name)
        self.project_name_entry.pack(side=tk.LEFT)
        self.project_path_label = tk.Label(self.project_frame, text='Project Path:')
        self.project_path_label.pack(side=tk.LEFT)
        self.project_path_entry = tk.Entry(self.project_frame, textvariable=self.project_path)
        self.project_path_entry.pack(side=tk.LEFT)
        self.project_button = tk.Button(self.project_frame, text='Select Project Path', command=self.select_project_path)
        self.project_button.pack(side=tk.LEFT)
        self.user_frame = tk.Frame(self.root)
        self.user_frame.pack()
        self.user_name_label = tk.Label(self.user_frame, text='User Name:')
        self.user_name_label.pack(side=tk.LEFT)
        self.user_name_entry = tk.Entry(self.user_frame, textvariable=self.user_name)
        self.user_name_entry.pack(side=tk.LEFT)
        self.user_button = tk.Button(self.user_frame, text='Enter User Name', command=self.enter_user_name)
        self.user_button.pack(side=tk.LEFT)
        self.lyrics_frame = tk.Frame(self.root)
        self.lyrics_frame.pack()
        self.lyrics_label = tk.Label(self.lyrics_frame, text='Lyrics:')
        self.lyrics_label.pack(side=tk.LEFT)
        self.lyrics_entry = tk.Text(self.lyrics_frame)
        self.lyrics_entry.pack(side=tk.LEFT)
        self.melody_frame = tk.Frame(self.root)
        self.melody_frame.pack()
        self.melody_label = tk.Label(self.melody_frame, text='Melody:')
        self.melody_label.pack(side=tk.LEFT)
        self.melody_entry = tk.Text(self.melody_frame)
        self.melody_entry.pack(side=tk.LEFT)
        self.harmony_frame = tk.Frame(self.root)
        self.harmony_frame.pack()
        self.harmony_label = tk.Label(self.harmony_frame, text='Harmony:')
        self.harmony_label.pack(side=tk.LEFT)
        self.harmony_entry = tk.Text(self.harmony_frame)
        self.harmony_entry.pack(side=tk.LEFT)
        self.audio_frame = tk.Frame(self.root)
        self.audio_frame.pack()
        self.audio_label = tk.Label(self.audio_frame, text='Audio:')
        self.audio_label.pack(side=tk.LEFT)
        self.audio_entry = tk.Entry(self.audio_frame)
        self.audio_entry.pack(side=tk.LEFT)
        self.sentiment_frame = tk.Frame(self.root)
        self.sentiment_frame.pack()
        self.sentiment_label.pack(side=tk.LEFT)
        self.sentiment_entry = tk.Text(self.sentiment_frame)
        self.sentiment_entry.pack(side=tk.LEFT)
        self.chat_frame = tk.Frame(self.root)
        self.chat_frame.pack()
        self.chat_log_label = tk.Label(self.chat_frame, text='Chat Log:')
        self.chat_log_label.pack(side=tk.LEFT)
        self.chat_log_entry = tk.Text(self.chat_frame)
        self.chat_log_entry.pack(side=tk.LEFT)
        self.chat_button.pack(side=tk.LEFT)
        self.version_control_frame = tk.Frame(self.root)
        self.version_control_frame.pack()
        self.version_control_button.pack(side=tk.LEFT)
        self.revert_button.pack(side=tk.LEFT)
        self.suggest_button.pack(side=tk.LEFT)
        self.project_name_label = tk.Label(self.root, text='Project Name: ' + self.project_name.get())
        self.project_name_label.pack()
        self.project_path_label = tk.Label(self.root, text='Project Path: ' + self.project_path.get())
        self.project_path_label.pack()
        self.user_name_label = tk.Label(self.root, text='User Name: ' + self.user_name.get())
        self.user_name_label.pack()
        self.lyrics_label = tk.Label(self.root, text='Lyrics:')
        self.lyrics_label.pack()
        self.melody_label = tk.Label(self.root, text='Melody:')
        self.melody_label.pack()
        self.harmony_label = tk.Label(self.root, text='Harmony:')
        self.harmony_label.pack()
        self.audio_label = tk.Label(self.root, text='Audio:')
        self.audio_label.pack()
        self.sentiment_label = tk.Label(self.root, text='Sentiment Analysis:')
        self.sentiment_label.pack()
        self.chat_log_label = tk.Label(self.root, text='Chat Log:')
        self.chat_log_label.pack()

    def select_project_path(self):
        path = filedialog.askdirectory()
        self.project_path.set(path)

    def enter_user_name(self):
        user_name = self.user_name.get()
        self.user_name.set(user_name)

    def upload_audio(self):
        file_path = filedialog.askopenfilename()
        self.audio_entry.delete(0, tk.END)
        self.audio_entry.insert(0, file_path)

    def send_chat(self):
        message = self.chat_entry.get()
        self.chat_log.insert(tk.END, message + '\n')
        self.chat_entry.delete(0, tk.END)

    def save_version(self):
        project_path = self.project_path.get()
        version = self.project_name.get() + '_v' + str(len(os.listdir(project_path)) + 1)
        os.mkdir(os.path.join(project_path, version))
        with open(os.path.join(project_path, version, 'lyrics.txt'), 'w') as f:
            f.write(self.lyrics.get('1.0', tk.END))
        with open(os.path.join(project_path, version, 'melody.txt'), 'w') as f:
            f.write(self.melody.get('1.0', tk.END))
        with open(os.path.join(project_path, version, 'harmony.txt'), 'w') as f:
            f.write(self.harmony.get('1.0', tk.END))
        with open(os.path.join(project_path, version, 'audio.txt'), 'w') as f:
            f.write(self.audio_entry.get())
        with open(os.path.join(project_path, version, 'sentiment.txt'), 'w') as f:
            f.write(self.sentiment_entry.get('1.0', tk.END))
        with open(os.path.join(project_path, version, 'chat_log.txt'), 'w') as f:
            f.write(self.chat_log.get('1.0', tk.END))

    def revert_version(self):
        project_path = self.project_path.get()
        versions = os.listdir(project_path)
        versions.sort()
        version = versions[-1]
        with open(os.path.join(project_path, version, 'lyrics.txt'), 'r') as f:
            self.lyrics.delete('1.0', tk.END)
            self.lyrics.insert('1.0', f.read())
        with open(os.path.join(project_path, version, 'melody.txt'), 'r') as f:
            self.melody.delete('1.0', tk.END)
            self.melody.insert('1.0', f.read())
        with open(os.path.join(project_path, version, 'harmony.txt'), 'r') as f:
            self.harmony.delete('1.0', tk.END)
            self.harmony.insert('1.0', f.read())
        with open(os.path.join(project_path, version, 'audio.txt'), 'r') as f:
            self.audio_entry.delete(0, tk.END)
            self.audio_entry.insert(0, f.read())
        with open(os.path.join(project_path, version, 'sentiment.txt'), 'r') as f:
            self.sentiment_entry.delete('1.0', tk.END)
            self.sentiment_entry.insert('1.0', f.read())
        with open(os.path.join(project_path, version, 'chat_log.txt'), 'r') as f:
            self.chat_log.delete('1.0', tk.END)
            self.chat_log.insert('1.0', f.read())

    def suggest_adjustments(self):
        # Suggest musical adjustments based on the current composition
        # This is a placeholder for a more complex algorithm
        # For now, it just suggests a random harmony
        harmony = self.harmony.get('1.0', tk.END)
        if harmony:
            self.harmony.delete('1.0', tk.END)
            self.harmony.insert('1.0', 'Random Harmony: ' + harmony)

    def play_audio(self):
        # Play the uploaded audio
        audio_path = self.audio_entry.get()
        if audio_path:
            audio = AudioSegment.from_file(audio_path)
            play(audio)

    def sentiment_analysis(self):
        # Perform sentiment analysis on the lyrics
        lyrics = self.lyrics.get('1.0', tk.END)
        if lyrics:
            sia = SentimentIntensityAnalyzer()
            sentiment = sia.polarity_scores(lyrics)
            self.sentiment_entry.delete('1.0', tk.END)
            self.sentiment_entry.insert('1.0', str(sentiment))

    def chat_server(self):
        # Start a chat server to handle incoming messages
        host = 'localhost'
        port = 12345
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr)
                    while True:
                        message = conn.recv(1024)
                        if not message:
                            break
                        self.chat_log.insert(tk.END, message.decode() + '\n')

    def start(self):
        # Start the chat server in a separate thread
        threading.Thread(target=self.chat_server).start()
        # Start the audio player in a separate thread
        threading.Thread(target=self.play_audio).start()
        # Start the sentiment analysis in a separate thread
        threading.Thread(target=self.sentiment_analysis).start()

if __name__ == '__main__':
    root = tk.Tk()
    app = MusicCollaborator(root)
    app.start()
    root.mainloop()