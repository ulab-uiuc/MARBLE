def reorder_layers(self, names):
        # Create a dictionary to store the layers
        layers_dict = {layer.name: layer for layer in self.layers}
        # Reorder the layers based on the names list
        self.layers = [layers_dict[name] for name in names if name in layers_dict]# solution.py
from PIL import Image, ImageEnhance, ImageFilter
import os

class Layer:
    """Represents an image layer."""
    def __init__(self, image, name):
        # Initialize the layer with an image and a name.
        self.image = image
        self.name = name

    def apply_effect(self, effect):
        # Apply a graphical effect to the layer.
        if effect == "brightness":
            enhancer = ImageEnhance.Brightness(self.image)
            self.image = enhancer.enhance(1.5)
        elif effect == "contrast":
            enhancer = ImageEnhance.Contrast(self.image)
            self.image = enhancer.enhance(1.5)
        elif effect == "blur":
            self.image = self.image.filter(ImageFilter.GaussianBlur(radius=2))
        elif effect == "sharpen":
            enhancer = ImageEnhance.Sharpness(self.image)
            self.image = enhancer.enhance(1.5)

class ImageCanvasComposer:
    """Represents the image canvas composer."""
    def __init__(self):
        # Initialize the composer with an empty list of layers.
        self.layers = []

    def add_layer(self, image, name):
        # Add a new layer to the composer.
        layer = Layer(image, name)
        self.layers.append(layer)

    def delete_layer(self, name):
        # Delete a layer from the composer.
        for layer in self.layers:
            if layer.name == name:
                self.layers.remove(layer)
                break

    def reorder_layers(self, names):
self.layers = [layer for layer in self.layers if layer.name in names]
        self.layers = [next(layer for layer in self.layers if layer.name == name) for name in names]
    def apply_effect(self, effect, layer_name=None):
        # Apply a graphical effect to a layer or the entire canvas.
        if layer_name:
            for layer in self.layers:
                if layer.name == layer_name:
                    layer.apply_effect(effect)
                    break
        else:
            for layer in self.layers:
                layer.apply_effect(effect)

    def blend_layers(self):
        # Blend the layers in the composer.
        # For simplicity, this example uses a simple overlay blend mode.
        # In a real application, you would want to implement more advanced blend modes.
        result = self.layers[0].image
        for layer in self.layers[1:]:
            result = Image.blend(result, layer.image, 0.5)
        return result

    def export_image(self, image, filename):
        # Export the final composite image.
        image.save(filename)

    def save_project(self, filename):
        # Save the project file.
        with open(filename, "w") as f:
            for layer in self.layers:
                f.write(f"{layer.name}:{os.path.abspath(layer.image.filename)}\n")

def main():
    # Create a new image canvas composer.
    composer = ImageCanvasComposer()

    # Load some images.
    image1 = Image.open("image1.jpg")
    image2 = Image.open("image2.jpg")

    # Add the images as layers to the composer.
    composer.add_layer(image1, "layer1")
    composer.add_layer(image2, "layer2")

    # Apply some effects to the layers.
    composer.apply_effect("brightness", "layer1")
    composer.apply_effect("contrast", "layer2")

    # Blend the layers.
    blended_image = composer.blend_layers()

    # Export the final composite image.
    composer.export_image(blended_image, "output.png")

    # Save the project file.
    composer.save_project("project.txt")

if __name__ == "__main__":
    main()