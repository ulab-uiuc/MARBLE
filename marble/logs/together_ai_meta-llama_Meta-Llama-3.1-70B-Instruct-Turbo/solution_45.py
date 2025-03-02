# notebook_collab_sketch.py

import tkinter as tk
from tkinter import ttk, colorchooser, filedialog
import threading
import time
import json
import os

class NotebookCollabSketch:
    def __init__(self, root):
        self.root = root
        self.root.title("Notebook Collab Sketch")
        self.root.geometry("800x600")

        # Initialize variables
        self.users = {}
        self.pages = {}
        self.current_page = None
        self.current_tool = "brush"
        self.current_color = "black"
        self.current_size = 5
        self.comments = {}

        # Create notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Create frame for drawing
        self.drawing_frame = tk.Frame(self.notebook)
        self.notebook.add(self.drawing_frame, text="Drawing")

        # Create canvas for drawing
        self.canvas = tk.Canvas(self.drawing_frame, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Create frame for tools
        self.tools_frame = tk.Frame(self.root)
        self.tools_frame.pack(fill="x")

        # Create buttons for tools
        self.brush_button = tk.Button(self.tools_frame, text="Brush", command=self.set_brush)
        self.brush_button.pack(side="left")

        self.pen_button = tk.Button(self.tools_frame, text="Pen", command=self.set_pen)
        self.pen_button.pack(side="left")

        self.marker_button = tk.Button(self.tools_frame, text="Marker", command=self.set_marker)
        self.marker_button.pack(side="left")

        # Create buttons for colors
        self.color_button = tk.Button(self.tools_frame, text="Color", command=self.set_color)
        self.color_button.pack(side="left")

        # Create buttons for sizes
        self.size_button = tk.Button(self.tools_frame, text="Size", command=self.set_size)
        self.size_button.pack(side="left")

        # Create frame for comments
        self.comments_frame = tk.Frame(self.root)
        self.comments_frame.pack(fill="x")

        # Create text box for comments
        self.comments_text = tk.Text(self.comments_frame, height=5)
        self.comments_text.pack(fill="x")

        # Create button for adding comments
        self.add_comment_button = tk.Button(self.comments_frame, text="Add Comment", command=self.add_comment)
        self.add_comment_button.pack(side="left")

        # Create frame for user management
        self.user_management_frame = tk.Frame(self.root)
        self.user_management_frame.pack(fill="x")

        # Create button for adding users
        self.add_user_button = tk.Button(self.user_management_frame, text="Add User", command=self.add_user)
        self.add_user_button.pack(side="left")

        # Create button for removing users
        self.remove_user_button = tk.Button(self.user_management_frame, text="Remove User", command=self.remove_user)
        self.remove_user_button.pack(side="left")

        # Create frame for page management
        self.page_management_frame = tk.Frame(self.root)
        self.page_management_frame.pack(fill="x")

        # Create button for adding pages
        self.add_page_button = tk.Button(self.page_management_frame, text="Add Page", command=self.add_page)
        self.add_page_button.pack(side="left")

        # Create button for removing pages
        self.remove_page_button = tk.Button(self.page_management_frame, text="Remove Page", command=self.remove_page)
        self.remove_page_button.pack(side="left")

        # Create frame for saving and loading
        self.save_load_frame = tk.Frame(self.root)
        self.save_load_frame.pack(fill="x")

        # Create button for saving
        self.save_button = tk.Button(self.save_load_frame, text="Save", command=self.save)
        self.save_button.pack(side="left")

        # Create button for loading
        self.load_button = tk.Button(self.save_load_frame, text="Load", command=self.load)
        self.load_button.pack(side="left")

        # Create thread for auto-saving
        self.auto_save_thread = threading.Thread(target=self.auto_save)
        self.auto_save_thread.start()

    def set_brush(self):
        self.current_tool = "brush"

    def set_pen(self):
        self.current_tool = "pen"

    def set_marker(self):
        self.current_tool = "marker"

    def set_color(self):
        self.current_color = colorchooser.askcolor()[1]

    def set_size(self):
        self.current_size = int(self.size_button['text'].split(" ")[1])
        self.size_button['text'] = "Size " + str(self.current_size)

    def add_comment(self):
        comment = self.comments_text.get("1.0", "end-1c")
        self.comments[comment] = self.current_page
        self.comments_text.delete("1.0", "end")

    def add_user(self):
        user_name = input("Enter user name: ")
        self.users[user_name] = "editor"

    def remove_user(self):
        user_name = input("Enter user name: ")
        if user_name in self.users:
            del self.users[user_name]

    def add_page(self):
        page_name = input("Enter page name: ")
        self.pages[page_name] = []
        self.current_page = page_name

    def remove_page(self):
        page_name = input("Enter page name: ")
        if page_name in self.pages:
            del self.pages[page_name]

    def save(self):
        with open("notebook.json", "w") as f:
            json.dump({"users": self.users, "pages": self.pages, "comments": self.comments}, f)

    def load(self):
        if os.path.exists("notebook.json"):
            with open("notebook.json", "r") as f:
                data = json.load(f)
                self.users = data["users"]
                self.pages = data["pages"]
                self.comments = data["comments"]

    def auto_save(self):
        while True:
            self.save()
            time.sleep(60)

if __name__ == "__main__":
    root = tk.Tk()
    app = NotebookCollabSketch(root)
    root.mainloop()