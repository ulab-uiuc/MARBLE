# solution.py

# Importing necessary libraries
import threading
import time
import json
import os

# User class to store user information
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.challenges = {}

# Challenge class to store challenge information
class Challenge:
    def __init__(self, name, description, test_cases):
        self.name = name
        self.description = description
        self.test_cases = test_cases

# FamilyCodeQuest class to manage the platform
class FamilyCodeQuest:
    def __init__(self):
        self.users = {}
        self.challenges = {}
        self.lock = threading.Lock()

    # Method to add a user
    def add_user(self, username, password):
        with self.lock:
            if username in self.users:
                print("Username already exists.")
                return
            self.users[username] = User(username, password)
            print("User added successfully.")

    # Method to add a challenge
    def add_challenge(self, name, description, test_cases):
        with self.lock:
            if name in self.challenges:
                print("Challenge already exists.")
                return
            self.challenges[name] = Challenge(name, description, test_cases)
            print("Challenge added successfully.")

    # Method to login a user
    def login(self, username, password):
        with self.lock:
            if username not in self.users:
                print("Username does not exist.")
                return
            if self.users[username].password != password:
                print("Incorrect password.")
                return
            print("Login successful.")

    # Method to save progress
    def save_progress(self, username):
        with self.lock:
            if username not in self.users:
                print("Username does not exist.")
                return
            user = self.users[username]
            with open(f"{username}.json", "w") as file:
                json.dump(user.challenges, file)
            print("Progress saved successfully.")

    # Method to load progress
    def load_progress(self, username):
        with self.lock:
            if username not in self.users:
                print("Username does not exist.")
                return
            if not os.path.exists(f"{username}.json"):
                print("No progress saved.")
                return
            with open(f"{username}.json", "r") as file:
                user = self.users[username]
                user.challenges = json.load(file)
            print("Progress loaded successfully.")

    # Method to provide feedback
    def provide_feedback(self, username, challenge_name, code):
        with self.lock:
            if username not in self.users:
                print("Username does not exist.")
                return
            if challenge_name not in self.challenges:
                print("Challenge does not exist.")
                return
            challenge = self.challenges[challenge_name]
            # Run the code and check if it passes the test cases
            # For simplicity, let's assume the code is a Python function
try:
            # Create a separate namespace for the code
            namespace = {}
            # Execute the code in the separate namespace
            exec(code, namespace)
            # Get the function name from the code
            function_name = [name for name in namespace if callable(namespace[name])][0]
            # Run the test cases
            for test_case in challenge.test_cases:
                input_value = eval(test_case["input"])
                output_value = namespace[function_name](input_value)
                if str(output_value) != test_case["output"]:
                    print("Incorrect solution.")
                    return
            print("Correct solution.")except Exception as e:
                print("Error in code:", str(e))

# Main function
def main():
    platform = FamilyCodeQuest()

    # Add users
    platform.add_user("user1", "password1")
    platform.add_user("user2", "password2")

    # Add challenges
    platform.add_challenge("challenge1", "Sort a list of numbers.", [
        {"input": "[1, 2, 3, 4, 5]", "output": "[1, 2, 3, 4, 5]"},
        {"input": "[5, 4, 3, 2, 1]", "output": "[1, 2, 3, 4, 5]"},
        {"input": "[]", "output": "[]"}
    ])

    # Login users
    platform.login("user1", "password1")
    platform.login("user2", "password2")

    # Save progress
    platform.save_progress("user1")

    # Load progress
    platform.load_progress("user1")

    # Provide feedback
    platform.provide_feedback("user1", "challenge1", """
def sort_list(numbers):
    return sorted(numbers)
""")

if __name__ == "__main__":
    main()