# solution.py

class MealMaster:
    def __init__(self):
        # Initialize the MealMaster with default values
        self.dietary_preferences = []
        self.health_goals = {}
        self.calorie_intake = 0
        self.macronutrient_ratios = {}
        self.food_allergies = []
        self.meal_plan = {}

    def set_dietary_preferences(self, preferences):
        """Set the user's dietary preferences."""
        self.dietary_preferences = preferences

    def set_health_goals(self, goals, calorie_intake, macronutrient_ratios):
        """Set the user's health goals and nutritional targets."""
        self.health_goals = goals
        self.calorie_intake = calorie_intake
        self.macronutrient_ratios = macronutrient_ratios

    def set_food_allergies(self, allergies):
        """Set the user's food allergies."""
        self.food_allergies = allergies

    def generate_meal_plan(self):
        """Generate a personalized meal plan for the week."""
        # For simplicity, we will create a static meal plan
        self.meal_plan = {
            "Monday": {
                "Breakfast": self.suggest_recipe("breakfast"),
                "Lunch": self.suggest_recipe("lunch"),
                "Dinner": self.suggest_recipe("dinner"),
                "Snacks": self.suggest_recipe("snack"),
            },
            "Tuesday": {
                "Breakfast": self.suggest_recipe("breakfast"),
                "Lunch": self.suggest_recipe("lunch"),
                "Dinner": self.suggest_recipe("dinner"),
                "Snacks": self.suggest_recipe("snack"),
            },
            # Add more days as needed...
        }

    def suggest_recipe(self, meal_type):
        """Suggest a recipe based on the meal type and dietary preferences."""
        # This is a placeholder for actual recipe suggestions
        recipes = {
            "breakfast": {
                "name": "Oatmeal with Fruits",
                "ingredients": ["Oats", "Banana", "Almond Milk"],
                "instructions": "Cook oats and top with banana and almond milk.",
                "nutrition": {"calories": 300, "protein": 10, "carbs": 50, "fats": 5, "fiber": 7}
            },
            "lunch": {
                "name": "Quinoa Salad",
                "ingredients": ["Quinoa", "Cucumber", "Tomato", "Olive Oil"],
                "instructions": "Mix all ingredients and serve chilled.",
                "nutrition": {"calories": 400, "protein": 15, "carbs": 60, "fats": 10, "fiber": 8}
            },
            "dinner": {
                "name": "Grilled Chicken with Veggies",
                "ingredients": ["Chicken Breast", "Broccoli", "Carrots"],
                "instructions": "Grill chicken and serve with steamed veggies.",
                "nutrition": {"calories": 500, "protein": 40, "carbs": 20, "fats": 15, "fiber": 5}
            },
            "snack": {
                "name": "Greek Yogurt with Honey",
                "ingredients": ["Greek Yogurt", "Honey"],
                "instructions": "Mix yogurt with honey and enjoy.",
                "nutrition": {"calories": 150, "protein": 10, "carbs": 20, "fats": 5, "fiber": 0}
            }
        }
        return recipes[meal_type]

    def display_meal_plan(self):
        """Display the generated meal plan."""
        for day, meals in self.meal_plan.items():
            print(f"{day}:")
            for meal, recipe in meals.items():
                print(f"  {meal}: {recipe['name']}")
                print(f"    Ingredients: {', '.join(recipe['ingredients'])}")
                print(f"    Instructions: {recipe['instructions']}")
                print(f"    Nutrition: {recipe['nutrition']}")
            print()

# Example usage
if __name__ == "__main__":
    meal_master = MealMaster()
    meal_master.set_dietary_preferences(["vegetarian"])
    meal_master.set_health_goals({"weight_loss": True}, 1500, {"protein": 30, "carbs": 50, "fats": 20})
    meal_master.set_food_allergies(["nuts"])
    meal_master.generate_meal_plan()
    meal_master.display_meal_plan()