# solution.py

# Import necessary libraries
import json
from typing import List, Dict, Any, Optional

# Define a class to represent a code snippet
class CodeSnippet:
    def __init__(self, content: str, language: str):
        self.content = content  # The actual code content
        self.language = language  # The programming language of the code
        self.version_history = []  # To keep track of versions
        self.current_version = 0  # To track the current version

    def add_version(self, content: str):
        """Add a new version of the code snippet."""
        self.version_history.append(content)
        self.current_version += 1

    def revert_to_version(self, version: int):
        """Revert to a specific version of the code snippet."""
        if 0 <= version < len(self.version_history):
            self.content = self.version_history[version]
            self.current_version = version
        else:
            raise ValueError("Invalid version number.")

# Define a class to represent a notebook
class Notebook:
    def __init__(self, title: str, is_private: bool = False):
        self.title = title  # Title of the notebook
        self.is_private = is_private  # Privacy status
        self.snippets: Dict[str, CodeSnippet] = {}  # Dictionary to hold code snippets

    def add_snippet(self, name: str, content: str, language: str):
        """Add a new code snippet to the notebook."""
        snippet = CodeSnippet(content, language)
        self.snippets[name] = snippet

    def search_snippet(self, keyword: str) -> List[str]:
        """Search for snippets containing the keyword."""
        return [name for name in self.snippets if keyword in name or keyword in self.snippets[name].content]

# Define a class to represent a user
class User:
    def __init__(self, username: str):
        self.username = username  # Username of the user
        self.notebooks: List[Notebook] = []  # List of notebooks owned by the user

    def create_notebook(self, title: str, is_private: bool = False):
        """Create a new notebook."""
        notebook = Notebook(title, is_private)
        self.notebooks.append(notebook)

# Define a class for the CodeSync application
class CodeSync:
    def __init__(self):
        self.users: Dict[str, User] = {}  # Dictionary to hold users

    def add_user(self, username: str):
        """Add a new user to the application."""
        if username not in self.users:
            self.users[username] = User(username)

    def get_user(self, username: str) -> Optional[User]:
        """Retrieve a user by username."""
        return self.users.get(username)

    def save_to_file(self, filename: str):
        """Save the current state of the application to a file."""
        with open(filename, 'w') as f:
            json.dump(self.users, f, default=lambda o: o.__dict__)

    def load_from_file(self, filename: str):
        """Load the application state from a file."""def load_from_file(self, filename: str):
        """Load the application state from a file."""
        with open(filename, 'r') as f:
            data = json.load(f)
            self.users = {username: User(username) for username in data.keys()}
            for username, user_data in data.items():
                user = self.users[username]
                user.notebooks = [Notebook(nb['title'], nb['is_private']) for nb in user_data['notebooks']]
                for nb in user.notebooks:
                    nb.snippets = {name: CodeSnippet(content, language) for name, content, language in user_data['snippets'].items()}            self.users = json.load(f)

# Example usage of the CodeSync application
if __name__ == "__main__":
    codesync = CodeSync()
    codesync.add_user("dev1")
    user = codesync.get_user("dev1")
    user.create_notebook("My First Notebook", is_private=True)
    notebook = user.notebooks[0]
    notebook.add_snippet("HelloWorld", "print('Hello, World!')", "Python")
    print(notebook.search_snippet("Hello"))  # Should return ['HelloWorld']