# image_canvas_composer.py

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import os

class Layer:
    """Represents an image layer."""
    def __init__(self, image):
        self.image = image
        self.transparency = 1.0
        self.x = 0
        self.y = 0

class ImageCanvasComposer:
    """A graphics application for creating and managing multiple canvas layers."""
    def __init__(self, root):
        self.root = root
        self.layers = []
        self.current_layer = None
        self.image = None
        self.photo = None
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()
        self.create_menu()

    def create_menu(self):
        """Creates the application menu."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New Layer", command=self.new_layer)
        filemenu.add_command(label="Load Layer", command=self.load_layer)
        filemenu.add_command(label="Delete Layer", command=self.delete_layer)
        filemenu.add_command(label="Export", command=self.export)
        filemenu.add_command(label="Save Project", command=self.save_project)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        editmenu = tk.Menu(menubar)
        menubar.add_cascade(label="Edit", menu=editmenu)
        editmenu.add_command(label="Brightness/Contrast", command=self.brightness_contrast)
        editmenu.add_command(label="Color Correction", command=self.color_correction)
        editmenu.add_command(label="Blur", command=self.blur)
        editmenu.add_command(label="Sharpen", command=self.sharpen)

    def new_layer(self):
        """Creates a new layer."""
        self.layers.append(Layer(None))
        self.current_layer = self.layers[-1]
        self.display_layer()

    def load_layer(self):
        """Loads an image layer from a file."""
        filename = filedialog.askopenfilename(filetypes=[("Image Files", ".jpg .jpeg .png .bmp")])
        if filename:
            image = Image.open(filename)
            self.layers.append(Layer(image))
            self.current_layer = self.layers[-1]
            self.display_layer()

    def delete_layer(self):
        """Deletes the current layer."""
        if self.current_layer:
            self.layers.remove(self.current_layer)
            self.current_layer = None
            self.display_layer()

    def display_layer(self):
        """Displays the current layer on the canvas."""
        if self.current_layer and self.current_layer.image:
            self.photo = ImageTk.PhotoImage(self.current_layer.image)
            self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
        else:
            self.canvas.delete("all")

    def export(self):
        """Exports the composite image."""
        if self.layers:
            composite = Image.new("RGB", (800, 600))
            for layer in self.layers:
                if layer.image:
                    composite.paste(layer.image, (layer.x, layer.y), layer.image)
            filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", ".png")])
            if filename:
                composite.save(filename)

    def save_project(self):
        """Saves the project."""
        filename = filedialog.asksaveasfilename(defaultextension=".icp", filetypes=[("Image Canvas Project", ".icp")])
        if filename:
            with open(filename, "w") as f:
                for layer in self.layers:
                    if layer.image:
                        f.write(f"image:{layer.image.filename}\n")
                        f.write(f"transparency:{layer.transparency}\n")
                        f.write(f"x:{layer.x}\n")
                        f.write(f"y:{layer.y}\n")
                    else:
                        f.write("image:None\n")

    def brightness_contrast(self):
        """Applies brightness and contrast adjustments to the current layer."""
        if self.current_layer and self.current_layer.image:
            enhancer = ImageEnhance.Brightness(self.current_layer.image)
            self.current_layer.image = enhancer.enhance(1.5)
            enhancer = ImageEnhance.Contrast(self.current_layer.image)
            self.current_layer.image = enhancer.enhance(1.5)
            self.display_layer()

    def color_correction(self):
        """Applies color correction to the current layer."""
        if self.current_layer and self.current_layer.image:
            enhancer = ImageEnhance.Color(self.current_layer.image)
            self.current_layer.image = enhancer.enhance(1.5)
            self.display_layer()

    def blur(self):
        """Applies a blur effect to the current layer."""
        if self.current_layer and self.current_layer.image:
            self.current_layer.image = self.current_layer.image.filter(ImageFilter.GaussianBlur(radius=5))
            self.display_layer()

    def sharpen(self):
        """Applies a sharpen effect to the current layer."""
        if self.current_layer and self.current_layer.image:
            enhancer = ImageEnhance.Sharpness(self.current_layer.image)
            self.current_layer.image = enhancer.enhance(1.5)
            self.display_layer()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCanvasComposer(root)
    root.mainloop()