# solution.py

# Importing necessary libraries
import tkinter as tk
from tkinter import ttk, filedialog, colorchooser
import threading
import pickle
import os

# Defining a class for the Notebook_CollabSketch application
class Notebook_CollabSketch:
    def __init__(self, root):
        self.root = root
        self.root.title("Notebook_CollabSketch")
        self.root.geometry("800x600")
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)
        self.pages = {}
        self.current_page = None
        self.history = {}
        self.users = {}
        self.roles = {"viewer": 0, "editor": 1, "admin": 2}
        self.current_user = None
        self.current_role = None
        self.tool = "brush"
        self.size = 5
        self.color = "black"
        self.comments = {}

        # Creating a menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New Page", command=self.new_page)
        self.file_menu.add_command(label="Save", command=self.save_page)
        self.file_menu.add_command(label="Load", command=self.load_page)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Creating a toolbar
        self.toolbar = tk.Frame(self.root)
        self.toolbar.pack(fill="x")
        self.brush_button = tk.Button(self.toolbar, text="Brush", command=lambda: self.set_tool("brush"))
        self.brush_button.pack(side="left")
        self.pen_button = tk.Button(self.toolbar, text="Pen", command=lambda: self.set_tool("pen"))
        self.pen_button.pack(side="left")
        self.marker_button = tk.Button(self.toolbar, text="Marker", command=lambda: self.set_tool("marker"))
        self.marker_button.pack(side="left")
        self.size_slider = tk.Scale(self.toolbar, from_=1, to=100, orient="horizontal", command=self.set_size)
        self.size_slider.set(5)
        self.size_slider.pack(side="left")
        self.color_button = tk.Button(self.toolbar, text="Color", command=self.set_color)
        self.color_button.pack(side="left")

        # Creating a status bar
        self.status_bar = tk.Label(self.root, text="Ready")
        self.status_bar.pack(fill="x")

        # Creating a canvas for drawing
        self.canvas = tk.Canvas(self.root, width=800, height=500)
        self.canvas.pack(fill="both", expand=True)

        # Creating a text box for comments
        self.comment_box = tk.Text(self.root)
        self.comment_box.pack(fill="both", expand=True)

        # Creating a button for sending comments
        self.send_button = tk.Button(self.root, text="Send", command=self.send_comment)
        self.send_button.pack(fill="x")

    # Method for creating a new page
    def new_page(self):
        page_name = "Page " + str(len(self.pages) + 1)
        self.pages[page_name] = self.canvas
        self.notebook.add(self.canvas, text=page_name)
        self.notebook.select(self.canvas)
        self.current_page = page_name
        self.history[self.current_page] = []
        self.comments[self.current_page] = []

    # Method for saving a page
    def save_page(self):
        page_name = self.current_page
        with open(page_name + ".pickle", "wb") as f:
            pickle.dump(self.history[page_name], f)
        self.status_bar.config(text="Page saved")

    # Method for loading a page
    def load_page(self):
        page_name = self.current_page
        with open(page_name + ".pickle", "rb") as f:
            self.history[page_name] = pickle.load(f)
        self.status_bar.config(text="Page loaded")

    # Method for setting the drawing tool
    def set_tool(self, tool):
        self.tool = tool
        self.status_bar.config(text="Tool set to " + tool)

    # Method for setting the drawing size
    def set_size(self, size):
        self.size = int(size)
        self.status_bar.config(text="Size set to " + size)

    # Method for setting the drawing color
    def set_color(self):
        self.color = colorchooser.askcolor()[1]
        self.status_bar.config(text="Color set to " + self.color)

    # Method for sending comments
    def send_comment(self):
        comment = self.comment_box.get("1.0", "end-1c")
        self.comments[self.current_page].append(comment)
        self.comment_box.delete("1.0", "end")
        self.status_bar.config(text="Comment sent")

    # Method for handling user interactions
    def handle_interaction(self, event):
        if self.tool == "brush":
            self.canvas.create_line(event.x, event.y, event.x, event.y, width=self.size, fill=self.color)
        elif self.tool == "pen":
            self.canvas.create_line(event.x, event.y, event.x, event.y, width=self.size, fill=self.color, capstyle="round")
        elif self.tool == "marker":
            self.canvas.create_line(event.x, event.y, event.x, event.y, width=self.size, fill=self.color, capstyle="projecting")
        self.history[self.current_page].append(self.canvas.find_all())
        self.status_bar.config(text="Drawing saved")

    # Method for running the application
    def run(self):
        self.root.mainloop()

# Creating a main function
def main():
    root = tk.Tk()
    app = Notebook_CollabSketch(root)
    app.run()

# Running the main function
if __name__ == "__main__":
    main()