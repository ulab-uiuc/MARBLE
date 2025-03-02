# solution.py

# CollaborativeDesignSuite: A multi-agent collaborative design tool

class User:
    """Class representing a user in the Collaborative Design Suite."""
    
    def __init__(self, username, password):
        """Initialize a new user with a username and password."""
        self.username = usernameimport bcrypt

        # Hash the password before storing it
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())    def authenticate_user(self, username, password):
        """Authenticate a user by checking username and password."""
        user = self.users.get(username)
        if user and user.password == password:if user and bcrypt.checkpw(password.encode('utf-8'), user.password):            return f"User {username} authenticated successfully."
        raise ValueError("Invalid username or password.")

class Canvas:
    """Class representing a collaborative drawing canvas."""
    
    def __init__(self):
        """Initialize the canvas with an empty list of elements."""
        self.elements = []
        self.annotations = []
    
    def add_element(self, element):
        """Add a design element to the canvas."""
        self.elements.append(element)
    
    def add_annotation(self, annotation):
        """Add an annotation to the canvas."""
        self.annotations.append(annotation)
    
    def get_elements(self):
        """Return the current elements on the canvas."""
        return self.elements
    
    def get_annotations(self):
        """Return the current annotations on the canvas."""
        return self.annotations

class Shape:
    """Class representing a geometric shape."""
    
    def __init__(self, shape_type, position):
        """Initialize a shape with its type and position."""
        self.shape_type = shape_type
        self.position = position  # Position could be a tuple (x, y)

class Texture:
    """Class representing a texture to be applied to shapes."""
    
    def __init__(self, texture_name):
        """Initialize a texture with its name."""
        self.texture_name = texture_name

class DesignTool:
    """Class to manage design tools for shapes and textures."""
    
    def __init__(self):
        """Initialize the design tool with no active shapes or textures."""
        self.shapes = []
        self.textures = []
    
    def create_shape(self, shape_type, position):
        """Create a new shape and add it to the shapes list."""
        shape = Shape(shape_type, position)
        self.shapes.append(shape)
        return shape
    
    def apply_texture(self, shape, texture):
        """Apply a texture to a shape if the shape exists."""
        if shape in self.shapes:
            shape.texture = texture
            return f"Texture {texture.texture_name} applied to shape."
        raise ValueError("Shape not found.")

class CollaborativeDesignSuite:
    """Main class for the Collaborative Design Suite application."""
    
    def __init__(self):
        """Initialize the design suite with user manager, canvas, and tools."""
        self.user_manager = UserManager()
        self.canvas = Canvas()
        self.design_tool = DesignTool()
        self.is_canvas_active = False
    
    def register_user(self, username, password):
        """Register a new user."""
        return self.user_manager.register_user(username, password)
    
    def login_user(self, username, password):
        """Authenticate a user and activate the canvas for collaboration."""
        auth_message = self.user_manager.authenticate_user(username, password)
        self.is_canvas_active = True  # Activate the canvas upon successful login
        return auth_message
    
    def create_shape(self, shape_type, position):
        """Create a shape on the canvas if the canvas is active."""
        if not self.is_canvas_active:
            raise ValueError("Canvas is not active. Please log in.")
        return self.design_tool.create_shape(shape_type, position)
    
    def add_shape_to_canvas(self, shape):
        """Add a shape to the canvas."""
        self.canvas.add_element(shape)
    
    def apply_texture_to_shape(self, shape, texture_name):
        """Apply a texture to a shape if the canvas is active."""
        if not self.is_canvas_active:
            raise ValueError("Canvas is not active. Please log in.")
        texture = Texture(texture_name)
        return self.design_tool.apply_texture(shape, texture)
    
    def add_annotation(self, annotation):
        """Add an annotation to the canvas if the canvas is active."""
        if not self.is_canvas_active:
            raise ValueError("Canvas is not active. Please log in.")
        self.canvas.add_annotation(annotation)

# Example usage
if __name__ == "__main__":
    suite = CollaborativeDesignSuite()
    print(suite.register_user("designer1", "password123"))
    print(suite.login_user("designer1", "password123"))
    
    shape = suite.create_shape("circle", (100, 150))
    suite.add_shape_to_canvas(shape)
    print(suite.apply_texture_to_shape(shape, "wood"))
    suite.add_annotation("This is a note on the design.")
    
    print("Canvas Elements:", suite.canvas.get_elements())
    print("Canvas Annotations:", suite.canvas.get_annotations())