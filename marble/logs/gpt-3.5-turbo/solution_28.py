class Layer:
    def __init__(self, name, image):
        self.name = name
        self.image = image

class ImageCanvasComposer:
    def __init__(self):
        self.layers = []

    def add_layer(self, layer):
        self.layers.append(layer)

    def delete_layer(self, layer_name):
        self.layers = [layer for layer in self.layers if layer.name != layer_name]

    def reorder_layers(self, layer_names):# Implement the functionality to apply graphical effects to individual layers or the entire canvas
        for layer in self.layers:self.layers = [layer for name in layer_names for layer in self.layers if layer.name == name]            pass    def blend_layers(self, blending_mode):
        # Blend layers using specified blending mode
        pass

    def adjust_transparency(self, layer_name, transparency):
        # Adjust transparency of a specific layer
        pass

    def adjust_position(self, layer_name, position):
        # Adjust position of a specific layer
        pass

    def adjust_size(self, layer_name, size):
        # Adjust size of a specific layer
        pass

    def export_image(self, file_format):
        # Export the final composite image in the specified format
        pass

# Example Usage:
# Create ImageCanvasComposer instance
composer = ImageCanvasComposer()

# Create and add layers
layer1 = Layer("Layer 1", "image1.jpg")
layer2 = Layer("Layer 2", "image2.jpg")
composer.add_layer(layer1)
composer.add_layer(layer2)

# Delete a layer
composer.delete_layer("Layer 1")

# Reorder layers
composer.reorder_layers(["Layer 2", "Layer 1"])

# Apply graphical effects
composer.apply_effect("brightness")
composer.apply_effect("blur")

# Blend layers
composer.blend_layers("overlay")

# Adjust transparency, position, and size of layers
composer.adjust_transparency("Layer 2", 0.5)
composer.adjust_position("Layer 2", (100, 100))
composer.adjust_size("Layer 2", (200, 200))

# Export the final composite image
composer.export_image("PNG")