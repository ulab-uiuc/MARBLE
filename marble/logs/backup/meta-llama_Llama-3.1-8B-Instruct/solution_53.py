# photo_collab_editor.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import PIL.Image, PIL.ImageTk
import io
import threading
import socket
import pickle

class PhotoCollabEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("PhotoCollabEditor")
        self.root.geometry("800x600")
        self.image_path = None
        self.image = None
        self.photo = None
        self.current_user = None
        self.users = {}
        self.history = []
        self.current_version = 0

        # Create main frames
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(fill="x")
        self.middle_frame = tk.Frame(self.root)
        self.middle_frame.pack(fill="both", expand=True)
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(fill="x")

        # Create top frame widgets
        self.open_button = tk.Button(self.top_frame, text="Open Image", command=self.open_image)
        self.open_button.pack(side="left")
        self.save_button = tk.Button(self.top_frame, text="Save Image", command=self.save_image)
        self.save_button.pack(side="left")
        self.comment_button = tk.Button(self.top_frame, text="Leave Comment", command=self.leave_comment)
        self.comment_button.pack(side="left")

        # Create middle frame widgets
        self.image_label = tk.Label(self.middle_frame)
        self.image_label.pack(fill="both", expand=True)
        self.tools_frame = tk.Frame(self.middle_frame)
        self.tools_frame.pack(fill="x")
        self.brightness_slider = tk.Scale(self.tools_frame, from_=0, to=100, orient="horizontal", label="Brightness")
        self.brightness_slider.pack(side="left")
        self.contrast_slider = tk.Scale(self.tools_frame, from_=0, to=100, orient="horizontal", label="Contrast")
        self.contrast_slider.pack(side="left")
        self.filter_button = tk.Button(self.tools_frame, text="Apply Filter", command=self.apply_filter)
        self.filter_button.pack(side="left")
        self.frame_button = tk.Button(self.tools_frame, text="Add Frame", command=self.add_frame)
        self.frame_button.pack(side="left")

        # Create bottom frame widgets
        self.comment_text = tk.Text(self.bottom_frame)
        self.comment_text.pack(fill="both", expand=True)
        self.comment_label = tk.Label(self.bottom_frame, text="Comments:")
        self.comment_label.pack(side="left")
        self.user_label = tk.Label(self.bottom_frame, text="Current User:")
        self.user_label.pack(side="left")
        self.user_entry = tk.Entry(self.bottom_frame)
        self.user_entry.pack(side="left")
        self.join_button = tk.Button(self.bottom_frame, text="Join", command=self.join)
        self.join_button.pack(side="left")

        # Create socket for real-time collaboration
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("localhost", 12345))
        self.server_socket.listen(5)
        self.client_socket, self.client_address = self.server_socket.accept()
        self.receive_thread = threading.Thread(target=self.receive_data)
        self.receive_thread.start()

    def open_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", ".jpg .jpeg .png")])
        if self.image_path:
            self.image = PIL.Image.open(self.image_path)
            self.photo = PIL.ImageTk.PhotoImage(self.image)
            self.image_label.config(image=self.photo)
            self.image_label.image = self.photo

    def save_image(self):
        if self.image_path:
            self.image.save(self.image_path)

    def leave_comment(self):
        comment = self.comment_text.get("1.0", "end-1c")
        self.history.append((self.current_user, comment))
        self.current_version += 1
        self.comment_text.delete("1.0", "end")
        self.send_data((self.current_user, comment))

    def apply_filter(self):
        filter_name = filedialog.askopenfilename(filetypes=[("Filter Files", ".filter")])
        if filter_name:
            with open(filter_name, "rb") as f:
                filter_data = pickle.load(f)
            self.image = PIL.Image.open(self.image_path)
            self.image = self.image.filter(filter_data)
            self.photo = PIL.ImageTk.PhotoImage(self.image)
            self.image_label.config(image=self.photo)
            self.image_label.image = self.photo

    def add_frame(self):
        frame_name = filedialog.askopenfilename(filetypes=[("Frame Files", ".frame")])
        if frame_name:
            with open(frame_name, "rb") as f:
                frame_data = pickle.load(f)
            self.image = PIL.Image.open(self.image_path)
            self.image = self.image.convert("RGB")
            self.image.paste(frame_data, (0, 0))
            self.photo = PIL.ImageTk.PhotoImage(self.image)
            self.image_label.config(image=self.photo)
            self.image_label.image = self.photo

    def join(self):
        self.current_user = self.user_entry.get()
        self.users[self.current_user] = self.client_socket
        self.send_data(("join", self.current_user))

    def receive_data(self):
        while True:
            data = self.client_socket.recv(1024)
            if data:
                user, comment = pickle.loads(data)
                self.history.append((user, comment))
                self.current_version += 1
                self.comment_text.insert("end", f"{user}: {comment}\n")
                self.comment_text.see("end")

    def send_data(self, data):
        self.client_socket.send(pickle.dumps(data))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoCollabEditor(root)
    app.run()