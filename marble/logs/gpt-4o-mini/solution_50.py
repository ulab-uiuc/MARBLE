# solution.py

from datetime import datetime
from typing import List, Dict, Any

class TravelMate:
    def __init__(self):
        # Initialize an empty itinerary
        self.itinerary = []

    def input_preferences(self, budget: float, start_date: str, end_date: str, activities: List[str], dietary_restrictions: List[str]):
        """
        Input user travel preferences and validate the dates.
        """
        self.budget = budget
        self.start_date = self.validate_date(start_date)
        self.end_date = self.validate_date(end_date)
        self.activities = activities
        self.dietary_restrictions = dietary_restrictions

        # Check if the end date is before the start date
        if self.start_date >= self.end_date:
            raise ValueError("End date must be after start date.")

    def validate_date(self, date_str: str) -> datetime:
        """
        Validate and convert date string to datetime object.
        """
        return datetime.strptime(date_str, "%Y-%m-%d")

    def generate_itinerary(self) -> List[Dict[str, Any]]:
        """
        Generate a personalized itinerary based on user preferences.
        """
        # Sample data for recommendations
        recommendations = [
            {
                "destination": "Paris",
                "description": "The city of lights, known for its art, fashion, and culture.",
                "price": 1200,
                "user_reviews": ["Amazing experience!", "Loved the Eiffel Tower!"],
                "activities": ["Cultural", "Relaxation"],
                "accommodation": "Hotel de Paris",
                "transportation": "Metro",
                "nutritional_info": "Vegan options available."
            },
            {
                "destination": "Tokyo",
                "description": "A bustling metropolis blending tradition and modernity.",
                "price": 1500,
                "user_reviews": ["Incredible food!", "Great shopping!"],
                "activities": ["Cultural", "Adventure"],
                "accommodation": "Tokyo Inn",
                "transportation": "Subway",
                "nutritional_info": "Gluten-free options available."
            }
        ]

        # Filter recommendations based on user preferences
        for rec in recommendations:for rec in recommendations:
            if rec["price"] <= self.budget and any(activity in rec["activities"] for activity in self.activities) and self.check_dietary_restrictions(rec):
                self.itinerary.append(rec)                self.itinerary.append(rec)

        return self.itinerary

    def save_itinerary(self, itinerary: List[Dict[str, Any]]):
        """
        Save the current itinerary.
        """
    def check_dietary_restrictions(self, recommendation: Dict[str, Any]) -> bool:
        """
        Check if the recommendation meets the user's dietary restrictions.
        """
        if not self.dietary_restrictions:
            return True
        for restriction in self.dietary_restrictions:
            if restriction.lower() in recommendation['nutritional_info'].lower():
                return True
        return False
        self.itinerary = itinerary

    def modify_itinerary(self, action: str, item: Dict[str, Any]):
        """
        Modify the itinerary by adding or removing items.
        """
        if action == "add":
            self.itinerary.append(item)
        elif action == "remove":
            self.itinerary.remove(item)

    def display_itinerary(self):
        """
        Display the current itinerary.
        """
        return self.itinerary


# Test Suite
def test_travel_mate():
    travel_mate = TravelMate()

    # Test case 1: Valid travel preferences
    try:
        travel_mate.input_preferences(2000, "2023-10-01", "2023-10-10", ["Cultural"], [])
        itinerary = travel_mate.generate_itinerary()
        assert len(itinerary) > 0, "Itinerary should not be empty."
    except Exception as e:
        print(f"Test case 1 failed: {e}")

    # Test case 2: Invalid travel dates
    try:
        travel_mate.input_preferences(2000, "2023-10-10", "2023-10-01", ["Cultural"], [])
    except ValueError as e:
        assert str(e) == "End date must be after start date.", "Error message not as expected."

    # Test case 3: Modify itinerary
    travel_mate.save_itinerary(itinerary)
    new_item = {
        "destination": "New York",
        "description": "The city that never sleeps.",
        "price": 1800,
        "user_reviews": ["Great nightlife!", "Central Park is beautiful."],
        "activities": ["Cultural"],
        "accommodation": "NY Hotel",
        "transportation": "Taxi",
        "nutritional_info": "Vegetarian options available."
    }
    travel_mate.modify_itinerary("add", new_item)
    assert len(travel_mate.itinerary) == 3, "Itinerary should have 3 items after adding."

    travel_mate.modify_itinerary("remove", new_item)
    assert len(travel_mate.itinerary) == 2, "Itinerary should have 2 items after removing."

    # Test case 4: User with no travel history
    travel_mate = TravelMate()
    travel_mate.input_preferences(2000, "2023-10-01", "2023-10-10", ["Adventure"], [])
    itinerary = travel_mate.generate_itinerary()
    assert len(itinerary) > 0, "Itinerary should not be empty for a new user."

    # Test case 5: Edge case with tight budget
    travel_mate.input_preferences(500, "2023-10-01", "2023-10-10", ["Cultural"], [])
    itinerary = travel_mate.generate_itinerary()
    assert len(itinerary) == 0, "Itinerary should be empty for a tight budget."

# Run tests
test_travel_mate()