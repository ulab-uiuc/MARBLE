# solution.py

class User:
    """Class representing a user in the Collaborative Design Suite."""
    
    def __init__(self, username, password):
        """Initialize a new user with a username and password."""
        self.username = username
        self.password = password  # In a real application, passwords should be hashed


class UserManager:
    """Class to manage user registration and authentication."""
    
    def __init__(self):
        """Initialize the user manager with an empty user list."""
        self.users = {}
    
    def register_user(self, username, password):
        """Register a new user if the username is not taken."""
        if username in self.users:
            raise ValueError("Username already exists.")
        self.users[username] = User(username, password)
        return f"User {username} registered successfully."
    
    def authenticate_user(self, username, password):
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


class ShapeTool:
    """Class for creating and managing shapes on the canvas."""
    
    def __init__(self, canvas):
        """Initialize the shape tool with a reference to the canvas."""
        self.canvas = canvas
    
    def create_shape(self, shape_type, dimensions):
        """Create a shape and add it to the canvas."""
        shape = {'type': shape_type, 'dimensions': dimensions}
        self.canvas.add_element(shape)
        return f"{shape_type} created with dimensions {dimensions}."


class TextureTool:
    """Class for applying textures to shapes on the canvas."""
    
    def __init__(self, canvas):
        """Initialize the texture tool with a reference to the canvas."""
        self.canvas = canvas
    
    def apply_texture(self, shape, texture):
        """Apply a texture to a specified shape."""
        if shape not in self.canvas.get_elements():
            raise ValueError("Shape not found on the canvas.")
        shape['texture'] = texture
        return f"Texture {texture} applied to {shape['type']}."


class AnnotationTool:
    """Class for adding annotations to the canvas."""
    
    def __init__(self, canvas):
        """Initialize the annotation tool with a reference to the canvas."""
        self.canvas = canvas
    
    def add_annotation(self, text):
        """Add an annotation to the canvas."""
        self.canvas.add_annotation(text)
        return f"Annotation added: {text}"


class CollaborativeDesignSuite:
    """Main class for the Collaborative Design Suite application."""
    
    def __init__(self):
        """Initialize the design suite with user manager and canvas."""
        self.user_manager = UserManager()
        self.canvas = Canvas()
        self.shape_tool = ShapeTool(self.canvas)
        self.texture_tool = TextureTool(self.canvas)
        self.annotation_tool = AnnotationTool(self.canvas)
        self.active_user = None
    
    def register_user(self, username, password):
        """Register a new user."""
        return self.user_manager.register_user(username, password)
    
    def login_user(self, username, password):
        """Log in a user."""
        self.active_user = self.user_manager.authenticate_user(username, password)
        return self.active_user
    
    def create_shape(self, shape_type, dimensions):
        """Create a shape on the canvas if a user is logged in."""
        if self.active_user:
            return self.shape_tool.create_shape(shape_type, dimensions)
        raise ValueError("User must be logged in to create shapes.")
    
    def apply_texture(self, shape, texture):
        """Apply a texture to a shape if a user is logged in."""
        if self.active_user:
            return self.texture_tool.apply_texture(shape, texture)
        raise ValueError("User must be logged in to apply textures.")
    
    def add_annotation(self, text):
        """Add an annotation to the canvas if a user is logged in."""
        if self.active_user:
            return self.annotation_tool.add_annotation(text)
        raise ValueError("User must be logged in to add annotations.")


# Example usage:
if __name__ == "__main__":
    app = CollaborativeDesignSuite()
    
    # User registration and login
    print(app.register_user("designer1", "password123"))
    print(app.login_user("designer1", "password123"))
    
    # Creating shapes
    print(app.create_shape("Circle", {"radius": 5}))
    print(app.create_shape("Rectangle", {"width": 10, "height": 5}))
    
    # Applying textures
    shape = app.canvas.get_elements()[0]  # Get the first shape
    print(app.apply_texture(shape, "Wood"))
    
    # Adding annotations
    print(app.add_annotation("This is a comment on the circle."))
    
    # Displaying canvas elements and annotations
    print("Canvas Elements:", app.canvas.get_elements())
    print("Canvas Annotations:", app.canvas.get_annotations())