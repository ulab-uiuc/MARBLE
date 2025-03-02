# solution.py
import threading
from datetime import datetime

# User class to store user information
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.exercises = []
def __init__(self, title, description, type, correct_answer=None):
    self.title = title
    self.description = description
    self.type = type
    self.answers = []
    self.reviews = []
    self.correct_answer = correct_answer
self.correct_answer = None

# Exercise class to store exercise information
class Exercise:
    def __init__(self, title, description, type):
        self.title = title
        self.description = description
        self.type = type
        self.answers = []
        self.reviews = []
        self.correct_answer = None

# LanguageCollaborator class to manage users and exercises
class LanguageCollaborator:
    def __init__(self):
        self.users = []
        self.exercises = []
        self.lock = threading.Lock()

    # Method to register a new user
    def register_user(self, username, password):def create_exercise(self, user, title, description, type, correct_answer=None):
    with self.lock:
        new_exercise = Exercise(title, description, type, correct_answer)
        user.exercises.append(new_exercise)
        self.exercises.append(new_exercise)
        return "Exercise created successfully"return "Exercise created successfully"

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
    def get_feedback(self, exercise):
        with self.lock:
            return exercise.reviews

    # Method to provide real-time feedback on an exercise
    def provide_real_time_feedback(self, exercise, answer):if exercise.type == "quiz":
    if answer == exercise.correct_answer:
        return "Correct answer"
    else:
        return "Incorrect answer"
elif exercise.type == "writing_prompt":
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(answer)
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    suggestions = []
    for token in filtered_tokens:
        # Use a dictionary or thesaurus API to get suggestions
        suggestions.append(token)
    return suggestionsreturn suggestions
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

# language_collaborator.py
class LanguageCollaboratorApp:
    def __init__(self):
        self.language_collaborator = LanguageCollaborator()

    def run(self):
        while True:
            print("1. Register a new user")
            print("2. Login a user")
            print("3. Create a new exercise")
            print("4. Share an exercise")
            print("5. Provide feedback on an exercise")
            print("6. Get feedback on an exercise")
            print("7. Provide real-time feedback on an exercise")
            print("8. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                username = input("Enter username: ")
                password = input("Enter password: ")
                print(self.language_collaborator.register_user(username, password))
            elif choice == "2":
                username = input("Enter username: ")
                password = input("Enter password: ")
                user = self.language_collaborator.login_user(username, password)
                if user:
                    print("Login successful")
                else:
                    print("Invalid username or password")
            elif choice == "3":
                username = input("Enter username: ")
                password = input("Enter password: ")
                user = self.language_collaborator.login_user(username, password)
                if user:
                    title = input("Enter exercise title: ")
                    description = input("Enter exercise description: ")
                    type = input("Enter exercise type: ")
                    print(self.language_collaborator.create_exercise(user, title, description, type))
                else:
                    print("Invalid username or password")
            elif choice == "4":
                username = input("Enter username: ")
                password = input("Enter password: ")
                user = self.language_collaborator.login_user(username, password)
                if user:
                    exercise_title = input("Enter exercise title: ")
                    exercise = self.language_collaborator.share_exercise(user, exercise_title)
                    if exercise:
                        print("Exercise shared successfully")
                    else:
                        print("Exercise not found")
                else:
                    print("Invalid username or password")
            elif choice == "5":
                username = input("Enter username: ")
                password = input("Enter password: ")
                user = self.language_collaborator.login_user(username, password)
                if user:
                    exercise_title = input("Enter exercise title: ")
                    exercise = self.language_collaborator.share_exercise(user, exercise_title)
                    if exercise:
                        feedback = input("Enter feedback: ")
                        print(self.language_collaborator.provide_feedback(user, exercise, feedback))
                    else:
                        print("Exercise not found")
                else:
                    print("Invalid username or password")
            elif choice == "6":
                username = input("Enter username: ")
                password = input("Enter password: ")
                user = self.language_collaborator.login_user(username, password)
                if user:
                    exercise_title = input("Enter exercise title: ")
                    exercise = self.language_collaborator.share_exercise(user, exercise_title)
                    if exercise:
                        print(self.language_collaborator.get_feedback(exercise))
                    else:
                        print("Exercise not found")
                else:
                    print("Invalid username or password")
            elif choice == "7":
                username = input("Enter username: ")
                password = input("Enter password: ")
                user = self.language_collaborator.login_user(username, password)
                if user:
                    exercise_title = input("Enter exercise title: ")
                    exercise = self.language_collaborator.share_exercise(user, exercise_title)
                    if exercise:
                        answer = input("Enter answer: ")
                        print(self.language_collaborator.provide_real_time_feedback(exercise, answer))
                    else:
                        print("Exercise not found")
                else:
                    print("Invalid username or password")
            elif choice == "8":
                break
            else:
                print("Invalid choice")

# Run the application
app = LanguageCollaboratorApp()
app.run()