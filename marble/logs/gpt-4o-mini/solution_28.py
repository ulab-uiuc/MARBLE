# solution.py

from PIL import Image, ImageEnhance, ImageFilter
import os

class Layer:
    """Class representing a single image layer."""
    
    def __init__(self, image_path):
        """Initialize the layer with an image from the given path."""
        self.image = Image.open(image_path)
        self.opacity = 1.0  # Opacity of the layer (1.0 = fully opaque)
    
    def apply_effect(self, effect):
        """Apply a graphical effect to the layer."""
        if effect == 'blur':
            self.image = self.image.filter(ImageFilter.BLUR)
        elif effect == 'sharpen':
            self.image = self.image.filter(ImageFilter.SHARPEN)
        elif effect == 'brightness':
            enhancer = ImageEnhance.Brightness(self.image)
            self.image = enhancer.enhance(1.5)  # Increase brightness
        elif effect == 'contrast':
            enhancer = ImageEnhance.Contrast(self.image)
            self.image = enhancer.enhance(1.5)  # Increase contrast
    
    def set_opacity(self, opacity):
        """Set the opacity of the layer."""
        self.opacity = opacity

class ImageCanvasComposer:
    """Class to manage multiple image layers and compose them into a final image."""
    
    def __init__(self):
        """Initialize the canvas with an empty list of layers."""
        self.layers = []
    
    def add_layer(self, image_path):
        """Add a new layer to the canvas."""
        new_layer = Layer(image_path)
        self.layers.append(new_layer)
    
    def delete_layer(self, index):
        """Delete a layer from the canvas by index."""
        if 0 <= index < len(self.layers):
            del self.layers[index]
    
    def reorder_layers(self, old_index, new_index):
        """Reorder layers by moving a layer from old_index to new_index."""
        if 0 <= old_index < len(self.layers) and 0 <= new_index < len(self.layers):
            layer = self.layers.pop(old_index)
            self.layers.insert(new_index, layer)
    
    def apply_effect_to_layer(self, index, effect):
        """Apply a graphical effect to a specific layer."""
        if 0 <= index < len(self.layers):
            self.layers[index].apply_effect(effect)def export_composite_image(self, output_path, format='PNG'):
        """Export the final composite image by blending all layers in the specified format."""
        if not self.layers:
            return
        
        # Start with the bottom layer
        composite_image = self.layers[0].image.convert("RGBA")
        
        for layer in self.layers[1:]:
            # Create a new image with the same size as the composite
            layer_image = layer.image.convert("RGBA")
            # Adjust opacity
            layer_image.putalpha(int(layer.opacity * 255))
            # Composite the images
            composite_image = Image.alpha_composite(composite_image, layer_image)
        
        # Save the final composite image in the specified format
        composite_image.save(output_path, format=format)        # Start with the bottom layer
        composite_image = self.layers[0].image.convert("RGBA")
        
        for layer in self.layers[1:]:
            # Create a new image with the same size as the composite
            layer_image = layer.image.convert("RGBA")
            # Adjust opacity
            layer_image.putalpha(int(layer.opacity * 255))
            # Composite the images
            composite_image = Image.alpha_composite(composite_image, layer_image)
        
        # Save the final composite image
        composite_image.save(output_path, format='PNG')

# Example usage
if __name__ == "__main__":
    composer = ImageCanvasComposer()
    
    # Add layers
    composer.add_layer("layer1.png")
    composer.add_layer("layer2.png")
    
    # Apply effects
    composer.apply_effect_to_layer(0, 'blur')
    composer.apply_effect_to_layer(1, 'sharpen')
    
    # Set layer opacity
    composer.layers[0].set_opacity(0.5)
    
    # Export the final composite image
    composer.export_composite_image("final_composite.png")