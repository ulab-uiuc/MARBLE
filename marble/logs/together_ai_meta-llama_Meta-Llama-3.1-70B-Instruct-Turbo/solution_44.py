# codesync.py

import threading
import time
import re
import unittest
from unittest.mock import Mock

class CodeSync:
    def __init__(self):
        self.notebooks = {}
        self.lock = threading.Lock()

    def create_notebook(self, name, access="public"):
        with self.lock:
            if name in self.notebooks:
                raise Exception("Notebook already exists")
            self.notebooks[name] = {
                "access": access,
                "content": "",
                "versions": [],
                "users": []
            }

    def edit_notebook(self, name, content, user):def get_notebook(self, name, user):
    with self.lock:
        if name not in self.notebooks:
            raise Exception("Notebook does not exist")
        if self.notebooks[name]["access"] == "private" and user not in self.notebooks[name]["users"]:
            raise Exception("Access denied")
        return self.notebooks[name]["content"]def revert_notebook(self, name, version, user):
        with self.lock:
if version is None:
        version = self.notebooks[name]['version']
    if self.notebooks[name]['version'] != version:
        raise Exception('Notebook has been modified by another user. Please refresh and try again.')
            if name not in self.notebooks:
                raise Exception("Notebook does not exist")
            if self.notebooks[name]["access"] == "private" and user not in self.notebooks[name]["users"]:
                raise Exception("Access denied")
            if version < 0 or version >= len(self.notebooks[name]["versions"]):
                raise Exception("Invalid version")
            self.notebooks[name]["content"] = self.notebooks[name]["versions"][version]

    def search_notebook(self, name, query, user):
        with self.lock:
            if name not in self.notebooks:
                raise Exception("Notebook does not exist")
            if self.notebooks[name]["access"] == "private" and user not in self.notebooks[name]["users"]:
                raise Exception("Access denied")
            return re.findall(query, self.notebooks[name]["content"])

    def syntax_highlight(self, content, language):
        # This is a simplified syntax highlighting function
        # In a real application, you would use a library like Pygments
        if language == "python":
            return re.sub(r"def\s+\w+\s*\(", "def **\g<0>", content)
        elif language == "javascript":
            return re.sub(r"function\s+\w+\s*\(", "function **\g<0>", content)
        elif language == "java":
            return re.sub(r"public\s+class\s+\w+", "public class **\g<0>", content)
        elif language == "c++":
            return re.sub(r"int\s+main\s*\(", "int **main**\g<0>", content)
        else:
            return content

    def code_completion(self, content, language):
        # This is a simplified code completion function
        # In a real application, you would use a library like Jedi
        if language == "python":
            return ["print(", "len(", "range("]
        elif language == "javascript":
            return ["console.log(", "Math.", "Array."]
        elif language == "java":
            return ["System.out.println(", "Math.", "String."]
        elif language == "c++":
            return ["std::cout << ", "std::", "int "]
        else:
            return []

class TestCodeSync(unittest.TestCase):
    def setUp(self):
        self.codesync = CodeSync()

    def test_create_notebook(self):
        self.codesync.create_notebook("test")
        self.assertIn("test", self.codesync.notebooks)

    def test_edit_notebook(self):
        self.codesync.create_notebook("test")
        self.codesync.edit_notebook("test", "Hello, world!", "user1")
        self.assertEqual(self.codesync.get_notebook("test", "user1"), "Hello, world!")

    def test_revert_notebook(self):
        self.codesync.create_notebook("test")
        self.codesync.edit_notebook("test", "Hello, world!", "user1")
        self.codesync.edit_notebook("test", "Goodbye, world!", "user1")
        self.codesync.revert_notebook("test", 0, "user1")
        self.assertEqual(self.codesync.get_notebook("test", "user1"), "Hello, world!")

    def test_search_notebook(self):
        self.codesync.create_notebook("test")
        self.codesync.edit_notebook("test", "Hello, world!", "user1")
        self.assertEqual(self.codesync.search_notebook("test", "Hello", "user1"), ["Hello"])

    def test_syntax_highlight(self):
        self.assertEqual(self.codesync.syntax_highlight("def hello():", "python"), "def **hello**():")

    def test_code_completion(self):
        self.assertEqual(self.codesync.code_completion("print(", "python"), ["print(", "len(", "range("])

if __name__ == "__main__":
    unittest.main()