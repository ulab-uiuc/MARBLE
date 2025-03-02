# meal_master.py

class MealMaster:
    def __init__(self):
        self.dietary_preferences = {
            "vegetarian": True,
            "vegan": False,
            "gluten-free": False,
            "low-carb": False
        }
        self.health_goals = {
            "weight_loss": False,
            "muscle_gain": False,
            "maintenance": True
        }
        self.food_allergies = []
        self.meal_plan = {
            "Monday": {
                "breakfast": None,
                "lunch": None,
                "dinner": None,
                "snack": None
            },
            "Tuesday": {
                "breakfast": None,
                "lunch": None,
                "dinner": None,
                "snack": None
            },
            "Wednesday": {
                "breakfast": None,
                "lunch": None,
                "dinner": None,
                "snack": None
            },
            "Thursday": {
                "breakfast": None,
                "lunch": None,
                "dinner": None,
                "snack": None
            },
            "Friday": {
                "breakfast": None,
                "lunch": None,
                "dinner": None,
                "snack": None
            },
            "Saturday": {
                "breakfast": None,
                "lunch": None,
                "dinner": None,
                "snack": None
            },
            "Sunday": {
                "breakfast": None,
                "lunch": None,
                "dinner": None,
                "snack": None
            }
        }
        self.recipes = {
            "breakfast": {
                "oatmeal": {
                    "ingredients": ["oats", "milk", "banana"],
                    "instructions": ["Cook oats in milk", "Add sliced banana"],
                    "nutritional_info": {
                        "calories": 300,
                        "protein": 5,
                        "carbohydrates": 60,
                        "fats": 10,
                        "fiber": 5
                    }
                },
                "scrambled_eggs": {
                    "ingredients": ["eggs", "salt", "pepper"],
                    "instructions": ["Scramble eggs in a pan", "Add salt and pepper to taste"],
                    "nutritional_info": {
                        "calories": 200,
                        "protein": 20,
                        "carbohydrates": 0,
                        "fats": 10,
                        "fiber": 0
                    }
                }
            },
            "lunch": {
                "grilled_chicken": {
                    "ingredients": ["chicken breast", "salt", "pepper"],
                    "instructions": ["Grill chicken breast in a pan", "Add salt and pepper to taste"],
                    "nutritional_info": {
                        "calories": 350,
                        "protein": 40,
                        "carbohydrates": 0,
                        "fats": 10,
                        "fiber": 0
                    }
                },
                "salad": {
                    "ingredients": ["lettuce", "tomatoes", "cucumber"],
                    "instructions": ["Combine lettuce, tomatoes, and cucumber in a bowl", "Add dressing of choice"],
                    "nutritional_info": {
                        "calories": 100,
                        "protein": 5,
                        "carbohydrates": 20,
                        "fats": 0,
                        "fiber": 5
                    }
                }
            },
            "dinner": {
                "grilled_salmon": {
                    "ingredients": ["salmon fillet", "salt", "pepper"],
                    "instructions": ["Grill salmon fillet in a pan", "Add salt and pepper to taste"],
                    "nutritional_info": {
                        "calories": 400,
                        "protein": 50,
                        "carbohydrates": 0,
                        "fats": 20,
                        "fiber": 0
                    }
                },
                "roasted_vegetables": {
                    "ingredients": ["broccoli", "carrots", "sweet potatoes"],
                    "instructions": ["Roast broccoli, carrots, and sweet potatoes in the oven", "Add salt and pepper to taste"],
                    "nutritional_info": {
                        "calories": 200,
                        "protein": 5,
                        "carbohydrates": 40,
                        "fats": 0,
                        "fiber": 10
                    }
                }
            },
            "snack": {
                "apple": {
                    "ingredients": ["apple"],
                    "instructions": ["Eat an apple"],
                    "nutritional_info": {
                        "calories": 95,
                        "protein": 0,
                        "carbohydrates": 25,
                        "fats": 0,
                        "fiber": 4
                    }
                },
                "banana": {
                    "ingredients": ["banana"],
                    "instructions": ["Eat a banana"],
                    "nutritional_info": {
                        "calories": 105,
                        "protein": 1,
                        "carbohydrates": 27,
                        "fats": 0,
                        "fiber": 3
                    }
                }
            }
        }

    def set_dietary_preferences(self):
        print("Dietary Preferences:")
        for preference in self.dietary_preferences:
            choice = input(f"{preference.capitalize()} (yes/no): ")
            if choice.lower() == "yes":
                self.dietary_preferences[preference] = True
            else:
                self.dietary_preferences[preference] = False

    def set_health_goals(self):
        print("Health Goals:")
        for goal in self.health_goals:
            choice = input(f"{goal.capitalize()} (yes/no): ")
            if choice.lower() == "yes":
                self.health_goals[goal] = True
            else:
                self.health_goals[goal] = False

    def set_food_allergies(self):
        print("Food Allergies:")
        allergy = input("Enter a food allergy (or 'done' if finished): ")
        while allergy.lower() != "done":
            self.food_allergies.append(allergy)
            allergy = input("Enter a food allergy (or 'done' if finished): ")

    def generate_meal_plan(self):
        for day in self.meal_plan:
        # Initialize meal plan with default recipes
        for day in self.meal_plan:
            for meal in self.meal_plan[day]:
            # Consider health goals when selecting recipes
            if health_goals['weight_loss']:
                # Select recipes that are lower in calories and fat
                for meal in self.meal_plan[day]:
                    if meal == 'breakfast':
                # Consider daily calorie intake and macronutrient ratios when selecting recipes
                if self.recipes[meal][self.meal_plan[day][meal]]['nutritional_info']['calories'] > daily_calorie_intake:
                    self.meal_plan[day][meal] = None
                # Avoid recipes that include allergenic ingredients
                if self.meal_plan[day][meal] in food_allergies:
                    self.meal_plan[day][meal] = None
                        self.meal_plan[day][meal] = 'oatmeal'
                    elif meal == 'lunch':
                        self.meal_plan[day][meal] = 'grilled_chicken'
                    elif meal == 'dinner':
                        self.meal_plan[day][meal] = 'grilled_salmon'
                    elif meal == 'snack':
                        self.meal_plan[day][meal] = 'apple'
            elif health_goals['muscle_gain']:
                # Select recipes that are higher in protein
                for meal in self.meal_plan[day]:
                    if meal == 'breakfast':
                        self.meal_plan[day][meal] = 'scrambled_eggs'
                    elif meal == 'lunch':
                        self.meal_plan[day][meal] = 'grilled_chicken'
                    elif meal == 'dinner':
                        self.meal_plan[day][meal] = 'grilled_salmon'
                    elif meal == 'snack':
                        self.meal_plan[day][meal] = 'banana'
            else:
                # Select default recipes
                for meal in self.meal_plan[day]:
                    if meal == 'breakfast':
                        self.meal_plan[day][meal] = 'oatmeal'
                    elif meal == 'lunch':
                        self.meal_plan[day][meal] = 'salad'
                    elif meal == 'dinner':
                        self.meal_plan[day][meal] = 'roasted_vegetables'
                    elif meal == 'snack':
                        self.meal_plan[day][meal] = 'apple'
                self.meal_plan[day][meal] = None
            for meal in self.meal_plan[day]:
                if meal == "breakfast":
                    if self.dietary_preferences["vegetarian"]:
                        self.meal_plan[day][meal] = "oatmeal"
                    else:
                        self.meal_plan[day][meal] = "scrambled_eggs"
                elif meal == "lunch":
                    if self.dietary_preferences["gluten-free"]:
                        self.meal_plan[day][meal] = "grilled_chicken"
                    else:
                        self.meal_plan[day][meal] = "salad"
                elif meal == "dinner":
                    if self.dietary_preferences["low-carb"]:
                        self.meal_plan[day][meal] = "grilled_salmon"
                    else:
                        self.meal_plan[day][meal] = "roasted_vegetables"
                elif meal == "snack":
                    if self.dietary_preferences["vegan"]:
                        self.meal_plan[day][meal] = "apple"
                    else:
                        self.meal_plan[day][meal] = "banana"

    def print_meal_plan(self):def generate_meal_plan(self, health_goals, food_allergies, daily_calorie_intake, macronutrient_ratios):        for day in self.meal_plan:
            print(f"{day}:")
            for meal in self.meal_plan[day]:
                print(f"  {meal.capitalize()}: {self.meal_plan[day][meal]}")
                print(f"    Ingredients: {self.recipes[meal][self.meal_plan[day][meal]]['ingredients']}")
                print(f"    Instructions: {self.recipes[meal][self.meal_plan[day][meal]]['instructions']}")
                print(f"    Nutritional Info: {self.recipes[meal][self.meal_plan[day][meal]]['nutritional_info']}")

    def save_meal_plan(self):
        with open("meal_plan.txt", "w") as file:
            for day in self.meal_plan:
                file.write(f"{day}:\n")
                for meal in self.meal_plan[day]:
                    file.write(f"  {meal.capitalize()}: {self.meal_plan[day][meal]}\n")
                    file.write(f"    Ingredients: {self.recipes[meal][self.meal_plan[day][meal]]['ingredients']}\n")
                    file.write(f"    Instructions: {self.recipes[meal][self.meal_plan[day][meal]]['instructions']}\n")
                    file.write(f"    Nutritional Info: {self.recipes[meal][self.meal_plan[day][meal]]['nutritional_info']}\n")

def main():
    meal_master = MealMaster()
    meal_master.set_dietary_preferences()
    meal_master.set_health_goals()
    meal_master.set_food_allergies()
    meal_master.generate_meal_plan()
    meal_master.print_meal_plan()
    meal_master.save_meal_plan()

if __name__ == "__main__":
    main()