# CodeSync - Collaborative Coding Notebook

class CodeSync:
    def __init__(self):
        self.notebooks = {}  # Dictionary to store notebooks
        self.users = {}  # Dictionary to store users and their permissions

    def create_notebook(self, notebook_name, is_private=False):
        """
        Create a new notebook with the given name.
        Args:
            notebook_name (str): Name of the notebook
            is_private (bool): Flag to indicate if the notebook is private
        """
        if notebook_name in self.notebooks:
            print("Notebook with the same name already exists.")
        else:
            self.notebooks[notebook_name] = {"content": "", "is_private": is_private}
            print(f"Notebook '{notebook_name}' created successfully.")
            self.notebooks[notebook_name]['collaborators'] = set()

    def edit_notebook(self, notebook_name, content):
        """
        Edit the content of a notebook.
        Args:
            notebook_name (str): Name of the notebook
            content (str): New content to be added to the notebook
        """
        if notebook_name in self.notebooks:
            self.notebooks[notebook_name]["content"] = content
            print(f"Notebook '{notebook_name}' updated successfully.")
        else:
            print("Notebook not found.")

    def get_notebook_content(self, notebook_name):
        """
        Get the content of a notebook.
        Args:
            notebook_name (str): Name of the notebook
        Returns:
            str: Content of the notebook
        """
        if notebook_name in self.notebooks:
            return self.notebooks[notebook_name]["content"]
        else:
            return "Notebook not found."

    def set_notebook_permission(self, notebook_name, user, permission):
        """
        Set permission for a user on a specific notebook.
        Args:
            notebook_name (str): Name of the notebook
            user (str): User for whom the permission is to be set
            permission (str): Permission level (e.g., read, write)
        """
        if notebook_name in self.notebooks:
            if user not in self.users:
                self.users[user] = {}
            self.users[user][notebook_name] = permission
            print(f"Permission set for user '{user}' on notebook '{notebook_name}' - {permission}.")
        else:
            print("Notebook not found.")

    def search_notebook(self, keyword):
        """
        Search for a keyword in all notebooks.
        Args:
            keyword (str): Keyword to search for
        Returns:
            list: List of notebooks containing the keyword
        """
        result = []
        for notebook_name, notebook in self.notebooks.items():
            if keyword in notebook["content"]:
                result.append(notebook_name)
        return result

# Test Cases
if __name__ == "__main__":
    codesync = CodeSync()

        # Test real-time collaboration
        # Test syntax highlighting
        # Test code completion
        # Test version control
        # Test access control
        # Test search functionality
    
    # Create a public notebook
    codesync.create_notebook("Public Notebook", is_private=False)
    
    # Create a private notebook
    codesync.create_notebook("Private Notebook", is_private=True)
    
    # Edit the content of the public notebook
    codesync.edit_notebook("Public Notebook", "print('Hello, World!')")
    
    # Set permission for a user on the private notebook
    codesync.set_notebook_permission("Private Notebook", "user1", "read")
    
    # Search for a keyword in notebooks
    search_result = codesync.search_notebook("print")
    print("Notebooks containing the keyword 'print':", search_result)