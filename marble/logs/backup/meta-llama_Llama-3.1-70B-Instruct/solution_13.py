# cultural_journey.py

class CulturalJourney:
    def __init__(self):
        self.quiz_module = QuizModule()
        self.puzzle_module = PuzzleModule()
        self.recipe_module = RecipeModule()def start_journey(self):
        print("Welcome to Cultural Journey!")
        self.menu()
def menu(self):
        while True:
            print("\nCultural Journey Menu:\n")
            print("1. Quiz Module")
            print("2. Puzzle Module")
            print("3. Recipe Module")
            print("4. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.quiz_module.start_quiz()
            elif choice == "2":
                self.puzzle_module.start_puzzle()
            elif choice == "3":
                self.recipe_module.start_recipe()
            elif choice == "4":
                print("Thank you for using Cultural Journey!")
                break
            else:
                print("Invalid choice. Please try again.")

    def start_journey(self):
        print("Welcome to Cultural Journey!")
        self.quiz_module.start_quiz()
        self.puzzle_module.start_puzzle()
        self.recipe_module.start_recipe()


# quiz_module.py

class QuizModule:
    def __init__(self):
        self.questions = {
            "What is the traditional clothing of Japan?": {
                "A": "Kimono",
                "B": "Sari",
                "C": "Cheongsam",
                "D": "Kaftan",
                "Answer": "A"
            },
            "Which festival is celebrated as the 'Festival of Lights' in India?": {
                "A": "Diwali",
                "B": "Holi",
                "C": "Navratri",
                "D": "Ganesh Chaturthi",
                "Answer": "A"
            },
            "What is the name of the traditional tea ceremony in China?": {
                "A": "Chanoyu",
                "B": "Sado",
                "C": "Gongfu",
                "D": "Jasmine",
                "Answer": "C"
            }
        }

    def start_quiz(self):
        print("Quiz Module Started!")
        score = 0
        for question, options in self.questions.items():
            print(question)
            for option, value in options.items():
                if option != "Answer":
                    print(f"{option}: {value}")
            answer = input("Enter your answer: ")
            if answer.upper() == options["Answer"]:
                print("Correct answer!")
                score += 1
            else:
                print(f"Wrong answer! The correct answer is {options['Answer']}.")
        print(f"Quiz finished! Your final score is {score} out of {len(self.questions)}.")


# puzzle_module.py

class PuzzleModule:
    def __init__(self):
        self.puzzles = {
            "Traditional Japanese clothing": {
                "pieces": ["Kimono", "Obi", "Geta", "Hakama"],
                "solution": ["Kimono", "Obi", "Geta", "Hakama"]
            },
            "Indian festival": {
                "pieces": ["Diwali", "Lamp", "Fireworks", "Sweets"],
                "solution": ["Diwali", "Lamp", "Fireworks", "Sweets"]
            },
            "Chinese tea ceremony": {
                "pieces": ["Tea", "Teapot", "Cups", "Table"],
                "solution": ["Tea", "Teapot", "Cups", "Table"]
            }
        }

    def start_puzzle(self):
        print("Puzzle Module Started!")
        for puzzle, details in self.puzzles.items():
            print(puzzle)
            print("Pieces:")
            for piece in details["pieces"]:
                print(piece)
            solution = input("Enter the correct order of pieces (separated by comma): ")
            solution = solution.split(",")
            solution = [piece.strip() for piece in solution]
            if solution == details["solution"]:
                print("Correct solution!")
            else:
                print(f"Wrong solution! The correct solution is {', '.join(details['solution'])}.")


# recipe_module.py

class RecipeModule:
    def __init__(self):
        self.recipes = {
            "Sushi (Japan)": {
                "ingredients": ["Rice", "Nori", "Salmon", "Avocado"],
                "instructions": ["Prepare rice", "Cut nori", "Slice salmon", "Assemble sushi"],
                "tips": ["Use short-grain rice", "Handle nori sheets carefully"],
                "cultural_insight": "Sushi is a traditional Japanese dish that originated in ancient times."
            },
            "Tandoori Chicken (India)": {
                "ingredients": ["Chicken", "Yogurt", "Spices", "Tandoor"],
                "instructions": ["Marinate chicken", "Grill in tandoor", "Serve with naan"],
                "tips": ["Use a mixture of spices", "Cook in a tandoor oven"],
                "cultural_insight": "Tandoori chicken is a popular Indian dish that originated in the Mughal Empire."
            },
            "Dumplings (China)": {
                "ingredients": ["Dough", "Pork", "Vegetables", "Soy sauce"],
                "instructions": ["Prepare dough", "Fill with pork and vegetables", "Steam dumplings"],
                "tips": ["Use a mixture of pork and vegetables", "Steam dumplings carefully"],
                "cultural_insight": "Dumplings are a traditional Chinese dish that dates back to the Eastern Han dynasty."
            }
        }

    def start_recipe(self):
        print("Recipe Module Started!")
        for recipe, details in self.recipes.items():
            print(recipe)
            print("Ingredients:")
            for ingredient in details["ingredients"]:
                print(ingredient)
            print("Instructions:")
            for instruction in details["instructions"]:
                print(instruction)
            print("Tips:")
            for tip in details["tips"]:
                print(tip)
            print("Cultural Insight:")
            print(details["cultural_insight"])


# main.py

if __name__ == "__main__":
    journey = CulturalJourney()
    journey.start_journey()