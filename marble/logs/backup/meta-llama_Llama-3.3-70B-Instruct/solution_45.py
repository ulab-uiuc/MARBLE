# solution.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
from datetime import datetime

# Notebook class
class Notebook:
    def __init__(self):
        self.pages = {}
        self.current_page = None
        self.users = {}
        self.history = {}

    def add_page(self, page_name):
        # Create a new page and add it to the notebook
        self.pages[page_name] = Page(page_name)
        self.current_page = page_name

    def switch_page(self, page_name):
        # Switch to a different page in the notebook
        if page_name in self.pages:
            self.current_page = page_name
        else:
            print("Page not found")

    def add_user(self, user_name, role):
        # Add a new user to the notebook
        self.users[user_name] = User(user_name, role)

    def save_changes(self):
        # Save changes to the current page
        if self.current_page:
            self.pages[self.current_page].save_changes()
            self.history[self.current_page] = self.pages[self.current_page].get_history()

    def get_history(self, page_name):
        # Get the history of changes for a page
        return self.history.get(page_name, [])

# Page class
class Page:
    def __init__(self, page_name):
        self.page_name = page_name
        self.drawings = []
        self.comments = []
        self.history = []

    def add_drawing(self, drawing):
        # Add a new drawing to the page
        self.drawings.append(drawing)
        self.history.append({"action": "add_drawing", "drawing": drawing})

    def add_comment(self, comment):
        # Add a new comment to the page
        self.comments.append(comment)
        self.history.append({"action": "add_comment", "comment": comment})

    def save_changes(self):
        # Save changes to the page
        self.history.append({"action": "save_changes", "timestamp": datetime.now()})

    def get_history(self):
        # Get the history of changes for the page
        return self.history

# User class
class User:
    def __init__(self, user_name, role):
        self.user_name = user_name
        self.role = role

    def get_permissions(self):
        # Get the permissions for the user based on their role
        if self.role == "admin":
            return ["view", "edit", "delete"]
        elif self.role == "editor":
            return ["view", "edit"]
        else:
            return ["view"]

# Drawing class
class Drawing:
    def __init__(self, tool, size, color):
        self.tool = tool
        self.size = size
        self.color = color

    def get_drawing(self):
        # Get the drawing details
        return {"tool": self.tool, "size": self.size, "color": self.color}

# Comment class
class Comment:
    def __init__(self, text, user_name):
        self.text = text
        self.user_name = user_name

    def get_comment(self):
        # Get the comment details
        return {"text": self.text, "user_name": self.user_name}

# GUI class
class GUI:
    def __init__(self, notebook):
        self.notebook = notebook
        self.root = tk.Tk()
        self.root.title("Notebook_CollabSketch")
        self.notebook_frame = tk.Frame(self.root)
        self.notebook_frame.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Create the GUI widgets
        self.page_name_label = tk.Label(self.notebook_frame, text="Page Name:")
        self.page_name_label.pack()
        self.page_name_entry = tk.Entry(self.notebook_frame)
        self.page_name_entry.pack()
        self.add_page_button = tk.Button(self.notebook_frame, text="Add Page", command=self.add_page)
        self.add_page_button.pack()
        self.switch_page_label = tk.Label(self.notebook_frame, text="Switch Page:")
        self.switch_page_label.pack()
        self.switch_page_entry = tk.Entry(self.notebook_frame)
        self.switch_page_entry.pack()
        self.switch_page_button = tk.Button(self.notebook_frame, text="Switch Page", command=self.switch_page)
        self.switch_page_button.pack()
        self.drawing_tool_label = tk.Label(self.notebook_frame, text="Drawing Tool:")
        self.drawing_tool_label.pack()
        self.drawing_tool_var = tk.StringVar()
        self.drawing_tool_var.set("brush")
        self.drawing_tool_option = tk.OptionMenu(self.notebook_frame, self.drawing_tool_var, "brush", "pen", "marker")
        self.drawing_tool_option.pack()
        self.drawing_size_label = tk.Label(self.notebook_frame, text="Drawing Size:")
        self.drawing_size_label.pack()
        self.drawing_size_entry = tk.Entry(self.notebook_frame)
        self.drawing_size_entry.pack()
        self.drawing_color_label = tk.Label(self.notebook_frame, text="Drawing Color:")
        self.drawing_color_label.pack()
        self.drawing_color_entry = tk.Entry(self.notebook_frame)
        self.drawing_color_entry.pack()
        self.add_drawing_button = tk.Button(self.notebook_frame, text="Add Drawing", command=self.add_drawing)
        self.add_drawing_button.pack()
        self.comment_label = tk.Label(self.notebook_frame, text="Comment:")
        self.comment_label.pack()
        self.comment_entry = tk.Entry(self.notebook_frame)
        self.comment_entry.pack()
        self.add_comment_button = tk.Button(self.notebook_frame, text="Add Comment", command=self.add_comment)
        self.add_comment_button.pack()
        self.save_changes_button = tk.Button(self.notebook_frame, text="Save Changes", command=self.save_changes)
        self.save_changes_button.pack()
        self.history_button = tk.Button(self.notebook_frame, text="Get History", command=self.get_history)
        self.history_button.pack()

    def add_page(self):
        # Add a new page to the notebook
        page_name = self.page_name_entry.get()
        self.notebook.add_page(page_name)
        self.page_name_entry.delete(0, tk.END)

    def switch_page(self):
        # Switch to a different page in the notebook
        page_name = self.switch_page_entry.get()
        self.notebook.switch_page(page_name)
        self.switch_page_entry.delete(0, tk.END)

    def add_drawing(self):
        # Add a new drawing to the current page
        tool = self.drawing_tool_var.get()
        size = self.drawing_size_entry.get()
        color = self.drawing_color_entry.get()
        drawing = Drawing(tool, size, color)
        self.notebook.pages[self.notebook.current_page].add_drawing(drawing)
        self.drawing_size_entry.delete(0, tk.END)
        self.drawing_color_entry.delete(0, tk.END)

    def add_comment(self):
        # Add a new comment to the current page
        comment = self.comment_entry.get()
        user_name = "user1"  # default user name
        comment_obj = Comment(comment, user_name)
        self.notebook.pages[self.notebook.current_page].add_comment(comment_obj)
        self.comment_entry.delete(0, tk.END)

    def save_changes(self):
        # Save changes to the current page
        self.notebook.save_changes()

    def get_history(self):
        # Get the history of changes for the current page
        history = self.notebook.get_history(self.notebook.current_page)
        print(history)

    def run(self):
        # Run the GUI event loop
        self.root.mainloop()

# Create a new notebook and GUI
notebook = Notebook()
gui = GUI(notebook)
gui.run()