# cultural_journey.py
# This is the main implementation file for the Cultural Journey system.

class CulturalJourney:
    """
    The CulturalJourney class represents the main system for exploring different cultures.
    It integrates various cultural elements into a single platform, allowing users to deepen their understanding of different traditions, customs, and cuisines from around the world.
    """

    def __init__(self):
        """
        Initializes the CulturalJourney system with the Quiz, Puzzle, and Recipe modules.
        """
        self.quiz_module = QuizModule()
        self.puzzle_module = PuzzleModule()
        self.recipe_module = RecipeModule()

    def start_quiz(self):
        """
        Starts the Quiz Module, allowing users to explore cultural traditions, customs, and festivals through multiple-choice questions.
        """
        print("Welcome to the Quiz Module!")
        self.quiz_module.display_questions()

    def start_puzzle(self):
        """
        Starts the Puzzle Module, allowing users to solve puzzles by matching pieces that represent different aspects of a culture.
        """
        print("Welcome to the Puzzle Module!")
        self.puzzle_module.display_puzzle()

    def start_recipe(self):
        """
        Starts the Recipe Module, allowing users to explore traditional dishes from different cultures.
        """
        print("Welcome to the Recipe Module!")
        self.recipe_module.display_recipe()

class QuizModule:
    """
    The QuizModule class represents the Quiz Module of the Cultural Journey system.
    It includes multiple-choice questions about cultural traditions, customs, and festivals.
    """

    def __init__(self):
        """
        Initializes the QuizModule with a list of questions and answers.
        """
        self.questions = [
            {
                "question": "What is the traditional New Year's celebration in China?",
                "options": ["Chinese New Year", "New Year's Eve", "Christmas"],
                "answer": "Chinese New Year"
            },
            {
                "question": "What is the traditional clothing worn by women in India?",
                "options": ["Sari", "Salwar Kameez", "Burqa"],
                "answer": "Sari"
            },
            {
                "question": "What is the traditional dish of Japan?",
                "options": ["Sushi", "Ramen", "Tempura"],
                "answer": "Sushi"
            }
        ]

    def display_questions(self):
        """
        Displays the questions and options to the user, allowing them to select an answer.
        """
        for question in self.questions:
            print(f"Question: {question['question']}")
            for option in question['options']:
                print(f"Option: {option}")
            answer = input("Enter your answer: ")
            if answer == question['answer']:
                print("Correct!")
            else:
                print(f"Incorrect. The correct answer is {question['answer']}")

class PuzzleModule:
    """
    The PuzzleModule class represents the Puzzle Module of the Cultural Journey system.
    It features cultural scenes and elements, allowing users to solve puzzles by matching pieces.
    """

    def __init__(self):
        """
        Initializes the PuzzleModule with a list of puzzle pieces.
        """
        self.puzzle_pieces = [
            {
                "name": "Traditional Clothing",
                "image": "sari.jpg"
            },
            {
                "name": "Landmark",
                "image": "taj_mahal.jpg"
            },
            {
                "name": "Animal",
                "image": "elephant.jpg"
            }
        ]

    def display_puzzle(self):
        """
        Displays the puzzle pieces to the user, allowing them to select and match pieces.
        """
        print("Welcome to the Puzzle Module!")
        for piece in self.puzzle_pieces:
            print(f"Piece: {piece['name']}")

class RecipeModule:
    """
    The RecipeModule class represents the Recipe Module of the Cultural Journey system.
    It allows users to explore traditional dishes from different cultures.
    """

    def __init__(self):
        """
        Initializes the RecipeModule with a list of recipes.
        """
        self.recipes = [
            {
                "name": "Sushi",
                "ingredients": ["Rice", "Fish", "Vegetables"],
                "instructions": ["Prepare the rice", "Prepare the fish", "Assemble the sushi"],
                "cultural_insights": ["Sushi is a traditional Japanese dish", "Sushi is often served with soy sauce and wasabi"]
            },
            {
                "name": "Tacos",
                "ingredients": ["Tortilla", "Meat", "Cheese"],
                "instructions": ["Prepare the tortilla", "Prepare the meat", "Assemble the taco"],
                "cultural_insights": ["Tacos are a traditional Mexican dish", "Tacos are often served with salsa and guacamole"]
            }
        ]

    def display_recipe(self):
        """
        Displays the recipe to the user, including ingredients, instructions, and cultural insights.
        """
        print("Welcome to the Recipe Module!")
        for recipe in self.recipes:
            print(f"Recipe: {recipe['name']}")
            print(f"Ingredients: {', '.join(recipe['ingredients'])}")
            print(f"Instructions: {', '.join(recipe['instructions'])}")
            print(f"Cultural Insights: {', '.join(recipe['cultural_insights'])}")

def main():
    """
    The main function initializes the CulturalJourney system and allows users to select a module to start.
    """
    cultural_journey = CulturalJourney()
    print("Welcome to the Cultural Journey system!")
    while True:
        print("Select a module to start:")
        print("1. Quiz Module")
        print("2. Puzzle Module")
        print("3. Recipe Module")
        print("4. Quit")
        choice = input("Enter your choice: ")
        if choice == "1":
            cultural_journey.start_quiz()
        elif choice == "2":
            cultural_journey.start_puzzle()
        elif choice == "3":
            cultural_journey.start_recipe()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()