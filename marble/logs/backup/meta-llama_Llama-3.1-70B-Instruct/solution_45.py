# notebook_collab_sketch.py

import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
import json
import os

class NotebookCollabSketch:
    def __init__(self, root):
        self.root = root
        self.root.title("Notebook Collab Sketch")
        self.root.geometry("800x600")

        # Initialize variables
        self.users = {}
        self.current_user = None
        self.current_page = None
        self.pages = {}
        self.tools = ["brush", "pen", "marker"]
        self.colors = ["black", "red", "blue", "green"]
        self.sizes = [1, 2, 3, 4, 5]
        self.comments = {}

        # Create notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Create frames for each page
        self.frames = {}
        for i in range(10):
            frame = tk.Frame(self.notebook)
            self.notebook.add(frame, text=f"Page {i+1}")
            self.frames[f"Page {i+1}"] = frame

        # Create drawing canvas
        self.canvases = {}
        for page, frame in self.frames.items():
            canvas = tk.Canvas(frame, width=800, height=600)
            canvas.pack(fill="both", expand=True)
            self.canvases[page] = canvas

        # Create toolbar
        self.toolbar = tk.Frame(self.root)
        self.toolbar.pack(fill="x")

        # Create tool buttons
        self.tool_buttons = {}
        for tool in self.tools:
            button = tk.Button(self.toolbar, text=tool, command=lambda tool=tool: self.select_tool(tool))
            button.pack(side="left")
            self.tool_buttons[tool] = button

        # Create color buttons
        self.color_buttons = {}
        for color in self.colors:
            button = tk.Button(self.toolbar, bg=color, width=5, command=lambda color=color: self.select_color(color))
            button.pack(side="left")
            self.color_buttons[color] = button

        # Create size buttons
        self.size_buttons = {}
        for size in self.sizes:
            button = tk.Button(self.toolbar, text=str(size), command=lambda size=size: self.select_size(size))
            button.pack(side="left")
            self.size_buttons[size] = button

        # Create comment button
        self.comment_button = tk.Button(self.toolbar, text="Comment", command=self.add_comment)
        self.comment_button.pack(side="left")

        # Create save button
        self.save_button = tk.Button(self.toolbar, text="Save", command=self.save_notebook)
        self.save_button.pack(side="left")

        # Create load button
        self.load_button = tk.Button(self.toolbar, text="Load", command=self.load_notebook)
        self.load_button.pack(side="left")

        # Create user management buttons
        self.user_button = tk.Button(self.toolbar, text="Add User", command=self.add_user)
        self.user_button.pack(side="left")

        self.login_button = tk.Button(self.toolbar, text="Login", command=self.login_user)
        self.login_button.pack(side="left")

        # Initialize current page and tool
        self.current_page = "Page 1"
        self.current_tool = "brush"
        self.current_color = "black"
        self.current_size = 1

        # Bind events
        for canvas in self.canvases.values():
            canvas.bind("<B1-Motion>", self.draw)
            canvas.bind("<Button-1>", self.start_drawing)

    def select_tool(self, tool):
        self.current_tool = tool

    def select_color(self, color):
        self.current_color = color

    def select_size(self, size):
        self.current_size = size

    def start_drawing(self, event):
        self.last_x, self.last_y = event.x, event.y

    def draw(self, event):
        canvas = self.canvases[self.current_page]
        canvas.create_line(self.last_x, self.last_y, event.x, event.y, 
                           width=self.current_size, fill=self.current_color, 
                           capstyle="round", smooth=True, splinesteps=36)
        self.last_x, self.last_y = event.x, event.y

    def add_comment(self):
        comment = tk.simpledialog.askstring("Comment", "Enter your comment")
        if comment:
            self.comments[self.current_page] = comment
            messagebox.showinfo("Comment Added", "Comment added successfully")

    def save_notebook(self):
        data = {
            "pages": self.pages,
            "comments": self.comments,
            "users": self.users
        }
        with open("notebook.json", "w") as f:
            json.dump(data, f)
        messagebox.showinfo("Notebook Saved", "Notebook saved successfully")

    def load_notebook(self):
        if os.path.exists("notebook.json"):
            with open("notebook.json", "r") as f:
                data = json.load(f)
            self.pages = data["pages"]
            self.comments = data["comments"]
            self.users = data["users"]
            messagebox.showinfo("Notebook Loaded", "Notebook loaded successfully")
        else:
            messagebox.showerror("Notebook Not Found", "Notebook not found")

    def add_user(self):
        username = tk.simpledialog.askstring("Add User", "Enter username")
        if username:
            self.users[username] = {"role": "editor"}
            messagebox.showinfo("User Added", "User added successfully")

    def login_user(self):
        username = tk.simpledialog.askstring("Login", "Enter username")
        if username in self.users:
            self.current_user = username
            messagebox.showinfo("Login Successful", "Login successful")
        else:
            messagebox.showerror("Invalid Username", "Invalid username")

if __name__ == "__main__":
    root = tk.Tk()
    app = NotebookCollabSketch(root)
    root.mainloop()