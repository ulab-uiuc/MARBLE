# travel_mate.py
# This is the main implementation of the TravelMate application.

import datetime
import unittest

class Destination:
    """Represents a destination with its name, description, price, and user reviews."""
    def __init__(self, name, description, price, reviews):
        self.name = name
        self.description = description
        self.price = price
        self.reviews = reviews

class Activity:
    """Represents an activity with its name, description, price, and user reviews."""
    def __init__(self, name, description, price, reviews):
        self.name = name
        self.description = description
        self.price = price
        self.reviews = reviews

class Accommodation:
    """Represents an accommodation with its name, description, price, and user reviews."""
    def __init__(self, name, description, price, reviews):
        self.name = name
        self.description = description
        self.price = price
        self.reviews = reviews

class Transportation:
    """Represents a transportation option with its name, description, price, and user reviews."""
    def __init__(self, name, description, price, reviews):
        self.name = name
        self.description = description
        self.price = price
        self.reviews = reviews

class Itinerary:
    """Represents a personalized itinerary with its destinations, activities, accommodations, and transportation options."""
    def __init__(self):
        self.destinations = []
        self.activities = []
        self.accommodations = []
        self.transportation = []

    def add_destination(self, destination):
        self.destinations.append(destination)

    def add_activity(self, activity):
        self.activities.append(activity)

    def add_accommodation(self, accommodation):
        self.accommodations.append(accommodation)

    def add_transportation(self, transportation):
        self.transportation.append(transportation)

    def remove_destination(self, destination_name):
        self.destinations = [d for d in self.destinations if d.name != destination_name]

    def remove_activity(self, activity_name):
        self.activities = [a for a in self.activities if a.name != activity_name]

    def remove_accommodation(self, accommodation_name):
        self.accommodations = [a for a in self.accommodations if a.name != accommodation_name]

    def remove_transportation(self, transportation_name):
        self.transportation = [t for t in self.transportation if t.name != transportation_name]

class TravelMate:
    """Represents the TravelMate application with its user preferences and itinerary."""
    def __init__(self):
        self.user_preferences = {}
        self.itinerary = Itinerary()

    def set_user_preferences(self, budget, travel_dates, activities, dietary_restrictions):
        self.user_preferences['budget'] = budget
        self.user_preferences['travel_dates'] = travel_dates
        self.user_preferences['activities'] = activities
        self.user_preferences['dietary_restrictions'] = dietary_restrictions

    def generate_itinerary(self):
        # Generate destinations based on user preferences
        destinations = []
        if 'cultural' in self.user_preferences['activities']:
            destinations.append(Destination('Paris', 'The City of Love', 1000, 4.5))
            destinations.append(Destination('Rome', 'The Eternal City', 1200, 4.8))
        if 'adventure' in self.user_preferences['activities']:
            destinations.append(Destination('Queenstown', 'The Adventure Capital', 1500, 4.9))
            destinations.append(Destination('Interlaken', 'The Adventure Hub', 1800, 4.7))
        if 'relaxation' in self.user_preferences['activities']:
            destinations.append(Destination('Bali', 'The Island of Gods', 800, 4.6))
            destinations.append(Destination('Maldives', 'The Tropical Paradise', 2000, 4.9))

        # Generate activities based on user preferences
        activities = []
        if 'cultural' in self.user_preferences['activities']:
            activities.append(Activity('Visit the Eiffel Tower', 'Experience the iconic landmark', 50, 4.5))
            activities.append(Activity('Explore the Colosseum', 'Discover the ancient history', 60, 4.8))
        if 'adventure' in self.user_preferences['activities']:
            activities.append(Activity('Skydiving in Queenstown', 'Feel the rush of adventure', 200, 4.9))
            activities.append(Activity('Paragliding in Interlaken', 'Soar through the skies', 250, 4.7))
        if 'relaxation' in self.user_preferences['activities']:
            activities.append(Activity('Yoga in Bali', 'Find inner peace', 30, 4.6))
            activities.append(Activity('Snorkeling in Maldives', 'Explore the underwater world', 100, 4.9))

        # Generate accommodations based on user preferences
        accommodations = []
        if 'budget' in self.user_preferences['activities']:
            accommodations.append(Accommodation('Hostel in Paris', 'Affordable and cozy', 20, 4.2))
            accommodations.append(Accommodation('Guesthouse in Rome', 'Comfortable and clean', 30, 4.5))
        if 'mid-range' in self.user_preferences['activities']:
            accommodations.append(Accommodation('Hotel in Queenstown', 'Modern and stylish', 80, 4.8))
            accommodations.append(Accommodation('Resort in Interlaken', 'Luxurious and scenic', 120, 4.9))
        if 'luxury' in self.user_preferences['activities']:
            accommodations.append(Accommodation('Villa in Bali', 'Private and serene', 150, 4.9))
            accommodations.append(Accommodation('Mansion in Maldives', 'Opulent and breathtaking', 300, 5.0))

        # Generate transportation options based on user preferences
        transportation = []
        if 'budget' in self.user_preferences['activities']:
            transportation.append(Transportation('Bus in Paris', 'Affordable and convenient', 10, 4.2))
            transportation.append(Transportation('Train in Rome', 'Comfortable and scenic', 20, 4.5))
        if 'mid-range' in self.user_preferences['activities']:
            transportation.append(Transportation('Taxi in Queenstown', 'Modern and efficient', 50, 4.8))
            transportation.append(Transportation('Rental Car in Interlaken', 'Flexible and convenient', 80, 4.9))
        if 'luxury' in self.user_preferences['activities']:
            transportation.append(Transportation('Private Car in Bali', 'Luxurious and personalized', 150, 4.9))
            transportation.append(Transportation('Helicopter in Maldives', 'Breathtaking and exclusive', 300, 5.0))

        # Add destinations, activities, accommodations, and transportation options to the itinerary
        self.itinerary.add_destination(destinations[0])
        self.itinerary.add_destination(destinations[1])
        self.itinerary.add_activity(activities[0])
        self.itinerary.add_activity(activities[1])
        self.itinerary.add_accommodation(accommodations[0])
        self.itinerary.add_accommodation(accommodations[1])
        self.itinerary.add_transportation(transportation[0])
        self.itinerary.add_transportation(transportation[1])

    def save_itinerary(self):
        # Save the itinerary to a file
        with open('itinerary.txt', 'w') as f:
            f.write('Destinations:\n')
            for destination in self.itinerary.destinations:
                f.write(f'- {destination.name}: {destination.description}, ${destination.price}, {destination.reviews}\n')
            f.write('\nActivities:\n')
            for activity in self.itinerary.activities:
                f.write(f'- {activity.name}: {activity.description}, ${activity.price}, {activity.reviews}\n')
            f.write('\nAccommodations:\n')
            for accommodation in self.itinerary.accommodations:
                f.write(f'- {accommodation.name}: {accommodation.description}, ${accommodation.price}, {accommodation.reviews}\n')
            f.write('\nTransportation:\n')
            for transportation in self.itinerary.transportation:
                f.write(f'- {transportation.name}: {transportation.description}, ${transportation.price}, {transportation.reviews}\n')

    def modify_itinerary(self):
        # Modify the itinerary based on user input
        print('Modify Itinerary:')
        print('1. Add Destination')
        print('2. Add Activity')
        print('3. Add Accommodation')
        print('4. Add Transportation')
        print('5. Remove Destination')
        print('6. Remove Activity')
        print('7. Remove Accommodation')
        print('8. Remove Transportation')
        choice = input('Enter your choice: ')
        if choice == '1':
            destination_name = input('Enter destination name: ')
            destination_description = input('Enter destination description: ')
            destination_price = float(input('Enter destination price: '))
            destination_reviews = float(input('Enter destination reviews: '))
            self.itinerary.add_destination(Destination(destination_name, destination_description, destination_price, destination_reviews))
        elif choice == '2':
            activity_name = input('Enter activity name: ')
            activity_description = input('Enter activity description: ')
            activity_price = float(input('Enter activity price: '))
            activity_reviews = float(input('Enter activity reviews: '))
            self.itinerary.add_activity(Activity(activity_name, activity_description, activity_price, activity_reviews))
        elif choice == '3':
            accommodation_name = input('Enter accommodation name: ')
            accommodation_description = input('Enter accommodation description: ')
            accommodation_price = float(input('Enter accommodation price: '))
            accommodation_reviews = float(input('Enter accommodation reviews: '))
            self.itinerary.add_accommodation(Accommodation(accommodation_name, accommodation_description, accommodation_price, accommodation_reviews))
        elif choice == '4':
            transportation_name = input('Enter transportation name: ')
            transportation_description = input('Enter transportation description: ')
            transportation_price = float(input('Enter transportation price: '))
            transportation_reviews = float(input('Enter transportation reviews: '))
            self.itinerary.add_transportation(Transportation(transportation_name, transportation_description, transportation_price, transportation_reviews))
        elif choice == '5':
            destination_name = input('Enter destination name to remove: ')
            self.itinerary.remove_destination(destination_name)
        elif choice == '6':
            activity_name = input('Enter activity name to remove: ')
            self.itinerary.remove_activity(activity_name)
        elif choice == '7':
            accommodation_name = input('Enter accommodation name to remove: ')
            self.itinerary.remove_accommodation(accommodation_name)
        elif choice == '8':
            transportation_name = input('Enter transportation name to remove: ')
            self.itinerary.remove_transportation(transportation_name)

class TestTravelMate(unittest.TestCase):
    def test_generate_itinerary(self):
        travel_mate = TravelMate()
        travel_mate.set_user_preferences(1000, [datetime.date(2024, 7, 1), datetime.date(2024, 7, 15)], ['cultural', 'adventure'], 'vegetarian')
        travel_mate.generate_itinerary()
        self.assertEqual(len(travel_mate.itinerary.destinations), 2)
        self.assertEqual(len(travel_mate.itinerary.activities), 2)
        self.assertEqual(len(travel_mate.itinerary.accommodations), 2)
        self.assertEqual(len(travel_mate.itinerary.transportation), 2)

    def test_save_itinerary(self):
        travel_mate = TravelMate()
        travel_mate.set_user_preferences(1000, [datetime.date(2024, 7, 1), datetime.date(2024, 7, 15)], ['cultural', 'adventure'], 'vegetarian')
        travel_mate.generate_itinerary()
        travel_mate.save_itinerary()
        with open('itinerary.txt', 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 12)

    def test_modify_itinerary(self):
        travel_mate = TravelMate()
        travel_mate.set_user_preferences(1000, [datetime.date(2024, 7, 1), datetime.date(2024, 7, 15)], ['cultural', 'adventure'], 'vegetarian')
        travel_mate.generate_itinerary()
        travel_mate.modify_itinerary()
        self.assertEqual(len(travel_mate.itinerary.destinations), 2)
        self.assertEqual(len(travel_mate.itinerary.activities), 2)
        self.assertEqual(len(travel_mate.itinerary.accommodations), 2)
        self.assertEqual(len(travel_mate.itinerary.transportation), 2)

if __name__ == '__main__':
    unittest.main()