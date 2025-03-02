# photo_collab_editor.py

import tkinter as tk
from tkinter import ttk
import threading
import socket
import pickle
import time
import random

class PhotoCollabEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("PhotoCollabEditor")
        self.root.geometry("800x600")
        self.photo = tk.PhotoImage(file="image.png")  # Load the initial image
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
        self.tools_frame = tk.Frame(self.root)
        self.tools_frame.pack(side="left")
        self.editing_tools = {
            "brightness": tk.IntVar(),
            "contrast": tk.IntVar(),
            "color_correction": tk.IntVar(),
            "filter": tk.StringVar(),
            "frame": tk.StringVar()
        }
        self.create_tools()
        self.comments_frame = tk.Frame(self.root)
        self.comments_frame.pack(side="right")
        self.comments = tk.Text(self.comments_frame)
        self.comments.pack()
        self.comment_entry = tk.Entry(self.comments_frame)
        self.comment_entry.pack()
        self.comment_button = tk.Button(self.comments_frame, text="Add Comment", command=self.add_comment)
        self.comment_button.pack()
        self.history_button = tk.Button(self.comments_frame, text="History", command=self.show_history)
        self.history_button.pack()
        self.collaborators = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("localhost", 12345))
        self.server_socket.listen(5)
        self.client_socket = None
        self.receive_thread = threading.Thread(target=self.receive_data)
        self.receive_thread.start()

    def create_tools(self):
        for tool, var in self.editing_tools.items():
            tk.Radiobutton(self.tools_frame, text=tool, variable=var, value=1).pack()
        tk.Button(self.tools_frame, text="Apply", command=self.apply_edits).pack()
        tk.Button(self.tools_frame, text="Save Custom Filter", command=self.save_custom_filter).pack()
        tk.Button(self.tools_frame, text="Save Custom Frame", command=self.save_custom_frame).pack()

    def apply_edits(self):
        # Apply the current edits to the photo
        brightness = self.editing_tools["brightness"].get()
        contrast = self.editing_tools["contrast"].get()
        color_correction = self.editing_tools["color_correction"].get()
        filter = self.editing_tools["filter"].get()
        frame = self.editing_tools["frame"].get()
        # Update the photo on the canvas
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
        # Send the edits to the client
        if self.client_socket:
            self.send_data({"edits": {"brightness": brightness, "contrast": contrast, "color_correction": color_correction, "filter": filter, "frame": frame}})

    def save_custom_filter(self):
        # Save the current filter as a custom filter
        filter_name = input("Enter a name for the custom filter: ")
        with open("custom_filters/" + filter_name + ".filter", "w") as f:
            f.write(str(self.editing_tools["filter"].get()))
        print("Custom filter saved successfully!")

    def save_custom_frame(self):
        # Save the current frame as a custom frame
        frame_name = input("Enter a name for the custom frame: ")
        with open("custom_frames/" + frame_name + ".frame", "w") as f:
            f.write(str(self.editing_tools["frame"].get()))
        print("Custom frame saved successfully!")

    def add_comment(self):
        # Add a comment to the comments text box
        comment = self.comment_entry.get()
        self.comments.insert(tk.END, comment + "\n")
        # Send the comment to the client
        if self.client_socket:
            self.send_data({"comment": comment})

    def show_history(self):
        # Show the history of edits made by the user
        history = []
        with open("history.txt", "r") as f:
            for line in f:
                history.append(line.strip())
        self.comments.delete(1.0, tk.END)
        for edit in history:
            self.comments.insert(tk.END, edit + "\n")

    def send_data(self, data):
        # Send data to the client
        self.client_socket.send(pickle.dumps(data))

    def receive_data(self):
        # Receive data from the client
        while True:
            try:
                self.client_socket, address = self.server_socket.accept()
                print("Connected to client at", address)
                while True:
                    data = self.client_socket.recv(1024)
                    if data:
                        data = pickle.loads(data)
                        if "edits" in data:
                            # Apply the edits to the photo
                            self.apply_edits()
                        elif "comment" in data:
                            # Add the comment to the comments text box
                            self.add_comment()
                        elif "history" in data:
                            # Show the history of edits made by the user
                            self.show_history()
            except Exception as e:
                print("Error:", e)

    def start_client(self):
        # Start the client
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("localhost", 12345))
        self.receive_thread = threading.Thread(target=self.receive_data)
        self.receive_thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoCollabEditor(root)
    root.mainloop()