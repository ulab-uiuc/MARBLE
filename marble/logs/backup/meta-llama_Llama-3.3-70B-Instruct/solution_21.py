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
        return None

    def run_test_cases(self, challenge_name, code):
        """
        Run the test cases for a challenge.

        Args:
        challenge_name (str): The name of the challenge.
        code (str): The user's code for the challenge.

        Returns:
        list: A list of test case results.
        """
        challenge = self.get_challenge(challenge_name)
        # Validate and sanitize the user's code
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return [{'input': '', 'expected_output': '', 'result': 'Error', 'error': str(e)}]
import ast
import numexpr

# Validate and sanitize the user's code
try:
    tree = ast.parse(code)exec_code = compile(code, '<string>', 'exec', flags=ast.PyCF_ONLY_AST)exec(exec_code, {'__builtins__': {}}, {'result': None})
    result = locals().get('result')
except Exception as e:
    results.append({'input': test_case['input'], 'expected_output': test_case['expected_output'], 'result': 'Error', 'error': str(e)})except SyntaxError as e:
    results.append({'input': test_case['input'], 'expected_output': test_case['expected_output'], 'result': 'Error', 'error': str(e)})
except Exception as e:
    results.append({'input': test_case['input'], 'expected_output': test_case['expected_output'], 'result': 'Error', 'error': str(e)})result = eval(test_case['input'])
                    if result == test_case['expected_output']:
                        results.append({'input': test_case['input'], 'expected_output': test_case['expected_output'], 'result': 'Pass'})
                    else:
                        results.append({'input': test_case['input'], 'expected_output': test_case['expected_output'], 'result': 'Fail'})
                except Exception as e:
                    results.append({'input': test_case['input'], 'expected_output': test_case['expected_output'], 'result': 'Error', 'error': str(e)})
            return results
        return None

# Create a FamilyCodeQuest platform
platform = FamilyCodeQuest()

# Create some challenges
challenge1 = Challenge('Sorting', 'Sort a list of numbers in ascending order.', [
    {'input': '[1, 2, 3, 4, 5]', 'expected_output': '[1, 2, 3, 4, 5]'},
    {'input': '[5, 4, 3, 2, 1]', 'expected_output': '[1, 2, 3, 4, 5]'},
    {'input': '[1, 1, 1, 1, 1]', 'expected_output': '[1, 1, 1, 1, 1]'}
])
challenge2 = Challenge('Searching', 'Find an element in a list.', [
    {'input': '[1, 2, 3, 4, 5]', 'expected_output': '3'},
    {'input': '[5, 4, 3, 2, 1]', 'expected_output': '3'},
    {'input': '[1, 1, 1, 1, 1]', 'expected_output': '1'}
])

# Add the challenges to the platform
platform.add_challenge(challenge1)
platform.add_challenge(challenge2)

# Create some users
user1 = User('user1')
user2 = User('user2')

# Add the users to the platform
platform.add_user(user1)
platform.add_user(user2)

# Save some progress
platform.save_progress('user1', 'Sorting', 'def sort_list(numbers): return sorted(numbers)')

# Load some progress
progress = platform.load_progress('user1', 'Sorting')
print(progress)

# Run some test cases
results = platform.run_test_cases('Sorting', 'def sort_list(numbers): return sorted(numbers)')
for result in results:
    print(result)

# Create a simple text-based interface
def main():
    print("Welcome to FamilyCodeQuest!")
    while True:
        print("1. View challenges")
        print("2. View user progress")
        print("3. Run test cases")
        print("4. Save progress")
        print("5. Load progress")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            print("Challenges:")
            for challenge in platform.challenges.values():
                print(challenge.name)
        elif choice == '2':
            username = input("Enter your username: ")
            user = platform.get_user(username)
            if user:
                print("Progress:")
                for challenge, code in user.progress.items():
                    print(f"{challenge}: {code}")
            else:
                print("User not found.")
        elif choice == '3':
            challenge_name = input("Enter the challenge name: ")
            code = input("Enter your code: ")
            results = platform.run_test_cases(challenge_name, code)
            for result in results:
                print(result)
        elif choice == '4':
            username = input("Enter your username: ")
            challenge_name = input("Enter the challenge name: ")
            code = input("Enter your code: ")
            platform.save_progress(username, challenge_name, code)
            print("Progress saved.")
        elif choice == '5':
            username = input("Enter your username: ")
            challenge_name = input("Enter the challenge name: ")
            progress = platform.load_progress(username, challenge_name)
            if progress:
                print(progress)
            else:
                print("No progress saved.")
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()