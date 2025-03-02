# solution.py
import datetime
from dataclasses import dataclass
from typing import List

# Define a data class for activities
@dataclass
class Activity:
    """Class to represent an activity."""
    name: str
    description: str
    price: float
    reviews: List[str]

# Define a data class for accommodations
@dataclass
class Accommodation:
    """Class to represent an accommodation."""
    name: str
    description: str
    price: float
    reviews: List[str]
    nutritional_info: str = ""

# Define a data class for transportation options
@dataclass
class Transportation:
    """Class to represent a transportation option."""
    name: str
    description: str
    price: float
    reviews: List[str]

# Define a data class for destinations
@dataclass
class Destination:
    """Class to represent a destination."""
    name: str
    description: str
    activities: List[Activity]
    accommodations: List[Accommodation]
    transportation: List[Transportation]

# Define a class for the TravelMate system
class TravelMate:
    """Class to represent the TravelMate system."""
    def __init__(self):
        self.destinations = []
        self.itineraries = {}

    def add_destination(self, destination: Destination):
        """Add a destination to the system."""
        self.destinations.append(destination)

    def generate_itinerary(self, user_preferences: dict):
        """Generate a personalized itinerary based on user preferences."""
        # Check if the user has provided valid travel dates
        if user_preferences["end_date"] < user_preferences["start_date"]:
            return "Error: Invalid travel dates. End date cannot be before start date."

        # Initialize the itinerary
        itinerary = {
            "destinations": [],
            "activities": [],
            "accommodations": [],
            "transportation": []
        }
'budget': user_preferences['budget'],
        'dietary_restrictions': user_preferences.get('dietary_restrictions', [])

        # Loop through the destinations and add them to the itinerary
        for destination in self.destinations:
            # Check if the destination matches the user's preferences
            if destination.name in user_preferences["preferred_destinations"]:
                itinerary["destinations"].append(destination)

                # Add activities to the itinerary
                for activity in destination.activities:
                    if activity.name in user_preferences["preferred_activities"]:
                        itinerary["activities"].append(activity)

                # Add accommodations to the itinerary
                for accommodation in destination.accommodations:
                    if accommodation.name in user_preferences["preferred_accommodations"]:
                        itinerary["accommodations"].append(accommodation)

                # Add transportation options to the itinerary
                for transportation in destination.transportation:
                    if transportation.name in user_preferences["preferred_transportation"]:
                        itinerary["transportation"].append(transportation)

        return itinerary

    def save_itinerary(self, user_id: int, itinerary: dict):
        """Save an itinerary for a user."""
        self.itineraries[user_id] = itinerary

    def modify_itinerary(self, user_id: int, itinerary: dict):
        """Modify an existing itinerary for a user."""
        if user_id in self.itineraries:
            self.itineraries[user_id] = itinerary
        else:
            return "Error: Itinerary not found for user."

# Define a test suite for the TravelMate system
class TestTravelMate:
    """Class to represent the test suite for the TravelMate system."""
    def __init__(self):
        self.travel_mate = TravelMate()

    def test_case_1(self):
        """Test case 1: Input valid travel preferences and verify that the generated itinerary is personalized and includes all required elements."""
        # Create a destination
        destination = Destination(
            name="Paris",
            description="The city of love",
            activities=[
                Activity(
                    name="Eiffel Tower",
                    description="The iconic Eiffel Tower",
                    price=20.0,
                    reviews=["Great experience!", "Beautiful view!"]
                )
            ],
            accommodations=[
                Accommodation(
                    name="Hotel Eiffel",
                    description="A luxurious hotel",
                    price=100.0,
                    reviews=["Great service!", "Comfortable room!"],
                    nutritional_info="Vegetarian options available"
                )
            ],
            transportation=[
                Transportation(
                    name="Metro",
                    description="The Paris metro system",
                    price=2.0,
                    reviews=["Easy to use!", "Convenient!"]
                )
            ]
        )

        # Add the destination to the TravelMate system
        self.travel_mate.add_destination(destination)

        # Generate an itinerary
        user_preferences = {
            "start_date": datetime.date(2024, 9, 1),
            "end_date": datetime.date(2024, 9, 10),
            "preferred_destinations": ["Paris"],
            "preferred_activities": ["Eiffel Tower"],
            "preferred_accommodations": ["Hotel Eiffel"],
            "preferred_transportation": ["Metro"]
        }
        itinerary = self.travel_mate.generate_itinerary(user_preferences)

        # Verify that the itinerary is personalized and includes all required elements
        assert len(itinerary["destinations"]) == 1
        assert len(itinerary["activities"]) == 1
        assert len(itinerary["accommodations"]) == 1
        assert len(itinerary["transportation"]) == 1

    def test_case_2(self):
        """Test case 2: Input invalid travel dates and verify that the system returns an appropriate error message."""
        # Generate an itinerary with invalid travel dates
        user_preferences = {
            "start_date": datetime.date(2024, 9, 10),
            "end_date": datetime.date(2024, 9, 1),
            "preferred_destinations": ["Paris"],
            "preferred_activities": ["Eiffel Tower"],
            "preferred_accommodations": ["Hotel Eiffel"],
            "preferred_transportation": ["Metro"]
        }
        itinerary = self.travel_mate.generate_itinerary(user_preferences)

        # Verify that the system returns an error message
        assert itinerary == "Error: Invalid travel dates. End date cannot be before start date."

    def test_case_3(self):
        """Test case 3: Test the save and modify itinerary feature by adding and removing items and verifying that the changes are reflected correctly."""
        # Create a destination
        destination = Destination(
            name="Paris",
            description="The city of love",
            activities=[
                Activity(
                    name="Eiffel Tower",
                    description="The iconic Eiffel Tower",
                    price=20.0,
                    reviews=["Great experience!", "Beautiful view!"]
                )
            ],
            accommodations=[
                Accommodation(
                    name="Hotel Eiffel",
                    description="A luxurious hotel",
                    price=100.0,
                    reviews=["Great service!", "Comfortable room!"],
                    nutritional_info="Vegetarian options available"
                )
            ],
            transportation=[
                Transportation(
                    name="Metro",
                    description="The Paris metro system",
                    price=2.0,
                    reviews=["Easy to use!", "Convenient!"]
                )
            ]
        )

        # Add the destination to the TravelMate system
        self.travel_mate.add_destination(destination)

        # Generate an itinerary
        user_preferences = {
            "start_date": datetime.date(2024, 9, 1),
            "end_date": datetime.date(2024, 9, 10),
            "preferred_destinations": ["Paris"],
            "preferred_activities": ["Eiffel Tower"],
            "preferred_accommodations": ["Hotel Eiffel"],
            "preferred_transportation": ["Metro"]
        }
        itinerary = self.travel_mate.generate_itinerary(user_preferences)

        # Save the itinerary
        self.travel_mate.save_itinerary(1, itinerary)

        # Modify the itinerary
        modified_itinerary = {
            "destinations": itinerary["destinations"],
            "activities": itinerary["activities"],
            "accommodations": itinerary["accommodations"],
            "transportation": itinerary["transportation"]
        }
        modified_itinerary["activities"].append(
            Activity(
                name="Louvre Museum",
                description="The famous Louvre Museum",
                price=15.0,
                reviews=["Great art!", "Beautiful building!"]
            )
        )
        self.travel_mate.modify_itinerary(1, modified_itinerary)

        # Verify that the changes are reflected correctly
        assert len(self.travel_mate.itineraries[1]["activities"]) == 2

    def test_case_4(self):
        """Test case 4: Input a user with no travel history and verify that the system still generates a personalized itinerary based on the provided preferences."""
        # Generate an itinerary for a user with no travel history
        user_preferences = {
            "start_date": datetime.date(2024, 9, 1),
            "end_date": datetime.date(2024, 9, 10),
            "preferred_destinations": ["Paris"],
            "preferred_activities": ["Eiffel Tower"],
            "preferred_accommodations": ["Hotel Eiffel"],
            "preferred_transportation": ["Metro"]
        }
        itinerary = self.travel_mate.generate_itinerary(user_preferences)

        # Verify that the system generates a personalized itinerary
        assert len(itinerary["destinations"]) == 0
        assert len(itinerary["activities"]) == 0
        assert len(itinerary["accommodations"]) == 0
        assert len(itinerary["transportation"]) == 0

    def test_case_5(self):
        """Test case 5: Test edge cases such as extremely tight budgets or very short travel durations to ensure the system can handle these scenarios gracefully."""
        # Generate an itinerary with an extremely tight budget
        user_preferences = {
            "start_date": datetime.date(2024, 9, 1),
            "end_date": datetime.date(2024, 9, 10),
            "preferred_destinations": ["Paris"],
            "preferred_activities": ["Eiffel Tower"],
            "preferred_accommodations": ["Hotel Eiffel"],
            "preferred_transportation": ["Metro"],
            "budget": 0.0
        }
        itinerary = self.travel_mate.generate_itinerary(user_preferences)

        # Verify that the system handles the edge case gracefully
        assert len(itinerary["destinations"]) == 0
        assert len(itinerary["activities"]) == 0
        assert len(itinerary["accommodations"]) == 0
        assert len(itinerary["transportation"]) == 0

# Run the test suite
test_travel_mate = TestTravelMate()
test_travel_mate.test_case_1()
test_travel_mate.test_case_2()
test_travel_mate.test_case_3()
test_travel_mate.test_case_4()
test_travel_mate.test_case_5()

# Create a TravelMate system and generate an itinerary
travel_mate = TravelMate()
destination = Destination(
    name="Paris",
    description="The city of love",
    activities=[
        Activity(
            name="Eiffel Tower",
            description="The iconic Eiffel Tower",
            price=20.0,
            reviews=["Great experience!", "Beautiful view!"]
        )
    ],
    accommodations=[
        Accommodation(
            name="Hotel Eiffel",
            description="A luxurious hotel",
            price=100.0,
            reviews=["Great service!", "Comfortable room!"],
            nutritional_info="Vegetarian options available"
        )
    ],
    transportation=[
        Transportation(
            name="Metro",
            description="The Paris metro system",
            price=2.0,
            reviews=["Easy to use!", "Convenient!"]
        )
    ]
)
travel_mate.add_destination(destination)
user_preferences = {
    "start_date": datetime.date(2024, 9, 1),
    "end_date": datetime.date(2024, 9, 10),
    "preferred_destinations": ["Paris"],
    "preferred_activities": ["Eiffel Tower"],
    "preferred_accommodations": ["Hotel Eiffel"],
    "preferred_transportation": ["Metro"]
}
itinerary = travel_mate.generate_itinerary(user_preferences)
print(itinerary)