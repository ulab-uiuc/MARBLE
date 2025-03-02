# CollaborativeDesignSuite.py

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Canvas:
    def __init__(self):
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)

class Shape:
    def __init__(self, shape_type):
        self.shape_type = shape_type

class Texture:
    def __init__(self, texture_type):
        self.texture_type = texture_type

class Annotation:
    def __init__(self, text):
        self.text = text

class CollaborativeDesignSuite:
    def __init__(self):
        self.users = {}
        self.canvas = Canvas()
        self.is_authenticated = False

    def register_user(self, username, password):
        if username in self.users:
            print("Username already exists. Please choose a different username.")
        else:
            self.users[username] = User(username, password)
            print("User registered successfully.")

    def login(self, username, password):
        if username in self.users and self.users[username].password == password:
            self.is_authenticated = True
            print("Login successful.")
        else:
            print("Invalid username or password. Please try again.")

    def draw_shape(self, shape_type):if self.is_authenticated:print("Please login to add shapes to the canvas.")else:
            print("Please login to add annotations.")


# Usage example
design_app = CollaborativeDesignSuite()

design_app.register_user("user1", "password1")
design_app.register_user("user2", "password2")

design_app.login("user1", "password1")

design_app.draw_shape("circle")
design_app.apply_texture("stripes")

design_app.add_annotation("Add more details to the design")