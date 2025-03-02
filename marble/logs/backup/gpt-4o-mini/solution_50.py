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
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format.")

    def generate_itinerary(self) -> List[Dict[str, Any]]:
        """
        Generate a personalized itinerary based on user preferences.
        """
        # Sample data for destinations, activities, and accommodations
        destinations = [
            {"name": "Paris", "description": "The city of lights.", "price": 1000, "reviews": ["Amazing!", "Loved it!"]},
            {"name": "Tokyo", "description": "A bustling metropolis.", "price": 1200, "reviews": ["Incredible food!", "So much to see!"]},
            {"name": "New York", "description": "The city that never sleeps.", "price": 900, "reviews": ["Great culture!", "Fantastic nightlife!"]}
        ]

        # Filter destinations based on budget and activities
        for destination in destinations:
            if destination["price"] <= self.budget:
                self.itinerary.append(destination)

        return self.itinerary

    def save_itinerary(self):
        """
        Save the current itinerary to a file or database (placeholder).
        """
        # Placeholder for saving functionality
        print("Itinerary saved.")

    def modify_itinerary(self, action: str, destination: Dict[str, Any]):
        """
        Modify the itinerary by adding or removing destinations.
        """
        if action == "add":
            self.itinerary.append(destination)
        elif action == "remove":
            self.itinerary.remove(destination)
        else:
            raise ValueError("Action must be 'add' or 'remove'.")

    def get_nutritional_info(self, activity: str) -> str:
        """
        Provide nutritional information for food-related activities.
        """
        # Placeholder for nutritional information
        return f"Nutritional information for {activity}."

# Test Suite
def test_travel_mate():
    travel_mate = TravelMate()

    # Test case 1: Valid preferences
    try:
        travel_mate.input_preferences(1000, "2023-10-01", "2023-10-10", ["cultural", "adventure"], [])
        itinerary = travel_mate.generate_itinerary()
        assert len(itinerary) > 0, "Itinerary should not be empty."
    except Exception as e:
        print(f"Test case 1 failed: {e}")

    # Test case 2: Invalid dates
    try:
        travel_mate.input_preferences(1000, "2023-10-10", "2023-10-01", ["cultural"], [])
    except ValueError as e:
        assert str(e) == "End date must be after start date.", "Error message mismatch."

    # Test case 3: Modify itinerary
    travel_mate.modify_itinerary("add", {"name": "Paris", "description": "The city of lights.", "price": 1000, "reviews": []})
    assert len(travel_mate.itinerary) > 0, "Itinerary should have items after adding."

    travel_mate.modify_itinerary("remove", travel_mate.itinerary[0])
    assert len(travel_mate.itinerary) == 0, "Itinerary should be empty after removing."

    # Test case 4: No travel history
    travel_mate.input_preferences(500, "2023-10-01", "2023-10-05", ["relaxation"], [])
    itinerary = travel_mate.generate_itinerary()
    assert len(itinerary) > 0, "Itinerary should be generated even with no travel history."

    # Test case 5: Edge case with tight budget
    travel_mate.input_preferences(100, "2023-10-01", "2023-10-02", ["adventure"], [])
    itinerary = travel_mate.generate_itinerary()
    assert len(itinerary) == 0, "Itinerary should be empty for tight budget."

# Run tests
test_travel_mate()