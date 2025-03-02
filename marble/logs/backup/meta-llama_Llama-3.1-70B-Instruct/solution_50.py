# travel_mate.py

class TravelMate:
    def __init__(self):
        self.users = {}
        self.destinations = {
            "Paris": {"description": "The City of Light", "price": 1000, "reviews": 4.5},
            "Rome": {"description": "The Eternal City", "price": 800, "reviews": 4.2},
            "Tokyo": {"description": "The Neon City", "price": 1200, "reviews": 4.8},
        }
        self.activities = {
            "cultural": {
                "Paris": {"description": "Visit the Louvre", "price": 20, "reviews": 4.5},
                "Rome": {"description": "Explore the Colosseum", "price": 15, "reviews": 4.2},
                "Tokyo": {"description": "Visit the Tokyo National Museum", "price": 10, "reviews": 4.8},
            },
            "adventure": {
                "Paris": {"description": "Go skydiving", "price": 200, "reviews": 4.5},
                "Rome": {"description": "Go bungee jumping", "price": 150, "reviews": 4.2},
                "Tokyo": {"description": "Go rock climbing", "price": 100, "reviews": 4.8},
            },
            "relaxation": {
                "Paris": {"description": "Take a Seine River cruise", "price": 50, "reviews": 4.5},
                "Rome": {"description": "Relax at a thermal spa", "price": 30, "reviews": 4.2},
                "Tokyo": {"description": "Take a traditional tea ceremony", "price": 20, "reviews": 4.8},
            },
        }
        self.accommodations = {
            "Paris": {"description": "Hotel Eiffel", "price": 200, "reviews": 4.5},
            "Rome": {"description": "Hotel Colosseum", "price": 150, "reviews": 4.2},
            "Tokyo": {"description": "Hotel Tokyo", "price": 100, "reviews": 4.8},
        }
        self.transportation = {
            "Paris": {"description": "Taxi", "price": 20, "reviews": 4.5},
            "Rome": {"description": "Metro", "price": 10, "reviews": 4.2},
            "Tokyo": {"description": "Bullet train", "price": 50, "reviews": 4.8},
        }

    def add_user(self, user_id, preferences):
        self.users[user_id] = {"preferences": preferences, "itinerary": []}

    def generate_itinerary(self, user_id):
        user = self.users.get(user_id)
        if not user:
            return "User not found"

        preferences = user["preferences"]
        budget = preferences["budget"]
        travel_dates = preferences["travel_dates"]
        activity_type = preferences["activity_type"]
        dietary_restrictions = preferences["dietary_restrictions"]

        if travel_dates["end_date"] < travel_dates["start_date"]:
            return "Invalid travel dates"

        itinerary = []
        destination = self.destinations.get(preferences["destination"])
        if destination:
            itinerary.append({"type": "destination", "description": destination["description"], "price": destination["price"], "reviews": destination["reviews"]})

        activity = self.activities.get(activity_type, {}).get(preferences["destination"])
        if activity:
            itinerary.append({"type": "activity", "description": activity["description"], "price": activity["price"], "reviews": activity["reviews"]})

        accommodation = self.accommodations.get(preferences["destination"])
        if accommodation:
            itinerary.append({"type": "accommodation", "description": accommodation["description"], "price": accommodation["price"], "reviews": accommodation["reviews"]})

        transportation = self.transportation.get(preferences["destination"])
        if transportation:
            itinerary.append({"type": "transportation", "description": transportation["description"], "price": transportation["price"], "reviews": transportation["reviews"]})

        user["itinerary"] = itinerary
        return itinerary

    def save_itinerary(self, user_id):
        user = self.users.get(user_id)
        if not user:
            return "User not found"
        return user["itinerary"]

    def modify_itinerary(self, user_id, item_type, item_description):
        user = self.users.get(user_id)
        if not user:
            return "User not found"

        itinerary = user["itinerary"]
        for item in itinerary:
            if item["type"] == item_type and item["description"] == item_description:
                itinerary.remove(item)
                return itinerary
        return "Item not found"

    def get_nutritional_info(self, user_id):
        user = self.users.get(user_id)
        if not user:
            return "User not found"

        itinerary = user["itinerary"]
        nutritional_info = []
        for item in itinerary:
            if item["type"] == "activity" or item["type"] == "accommodation":
                nutritional_info.append({"description": item["description"], "calories": 500, "protein": 20, "fat": 10, "carbohydrates": 60})
        return nutritional_info


# test_travel_mate.py

import unittest
from travel_mate import TravelMate

class TestTravelMate(unittest.TestCase):
    def setUp(self):
        self.travel_mate = TravelMate()

    def test_add_user(self):
        user_id = "user1"
        preferences = {
            "budget": 1000,
            "travel_dates": {"start_date": "2024-01-01", "end_date": "2024-01-08"},
            "activity_type": "cultural",
            "destination": "Paris",
            "dietary_restrictions": "vegetarian"
        }
        self.travel_mate.add_user(user_id, preferences)
        self.assertIn(user_id, self.travel_mate.users)

    def test_generate_itinerary(self):
        user_id = "user1"
        preferences = {
            "budget": 1000,
            "travel_dates": {"start_date": "2024-01-01", "end_date": "2024-01-08"},
            "activity_type": "cultural",
            "destination": "Paris",
            "dietary_restrictions": "vegetarian"
        }
        self.travel_mate.add_user(user_id, preferences)
        itinerary = self.travel_mate.generate_itinerary(user_id)
        self.assertIsInstance(itinerary, list)
        self.assertGreater(len(itinerary), 0)

    def test_invalid_travel_dates(self):
        user_id = "user1"
        preferences = {
            "budget": 1000,
            "travel_dates": {"start_date": "2024-01-08", "end_date": "2024-01-01"},
            "activity_type": "cultural",
            "destination": "Paris",
            "dietary_restrictions": "vegetarian"
        }
        self.travel_mate.add_user(user_id, preferences)
        itinerary = self.travel_mate.generate_itinerary(user_id)
        self.assertEqual(itinerary, "Invalid travel dates")

    def test_save_itinerary(self):
        user_id = "user1"
        preferences = {
            "budget": 1000,
            "travel_dates": {"start_date": "2024-01-01", "end_date": "2024-01-08"},
            "activity_type": "cultural",
            "destination": "Paris",
            "dietary_restrictions": "vegetarian"
        }
        self.travel_mate.add_user(user_id, preferences)
        self.travel_mate.generate_itinerary(user_id)
        itinerary = self.travel_mate.save_itinerary(user_id)
        self.assertIsInstance(itinerary, list)
        self.assertGreater(len(itinerary), 0)

    def test_modify_itinerary(self):
        user_id = "user1"
        preferences = {
            "budget": 1000,
            "travel_dates": {"start_date": "2024-01-01", "end_date": "2024-01-08"},
            "activity_type": "cultural",
            "destination": "Paris",
            "dietary_restrictions": "vegetarian"
        }
        self.travel_mate.add_user(user_id, preferences)
        self.travel_mate.generate_itinerary(user_id)
        itinerary = self.travel_mate.modify_itinerary(user_id, "activity", "Visit the Louvre")
        self.assertIsInstance(itinerary, list)
        self.assertGreater(len(itinerary), 0)

    def test_get_nutritional_info(self):
        user_id = "user1"
        preferences = {
            "budget": 1000,
            "travel_dates": {"start_date": "2024-01-01", "end_date": "2024-01-08"},
            "activity_type": "cultural",
            "destination": "Paris",
            "dietary_restrictions": "vegetarian"
        }
        self.travel_mate.add_user(user_id, preferences)
        self.travel_mate.generate_itinerary(user_id)
        nutritional_info = self.travel_mate.get_nutritional_info(user_id)
        self.assertIsInstance(nutritional_info, list)
        self.assertGreater(len(nutritional_info), 0)

if __name__ == "__main__":
    unittest.main()