# solution.py

# Import necessary libraries
import json
from collections import defaultdict
from typing import List, Dict, Any

# Define a class to represent a single drawing tool
class DrawingTool:
    def __init__(self, name: str, size: int, color: str):
        self.name = name  # Name of the tool (e.g., brush, pen)
        self.size = size  # Size of the tool
        self.color = color  # Color of the tool

# Define a class to represent a page in the notebook
class Page:
    def __init__(self):
        self.drawing_data = []  # List to hold drawing data
        self.annotations = []  # List to hold annotations
        self.history = []  # History of changes for undo functionality

    def add_drawing(self, drawing: Dict[str, Any]):
        self.history.append(drawing)  # Save current state to history
        self.drawing_data.append(drawing)  # Add new drawing

    def add_annotation(self, annotation: str):
        self.annotations.append(annotation)  # Add annotation to the page

# Define a class to represent a user in the application
class User:
    def __init__(self, username: str, role: str):
        self.username = username  # Username of the user
        self.role = role  # Role of the user (viewer, editor, admin)

# Define a class to represent the collaborative notebook
class NotebookCollabSketch:
    def __init__(self):
        self.pages = []  # List of pages in the notebook
        self.users = []  # List of users collaborating
        self.current_page_index = 0  # Index of the current page

    def add_user(self, user: User):
        self.users.append(user)  # Add a new user to the notebook

    def create_page(self):
        self.pages.append(Page())  # Create a new page

    def switch_page(self, index: int):
        if 0 <= index < len(self.pages):
            self.current_page_index = index  # Switch to the specified page

    def add_drawing_to_current_page(self, drawing: Dict[str, Any]):
        self.pages[self.current_page_index].add_drawing(drawing)  # Add drawing to the current page

    def add_annotation_to_current_page(self, annotation: str):def add_annotation_to_current_page(self, annotation: str):
        user_roles = [user.role for user in self.users]
        if 'editor' in user_roles or 'admin' in user_roles:
            self.pages[self.current_page_index].add_annotation(annotation)  # Add annotation to the current page
        else:
            raise PermissionError("User does not have permission to add annotations.")    def get_current_page_data(self) -> Dict[str, Any]:
        # Return the current page's drawing data and annotations
        return {
            "drawings": self.pages[self.current_page_index].drawing_data,
            "annotations": self.pages[self.current_page_index].annotations
        }

    def save_notebook(self, filename: str):
        # Save the notebook state to a JSON file
        with open(filename, 'w') as f:
            json.dump(self.serialize(), f)

    def load_notebook(self, filename: str):
        # Load the notebook state from a JSON file
        with open(filename, 'r') as f:
            data = json.load(f)
            self.deserialize(data)

    def serialize(self) -> Dict[str, Any]:
        # Convert the notebook state to a serializable format
        return {
            "pages": [self.serialize_page(page) for page in self.pages],
            "users": [user.username for user in self.users]
        }

    def serialize_page(self, page: Page) -> Dict[str, Any]:
        # Serialize a single page
        return {
            "drawing_data": page.drawing_data,
            "annotations": page.annotations,
            "history": page.history
        }

    def deserialize(self, data: Dict[str, Any]):
        # Load the notebook state from a serialized format
        self.pages = [self.deserialize_page(page_data) for page_data in data["pages"]]
        self.users = [User(username, "editor") for username in data["users"]]  # Default role as editor

    def deserialize_page(self, page_data: Dict[str, Any]) -> Page:
        # Deserialize a single page
        page = Page()
        page.drawing_data = page_data["drawing_data"]
        page.annotations = page_data["annotations"]
        page.history = page_data["history"]
        return page

# Example usage
if __name__ == "__main__":
    notebook = NotebookCollabSketch()  # Create a new collaborative notebook
    notebook.add_user(User("Alice", "editor"))  # Add a user
    notebook.create_page()  # Create a new page
    notebook.add_drawing_to_current_page({"tool": "brush", "size": 5, "color": "blue", "coordinates": [(0, 0), (1, 1)]})  # Add a drawing
    notebook.add_annotation_to_current_page("This is a sketch of a tree.")  # Add an annotation
    print(notebook.get_current_page_data())  # Print current page data
    notebook.save_notebook("notebook.json")  # Save the notebook to a file