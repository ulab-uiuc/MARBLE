# solution.py

import tkinter as tk
from tkinter import ttk
import threading
import time
import random

class User:
    def __init__(self, username):
        self.username = username
        self.score = 0
        self.assists = 0

class SportGame_Collaborative_Analytics:
    def __init__(self, root):
        self.root = root
        self.root.title("Sport Game Collaborative Analytics")
        self.users = {}
        self.data = {}
        self.lock = threading.Lock()

        # Create user account frame
        self.user_frame = ttk.Frame(self.root)
        self.user_frame.pack(fill="x")

        self.username_label = ttk.Label(self.user_frame, text="Username:")
        self.username_label.pack(side="left")

        self.username_entry = ttk.Entry(self.user_frame)
        self.username_entry.pack(side="left")

        self.create_button = ttk.Button(self.user_frame, text="Create Account", command=self.create_account)
        self.create_button.pack(side="left")

        # Create input frame
        self.input_frame = ttk.Frame(self.root)
        self.input_frame.pack(fill="x")

        self.player_name_label = ttk.Label(self.input_frame, text="Player Name:")
        self.player_name_label.pack(side="left")

        self.player_name_entry = ttk.Entry(self.input_frame)
        self.player_name_entry.pack(side="left")

        self.score_label = ttk.Label(self.input_frame, text="Score:")
        self.score_label.pack(side="left")

        self.score_entry = ttk.Entry(self.input_frame)
        self.score_entry.pack(side="left")

        self.assists_label = ttk.Label(self.input_frame, text="Assists:")
        self.assists_label.pack(side="left")

        self.assists_entry = ttk.Entry(self.input_frame)
        self.assists_entry.pack(side="left")

        self.input_button = ttk.Button(self.input_frame, text="Input Data", command=self.input_data)
        self.input_button.pack(side="left")

        # Create report frame
        self.report_frame = ttk.Frame(self.root)
        self.report_frame.pack(fill="x")

        self.report_button = ttk.Button(self.report_frame, text="Generate Report", command=self.generate_report)
        self.report_button.pack(side="left")

        self.report_text = tk.Text(self.report_frame)
        self.report_text.pack(fill="both", expand=True)

    def create_account(self):
        username = self.username_entry.get()
        if username not in self.users:
            self.users[username] = User(username)
            self.username_entry.delete(0, "end")
            self.username_label.config(text="Account created successfully!")
        else:
            self.username_label.config(text="Username already exists!")

    def input_data(self):
        player_name = self.player_name_entry.get()
        score = self.score_entry.get()
        assists = self.assists_entry.get()

        if player_name and score and assists:
            with self.lock:
                if player_name not in self.data:
                    self.data[player_name] = {"score": score, "assists": assists}
                else:
                    self.data[player_name]["score"] = score
                    self.data[player_name]["assists"] = assists

                self.player_name_entry.delete(0, "end")
                self.score_entry.delete(0, "end")
                self.assists_entry.delete(0, "end")

                self.update_report()

    def generate_report(self):
        report = "Player Performance Report:\n"
        for player, data in self.data.items():
            report += f"{player}: Score - {data['score']}, Assists - {data['assists']}\n"

        self.report_text.delete(1.0, "end")
        self.report_text.insert("end", report)

    def update_report(self):
        report = "Player Performance Report:\n"
        for player, data in self.data.items():
            report += f"{player}: Score - {data['score']}, Assists - {data['assists']}\n"

        self.report_text.delete(1.0, "end")
        self.report_text.insert("end", report)

    def start(self):
        self.root.mainloop()

def main():
    root = tk.Tk()
    app = SportGame_Collaborative_Analytics(root)
    app.start()

if __name__ == "__main__":
    main()