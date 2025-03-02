# family_code_quest.py

class User:
    """Represents a user in the FamilyCodeQuest platform."""
    
    def __init__(self, username):
        """Initializes a User object with a username."""
        self.username = username
        self.challenges = {}  # Stores the challenges the user is working on

    def join_challenge(self, challenge):
        """Adds a challenge to the user's list of challenges."""
        self.challenges[challenge.name] = challenge

    def save_progress(self):
        """Saves the user's progress in all challenges."""
        for challenge in self.challenges.values():
            challenge.save_progress(self.username)

    def load_progress(self):
        """Loads the user's progress in all challenges."""
        for challenge in self.challenges.values():
            challenge.load_progress(self.username)


class Challenge:
    """Represents a coding challenge in the FamilyCodeQuest platform."""
    
    def __init__(self, name, instructions, test_cases):
        """Initializes a Challenge object with a name, instructions, and test cases."""
        self.name = name
        self.instructions = instructions
        self.test_cases = test_cases
        self.progress = {}  # Stores the progress of users in this challenge

    def save_progress(self, username):
        """Saves the progress of a user in this challenge."""
        # For simplicity, we assume the progress is stored in a file
        with open(f"{username}_{self.name}_progress.txt", "w") as f:
            f.write(self.progress.get(username, ""))

    def load_progress(self, username):
        """Loads the progress of a user in this challenge."""
        try:
            with open(f"{username}_{self.name}_progress.txt", "r") as f:
                self.progress[username] = f.read()
        except FileNotFoundError:
            self.progress[username] = ""

    def check_solution(self, solution, username):
        """Checks if a user's solution is correct."""
        for test_case in self.test_cases:
            input_scenario, expected_output = test_case
            if solution(input_scenario) != expected_output:
                return False
        return True

    def provide_feedback(self, solution, username):
        """Provides feedback to a user if their solution is incorrect."""
        for test_case in self.test_cases:
            input_scenario, expected_output = test_case
            if solution(input_scenario) != expected_output:
                print(f"Hint: Your solution failed on the input scenario {input_scenario}.")
                print(f"Expected output: {expected_output}")
                print(f"Your output: {solution(input_scenario)}")
                return


class FamilyCodeQuest:def submit_solution(self, username, challenge_name, solution):    user = self.users.get(username)
        challenge = self.challenges.get(challenge_name)
        if user and challenge:if challenge.check_solution(solution, username):
user.join_challenge(challenge)
        if challenge_name in user.challenges:
                print(f"Solution for challenge '{challenge_name}' is correct!")
        else:
            else:
                challenge.provide_feedback(solution, username)
        else:
            print("User or challenge not found.")


# Example usage:

# Create challenges
challenge1 = Challenge("Sorting Challenge", "Sort a list of numbers in ascending order.", [
    ([3, 2, 1], [1, 2, 3]),
    ([], []),
    ([5, 5, 5], [5, 5, 5]),
    ([-1, 0, 1], [-1, 0, 1])
])

challenge2 = Challenge("Math Challenge", "Calculate the sum of two numbers.", [
    ((1, 2), 3),
    ((0, 0), 0),
    ((-1, 1), 0)
])

# Create users
user1 = User("Alice")
user2 = User("Bob")

# Create the FamilyCodeQuest platform
platform = FamilyCodeQuest()
platform.add_user("Alice")
platform.add_user("Bob")
platform.add_challenge(challenge1)
platform.add_challenge(challenge2)

# Start challenges
platform.start_challenge("Alice", "Sorting Challenge")
platform.start_challenge("Bob", "Math Challenge")

# Submit solutions
def sorting_solution(numbers):
    return sorted(numbers)

def math_solution(numbers):
    return numbers[0] + numbers[1]

platform.submit_solution("Alice", "Sorting Challenge", sorting_solution)
platform.submit_solution("Bob", "Math Challenge", math_solution)