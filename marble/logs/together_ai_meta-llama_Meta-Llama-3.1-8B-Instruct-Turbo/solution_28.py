# layer.py
class Layer:
    """
    Represents a layer in the ImageCanvasComposer application.
    """

    def __init__(self, name, image):
        """
        Initializes a new layer with the given name and image.

        Args:
            name (str): The name of the layer.
            image (Image): The image associated with the layer.
        """
        self.name = name
        self.image = image

    def apply_effect(self, effect):
        """
        Applies the given effect to the layer's image.

        Args:
            effect (Effect): The effect to apply.
        """
        self.image = effect.apply(self.image)


# effect.py
from PIL import Image

class Effect:
    """
    Represents a graphical effect that can be applied to an image.
    """

    def apply(self, image):
        """
        Applies the effect to the given image.

        Args:
            image (Image): The image to apply the effect to.

        Returns:
            Image: The image with the effect applied.
        """
        raise NotImplementedError


class BrightnessEffect(Effect):
    """
    Adjusts the brightness of an image.
    """

    def __init__(self, brightness):
        """
        Initializes a new brightness effect with the given brightness.

        Args:
            brightness (int): The amount to adjust the brightness by.
        """
        self.brightness = brightness

    def apply(self, image):
        """
        Applies the brightness effect to the given image.

        Args:
            image (Image): The image to apply the effect to.

        Returns:
            Image: The image with the brightness effect applied.
        """
        pixels = image.load()
        for x in range(image.size[0]):
            for y in range(image.size[1]):
                r, g, b = pixels[x, y]
                pixels[x, y] = (r + self.brightness, g + self.brightness, b + self.brightness)
        return image


class ContrastEffect(Effect):
    """
    Adjusts the contrast of an image.
    """

    def __init__(self, contrast):
        """
        Initializes a new contrast effect with the given contrast.

        Args:
            contrast (int): The amount to adjust the contrast by.
        """
        self.contrast = contrast

    def apply(self, image):
        """
        Applies the contrast effect to the given image.

        Args:
            image (Image): The image to apply the effect to.

        Returns:
            Image: The image with the contrast effect applied.
        """
        pixels = image.load()
        for x in range(image.size[0]):
            for y in range(image.size[1]):
                r, g, b = pixels[x, y]
                pixels[x, y] = (int(r * (1 + self.contrast)), int(g * (1 + self.contrast)), int(b * (1 + self.contrast)))
        return image


# image_canvas_composer.py
from PIL import Image
from layer import Layer
from effect import Effect, BrightnessEffect, ContrastEffect

class ImageCanvasComposer:
    """
    Represents the ImageCanvasComposer application.
    """

    def __init__(self):
        """
        Initializes a new ImageCanvasComposer instance.
        """
        self.layers = []

    def add_layer(self, name, image):
        """
        Adds a new layer to the composer.

        Args:
            name (str): The name of the layer.
            image (Image): The image associated with the layer.
        """
        self.layers.append(Layer(name, image))

    def delete_layer(self, index):
        """
        Deletes the layer at the given index.

        Args:
            index (int): The index of the layer to delete.
        """
        del self.layers[index]

    def reorder_layers(self, index, new_index):
        """
        Reorders the layers by swapping the layer at the given index with the layer at the new index.

        Args:
            index (int): The index of the layer to swap.
            new_index (int): The new index of the layer.
        """
        self.layers[index], self.layers[new_index] = self.layers[new_index], self.layers[index]

    def apply_effect(self, effect):
        """
        Applies the given effect to all layers.

        Args:
            effect (Effect): The effect to apply.
        """
        for layer in self.layers:
            layer.apply_effect(effect)

    def export_image(self, filename):
        """
        Exports the final composite image to the given filename.

        Args:
            filename (str): The filename to export the image to.
        """
        composite_image = Image.new('RGB', (self.layers[0].image.size[0], self.layers[0].image.size[1]))
        for layer in self.layers:
            composite_image.paste(layer.image, (0, 0))
        composite_image.save(filename)


# main.py
from image_canvas_composer import ImageCanvasComposer
from effect import BrightnessEffect, ContrastEffect

def main():
    composer = ImageCanvasComposer()

    # Create a new image
    image = Image.new('RGB', (100, 100))
    pixels = image.load()
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            pixels[x, y] = (255, 0, 0)

    # Add the image to the composer
    composer.add_layer('Layer 1', image)

    # Apply a brightness effect
    composer.apply_effect(BrightnessEffect(50))

    # Export the final composite image
    composer.export_image('output.png')

if __name__ == '__main__':
    main()