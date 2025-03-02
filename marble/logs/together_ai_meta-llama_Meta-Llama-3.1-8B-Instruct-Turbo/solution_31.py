# language_collaborator.py
# This is the main implementation of the LanguageCollaborator program.

class User:
    """Represents a user in the LanguageCollaborator system."""
    
    def __init__(self, username, password):
        """
        Initializes a User object.
        
        Args:
            username (str): The username of the user.
            password (str): The password of the user.
        """
        self.username = username
        self.password = password
        self.exercises = []
        self.reviews = []

class Exercise:
    """Represents a language exercise in the LanguageCollaborator system."""
    
    def __init__(self, title, type, content):
        """
        Initializes an Exercise object.
        
        Args:
            title (str): The title of the exercise.
            type (str): The type of the exercise (e.g., grammar quiz, vocabulary test, writing prompt).
            content (str): The content of the exercise.
        """
        self.title = title
        self.type = type
        self.content = content
        self.feedback = None

class LanguageCollaborator:
    """Represents the LanguageCollaborator system."""
    
    def __init__(self):
        """
        Initializes a LanguageCollaborator object.
        """
        self.users = {}
        self.exercises = {}

    def login(self, username, password):
        """
        Logs in a user.
        
        Args:
            username (str): The username of the user.
            password (str): The password of the user.
        
        Returns:
            bool: True if the user is logged in successfully, False otherwise.
        """
        if username in self.users and self.users[username].password == password:
            return True
        return False

    def create_exercise(self, username, title, type, content):
        """
        Creates a new exercise.
        
        Args:
            username (str): The username of the user creating the exercise.
            title (str): The title of the exercise.
            type (str): The type of the exercise.
            content (str): The content of the exercise.
        
        Returns:
            Exercise: The created exercise.
        """
        exercise = Exercise(title, type, content)
        self.exercises[username] = exercise
        self.users[username].exercises.append(exercise)
        return exercise

    def share_exercise(self, username, exercise_title):
        """
        Shares an exercise with other users.
        
        Args:
            username (str): The username of the user sharing the exercise.
            exercise_title (str): The title of the exercise to be shared.
        
        Returns:
            bool: True if the exercise is shared successfully, False otherwise.
        """
        if username in self.exercises and exercise_title in [e.title for e in self.exercises[username].exercises]:
            for user in self.users:
                if user != username:
                    self.users[user].exercises.append(self.exercises[username].exercises[0])
            return True
        return False

    def provide_feedback(self, username, exercise_title, feedback):
        """
        Provides feedback on an exercise.
        
        Args:
            username (str): The username of the user providing the feedback.
            exercise_title (str): The title of the exercise to be reviewed.
            feedback (str): The feedback to be provided.
        
        Returns:
            bool: True if the feedback is provided successfully, False otherwise.
        """
        if username in self.exercises and exercise_title in [e.title for e in self.exercises[username].exercises]:
            for exercise in self.exercises[username].exercises:
                if exercise.title == exercise_title:
                    exercise.feedback = feedback
                    return True
        return False

    def review_exercise(self, username, exercise_title):
        """
        Reviews an exercise.
        
        Args:
            username (str): The username of the user reviewing the exercise.
            exercise_title (str): The title of the exercise to be reviewed.
        
        Returns:
            str: The feedback on the exercise.
        """
        if username in self.exercises and exercise_title in [e.title for e in self.exercises[username].exercises]:
            for exercise in self.exercises[username].exercises:
                if exercise.title == exercise_title:
                    return exercise.feedback
        return None

def main():
    # Create a LanguageCollaborator object
    collaborator = LanguageCollaborator()

    # Create users
    user1 = User("user1", "password1")
    user2 = User("user2", "password2")
    collaborator.users["user1"] = user1
    collaborator.users["user2"] = user2

    # Create exercises
    exercise1 = collaborator.create_exercise("user1", "Exercise 1", "grammar quiz", "This is a grammar quiz.")
    exercise2 = collaborator.create_exercise("user2", "Exercise 2", "vocabulary test", "This is a vocabulary test.")

    # Share exercises
    collaborator.share_exercise("user1", "Exercise 1")
    collaborator.share_exercise("user2", "Exercise 2")

    # Provide feedback
    collaborator.provide_feedback("user1", "Exercise 1", "Great job!")
    collaborator.provide_feedback("user2", "Exercise 2", "Good effort!")

    # Review exercises
    print(collaborator.review_exercise("user1", "Exercise 1"))  # Output: Great job!
    print(collaborator.review_exercise("user2", "Exercise 2"))  # Output: Good effort!

if __name__ == "__main__":
    main()