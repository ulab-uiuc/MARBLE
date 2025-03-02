# layer_manager.py
class Layer:
    def __init__(self, name, image):
        self.name = name
        self.image = image
        self.position = (0, 0)
        self.size = (image.width, image.height)
        self.transparency = 1.0

class LayerManager:
    def __init__(self):
        self.layers = []

    def add_layer(self, name, image):
        self.layers.append(Layer(name, image))

    def delete_layer(self, index):
        if index < len(self.layers):
            del self.layers[index]

    def reorder_layer(self, index, new_index):
        if index < len(self.layers) and new_index < len(self.layers):
            self.layers.insert(new_index, self.layers.pop(index))

    def get_layer(self, index):
        if index < len(self.layers):
            return self.layers[index]
        else:
            return None

    def get_all_layers(self):
        return self.layers

# image_effects.py
from PIL import Image, ImageEnhance, ImageFilter

class ImageEffects:
    def __init__(self, image):
        self.image = image

    def adjust_brightness(self, brightness):
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(brightness)

    def adjust_contrast(self, contrast):
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(contrast)

    def apply_blur(self):
        self.image = self.image.filter(ImageFilter.GaussianBlur(radius=5))

    def apply_sharpen(self):
        self.image = self.image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

# image_composer.py
from PIL import Image

class ImageComposer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.layers = []

    def add_layer(self, layer):
        self.layers.append(layer)

    def delete_layer(self, index):
        if index < len(self.layers):
            del self.layers[index]

    def reorder_layer(self, index, new_index):
        if index < len(self.layers) and new_index < len(self.layers):
            self.layers.insert(new_index, self.layers.pop(index))

    def compose_image(self):
        composite_image = Image.new('RGB', (self.width, self.height))
        for layer in self.layers:
            composite_image.paste(layer.image, layer.position)
        return composite_image

# image_exporter.py
from PIL import Image

class ImageExporter:
    def __init__(self, image):
        self.image = image

    def export_png(self, filename):
        self.image.save(filename, 'PNG')

    def export_jpeg(self, filename):
        self.image.save(filename, 'JPEG')

    def export_psd(self, filename):
        self.image.save(filename, 'PSD')

# solution.py
from PIL import Image
from layer_manager import LayerManager
from image_effects import ImageEffects
from image_composer import ImageComposer
from image_exporter import ImageExporter

class ImageCanvasComposer:
    def __init__(self):
        self.layer_manager = LayerManager()
        self.image_composer = ImageComposer(800, 600)
        self.image_exporter = ImageExporter(Image.new('RGB', (800, 600)))

    def create_layer(self, name, image_path):
        image = Image.open(image_path)
        self.layer_manager.add_layer(name, image)

    def delete_layer(self, index):
        self.layer_manager.delete_layer(index)

    def reorder_layer(self, index, new_index):
        self.layer_manager.reorder_layer(index, new_index)

    def apply_brightness_effect(self, index, brightness):
        layer = self.layer_manager.get_layer(index)
        if layer:
            image_effects = ImageEffects(layer.image)
            image_effects.adjust_brightness(brightness)
            layer.image = image_effects.image

    def apply_contrast_effect(self, index, contrast):
        layer = self.layer_manager.get_layer(index)
        if layer:
            image_effects = ImageEffects(layer.image)
            image_effects.adjust_contrast(contrast)
            layer.image = image_effects.image

    def apply_blur_effect(self, index):
        layer = self.layer_manager.get_layer(index)
        if layer:
            image_effects = ImageEffects(layer.image)
            image_effects.apply_blur()
            layer.image = image_effects.image

    def apply_sharpen_effect(self, index):
        layer = self.layer_manager.get_layer(index)
        if layer:
            image_effects = ImageEffects(layer.image)
            image_effects.apply_sharpen()
            layer.image = image_effects.image

    def compose_image(self):
        self.image_composer.layers = self.layer_manager.layers
        return self.image_composer.compose_image()

    def export_image(self, filename):
        image = self.compose_image()
        self.image_exporter.image = image
        self.image_exporter.export_png(filename)

# Example usage:
composer = ImageCanvasComposer()
composer.create_layer('Layer 1', 'image1.jpg')
composer.create_layer('Layer 2', 'image2.jpg')
composer.apply_brightness_effect(0, 1.5)
composer.apply_contrast_effect(1, 1.2)
composer.compose_image()
composer.export_image('output.png')