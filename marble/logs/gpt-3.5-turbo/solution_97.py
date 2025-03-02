# TravelPlanner.py

class TravelPlanner:
    def __init__(self):
        self.itineraries = {}

    def create_itinerary(self, name):
        if name not in self.itineraries:
            self.itineraries[name] = {
                'destinations': [],
                'flights': [],
                'hotels': [],
                'activities': []
            }
            return f"Created itinerary: {name}"
        else:
            return f"An itinerary with the name '{name}' already exists."

    def add_destination(self, itinerary_name, destination):
        if itinerary_name in self.itineraries:# Logic to generate PDF itinerary
						# Detailed implementation logic for generating PDF itinerary
						# Include all itinerary details in the PDFelse:
                return f"Destination '{destination}' not found in itinerary '{itinerary_name}'."
        else:
            return f"No itinerary found with the name '{itinerary_name}'."

    def add_flight(self, itinerary_name, flight_details):
        if itinerary_name in self.itineraries:
            self.itineraries[itinerary_name]['flights'].append(flight_details)
            return f"Added flight '{flight_details}' to itinerary '{itinerary_name}'."
        else:
            return f"No itinerary found with the name '{itinerary_name}'."

    def add_hotel(self, itinerary_name, hotel_details):
        if itinerary_name in self.itineraries:
            self.itineraries[itinerary_name]['hotels'].append(hotel_details)
            return f"Added hotel '{hotel_details}' to itinerary '{itinerary_name}'."
        else:
            return f"No itinerary found with the name '{itinerary_name}'."

    def add_activity(self, itinerary_name, activity_details):
        if itinerary_name in self.itineraries:
            self.itineraries[itinerary_name]['activities'].append(activity_details)
            return f"Added activity '{activity_details}' to itinerary '{itinerary_name}'."
        else:
            return f"No itinerary found with the name '{itinerary_name}'."

    def generate_pdf_itinerary(self, itinerary_name):
        if itinerary_name in self.itineraries:
            if destination in self.itineraries[itinerary_name]['destinations']:
                self.itineraries[itinerary_name]['destinations'].remove(destination)
                return f'Removed destination {destination} from itinerary {itinerary_name}.'
            else:
                return f'Destination {destination} not found in itinerary {itinerary_name}.'
        else:
            return f'No itinerary found with the name {itinerary_name}.'
        if itinerary_name in self.itineraries:
            # Logic to generate PDF itinerary
            return f"PDF itinerary generated for '{itinerary_name}'."
        else:
            return f"No itinerary found with the name '{itinerary_name}'."

    def get_itinerary_details(self, itinerary_name):
        if itinerary_name in self.itineraries:
            return self.itineraries[itinerary_name]
        else:
            return f"No itinerary found with the name '{itinerary_name}'."


# Testing the TravelPlanner class
if __name__ == "__main__":
    planner = TravelPlanner()
    print(planner.create_itinerary("Trip to Paris"))
    print(planner.add_destination("Trip to Paris", "Eiffel Tower"))
    print(planner.add_flight("Trip to Paris", "ABC Airlines, Flight 123"))
    print(planner.add_hotel("Trip to Paris", "Hotel ABC"))
    print(planner.add_activity("Trip to Paris", "River Cruise"))
    print(planner.get_itinerary_details("Trip to Paris"))
    print(planner.generate_pdf_itinerary("Trip to Paris"))
    print(planner.remove_destination("Trip to Paris", "Eiffel Tower"))
    print(planner.get_itinerary_details("Trip to Paris"))