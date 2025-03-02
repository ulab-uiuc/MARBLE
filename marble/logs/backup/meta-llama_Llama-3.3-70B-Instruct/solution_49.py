# solution.py
import json

class MealMaster:
    def __init__(self):
        # Initialize an empty dictionary to store user data
        self.user_data = {}
        # Initialize an empty dictionary to store meal plans
        self.meal_plans = {}

    def get_dietary_preferences(self):
        # Get user's dietary preferences
        print("Select your dietary preferences:")
        print("1. Vegetarian")
        print("2. Vegan")
        print("3. Gluten-free")
        print("4. Low-carb")
        preferences = input("Enter your choice (separated by comma): ")
        return preferences.split(',')

    def get_health_goals(self):
        # Get user's health goals
        print("Select your health goals:")
        print("1. Weight loss")
        print("2. Muscle gain")
        print("3. Maintenance")
        goals = input("Enter your choice: ")
        return goals

    def get_calorie_intake(self):
        # Get user's daily calorie intake
        while True:
            try:
                calorie_intake = int(input("Enter your daily calorie intake: "))
                return calorie_intake
            except ValueError:
                print("Invalid input. Please enter a number.")

    def get_macronutrient_ratios(self):
        # Get user's macronutrient ratios
        while True:
            try:
                protein_ratio = float(input("Enter your protein ratio (in %): "))
                carbohydrate_ratio = float(input("Enter your carbohydrate ratio (in %): "))
                fat_ratio = float(input("Enter your fat ratio (in %): "))
                if protein_ratio + carbohydrate_ratio + fat_ratio == 100:
                    return protein_ratio, carbohydrate_ratio, fat_ratio
                else:
                    print("Invalid input. The sum of ratios should be 100.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def get_food_allergies(self):
        # Get user's food allergies
        allergies = input("Enter your food allergies (separated by comma): ")
        return allergies.split(',')

    def generate_meal_plan(self):
        # Generate a personalized meal plan for the weekmeal_plan = {}
        dietary_preferences = self.user_data['dietary_preferences']
self.user_data = {'dietary_preferences': self.get_dietary_preferences(), 'health_goals': self.get_health_goals(), 'calorie_intake': self.get_calorie_intake(), 'macronutrient_ratios': self.get_macronutrient_ratios(), 'food_allergies': self.get_food_allergies()}
        health_goals = self.user_data['health_goals']
        calorie_intake = self.user_data['calorie_intake']
        macronutrient_ratios = self.user_data['macronutrient_ratios']
        food_allergies = self.user_data['food_allergies']
        
        # Use a database of recipes and nutritional information to generate a meal plan
        # For simplicity, assume we have a list of recipes and their nutritional information
        recipes = [
            {'name': 'Oatmeal with fruits', 'ingredients': ['oats', 'milk', 'fruits'], 'preparation': 'Cook oats with milk and add fruits', 'nutrition': {'calories': 300, 'protein': 10, 'carbohydrates': 50, 'fats': 10, 'fiber': 5}},
            {'name': 'Grilled chicken with vegetables', 'ingredients': ['chicken', 'vegetables', 'oil'], 'preparation': 'Grill chicken and vegetables with oil', 'nutrition': {'calories': 400, 'protein': 40, 'carbohydrates': 10, 'fats': 20, 'fiber': 5}},
            # Add more recipes as needed
        ]
        
        # Apply algorithms to select meals that meet the user's requirements
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            meal_plan[day] = {}
            for meal in ['breakfast', 'lunch', 'dinner', 'snack']:
                # Select a recipe that meets the user's dietary preferences, health goals, calorie intake, macronutrient ratios, and food allergies
                selected_recipe = None
                for recipe in recipes:
                    if recipe['name'] not in food_allergies and recipe['nutrition']['calories'] <= calorie_intake and recipe['nutrition']['protein'] >= macronutrient_ratios[0] and recipe['nutrition']['carbohydrates'] >= macronutrient_ratios[1] and recipe['nutrition']['fats'] >= macronutrient_ratios[2]:
                        selected_recipe = recipe
                        break
                if selected_recipe:
                    meal_plan[day][meal] = selected_recipe
                else:
                    print(f'No recipe found for {day} {meal}')        return meal_plan

    def calculate_nutrition(self, meal):
        # Calculate nutritional information for a meal
        nutrition = {
            "calories": 0,
            "protein": 0,
            "carbohydrates": 0,
            "fats": 0,
            "fiber": 0
        }
        # For simplicity, assume the nutritional values are as follows
        if meal["name"] == "Oatmeal with fruits":
            nutrition["calories"] = 300
            nutrition["protein"] = 10
            nutrition["carbohydrates"] = 50
            nutrition["fats"] = 10
            nutrition["fiber"] = 5
        elif meal["name"] == "Grilled chicken with vegetables":
            nutrition["calories"] = 400
            nutrition["protein"] = 40
            nutrition["carbohydrates"] = 10
            nutrition["fats"] = 20
            nutrition["fiber"] = 5
        elif meal["name"] == "Quinoa with lentils":
            nutrition["calories"] = 500
            nutrition["protein"] = 20
            nutrition["carbohydrates"] = 60
            nutrition["fats"] = 10
            nutrition["fiber"] = 10
        elif meal["name"] == "Apple slices with almond butter":
            nutrition["calories"] = 150
            nutrition["protein"] = 4
            nutrition["carbohydrates"] = 20
            nutrition["fats"] = 8
            nutrition["fiber"] = 4
        # Add more meal options as needed
        return nutrition

    def save_meal_plan(self, meal_plan):
        # Save the meal plan to a file
        with open("meal_plan.json", "w") as file:
            json.dump(meal_plan, file)

    def load_meal_plan(self):
        # Load a saved meal plan from a file
        try:
            with open("meal_plan.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return None

    def modify_meal_plan(self, meal_plan):
        # Modify a meal plan
        print("Select a day to modify:")
        print("1. Monday")
        print("2. Tuesday")
        print("3. Wednesday")
        print("4. Thursday")
        print("5. Friday")
        print("6. Saturday")
        print("7. Sunday")
        day = int(input("Enter your choice: "))
        days = list(meal_plan.keys())
        day = days[day - 1]
        print("Select a meal to modify:")
        print("1. Breakfast")
        print("2. Lunch")
        print("3. Dinner")
        print("4. Snack")
        meal = int(input("Enter your choice: "))
        meals = list(meal_plan[day].keys())
        meal = meals[meal - 1]
        print("Enter new meal details:")
        name = input("Enter meal name: ")
        ingredients = input("Enter ingredients (separated by comma): ").split(',')
        preparation = input("Enter preparation instructions: ")
        meal_plan[day][meal] = {"name": name, "ingredients": ingredients, "preparation": preparation}
        return meal_plan

def main():
    meal_master = MealMaster()
    print("Welcome to MealMaster!")
    while True:
        print("1. Create a new meal plan")
        print("2. Load a saved meal plan")
        print("3. Modify a meal plan")
        print("4. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            dietary_preferences = meal_master.get_dietary_preferences()
            health_goals = meal_master.get_health_goals()
            calorie_intake = meal_master.get_calorie_intake()
            macronutrient_ratios = meal_master.get_macronutrient_ratios()
            food_allergies = meal_master.get_food_allergies()
            meal_plan = meal_master.generate_meal_plan()
            for day, meals in meal_plan.items():
                print(f"Day: {day}")
                for meal, details in meals.items():
                    print(f"Meal: {meal}")
                    print(f"Name: {details['name']}")
                    print(f"Ingredients: {', '.join(details['ingredients'])}")
                    print(f"Preparation: {details['preparation']}")
                    nutrition = meal_master.calculate_nutrition(details)
                    print(f"Nutrition: Calories - {nutrition['calories']}, Protein - {nutrition['protein']}g, Carbohydrates - {nutrition['carbohydrates']}g, Fats - {nutrition['fats']}g, Fiber - {nutrition['fiber']}g")
                    print()
            meal_master.save_meal_plan(meal_plan)
        elif choice == 2:
            meal_plan = meal_master.load_meal_plan()
            if meal_plan:
                for day, meals in meal_plan.items():
                    print(f"Day: {day}")
                    for meal, details in meals.items():
                        print(f"Meal: {meal}")
                        print(f"Name: {details['name']}")
                        print(f"Ingredients: {', '.join(details['ingredients'])}")
                        print(f"Preparation: {details['preparation']}")
                        nutrition = meal_master.calculate_nutrition(details)
                        print(f"Nutrition: Calories - {nutrition['calories']}, Protein - {nutrition['protein']}g, Carbohydrates - {nutrition['carbohydrates']}g, Fats - {nutrition['fats']}g, Fiber - {nutrition['fiber']}g")
                        print()
            else:
                print("No saved meal plan found.")
        elif choice == 3:
            meal_plan = meal_master.load_meal_plan()
            if meal_plan:
                meal_plan = meal_master.modify_meal_plan(meal_plan)
                meal_master.save_meal_plan(meal_plan)
            else:
                print("No saved meal plan found.")
        elif choice == 4:
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()