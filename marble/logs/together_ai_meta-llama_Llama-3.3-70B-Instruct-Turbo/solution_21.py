# solution.py
# Importing necessary libraries
import os
import json
from datetime import datetime

# Class to represent a coding challenge
class Challenge:
    def __init__(self, name, description, test_cases):
        """
        Initialize a Challenge object.

        Args:
        name (str): The name of the challenge.
        description (str): A brief description of the challenge.
        test_cases (list): A list of test cases for the challenge.
        """
        self.name = name
        self.description = description
        self.test_cases = test_cases

# Class to represent a user
class User:
    def __init__(self, username):
        """
        Initialize a User object.

        Args:
        username (str): The username of the user.
        """
        self.username = username
        self.progress = {}

    def save_progress(self, challenge_name, code):
        """
        Save the user's progress for a challenge.

        Args:
        challenge_name (str): The name of the challenge.
        code (str): The user's code for the challenge.
        """
        self.progress[challenge_name] = code

    def load_progress(self, challenge_name):
        """
        Load the user's progress for a challenge.

        Args:
        challenge_name (str): The name of the challenge.

        Returns:
        str: The user's code for the challenge, or None if no progress is saved.
        """
        return self.progress.get(challenge_name)

# Class to represent the FamilyCodeQuest platform
class FamilyCodeQuest:
    def __init__(self):
def safe_exec(self, code, input_scenario):
    # Create a restricted environment
    env = {}
    try:
        exec(code, env)
        output = env['output']
        return output
    except Exception as e:
        print(f"Error executing code: {e}")
        return None
import ast
import io
import sys
        """
        Initialize the FamilyCodeQuest platform.
        """
        self.challenges = {}
        self.users = {}

    def add_challenge(self, challenge):
        """
        Add a challenge to the platform.

        Args:
        challenge (Challenge): The challenge to add.
        """
        self.challenges[challenge.name] = challenge

    def add_user(self, user):
        """
        Add a user to the platform.

        Args:
        user (User): The user to add.
        """
        self.users[user.username] = user

    def get_challenge(self, challenge_name):
        """
        Get a challenge by name.

        Args:
        challenge_name (str): The name of the challenge.

        Returns:
        Challenge: The challenge, or None if not found.
        """
        return self.challenges.get(challenge_name)

    def get_user(self, username):
        """
        Get a user by username.

        Args:
        username (str): The username of the user.

        Returns:
        User: The user, or None if not found.
        """
        return self.users.get(username)

    def save_progress(self, username, challenge_name, code):
        """
        Save a user's progress for a challenge.

        Args:
        username (str): The username of the user.
        challenge_name (str): The name of the challenge.
        code (str): The user's code for the challenge.
        """
        user = self.get_user(username)
        if user:
            user.save_progress(challenge_name, code)

    def load_progress(self, username, challenge_name):
        """
        Load a user's progress for a challenge.

        Args:
        username (str): The username of the user.
        challenge_name (str): The name of the challenge.

        Returns:
        str: The user's code for the challenge, or None if no progress is saved.
        """
        user = self.get_user(username)
        if user:
            return user.load_progress(challenge_name)

    def run_test_cases(self, challenge_name, code):
        """
        Run the test cases for a challenge.

        Args:
        challenge_name (str): The name of the challenge.
        code (str): The user's code for the challenge.

        Returns:
        bool: True if all test cases pass, False otherwise.
        """
        challenge = self.get_challenge(challenge_name)
        if challenge:
            # Execute the user's code with the test cases
            # This is a simplified example and may need to be modified based on the actual code execution
            for test_case in challenge.test_cases:
                input_scenario = test_case['input']
                expected_output = test_case['expected_output']
                try:
                    # Execute the user's code with the input scenario
                    output = eval(code, {'input': input_scenario})
                    if output != expected_output:
                        return False
                except Exception as e:
                    print(f"Error running test case: {e}")
                    return False
            return True
        return False

    def provide_feedback(self, challenge_name, code):
        """
        Provide feedback for a challenge.

        Args:
        challenge_name (str): The name of the challenge.
        code (str): The user's code for the challenge.

        Returns:
        str: Feedback for the user.
        """
        challenge = self.get_challenge(challenge_name)
        if challenge:
            # Check if the user's code is correct
            if self.run_test_cases(challenge_name, code):
                return "Correct! Your code passes all test cases."
            else:
                return "Incorrect. Please check your code and try again."
        return "Challenge not found."

# Example usage
if __name__ == "__main__":
    # Create the FamilyCodeQuest platform
    platform = FamilyCodeQuest()

    # Create some challenges
    challenge1 = Challenge("Sorting Challenge", "Sort a list of numbers in ascending order.", [
        {'input': [3, 2, 1], 'expected_output': [1, 2, 3]},
        {'input': [1, 2, 3], 'expected_output': [1, 2, 3]},
        {'input': [], 'expected_output': []}
    ])
    challenge2 = Challenge("Math Challenge", "Calculate the sum of two numbers.", [
        {'input': (2, 3), 'expected_output': 5},
        {'input': (1, 1), 'expected_output': 2},
        {'input': (0, 0), 'expected_output': 0}
    ])

    # Add the challenges to the platform
    platform.add_challenge(challenge1)
    platform.add_challenge(challenge2)

    # Create some users
    user1 = User("user1")
    user2 = User("user2")

    # Add the users to the platform
    platform.add_user(user1)
    platform.add_user(user2)

    # Save and load progress
    platform.save_progress("user1", "Sorting Challenge", "def sort_numbers(numbers): return sorted(numbers)")
    print(platform.load_progress("user1", "Sorting Challenge"))

    # Run test cases and provide feedback
    print(platform.run_test_cases("Sorting Challenge", "def sort_numbers(numbers): return sorted(numbers)"))
    print(platform.provide_feedback("Sorting Challenge", "def sort_numbers(numbers): return sorted(numbers)"))