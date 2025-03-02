class User:
    def __init__(self, username):
        self.username = username
        self.exercises = []

    def create_exercise(self, exercise):
        self.exercises.append(exercise)

    def share_exercise(self, exercise, user):
        user.exercises.append(exercise)
        print(f"{self.username} shared an exercise with {user.username}")

    def provide_feedback(self, exercise, feedback):
        exercise.feedback = feedback
        print(f'{self.username} reviewed an exercise and provided feedback')
        exercise.feedback = feedback
        print(f"{self.username} provided feedback on an exercise")


class Exercise:
    def __init__(self, content):
        self.content = content
        self.feedback = None


# Test Cases
# Input scenarios
user1 = User("Alice")
user2 = User("Bob")

exercise1 = Exercise("Grammar quiz")
exercise2 = Exercise("Vocabulary test")

user1.create_exercise(exercise1)
user2.create_exercise(exercise2)

user1.share_exercise(exercise1, user2)

# Expected outputs
user2.provide_feedback(exercise1, "Good job on the quiz!")

# Edge cases
# Handling invalid input
try:
    user1.share_exercise(exercise3, user2)
except NameError:
    print("Exercise not found.")

# Simultaneous actions
user1.share_exercise(exercise2, user2)
user2.provide_feedback(exercise2, "Nice vocabulary test!")

# No peer reviews available
exercise3 = Exercise("Writing prompt")
user1.create_exercise(exercise3)
print("No peer reviews available for the writing prompt exercise.")