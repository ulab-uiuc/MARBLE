class QuizModule:
    def __init__(self):
        self.questions = []
    
    def add_question(self, question, options, correct_answer):
        """
        Add a new multiple-choice question to the quiz module.
        
        Args:
        question (str): The question to be added.
        options (list): List of options for the question.
        correct_answer (str): The correct answer for the question.
        """
        self.questions.append({
            'question': question,
            'options': options,
            'correct_answer': correct_answer
        })
    
    def display_question(self, question_num):
        """
        Display a specific question from the quiz module.
        
        Args:
        question_num (int): The index of the question to display.
        """
        if question_num < len(self.questions):
            question = self.questions[question_num]['question']
            options = self.questions[question_num]['options']
            print(f"Question {question_num + 1}: {question}")
            for i, option in enumerate(options):
                print(f"{i + 1}. {option}")
        else:
            print("Question number out of range.")
    
    def check_answer(self, question_num, user_answer):
        """
        Check if the user's answer is correct for a specific question.
        
        Args:
        question_num (int): The index of the question to check.
        user_answer (str): The user's answer to the question.
        
        Returns:
        bool: True if the user's answer is correct, False otherwise.
        """
        if question_num < len(self.questions):
            correct_answer = self.questions[question_num]['correct_answer']
            return user_answer == correct_answer
        else:
            return False


class PuzzleModule:
    def __init__(self):
        self.puzzles = []
    
    def add_puzzle(self, puzzle_image, solution):
        """
        Add a new puzzle to the puzzle module.
        
        Args:
        puzzle_image (str): Path to the image representing the puzzle.
        solution (str): Description or solution of the puzzle.
        """
        self.puzzles.append({
            'puzzle_image': puzzle_image,
            'solution': solution
        })
    
    def display_puzzle(self, puzzle_num):
        """
        Display a specific puzzle from the puzzle module.
        
        Args:
        puzzle_num (int): The index of the puzzle to display.
        """
        if puzzle_num < len(self.puzzles):
            puzzle_image = self.puzzles[puzzle_num]['puzzle_image']
            print(f"Displaying Puzzle {puzzle_num + 1}: {puzzle_image}")
        else:
            print("Puzzle number out of range.")
    
    def check_solution(self, puzzle_num, user_solution):
        """
        Check if the user's solution matches the correct solution for a specific puzzle.
        
        Args:
        puzzle_num (int): The index of the puzzle to check.
        user_solution (str): The user's solution to the puzzle.
        
        Returns:
        bool: True if the user's solution is correct, False otherwise.
        """
        if puzzle_num < len(self.puzzles):
            correct_solution = self.puzzles[puzzle_num]['solution']
            return user_solution == correct_solution
        else:
            return False


class RecipeModule:
    def __init__(self):
        self.recipes = {}
    
    def add_recipe(self, cuisine, recipe_name, ingredients, instructions):
        """
        Add a new recipe to the recipe module.
        
        Args:
        cuisine (str): The cuisine or culture the recipe belongs to.
        recipe_name (str): Name of the recipe.
        ingredients (list): List of ingredients required for the recipe.
        instructions (str): Step-by-step instructions to prepare the recipe.
        """
        if cuisine not in self.recipes:
            self.recipes[cuisine] = []
        
        self.recipes[cuisine].append({
            'recipe_name': recipe_name,
            'ingredients': ingredients,
            'instructions': instructions
        })
    
    def display_recipe(self, cuisine):
        """
        Display recipes from a specific cuisine in the recipe module.
        
        Args:
        cuisine (str): The cuisine or culture to display recipes for.
        """
        if cuisine in self.recipes:
            print(f"Recipes from {cuisine}:")
            for idx, recipe in enumerate(self.recipes[cuisine]):
                print(f"Recipe {idx + 1}: {recipe['recipe_name']}")
                print("Ingredients:")
                for ingredient in recipe['ingredients']:
                    print(f"- {ingredient}")
                print("Instructions:")
                print(recipe['instructions'])
                print()
        else:
            print("No recipes found for the specified cuisine.")


# Sample Usage:

# Quiz Module
quiz = QuizModule()
quiz.add_question("What is the traditional dress of Japan?", ["Kimono", "Sari", "Hanbok"], "Kimono")
quiz.add_question("Which festival is known as the Festival of Lights?", ["Diwali", "Holi", "Eid"], "Diwali")
quiz.display_question(0)
print(quiz.check_answer(0, "Kimono"))

# Puzzle Module
puzzle = PuzzleModule()
puzzle.add_puzzle("japan_puzzle.jpg", "Match the images to their respective traditional Japanese symbols.")
puzzle.display_puzzle(0)
print(puzzle.check_solution(0, "Match the images to their respective traditional Japanese symbols."))

# Recipe Module
recipe = RecipeModule()
recipe.add_recipe("Japanese", "Sushi", ["Rice", "Nori", "Fish", "Vegetables"], "Step 1: Prepare sushi rice. Step 2: Lay out nori sheet. Step 3: Add fillings. Step 4: Roll and cut.")
recipe.add_recipe("Indian", "Chicken Tikka Masala", ["Chicken", "Yogurt", "Spices", "Tomato Sauce"], "Step 1: Marinate chicken. Step 2: Grill chicken. Step 3: Prepare sauce. Step 4: Combine and simmer.")
recipe.display_recipe("Japanese")
recipe.display_recipe("Italian")