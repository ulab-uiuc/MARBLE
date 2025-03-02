# cultural_journey.py

class CulturalJourney:
    def __init__(self):
        self.quiz_module = QuizModule()
        self.puzzle_module = PuzzleModule()
        self.recipe_module = RecipeModule()def start_journey(self):
        print("Welcome to Cultural Journey!")
        if self.quiz_module.start_quiz():
            if self.puzzle_module.start_puzzle():
                self.recipe_module.start_recipe()

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
            },def start_quiz(self):
        print("Quiz Module Started!")
        score = 0
        for question, options in self.questions.items():
            print(question)
            for option, value in options.items():
                if option != "Answer":
                    print(f"{option}: {value}")
            answer = input("Enter your answer: ")
            if answer.upper() == options["Answer"]:
                print("Correct!")
                score += 1
            else:
                print(f"Sorry, the correct answer is {options['Answer']}.")
        print(f"Quiz finished! Your score is {score} out of {len(self.questions)}")
        return score >= len(self.questions) / 2
            "What is the main festival of India?": {
                "A": "Diwali",
                "B": "Holi",
                "C": "Navratri",
                "D": "Eid al-Fitr",
                "Answer": "A"
            },
            "What is the traditional music of China?": {
                "A": "Pipa",
                "B": "Erhu",
                "C": "Guzheng",
                "D": "Dizi",
                "Answer": "B"
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
                print("Correct!")
                score += 1
            else:
                print(f"Sorry, the correct answer is {options['Answer']}.")
        print(f"Quiz finished! Your score is {score} out of {len(self.questions)}")


# puzzle_module.py

class PuzzleModule:
    def __init__(self):
        self.puzzles = {
            "Puzzle 1": {
                "pieces": ["piece1", "piece2", "piece3", "piece4"],
                "solution": ["piece1", "piece2", "piece3", "piece4"]
            },def start_puzzle(self):
        print("Puzzle Module Started!")
        score = 0
        for puzzle, details in self.puzzles.items():
            print(puzzle)
            print("Pieces:")
            for piece in details["pieces"]:
                print(piece)
            user_solution = input("Enter your solution (comma-separated): ").split(",")
            if user_solution == details["solution"]:
                print("Correct!")
                score += 1
            else:
                print(f"Sorry, the correct solution is {', '.join(details['solution'])}.")
        print(f"Puzzle finished! Your score is {score} out of {len(self.puzzles)}")
        return score >= len(self.puzzles) / 2
            "Puzzle 2": {
                "pieces": ["piece5", "piece6", "piece7", "piece8"],
                "solution": ["piece5", "piece6", "piece7", "piece8"]
            }
        }

    def start_puzzle(self):
        print("Puzzle Module Started!")
        for puzzle, details in self.puzzles.items():
            print(puzzle)
            print("Pieces:")
            for piece in details["pieces"]:
                print(piece)
            user_solution = input("Enter your solution (comma-separated): ").split(",")
            if user_solution == details["solution"]:
                print("Correct!")
            else:
                print(f"Sorry, the correct solution is {', '.join(details['solution'])}.")


# recipe_module.py

class RecipeModule:
    def __init__(self):
        self.recipes = {
            "Recipe 1": {
                "name": "Sushi",
                "ingredients": ["rice", "fish", "seaweed"],
                "instructions": ["Prepare the rice", "Prepare the fish", "Assemble the sushi"],
                "cultural_insight": "Sushi is a traditional Japanese dish that originated in ancient times."
            },
            "Recipe 2": {
                "name": "Tacos",
                "ingredients": ["tortillas", "meat", "cheese"],
                "instructions": ["Prepare the tortillas", "Prepare the meat", "Assemble the tacos"],
                "cultural_insight": "Tacos are a traditional Mexican dish that originated in the central region of Mexico."
            }
        }

    def start_recipe(self):
        print("Recipe Module Started!")
        for recipe, details in self.recipes.items():
            print(recipe)
            print("Name:", details["name"])
            print("Ingredients:")
            for ingredient in details["ingredients"]:
                print(ingredient)
            print("Instructions:")
            for instruction in details["instructions"]:
                print(instruction)
            print("Cultural Insight:", details["cultural_insight"])


# main.py

if __name__ == "__main__":
    cultural_journey = CulturalJourney()
    cultural_journey.start_journey()