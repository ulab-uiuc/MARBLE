# solution.py

# Cultural_Journey: A software system for exploring different cultures through quizzes, puzzles, and recipes.

class QuizModule:
    """A class to represent the Quiz Module of the Cultural Journey."""
    
    def __init__(self):
        """Initialize the quiz with a set of questions and answers."""
        self.questions = [
            {
                "question": "What is the traditional Japanese art of folding paper called?",
                "options": ["Origami", "Ikebana", "Calligraphy", "Sumi-e"],
                "answer": "Origami"
            },
            {
                "question": "Which festival is known as the Festival of Lights?",
                "options": ["Diwali", "Holi", "Eid", "Christmas"],
                "answer": "Diwali"
            },
            {
                "question": "What is the main ingredient in traditional sushi?",
                "options": ["Rice", "Noodles", "Fish", "Seaweed"],
                "answer": "Rice"
            }
        ]
    
    def take_quiz(self):
        """Conduct the quiz and return the score."""
        score = 0
        for q in self.questions:
            print(q["question"])
            for idx, option in enumerate(q["options"], start=1):
                print(f"{idx}. {option}")            while True:
                answer = input("Select the correct option (1-{}): ".format(len(q["options"])))
                if answer.isdigit() and 1 <= int(answer) <= len(q["options"]):
                    if q["options"][int(answer) - 1] == q["answer"]:
                        score += 1
                        print("Correct!\n")
                    else:
                        print(f"Wrong! The correct answer is: {q['answer']}\n")
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and {}.".format(len(q["options"])))        print(f"Your final score is: {score}/{len(self.questions)}")
        return score


class PuzzleModule:
    """A class to represent the Puzzle Module of the Cultural Journey."""
    
    def __init__(self):
        """Initialize the puzzle with cultural scenes."""
        self.puzzles = [
            {
                "scene": "Traditional Japanese Tea Ceremony",
                "pieces": ["Tea Set", "Tatami Mat", "Kimono", "Chaji"],
                "solution": "Tea Set, Tatami Mat, Kimono, Chaji"
            },
            {
                "scene": "Mexican Day of the Dead",
                "pieces": ["Sugar Skull", "Marigold Flowers", "Cempasuchil", "Ofrenda"],
                "solution": "Sugar Skull, Marigold Flowers, Cempasuchil, Ofrenda"
            }
        ]
    
    def solve_puzzle(self):
        """Simulate solving a puzzle by matching pieces."""
        for puzzle in self.puzzles:
            print(f"Puzzle Scene: {puzzle['scene']}")
            print("Available pieces:")
            for piece in puzzle["pieces"]:
                print(f"- {piece}")
            input("Press Enter to see the solution...")
            print(f"Solution: {puzzle['solution']}\n")


class RecipeModule:
    """A class to represent the Recipe Module of the Cultural Journey."""
    
    def __init__(self):
        """Initialize the recipe with traditional dishes."""
        self.recipes = {
            "Sushi": {
                "ingredients": ["Sushi Rice", "Nori", "Fresh Fish", "Vegetables"],
                "instructions": "1. Cook the sushi rice. 2. Prepare the fillings. 3. Roll the sushi.",
                "cooking_tips": "Use fresh ingredients for the best flavor.",
                "cultural_insight": "Sushi is a traditional Japanese dish that has gained worldwide popularity."
            },
            "Tacos": {
                "ingredients": ["Taco Shells", "Ground Beef", "Lettuce", "Tomato", "Cheese"],
                "instructions": "1. Cook the beef. 2. Fill the taco shells. 3. Add toppings.",
                "cooking_tips": "Use a variety of toppings for a more flavorful taco.",
                "cultural_insight": "Tacos are a staple of Mexican cuisine and come in many varieties."
            }
        }
    
    def explore_recipes(self):
        """Allow users to explore recipes."""
        for dish, details in self.recipes.items():
            print(f"\nDish: {dish}")
            print("Ingredients:", ", ".join(details["ingredients"]))
            print("Instructions:", details["instructions"])
            print("Cooking Tips:", details["cooking_tips"])
            print("Cultural Insight:", details["cultural_insight"])


def main():
    """Main function to run the Cultural Journey program."""
    print("Welcome to Cultural Journey!")
    
    # Initialize modules
    quiz = QuizModule()
    puzzle = PuzzleModule()
    recipe = RecipeModule()
    
    # Run the quiz module
    print("Starting the Quiz Module...")
    quiz.take_quiz()
    
    # Run the puzzle module
    print("\nStarting the Puzzle Module...")
    puzzle.solve_puzzle()
    
    # Run the recipe module
    print("\nStarting the Recipe Module...")
    recipe.explore_recipes()


if __name__ == "__main__":
    main()