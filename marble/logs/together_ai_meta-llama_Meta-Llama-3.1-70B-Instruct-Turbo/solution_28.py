# image_canvas_composer.py

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import os

class Layer:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.photo = ImageTk.PhotoImage(self.image)
        self.transparency = 1.0
        self.x = 0
        self.y = 0

    def apply_effect(self, effect):
        if effect == 'brightness':
            enhancer = ImageEnhance.Brightness(self.image)
            self.image = enhancer.enhance(1.5)
        elif effect == 'contrast':
            enhancer = ImageEnhance.Contrast(self.image)
            self.image = enhancer.enhance(1.5)
        elif effect == 'blur':
            self.image = self.image.filter(ImageFilter.GaussianBlur(radius=2))
        elif effect == 'sharpen':
            enhancer = ImageEnhance.Sharpness(self.image)
            self.image = enhancer.enhance(1.5)
        self.photo = ImageTk.PhotoImage(self.image)

    def set_transparency(self, transparency):
        self.transparency = transparency

    def set_position(self, x, y):
        self.x = x
        self.y = y


class ImageCanvasComposer:
    def __init__(self, root):
        self.root = root
        self.layers = []
        self.current_layer = None
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()

        self.layer_frame = tk.Frame(self.root)
        self.layer_frame.pack()

        self.add_layer_button = tk.Button(self.layer_frame, text='Add Layer', command=self.add_layer)
        self.add_layer_button.pack(side=tk.LEFT)

        self.delete_layer_button = tk.Button(self.layer_frame, text='Delete Layer', command=self.delete_layer)
        self.delete_layer_button.pack(side=tk.LEFT)

        self.reorder_layer_button = tk.Button(self.layer_frame, text='Reorder Layers', command=self.reorder_layers)
        self.reorder_layer_button.pack(side=tk.LEFT)

        self.effects_frame = tk.Frame(self.root)
        self.effects_frame.pack()

        self.brightness_button = tk.Button(self.effects_frame, text='Brightness', command=lambda: self.apply_effect('brightness'))
        self.brightness_button.pack(side=tk.LEFT)

        self.contrast_button = tk.Button(self.effects_frame, text='Contrast', command=lambda: self.apply_effect('contrast'))
        self.contrast_button.pack(side=tk.LEFT)

        self.blur_button = tk.Button(self.effects_frame, text='Blur', command=lambda: self.apply_effect('blur'))
        self.blur_button.pack(side=tk.LEFT)

        self.sharpen_button = tk.Button(self.effects_frame, text='Sharpen', command=lambda: self.apply_effect('sharpen'))
        self.sharpen_button.pack(side=tk.LEFT)

        self.blend_frame = tk.Frame(self.root)
        self.blend_frame.pack()

        self.transparency_label = tk.Label(self.blend_frame, text='Transparency:')
        self.transparency_label.pack(side=tk.LEFT)

        self.transparency_slider = tk.Scale(self.blend_frame, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, command=self.set_transparency)
        self.transparency_slider.pack(side=tk.LEFT)

        self.position_label = tk.Label(self.blend_frame, text='Position:')
        self.position_label.pack(side=tk.LEFT)

        self.x_entry = tk.Entry(self.blend_frame)
        self.x_entry.pack(side=tk.LEFT)

        self.y_entry = tk.Entry(self.blend_frame)
        self.y_entry.pack(side=tk.LEFT)

        self.set_position_button = tk.Button(self.blend_frame, text='Set Position', command=self.set_position)
        self.set_position_button.pack(side=tk.LEFT)

        self.export_frame = tk.Frame(self.root)
        self.export_frame.pack()

        self.export_button = tk.Button(self.export_frame, text='Export', command=self.export)
        self.export_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(self.export_frame, text='Save', command=self.save)
        self.save_button.pack(side=tk.LEFT)

    def add_layer(self):
        image_path = filedialog.askopenfilename()
        if image_path:
            layer = Layer(image_path)
            self.layers.append(layer)
            self.current_layer = layer
            self.canvas.create_image(0, 0, image=layer.photo, anchor='nw')

    def delete_layer(self):
        if self.current_layer:
            self.layers.remove(self.current_layer)
            self.canvas.delete('all')
            for layer in self.layers:
                self.canvas.create_image(0, 0, image=layer.photo, anchor='nw')
            self.current_layer = None

    def reorder_layers(self):
        if self.layers:
            self.layers.reverse()
            self.canvas.delete('all')
            for layer in self.layers:
                self.canvas.create_image(0, 0, image=layer.photo, anchor='nw')

    def apply_effect(self, effect):
        if self.current_layer:
            self.current_layer.apply_effect(effect)
            self.canvas.delete('all')
            for layer in self.layers:
                self.canvas.create_image(0, 0, image=layer.photo, anchor='nw')

    def set_transparency(self, transparency):
        if self.current_layer:
            self.current_layer.set_transparency(float(transparency))

    def set_position(self):
        if self.current_layer:
            x = int(self.x_entry.get())
            y = int(self.y_entry.get())
            self.current_layer.set_position(x, y)
            self.canvas.delete('all')
            for layer in self.layers:
                self.canvas.create_image(layer.x, layer.y, image=layer.photo, anchor='nw')

    def export(self):
        if self.layers:
            composite_image = Image.new('RGB', (800, 600))
            for layer in self.layers:
                composite_image.paste(layer.image, (layer.x, layer.y), layer.image)
            composite_image.save('composite_image.png')

    def save(self):
        if self.layers:
            with open('project.txt', 'w') as f:
                for layer in self.layers:
                    f.write(f'{layer.image_path},{layer.transparency},{layer.x},{layer.y}\n')


if __name__ == '__main__':
    root = tk.Tk()
    composer = ImageCanvasComposer(root)
    root.mainloop()