# solution.py
import threading
from datetime import datetimeclass User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.exercises = []    def __init__(self, title, description, type, correct_answers=None, expected_grammar=None, expected_vocabulary=None):
        self.title = title
        self.description = description
        self.type = type
        self.answers = []
        self.reviews = []
        self.correct_answers = correct_answers
        self.expected_grammar = expected_grammar
        self.expected_vocabulary = expected_vocabulary    def __init__(self, title, description, type):
        self.title = title
        self.description = description
        self.type = type
        self.answers = []
        self.reviews = []

# LanguageCollaborator class to manage users and exercises
class LanguageCollaborator:
    def __init__(self):
        self.users = []
        self.exercises = []
        self.lock = threading.Lock()

    # Method to register a new user
    def register_user(self, username, password):
        with self.lock:
            for user in self.users:
                if user.username == username:
                    return "Username already exists"
            new_user = User(username, password)
            self.users.append(new_user)
            return "User registered successfully"

    # Method to login a user
    def login_user(self, username, password):
        with self.lock:
            for user in self.users:
                if user.username == username and user.password == password:
                    return user
            return "Invalid username or password"

    # Method to create a new exercise
    def create_exercise(self, user, title, description, type):
        with self.lock:
            new_exercise = Exercise(title, description, type)
            user.exercises.append(new_exercise)
            self.exercises.append(new_exercise)
            return "Exercise created successfully"

    # Method to share an exercise
    def share_exercise(self, user, exercise_title):
        with self.lock:
            for exercise in user.exercises:
                if exercise.title == exercise_title:
                    return exercise
            return "Exercise not found"

    # Method to provide feedback on an exercise
    def provide_feedback(self, user, exercise, feedback):
        with self.lock:
            exercise.reviews.append((user.username, feedback))
            return "Feedback provided successfully"

    # Method to get feedback on an exercise
    def get_feedback(self, exercise):def provide_real_time_feedback(self, exercise, answer):
    with self.lock:
        if exercise.type == "quiz":
            if answer in exercise.correct_answers:
                return "Correct answer"
            else:
                return f"Incorrect answer. The correct answer is {exercise.correct_answers[0]}"
        elif exercise.type == "writing_prompt":
            # Provide grammar/vocabulary suggestions
            grammar_suggestions = []
            vocabulary_suggestions = []
            for word in answer.split():
                if word not in exercise.expected_vocabulary:
                    vocabulary_suggestions.append(word)
                if word not in exercise.expected_grammar:
                    grammar_suggestions.append(word)
            return f"Grammar suggestions: {grammar_suggestions}, Vocabulary suggestions: {vocabulary_suggestions}"        if exercise.type == "quiz":
                # Provide correct/incorrect answer feedback
                if answer == "correct":
                    return "Correct answer"
                else:
                    return "Incorrect answer"
            elif exercise.type == "writing_prompt":
                # Provide grammar/vocabulary suggestions
                return "Grammar and vocabulary suggestions"

# Test cases
def test_language_collaborator():
    language_collaborator = LanguageCollaborator()

    # Test case 1: Register a new user
    print(language_collaborator.register_user("user1", "password1"))

    # Test case 2: Login a user
    user1 = language_collaborator.login_user("user1", "password1")
    print(user1.username)

    # Test case 3: Create a new exercise
    print(language_collaborator.create_exercise(user1, "Exercise 1", "Description 1", "quiz"))

    # Test case 4: Share an exercise
    exercise1 = language_collaborator.share_exercise(user1, "Exercise 1")
    print(exercise1.title)

    # Test case 5: Provide feedback on an exercise
    print(language_collaborator.provide_feedback(user1, exercise1, "Good job"))

    # Test case 6: Get feedback on an exercise
    print(language_collaborator.get_feedback(exercise1))

    # Test case 7: Provide real-time feedback on an exercise
    print(language_collaborator.provide_real_time_feedback(exercise1, "correct"))

# Run test cases
test_language_collaborator()

# Test case for multiple users
def test_multiple_users():
    language_collaborator = LanguageCollaborator()

    # Test case 1: Register multiple users
    print(language_collaborator.register_user("user1", "password1"))
    print(language_collaborator.register_user("user2", "password2"))

    # Test case 2: Login multiple users
    user1 = language_collaborator.login_user("user1", "password1")
    user2 = language_collaborator.login_user("user2", "password2")
    print(user1.username)
    print(user2.username)

    # Test case 3: Create exercises for multiple users
    print(language_collaborator.create_exercise(user1, "Exercise 1", "Description 1", "quiz"))
    print(language_collaborator.create_exercise(user2, "Exercise 2", "Description 2", "writing_prompt"))

    # Test case 4: Share exercises among multiple users
    exercise1 = language_collaborator.share_exercise(user1, "Exercise 1")
    exercise2 = language_collaborator.share_exercise(user2, "Exercise 2")
    print(exercise1.title)
    print(exercise2.title)

    # Test case 5: Provide feedback on exercises among multiple users
    print(language_collaborator.provide_feedback(user1, exercise2, "Good job"))
    print(language_collaborator.provide_feedback(user2, exercise1, "Well done"))

# Run test case for multiple users
test_multiple_users()

# Test case for edge cases
def test_edge_cases():
    language_collaborator = LanguageCollaborator()

    # Test case 1: Handle invalid input
    print(language_collaborator.register_user("user1", ""))

    # Test case 2: Handle simultaneous actions from multiple users
    user1 = language_collaborator.login_user("user1", "password1")
    user2 = language_collaborator.login_user("user2", "password2")
    exercise1 = language_collaborator.share_exercise(user1, "Exercise 1")
    exercise2 = language_collaborator.share_exercise(user2, "Exercise 2")
    print(language_collaborator.provide_feedback(user1, exercise2, "Good job"))
    print(language_collaborator.provide_feedback(user2, exercise1, "Well done"))

    # Test case 3: Handle scenarios where no peer reviews are available
    print(language_collaborator.get_feedback(exercise1))

# Run test case for edge cases
test_edge_cases()