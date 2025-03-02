# language_collaborator.py

class User:
    """Represents a user in the LanguageCollaborator system."""
    
    def __init__(self, username, password):
        """
        Initializes a User object.

        Args:
            username (str): The username chosen by the user.
            password (str): The password chosen by the user.
        """
        self.username = username
        self.password = password
        self.exercises = []

    def create_exercise(self, exercise_type, content):
        """
        Creates a new exercise for the user.

        Args:
            exercise_type (str): The type of exercise (e.g., grammar quiz, vocabulary test, writing prompt).
            content (str): The content of the exercise.

        Returns:
            Exercise: The newly created Exercise object.
        """
        exercise = Exercise(exercise_type, content)
        self.exercises.append(exercise)
        return exercise

    def share_exercise(self, exercise, recipient):
        """
        Shares an exercise with another user.

        Args:
            exercise (Exercise): The exercise to be shared.
            recipient (User): The user to whom the exercise is being shared.
        """
        recipient.exercises.append(exercise)


class Exercise:
    """Represents an exercise in the LanguageCollaborator system."""
    
    def __init__(self, exercise_type, content):
        """
        Initializes an Exercise object.

        Args:
            exercise_type (str): The type of exercise (e.g., grammar quiz, vocabulary test, writing prompt).
            content (str): The content of the exercise.
        """
        self.exercise_type = exercise_type
        self.content = content
        self.feedback = []

    def provide_feedback(self, feedback):
        """
        Provides feedback on the exercise.

        Args:
            feedback (str): The feedback to be provided.
        """
        self.feedback.append(feedback)


class LanguageCollaborator:
    """Represents the LanguageCollaborator system."""
    
    def __init__(self):
        """
        Initializes the LanguageCollaborator system.
        """
        self.users = {}

    def register_user(self, username, password):
        """
        Registers a new user in the system.

        Args:
            username (str): The username chosen by the user.
            password (str): The password chosen by the user.

        Returns:
            User: The newly registered User object.
        """
        user = User(username, password)
        self.users[username] = user
        return user

    def login_user(self, username, password):
        """
        Logs in an existing user in the system.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            User: The logged-in User object, or None if the login fails.
        """
        if username in self.users and self.users[username].password == password:
            return self.users[username]
        else:
            return None

    def get_user(self, username):
        """
        Retrieves a user by their username.

        Args:
            username (str): The username of the user.

        Returns:
            User: The User object associated with the username, or None if not found.
        """
        return self.users.get(username)


def test_language_collaborator():
    """
    Tests the LanguageCollaborator system.
    """
    collaborator = LanguageCollaborator()

    # Register users
    user1 = collaborator.register_user("user1", "password1")
    user2 = collaborator.register_user("user2", "password2")

    # Login users
    logged_in_user1 = collaborator.login_user("user1", "password1")
    logged_in_user2 = collaborator.login_user("user2", "password2")

    # Create exercises
    exercise1 = user1.create_exercise("grammar quiz", "What is the correct form of the verb 'to be' in the present tense?")
    exercise2 = user2.create_exercise("vocabulary test", "What is the meaning of the word 'perspicacious'?")

    # Share exercises
    user1.share_exercise(exercise1, user2)
    user2.share_exercise(exercise2, user1)

    # Provide feedback
    exercise1.provide_feedback("Correct answer: 'is'")
    exercise2.provide_feedback("Correct answer: 'having a keen understanding and insight'")

    # Test exercise sharing and feedback
    assert exercise1 in user2.exercises
    assert exercise2 in user1.exercises
    assert "Correct answer: 'is'" in exercise1.feedback
    assert "Correct answer: 'having a keen understanding and insight'" in exercise2.feedback

    print("All tests passed.")


if __name__ == "__main__":
    test_language_collaborator()