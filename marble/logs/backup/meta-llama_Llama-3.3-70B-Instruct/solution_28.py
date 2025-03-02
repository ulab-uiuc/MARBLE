# solution.py
from PIL import Image, ImageEnhance, ImageFilter
import os

class Layer:
    """Represents an image layer."""
    def __init__(self, image_path, name):
        # Initialize the layer with an image path and a name.
        self.image = Image.open(image_path)
        self.name = name
        self.brightness = 1.0
        self.contrast = 1.0
        self.transparency = 1.0
        self.position = (0, 0)
        self.size = (self.image.width, self.image.height)

    def apply_brightness(self, value):
        # Apply brightness adjustment to the layer.
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(value)
        self.brightness = value

    def apply_contrast(self, value):
        # Apply contrast adjustment to the layer.
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(value)
        self.contrast = value

    def apply_blur(self, radius):
        # Apply blur effect to the layer.
        self.image = self.image.filter(ImageFilter.GaussianBlur(radius))

    def apply_sharpen(self, factor):
        # Apply sharpen effect to the layer.
        enhancer = ImageEnhance.Sharpness(self.image)
        self.image = enhancer.enhance(factor)

    def resize(self, size):
        # Resize the layer.
        self.image = self.image.resize(size)
        self.size = size

    def move(self, position):
        # Move the layer to a new position.
        self.position = position


class ImageCanvasComposer:
    """Represents the image canvas composer application."""
    def __init__(self):
        # Initialize the application with an empty list of layers.
        self.layers = []

    def add_layer(self, image_path, name):
        # Add a new layer to the application.
        layer = Layer(image_path, name)
        self.layers.append(layer)

    def delete_layer(self, name):
        # Delete a layer by its name.
        self.layers = [layer for layer in self.layers if layer.name != name]

    def reorder_layers(self, new_order):
        # Reorder the layers based on a new order.
        self.layers = [self.layers[i] for i in new_order]

    def apply_effect(self, name, effect, *args):
        # Apply an effect to a layer.
        for layer in self.layers:
            if layer.name == name:
                if effect == "brightness":
                    layer.apply_brightness(*args)
                elif effect == "contrast":
                    layer.apply_contrast(*args)
                elif effect == "blur":
                    layer.apply_blur(*args)
                elif effect == "sharpen":
                    layer.apply_sharpen(*args)

    def blend_layers(self):
        # Blend all layers into a single image.
        composite = Image.new("RGBA", (max(layer.size[0] for layer in self.layers), max(layer.size[1] for layer in self.layers)))
        for layer in self.layers:
            composite.paste(layer.image, layer.position, layer.image.convert("RGBA"))
        return composite

    def export_image(self, image, filename):def save_project(self, filename):
    with open(filename, "w") as f:
        for layer in self.layers:
            f.write(f"{layer.name},{layer.image.filename},{layer.brightness},{layer.contrast},{layer.transparency},{layer.position[0]},{layer.position[1]},{layer.size[0]},{layer.size[1]}\n")    def load_project(self, filename):
        # Load a project from a file.
        self.layers = []
        with open(filename, "r") as f:
            for line in f.readlines():
                name, image_path, brightness, contrast, transparency, position_x, position_y, size_x, size_y = line.strip().split(",")
                layer = Layer(image_path, name)
                layer.brightness = float(brightness)
                layer.contrast = float(contrast)
                layer.transparency = float(transparency)
                layer.position = (int(position_x), int(position_y))
                layer.size = (int(size_x), int(size_y))
                self.layers.append(layer)


def main():
    # Create an instance of the ImageCanvasComposer application.
    composer = ImageCanvasComposer()

    # Add some layers to the application.
    composer.add_layer("image1.jpg", "Layer 1")
    composer.add_layer("image2.jpg", "Layer 2")

    # Apply some effects to the layers.
    composer.apply_effect("Layer 1", "brightness", 1.5)
    composer.apply_effect("Layer 2", "contrast", 2.0)

    # Blend the layers into a single image.
    composite = composer.blend_layers()

    # Export the final composite image to a file.
    composer.export_image(composite, "output.png")

    # Save the project to a file.
    composer.save_project("project.txt")

    # Load the project from a file.
    composer.load_project("project.txt")


if __name__ == "__main__":
    main()