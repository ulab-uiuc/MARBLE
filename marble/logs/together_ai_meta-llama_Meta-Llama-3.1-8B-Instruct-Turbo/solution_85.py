# solution.py

import tkinter as tk
from tkinter import ttk
import threading
import time
import random

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.data = {}

class SportGame_Collaborative_Analytics:
    def __init__(self, root):
        self.root = root
        self.users = {}
        self.current_user = None
        self.data = {}
        self.lock = threading.Lock()

        # Create login frame
        self.login_frame = ttk.Frame(self.root)
        self.login_frame.pack(fill="both", expand=True)

        # Create username and password entry fields
        self.username_label = ttk.Label(self.login_frame, text="Username:")
        self.username_label.pack(side="left")
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.pack(side="left")

        self.password_label = ttk.Label(self.login_frame, text="Password:")
        self.password_label.pack(side="left")
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.pack(side="left")

        # Create login button
        self.login_button = ttk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.pack(side="left")

        # Create register frame
        self.register_frame = ttk.Frame(self.root)
        self.register_frame.pack(fill="both", expand=True)

        # Create username and password entry fields for registration
        self.register_username_label = ttk.Label(self.register_frame, text="Username:")
        self.register_username_label.pack(side="left")
        self.register_username_entry = ttk.Entry(self.register_frame)
        self.register_username_entry.pack(side="left")

        self.register_password_label = ttk.Label(self.register_frame, text="Password:")
        self.register_password_label.pack(side="left")
        self.register_password_entry = ttk.Entry(self.register_frame, show="*")
        self.register_password_entry.pack(side="left")

        # Create register button
        self.register_button = ttk.Button(self.register_frame, text="Register", command=self.register)
        self.register_button.pack(side="left")

        # Create data entry frame
        self.data_entry_frame = ttk.Frame(self.root)
        self.data_entry_frame.pack(fill="both", expand=True)

        # Create player name entry field
        self.player_name_label = ttk.Label(self.data_entry_frame, text="Player Name:")
        self.player_name_label.pack(side="left")
        self.player_name_entry = ttk.Entry(self.data_entry_frame)
        self.player_name_entry.pack(side="left")

        # Create score entry field
        self.score_label = ttk.Label(self.data_entry_frame, text="Score:")
        self.score_label.pack(side="left")
        self.score_entry = ttk.Entry(self.data_entry_frame)
        self.score_entry.pack(side="left")

        # Create assist entry field
        self.assist_label = ttk.Label(self.data_entry_frame, text="Assist:")
        self.assist_label.pack(side="left")
        self.assist_entry = ttk.Entry(self.data_entry_frame)
        self.assist_entry.pack(side="left")

        # Create submit button
        self.submit_button = ttk.Button(self.data_entry_frame, text="Submit", command=self.submit_data)
        self.submit_button.pack(side="left")

        # Create report frame
        self.report_frame = ttk.Frame(self.root)
        self.report_frame.pack(fill="both", expand=True)

        # Create report button
        self.report_button = ttk.Button(self.report_frame, text="Report", command=self.generate_report)
        self.report_button.pack(side="left")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in self.users and self.users[username].password == password:
            self.current_user = username
            self.login_frame.pack_forget()
            self.data_entry_frame.pack(fill="both", expand=True)
        else:
            print("Invalid username or password")

    def register(self):
        username = self.register_username_entry.get()
        password = self.register_password_entry.get()
        if username not in self.users:
            self.users[username] = User(username, password)
            print("User registered successfully")
        else:
            print("Username already exists")

    def submit_data(self):
        with self.lock:
            player_name = self.player_name_entry.get()
            score = self.score_entry.get()
            assist = self.assist_entry.get()
            if player_name and score and assist:
                if player_name not in self.data:
                    self.data[player_name] = {"score": score, "assist": assist}
                else:
                    self.data[player_name]["score"] = score
                    self.data[player_name]["assist"] = assist
                print("Data submitted successfully")
                self.player_name_entry.delete(0, "end")
                self.score_entry.delete(0, "end")
                self.assist_entry.delete(0, "end")
            else:
                print("Please fill all fields")

    def generate_report(self):
        with self.lock:
            report = ""
            for player, data in self.data.items():
                report += f"Player: {player}\n"
                report += f"Score: {data['score']}\n"
                report += f"Assist: {data['assist']}\n\n"
            print(report)

def main():
    root = tk.Tk()
    app = SportGame_Collaborative_Analytics(root)
    root.mainloop()

if __name__ == "__main__":
    main()