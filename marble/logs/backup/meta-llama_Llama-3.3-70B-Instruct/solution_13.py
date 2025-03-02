# solution.py

# Importing necessary libraries
import random

# Cultural_Journey class
class Cultural_Journey:
    def __init__(self):
        # Initialize quiz, puzzle, and recipe modules
        self.quiz_module = Quiz_Module()
        self.puzzle_module = Puzzle_Module()
        self.recipe_module = Recipe_Module()

    # Method to start the cultural journey
    def start_journey(self):
        print("Welcome to Cultural Journey!")
        print("Please select a module to explore:")
        print("1. Quiz Module")
        print("2. Puzzle Module")
        print("3. Recipe Module")
        
        choice = input("Enter your choice (1/2/3): ")
        
        if choice == "1":
            self.quiz_module.start_quiz()
        elif choice == "2":
            self.puzzle_module.start_puzzle()
        elif choice == "3":
            self.recipe_module.start_recipe()
        else:
            print("Invalid choice. Please try again.")

# Quiz_Module class
class Quiz_Module:
    def __init__(self):
        # Initialize quiz questions and answers
        self.questions = {
            "What is the traditional Japanese New Year's food?": ["Sushi", "Ramen", "Mochi", "Tempura"],
            "Which Indian festival is known as the 'Festival of Lights'?": ["Diwali", "Holi", "Navratri", "Ganesh Chaturthi"],
            "What is the name of the traditional Chinese lion dance?": ["Dragon Dance", "Lion Dance", "Tiger Dance", "Snake Dance"]
        }
        self.answers = {
            "What is the traditional Japanese New Year's food?": "Mochi",
            "Which Indian festival is known as the 'Festival of Lights'?": "Diwali",
            "What is the name of the traditional Chinese lion dance?": "Lion Dance"
        }

    # Method to start the quiz
    def start_quiz(self):
        print("Welcome to the Quiz Module!")
        score = 0
        for question, options in self.questions.items():
            print(question)
            for i, option in enumerate(options):
                print(f"{i+1}. {option}")
            answer = input("Enter the correct answer (1/2/3/4): ")
            if options[int(answer) - 1] == self.answers[question]:
                print("Correct answer!")
                score += 1
            else:
                print(f"Sorry, the correct answer is {self.answers[question]}.")
        print(f"Your final score is {score} out of {len(self.questions)}.")

# Puzzle_Module class
class Puzzle_Module:
    def __init__(self):
        # Initialize puzzle piecesself.pieces = {        self.pieces = {
            "Traditional Japanese clothing": {"Kimono": "A traditional Japanese garment", "Yukata": "A lightweight summer kimono", "Hakama": "A traditional Japanese skirt", "Obi": "A sash worn with a kimono"},
            "Indian landmarks": {"Taj Mahal": "A white marble mausoleum", "Red Fort": "A historic fort in Delhi", "Qutub Minar": "The tallest minaret in India", "India Gate": "A war memorial in New Delhi"},
            "Chinese animals": {"Dragon": "A mythical creature", "Panda": "A bear native to China", "Tiger": "A large cat", "Snake": "A reptile"}
        }        }
    # Method to start the puzzle
    def start_puzzle(self):
        print("Welcome to the Puzzle Module!")score = 0
        for category, pieces in self.pieces.items():
            print(category)
            print("Match the following pieces to their descriptions:")
            for i, (piece, description) in enumerate(pieces.items()):
                print(f"{i+1}. {piece}")
            for i, (piece, description) in enumerate(pieces.items()):
                answer = input(f"Enter the description for {piece}: ")
                if answer.lower() == description.lower():
                    print("Correct match!")
                    score += 1
                else:
                    print(f"Sorry, the correct description is {description}.")print(f"Your final score is {score} out of {len(self.pieces)}.")

# Recipe_Module class
class Recipe_Module:
    def __init__(self):
        # Initialize recipes
        self.recipes = {
            "Japanese Sushi": {
                "ingredients": ["Rice", "Nori", "Salmon", "Avocado"],
                "instructions": ["Prepare the rice", "Cut the nori", "Assemble the sushi", "Serve"],
                "tips": ["Use short-grain rice", "Handle the nori gently", "Add wasabi and soy sauce for flavor"]
            },
            "Indian Chicken Tikka Masala": {
                "ingredients": ["Chicken", "Yogurt", "Spices", "Tomato sauce"],
                "instructions": ["Marinate the chicken", "Grill the chicken", "Make the tomato sauce", "Serve"],
                "tips": ["Use boneless chicken", "Add cumin and coriander for flavor", "Serve with basmati rice"]
            },
            "Chinese Kung Pao Chicken": {
                "ingredients": ["Chicken", "Peanuts", "Vegetables", "Soy sauce"],
                "instructions": ["Stir-fry the chicken", "Add the peanuts and vegetables", "Season with soy sauce", "Serve"],
                "tips": ["Use Sichuan peppercorns for flavor", "Add chili peppers for spice", "Serve with steamed rice"]
            }
        }

    # Method to start the recipe exploration
    def start_recipe(self):
        print("Welcome to the Recipe Module!")
        for recipe, details in self.recipes.items():
            print(recipe)
            print("Ingredients:")
            for ingredient in details["ingredients"]:
                print(f"- {ingredient}")
            print("Instructions:")
            for i, instruction in enumerate(details["instructions"]):
                print(f"{i+1}. {instruction}")
            print("Tips:")
            for tip in details["tips"]:
                print(f"- {tip}")
            input("Press Enter to continue to the next recipe...")

# Main function
def main():
    cultural_journey = Cultural_Journey()
    cultural_journey.start_journey()

# Run the main function
if __name__ == "__main__":
    main()