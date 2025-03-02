# meal_master.py
# This is the main implementation of the MealMaster program.

class User:
    """Represents a user with their dietary preferences, health goals, and food allergies."""
    
    def __init__(self, name, dietary_preferences, health_goals, food_allergies):
        """
        Initializes a User object.

        Args:
            name (str): The user's name.
            dietary_preferences (list): A list of the user's dietary preferences (e.g., vegetarian, vegan, gluten-free, low-carb).
            health_goals (str): The user's health goal (e.g., weight loss, muscle gain, maintenance).
            food_allergies (list): A list of the user's food allergies or intolerances.
        """
        self.name = name
        self.dietary_preferences = dietary_preferences
        self.health_goals = health_goals
        self.food_allergies = food_allergies


class Meal:
    """Represents a meal with its recipe, ingredients, and nutritional information."""
    
    def __init__(self, name, recipe, ingredients, nutritional_info):
        """
        Initializes a Meal object.

        Args:
            name (str): The meal's name.
            recipe (str): The meal's recipe.
            ingredients (list): A list of the meal's ingredients.
            nutritional_info (dict): A dictionary containing the meal's nutritional information (e.g., calories, protein, carbohydrates, fats, fiber).
        """
        self.name = name
        self.recipe = recipe
        self.ingredients = ingredients
        self.nutritional_info = nutritional_info


class MealPlan:
    """Represents a meal plan with its meals and user information."""
    
    def __init__(self, user, meals):
        """
        Initializes a MealPlan object.

        Args:
            user (User): The user who owns the meal plan.
            meals (list): A list of meals in the meal plan.
        """
        self.user = user
        self.meals = meals


class MealMaster:
    """Represents the MealMaster program with its functionality to generate meal plans and provide nutritional information."""
    
    def __init__(self):
        """
        Initializes a MealMaster object.
        """
        self.meal_database = {
            "breakfast": [
                Meal("Scrambled Eggs", "Scramble eggs with salt and pepper.", ["eggs", "salt", "pepper"], {"calories": 200, "protein": 20, "carbohydrates": 0, "fats": 10, "fiber": 0}),
                Meal("Oatmeal", "Cook oatmeal with milk and fruit.", ["oatmeal", "milk", "fruit"], {"calories": 300, "protein": 5, "carbohydrates": 60, "fats": 10, "fiber": 4})
            ],
            "lunch": [
                Meal("Grilled Chicken", "Grill chicken breast with vegetables.", ["chicken breast", "vegetables"], {"calories": 400, "protein": 50, "carbohydrates": 0, "fats": 20, "fiber": 0}),
                Meal("Salad", "Mix greens with vegetables and a protein source.", ["greens", "vegetables", "protein source"], {"calories": 200, "protein": 20, "carbohydrates": 10, "fats": 10, "fiber": 5})
            ],
            "dinner": [
                Meal("Grilled Salmon", "Grill salmon with vegetables.", ["salmon", "vegetables"], {"calories": 500, "protein": 50, "carbohydrates": 0, "fats": 30, "fiber": 0}),
                Meal("Beef Stir-Fry", "Stir-fry beef with vegetables.", ["beef", "vegetables"], {"calories": 600, "protein": 60, "carbohydrates": 20, "fats": 40, "fiber": 5})
            ],
            "snacks": [
                Meal("Apple Slices", "Slice an apple.", ["apple"], {"calories": 100, "protein": 0, "carbohydrates": 25, "fats": 0, "fiber": 4}),
                Meal("Carrot Sticks", "Slice a carrot.", ["carrot"], {"calories": 50, "protein": 0, "carbohydrates": 10, "fats": 0, "fiber": 2})
            ]
        }

    def get_meal_plan(self, user):
        """
        Generates a meal plan for the given user based on their dietary preferences, health goals, and food allergies.

        Args:
            user (User): The user who needs a meal plan.

        Returns:
            MealPlan: A meal plan for the user.
        """
        meal_plan = MealPlan(user, [])
        for meal_type in self.meal_database:
            for meal in self.meal_database[meal_type]:
                if all(ingredient not in user.food_allergies for ingredient in meal.ingredients):if any(ingredient in user.dietary_preferences for ingredient in meal.ingredients) and all(ingredient not in user.food_allergies for ingredient in meal.ingredients):    meal_plan.meals.append(meal)
        return meal_plan

    def get_nutritional_info(self, meal):
        """
        Returns the nutritional information for the given meal.

        Args:
            meal (Meal): The meal for which to get nutritional information.

        Returns:
            dict: A dictionary containing the meal's nutritional information.
        """
        return meal.nutritional_info


def main():
    # Create a MealMaster object
    meal_master = MealMaster()

    # Create a User object
    user = User("John Doe", ["vegetarian", "gluten-free"], "weight loss", ["eggs"])

    # Get a meal plan for the user
    meal_plan = meal_master.get_meal_plan(user)

    # Print the meal plan
    print("Meal Plan for", user.name)
    for i, meal in enumerate(meal_plan.meals):
        print(f"Day {i+1}:")
        print(f"  {meal.name}:")
        print(f"    Recipe: {meal.recipe}")
        print(f"    Ingredients: {', '.join(meal.ingredients)}")
        print(f"    Nutritional Information: {meal_master.get_nutritional_info(meal)}")
        print()


if __name__ == "__main__":
    main()