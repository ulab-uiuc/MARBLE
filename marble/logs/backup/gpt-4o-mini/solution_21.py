# solution.py

# Import necessary libraries
import json
from typing import List, Dict, Any, Tuple

# Class to represent a coding challenge
class CodingChallenge:
    def __init__(self, title: str, description: str, test_cases: List[Tuple[Any, Any]]):
        """
        Initialize a coding challenge with a title, description, and test cases.
        
        :param title: Title of the challenge
        :param description: Description of the challenge
        :param test_cases: List of tuples containing input and expected output
        """
        self.title = title
        self.description = description
        self.test_cases = test_cases

# Class to manage user sessions and challenges
class FamilyCodeQuest:
    def __init__(self):
        """
        Initialize the FamilyCodeQuest platform with users and challenges.
        """
        self.users = {}  # Dictionary to hold user sessions
        self.challenges = []  # List to hold coding challenges
        self.load_challenges()  # Load predefined challenges

    def load_challenges(self):
        """
        Load predefined coding challenges into the platform.
        """
        # Example challenges
        self.challenges.append(CodingChallenge(
            title="Sort a List",
            description="Write a function that sorts a list of numbers.",
            test_cases=[
                ([3, 1, 2], [1, 2, 3]),
                ([], []),
                ([5, 3, 5, 2], [2, 3, 5, 5]),
                ([-1, 0, 1], [-1, 0, 1])
            ]
        ))

    def register_user(self, username: str):
        """
        Register a new user in the platform.
        
        :param username: The username of the new user
        """
        if username not in self.users:
            self.users[username] = {"progress": None}
            print(f"User {username} registered successfully.")
        else:
            print(f"User {username} already exists.")

    def save_progress(self, username: str, progress: Any):
        """
        Save the user's progress on a challenge.
        
        :param username: The username of the user
        :param progress: The progress data to save
        """
        if username in self.users:
            self.users[username]["progress"] = progress
            print(f"Progress saved for user {username}.")
        else:
            print(f"User {username} not found.")

    def load_progress(self, username: str) -> Any:
        """
        Load the user's progress on a challenge.
        
        :param username: The username of the user
        :return: The user's progress data
        """
        return self.users.get(username, {}).get("progress", None)

    def run_test_cases(self, challenge: CodingChallenge, user_solution: Any) -> List[str]:
        """
        Run the test cases against the user's solution.
        
        :param challenge: The coding challenge to test
        :param user_solution: The user's solution function
        :return: List of results for each test case
        """
        results = []
        for i, (input_data, expected_output) in enumerate(challenge.test_cases):
            try:
                output = user_solution(*input_data)  # Call the user's solution
                if output == expected_output:
                    results.append(f"Test case {i + 1}: Passed")
                else:
                    results.append(f"Test case {i + 1}: Failed (Expected {expected_output}, got {output})")
            except Exception as e:
                results.append(f"Test case {i + 1}: Error ({str(e)})")
        return results

# Example of how to use the FamilyCodeQuest platform
if __name__ == "__main__":
    platform = FamilyCodeQuest()
    platform.register_user("Alice")
    
    # Example user solution for the sorting challenge
    def user_sort_function(numbers: List[int]) -> List[int]:
        return sorted(numbers)

    # Running the test cases for the first challenge
    challenge = platform.challenges[0]
    results = platform.run_test_cases(challenge, user_sort_function)
    
    # Print the results of the test cases
    for result in results:
        print(result)