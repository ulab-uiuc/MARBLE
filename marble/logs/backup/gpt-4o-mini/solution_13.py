# solution.py

# Cultural_Journey: A software system for exploring different cultures through quizzes, puzzles, and recipes.

class QuizModule:
    """A module for conducting quizzes about cultural traditions, customs, and festivals."""
    
    def __init__(self):
        # Initialize a list to hold quiz questions and answers
        self.questions = []
    
    def add_question(self, question, options, correct_answer):
        """Add a question to the quiz.
        
        Args:
            question (str): The quiz question.
            options (list): A list of answer options.
            correct_answer (str): The correct answer from the options.
        """
        self.questions.append({
            'question': question,
            'options': options,
            'correct_answer': correct_answer
        })
    
    def take_quiz(self):
        """Conduct the quiz and return the score."""
        score = 0
        for q in self.questions:
            print(q['question'])
            for idx, option in enumerate(q['options']):
                print(f"{idx + 1}. {option}")
            answer = input("Select the correct option (1-4): ")
            if q['options'][int(answer) - 1] == q['correct_answer']:
                score += 1
        return score


class PuzzleModule:
    """A module for solving cultural puzzles."""
    
    def __init__(self):
        # Initialize a list to hold puzzles
        self.puzzles = []
    
    def add_puzzle(self, puzzle_description, pieces):
        """Add a puzzle to the module.
        
        Args:
            puzzle_description (str): Description of the puzzle.
            pieces (list): List of pieces that make up the puzzle.
        """
        self.puzzles.append({
            'description': puzzle_description,
            'pieces': pieces
        })
    
    def solve_puzzle(self):
        """Simulate solving a puzzle."""
        for puzzle in self.puzzles:
            print(puzzle['description'])
            print("Pieces to match:", puzzle['pieces'])
            input("Press Enter to simulate solving the puzzle...")
            print("Puzzle solved!")


class RecipeModule:
    """A module for exploring traditional recipes."""
    
    def __init__(self):
        # Initialize a list to hold recipes
        self.recipes = []
    
    def add_recipe(self, name, ingredients, instructions, cultural_insight):
        """Add a recipe to the module.
        
        Args:
            name (str): Name of the dish.
            ingredients (list): List of ingredients.
            instructions (str): Cooking instructions.
            cultural_insight (str): Insight into the cultural significance of the dish.
        """
        self.recipes.append({
            'name': name,
            'ingredients': ingredients,
            'instructions': instructions,
            'cultural_insight': cultural_insight
        })
    
    def explore_recipes(self):
        """Display all recipes."""
        for recipe in self.recipes:
            print(f"Dish: {recipe['name']}")
            print("Ingredients:", recipe['ingredients'])
            print("Instructions:", recipe['instructions'])
            print("Cultural Insight:", recipe['cultural_insight'])
            print()


def main():
    """Main function to run the Cultural Journey system."""
    
    # Create instances of each module
    quiz_module = QuizModule()
    puzzle_module = PuzzleModule()
    recipe_module = RecipeModule()
    
    # Populate the Quiz Module
    quiz_module.add_question(
        "What is the traditional Japanese art of folding paper called?",
        ["Origami", "Ikebana", "Calligraphy", "Sumi-e"],
        "Origami"
    )
    quiz_module.add_question(
        "Which festival is known as the Festival of Lights in India?",
        ["Diwali", "Holi", "Eid", "Christmas"],
        "Diwali"
    )
    
    # Take the quiz
    print("Welcome to the Cultural Journey Quiz!")
    score = quiz_module.take_quiz()
    print(f"Your score: {score}/{len(quiz_module.questions)}")
    
    # Populate the Puzzle Module
    puzzle_module.add_puzzle(
        "Match the pieces to form a traditional Indian dance scene.",
        ["Dancer", "Drum", "Costume", "Audience"]
    )
    
    # Solve the puzzle
    print("\nNow, let's solve a cultural puzzle!")
    puzzle_module.solve_puzzle()
    
    # Populate the Recipe Module
    recipe_module.add_recipe(
        "Sushi",
        ["Rice", "Nori", "Fish", "Vegetables"],
        "1. Cook the rice. 2. Prepare the fillings. 3. Roll the sushi.",
        "Sushi is a traditional Japanese dish that has become popular worldwide."
    )
    
    # Explore recipes
    print("\nExplore traditional recipes:")
    recipe_module.explore_recipes()


if __name__ == "__main__":
    main()