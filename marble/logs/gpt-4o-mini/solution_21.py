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

    def run_tests(self, user_solution: Any) -> List[str]:
        """
        Run the provided user solution against the test cases and return results.
        
        :param user_solution: The user's solution to the challenge
        :return: List of results for each test case
        """
        results = []
        for i, (input_data, expected) in enumerate(self.test_cases):
            result = user_solution(*input_data)
            if result == expected:
                results.append(f"Test case {i + 1}: Passed")
            else:
                results.append(f"Test case {i + 1}: Failed (Expected {expected}, got {result})")
        return results

# Class to manage user sessions and progress
class UserSession:
    def __init__(self):
        """
        Initialize a user session to manage user progress and challenges.
        """
        self.progress = {}

    def save_progress(self, user_id: str, challenge_title: str, solution: Any):
        """
        Save the user's progress for a specific challenge.
        
        :param user_id: Unique identifier for the user
        :param challenge_title: Title of the challenge
        :param solution: User's solution to the challenge
        """
        self.progress[user_id] = {challenge_title: solution}
        with open('progress.json', 'w') as f:
            json.dump(self.progress, f)

    def load_progress(self, user_id: str) -> Dict[str, Any]:
        """
        Load the user's progress for a specific challenge.
        
        :param user_id: Unique identifier for the user
        :return: User's progress for the challenge
        """
        try:
            with open('progress.json', 'r') as f:
                self.progress = json.load(f)
            return self.progress.get(user_id, {})
        except FileNotFoundError:
            return {}

# Class to provide hints and feedback
class FeedbackSystem:
    def __init__(self):
        """
        Initialize the feedback system to provide hints and explanations.
        """
        self.hints = {
            "sorting": "Try using a built-in sorting function or implement a sorting algorithm like bubble sort.",
            "fibonacci": "Remember that each number is the sum of the two preceding ones."
        }

    def get_hint(self, challenge_title: str) -> str:
        """
        Get a hint for a specific challenge.
        
        :param challenge_title: Title of the challenge
        :return: Hint for the challenge
        """
        return self.hints.get(challenge_title, "No hints available for this challenge.")

# Example coding challenges
challenges = [
    CodingChallenge(
        title="Sorting Challenge",
        description="Sort a list of numbers.",
        test_cases=[
            ([[],], []),  # Edge case: empty list
            ([1, 2, 3, 2, 1], [1, 1, 2, 2, 3]),  # List with duplicates
            ([3, 1, 2], [1, 2, 3]),  # Normal case
            ([0, -1, 1], [-1, 0, 1])  # List with negative numbers
        ]
    ),
    CodingChallenge(
        title="Fibonacci Challenge",
        description="Calculate the nth Fibonacci number.",
        test_cases=[
            ([0], 0),  # Base case
            ([1], 1),  # Base case
            ([5], 5),  # Normal case
            ([10], 55)  # Larger case
        ]
    )
]

# Main function to simulate the platform
def main():
    user_session = UserSession()
    feedback_system = FeedbackSystem()

    # Simulate user interaction
    user_id = "user123"
    challenge = challenges[0]  # Selecting the first challenge

    print(f"Welcome to FamilyCodeQuest! Challenge: {challenge.title}")
    print(challenge.description)

    # Simulate user solution (this would be replaced with actual user input)
    user_solution = lambda lst: sorted(lst)  # Example user solution for sorting

    # Run tests and provide feedback
    results = challenge.run_tests(user_solution)
    for result in results:
        print(result)

    # Save progress
    user_session.save_progress(user_id, challenge.title, user_solution)

    # Load progress
    progress = user_session.load_progress(user_id)
    print(f"Loaded progress for {user_id}: {progress}")

    # Get a hint
    hint = feedback_system.get_hint(challenge.title)
    print(f"Hint: {hint}")

if __name__ == "__main__":
    main()