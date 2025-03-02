# meal_master.py
# This is the main implementation of the MealMaster program.

class User:
    """Represents a user with their dietary preferences, health goals, and food allergies."""
    
    def __init__(self, name):
        self.name = name
        self.dietary_preferences = []
        self.health_goals = []
        self.food_allergies = []

    def add_dietary_preference(self, preference):
        """Adds a dietary preference to the user's list."""
        self.dietary_preferences.append(preference)

    def add_health_goal(self, goal):
        """Adds a health goal to the user's list."""
        self.health_goals.append(goal)

    def add_food_allergy(self, allergy):
        """Adds a food allergy to the user's list."""
        self.food_allergies.append(allergy)


class Meal:
    """Represents a meal with its ingredients, preparation instructions, and nutritional information."""
    
    def __init__(self, name, ingredients, instructions, calories, protein, carbohydrates, fats, fiber):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        self.calories = calories
        self.protein = protein
        self.carbohydrates = carbohydrates
        self.fats = fats
        self.fiber = fiber

    def __str__(self):
        return f"{self.name}\nIngredients: {', '.join(self.ingredients)}\nInstructions: {self.instructions}\nNutritional Information:\nCalories: {self.calories}\nProtein: {self.protein}g\nCarbohydrates: {self.carbohydrates}g\nFats: {self.fats}g\nFiber: {self.fiber}g"


class MealPlan:
    """Represents a meal plan for a user with their dietary preferences, health goals, and food allergies."""
    
    def __init__(self, user):
        self.user = user
        self.meals = []

    def add_meal(self, meal):
        """Adds a meal to the user's meal plan."""
        self.meals.append(meal)

    def generate_meal_plan(self):
        """Generates a personalized meal plan for the user based on their dietary preferences, health goals, and food allergies."""
        # This is a simplified example and actual implementation would require a database of recipes and nutritional information.
        meal_plan = {
            "Monday": {
                "Breakfast": Meal("Oatmeal", ["oats", "milk", "banana"], "Cook oats and milk, add banana.", 300, 5, 40, 10, 5),
                "Lunch": Meal("Grilled Chicken", ["chicken", "salad", "vinaigrette"], "Grill chicken and serve with salad.", 400, 30, 10, 20, 5),
                "Dinner": Meal("Vegetable Stir Fry", ["vegetables", "oil", "soy sauce"], "Stir fry vegetables and serve.", 500, 10, 20, 20, 10),
                "Snack": Meal("Apple", ["apple"], "Serve apple.", 100, 0, 20, 0, 4)
            },
            "Tuesday": {
                "Breakfast": Meal("Scrambled Eggs", ["eggs", "milk", "salt"], "Scramble eggs and serve.", 200, 15, 5, 10, 0),
                "Lunch": Meal("Turkey Sandwich", ["turkey", "bread", "cheese"], "Assemble sandwich and serve.", 500, 30, 30, 20, 5),
                "Dinner": Meal("Quinoa Bowl", ["quinoa", "chicken", "vegetables"], "Cook quinoa and serve with chicken and vegetables.", 600, 30, 30, 20, 10),
                "Snack": Meal("Carrot Sticks", ["carrots", "hummus"], "Serve carrot sticks with hummus.", 100, 2, 10, 0, 5)
            }
        }
        return meal_plan

    def save_meal_plan(self):
        """Saves the user's meal plan to a file."""
        with open(f"{self.user.name}_meal_plan.txt", "w") as file:
            for day, meals in self.generate_meal_plan().items():
                file.write(f"{day}:\n")
                for meal_name, meal in meals.items():
                    file.write(f"{meal_name}:\n{meal}\n\n")


class RecipeDatabase:
    """Represents a database of recipes with their ingredients, preparation instructions, and nutritional information."""
    
    def __init__(self):
        self.recipes = {
            "Oatmeal": {
                "ingredients": ["oats", "milk", "banana"],
                "instructions": "Cook oats and milk, add banana.",
                "calories": 300,
                "protein": 5,
                "carbohydrates": 40,
                "fats": 10,
                "fiber": 5
            },
            "Grilled Chicken": {
                "ingredients": ["chicken", "salad", "vinaigrette"],
                "instructions": "Grill chicken and serve with salad.",
                "calories": 400,
                "protein": 30,
                "carbohydrates": 10,
                "fats": 20,
                "fiber": 5
            },
            "Vegetable Stir Fry": {
                "ingredients": ["vegetables", "oil", "soy sauce"],
                "instructions": "Stir fry vegetables and serve.",
                "calories": 500,
                "protein": 10,
                "carbohydrates": 20,
                "fats": 20,
                "fiber": 10
            },
            "Apple": {
                "ingredients": ["apple"],
                "instructions": "Serve apple.",
                "calories": 100,
                "protein": 0,
                "carbohydrates": 20,
                "fats": 0,
                "fiber": 4
            },
            "Scrambled Eggs": {
                "ingredients": ["eggs", "milk", "salt"],
                "instructions": "Scramble eggs and serve.",
                "calories": 200,
                "protein": 15,
                "carbohydrates": 5,
                "fats": 10,
                "fiber": 0
            },
            "Turkey Sandwich": {
                "ingredients": ["turkey", "bread", "cheese"],
                "instructions": "Assemble sandwich and serve.",
                "calories": 500,
                "protein": 30,
                "carbohydrates": 30,
                "fats": 20,
                "fiber": 5
            },
            "Quinoa Bowl": {
                "ingredients": ["quinoa", "chicken", "vegetables"],
                "instructions": "Cook quinoa and serve with chicken and vegetables.",
                "calories": 600,
                "protein": 30,
                "carbohydrates": 30,
                "fats": 20,
                "fiber": 10
            },
            "Carrot Sticks": {
                "ingredients": ["carrots", "hummus"],
                "instructions": "Serve carrot sticks with hummus.",
                "calories": 100,
                "protein": 2,
                "carbohydrates": 10,
                "fats": 0,
                "fiber": 5
            }
        }

    def get_recipe(self, name):
        """Returns a recipe from the database by name."""
        return self.recipes.get(name)


def main():
    # Create a user
    user = User("John")

    # Add dietary preferences
    user.add_dietary_preference("vegetarian")
    user.add_dietary_preference("gluten-free")

    # Add health goals
    user.add_health_goal("weight loss")
    user.add_health_goal("muscle gain")

    # Add food allergies
    user.add_food_allergy("peanuts")
    user.add_food_allergy("shellfish")

    # Create a meal plan
    meal_plan = MealPlan(user)

    # Add meals to the meal plan
    meal_plan.add_meal(Meal("Oatmeal", ["oats", "milk", "banana"], "Cook oats and milk, add banana.", 300, 5, 40, 10, 5))
    meal_plan.add_meal(Meal("Grilled Chicken", ["chicken", "salad", "vinaigrette"], "Grill chicken and serve with salad.", 400, 30, 10, 20, 5))
    meal_plan.add_meal(Meal("Vegetable Stir Fry", ["vegetables", "oil", "soy sauce"], "Stir fry vegetables and serve.", 500, 10, 20, 20, 10))
    meal_plan.add_meal(Meal("Apple", ["apple"], "Serve apple.", 100, 0, 20, 0, 4))

    # Generate and save the meal plan
    meal_plan.save_meal_plan()


if __name__ == "__main__":
    main()