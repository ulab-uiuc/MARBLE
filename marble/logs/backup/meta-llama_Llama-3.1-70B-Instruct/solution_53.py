# photo_collab_editor.py

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import threading
import time
import uuid

class PhotoCollabEditor:
    def __init__(self, root):
        self.root = root
        self.image_path = None
        self.image = None
        self.photo = None
        self.editing_tools = []
        self.comments = {}
        self.version_control = []
        self.current_version = 0

        # Create main frames
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.image_frame = tk.Frame(self.main_frame)
        self.image_frame.pack(side="left", fill="both", expand=True)

        self.tools_frame = tk.Frame(self.main_frame)
        self.tools_frame.pack(side="right", fill="y")

        # Create image label
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(fill="both", expand=True)

        # Create editing tools
        self.create_editing_tools()

        # Create comment section
        self.comment_section = tk.Frame(self.tools_frame)
        self.comment_section.pack(fill="x")

        self.comment_label = tk.Label(self.comment_section, text="Comments:")
        self.comment_label.pack(side="left")

        self.comment_entry = tk.Entry(self.comment_section)
        self.comment_entry.pack(side="left", fill="x", expand=True)

        self.comment_button = tk.Button(self.comment_section, text="Post", command=self.post_comment)
        self.comment_button.pack(side="left")

        # Create version control
        self.version_control_button = tk.Button(self.tools_frame, text="Version Control", command=self.version_control_window)
        self.version_control_button.pack(fill="x")

    def create_editing_tools(self):
        # Create brightness tool
        self.brightness_tool = tk.Frame(self.tools_frame)
        self.brightness_tool.pack(fill="x")

        self.brightness_label = tk.Label(self.brightness_tool, text="Brightness:")
        self.brightness_label.pack(side="left")

        self.brightness_scale = tk.Scale(self.brightness_tool, from_=-100, to=100, orient="horizontal", command=self.adjust_brightness)
        self.brightness_scale.pack(side="left", fill="x", expand=True)

        self.editing_tools.append(self.brightness_tool)

        # Create contrast tool
        self.contrast_tool = tk.Frame(self.tools_frame)
        self.contrast_tool.pack(fill="x")

        self.contrast_label = tk.Label(self.contrast_tool, text="Contrast:")
        self.contrast_label.pack(side="left")

        self.contrast_scale = tk.Scale(self.contrast_tool, from_=-100, to=100, orient="horizontal", command=self.adjust_contrast)
        self.contrast_scale.pack(side="left", fill="x", expand=True)

        self.editing_tools.append(self.contrast_tool)

        # Create filter tool
        self.filter_tool = tk.Frame(self.tools_frame)
        self.filter_tool.pack(fill="x")

        self.filter_label = tk.Label(self.filter_tool, text="Filter:")
        self.filter_label.pack(side="left")

        self.filter_option = tk.StringVar(self.filter_tool)
        self.filter_option.set("None")

        self.filter_menu = tk.OptionMenu(self.filter_tool, self.filter_option, "None", "Blur", "Contour", "Detail", "Edge Enhance", "Emboss", "Find Edges", "Sharpen", "Smooth", "Smooth More")
        self.filter_menu.pack(side="left", fill="x", expand=True)

        self.filter_button = tk.Button(self.filter_tool, text="Apply", command=self.apply_filter)
        self.filter_button.pack(side="left")

        self.editing_tools.append(self.filter_tool)

        # Create frame tool
        self.frame_tool = tk.Frame(self.tools_frame)
        self.frame_tool.pack(fill="x")

        self.frame_label = tk.Label(self.frame_tool, text="Frame:")
        self.frame_label.pack(side="left")

        self.frame_option = tk.StringVar(self.frame_tool)
        self.frame_option.set("None")

        self.frame_menu = tk.OptionMenu(self.frame_tool, self.frame_option, "None", "Simple Border", "Rounded Border")
        self.frame_menu.pack(side="left", fill="x", expand=True)

        self.frame_button = tk.Button(self.frame_tool, text="Apply", command=self.apply_frame)
        self.frame_button.pack(side="left")

        self.editing_tools.append(self.frame_tool)

    def open_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", ".jpg .jpeg .png .bmp")])
        if self.image_path:
            self.image = Image.open(self.image_path)
            self.photo = ImageTk.PhotoImage(self.image)
            self.image_label.config(image=self.photo)
            self.image_label.image = self.photo

    def adjust_brightness(self, value):
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(float(value) / 100 + 1)
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label.config(image=self.photo)
        self.image_label.image = self.photo

    def adjust_contrast(self, value):
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(float(value) / 100 + 1)
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label.config(image=self.photo)
        self.image_label.image = self.photo

    def apply_filter(self):
        filter_name = self.filter_option.get()
        if filter_name != "None":
            self.image = self.image.filter(getattr(ImageFilter, filter_name))
            self.photo = ImageTk.PhotoImage(self.image)
            self.image_label.config(image=self.photo)
            self.image_label.image = self.photo

    def apply_frame(self):
        frame_name = self.frame_option.get()
        if frame_name != "None":
            if frame_name == "Simple Border":
                self.image = self.image.crop((5, 5, self.image.width - 5, self.image.height - 5))
            elif frame_name == "Rounded Border":
                self.image = self.image.crop((10, 10, self.image.width - 10, self.image.height - 10))
            self.photo = ImageTk.PhotoImage(self.image)
            self.image_label.config(image=self.photo)
            self.image_label.image = self.photo

    def post_comment(self):
        comment = self.comment_entry.get()
        if comment:
            comment_id = str(uuid.uuid4())
            self.comments[comment_id] = comment
            self.comment_entry.delete(0, "end")
            self.update_comments()

    def update_comments(self):
        comment_text = ""
        for comment_id, comment in self.comments.items():
            comment_text += f"{comment}\n"
        self.comment_label.config(text=comment_text)

    def version_control_window(self):
        self.version_control_window = tk.Toplevel(self.root)
        self.version_control_window.title("Version Control")

        self.version_control_listbox = tk.Listbox(self.version_control_window)
        self.version_control_listbox.pack(fill="both", expand=True)

        for i in range(len(self.version_control)):
            self.version_control_listbox.insert("end", f"Version {i+1}")

        self.revert_button = tk.Button(self.version_control_window, text="Revert", command=self.revert_version)
        self.revert_button.pack(fill="x")

    def revert_version(self):
        selected_index = self.version_control_listbox.curselection()
        if selected_index:
            self.image = self.version_control[selected_index[0]]
            self.photo = ImageTk.PhotoImage(self.image)
            self.image_label.config(image=self.photo)
            self.image_label.image = self.photo

def main():
    root = tk.Tk()
    root.title("Photo Collab Editor")

    editor = PhotoCollabEditor(root)

    open_button = tk.Button(root, text="Open Image", command=editor.open_image)
    open_button.pack(fill="x")

    root.mainloop()

if __name__ == "__main__":
    main()