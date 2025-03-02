# solution.py

import json
import requests
from fpdf import FPDF
from datetime import datetime
from threading import Lock

# Class to represent a travel itinerary
class Itinerary:
    def __init__(self, name):
        self.name = name
        self.destinations = []
        self.flights = []
        self.hotels = []
        self.activities = []
        self.lock = Lock()  # Lock for thread-safe operations

    def add_destination(self, destination):
        """Add a destination to the itinerary."""
        with self.lock:
            if destination not in self.destinations:
                self.destinations.append(destination)
                return True
            return False

    def remove_destination(self, destination):
        """Remove a destination from the itinerary."""
        with self.lock:
            if destination in self.destinations:
                self.destinations.remove(destination)
                return True
            return False

    def add_flight(self, flight):
        """Add a flight to the itinerary."""
        with self.lock:
            self.flights.append(flight)

    def add_hotel(self, hotel):
        """Add a hotel to the itinerary."""
        with self.lock:
            self.hotels.append(hotel)

    def add_activity(self, activity):
        """Add an activity to the itinerary."""
        with self.lock:
            self.activities.append(activity)

    def generate_pdf(self):
        """Generate a PDF of the itinerary."""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt=self.name, ln=True, align='C')
        pdf.cell(200, 10, txt="Destinations:", ln=True)
        for destination in self.destinations:
            pdf.cell(200, 10, txt=destination, ln=True)

        pdf.cell(200, 10, txt="Flights:", ln=True)
        for flight in self.flights:
            pdf.cell(200, 10, txt=flight, ln=True)

        pdf.cell(200, 10, txt="Hotels:", ln=True)
        for hotel in self.hotels:
            pdf.cell(200, 10, txt=hotel, ln=True)

        pdf.cell(200, 10, txt="Activities:", ln=True)
        for activity in self.activities:
            pdf.cell(200, 10, txt=activity, ln=True)

        pdf_file_name = f"{self.name.replace(' ', '_')}_itinerary.pdf"
        pdf.output(pdf_file_name)
        return pdf_file_name

# Class to handle travel planning
class TravelPlanner:
    def __init__(self):
        self.itineraries = {}

    def create_itinerary(self, name):
        """Create a new itinerary."""
        if name not in self.itineraries:
            self.itineraries[name] = Itinerary(name)
            return True
        return False

    def get_itinerary(self, name):
        """Get an itinerary by name."""
        return self.itineraries.get(name)

    def fetch_flight_info(self, flight_number):
        """Fetch real-time flight information from an API."""
        # Placeholder for actual API call        try:
            response = requests.get(f"https://api.example.com/flights/{flight_number}")
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 429:
                print("Error: Too many requests. Please try again later.")
            else:
                print(f"HTTP error occurred: {http_err}")        return None        else:
            return None

    def send_notification(self, message):
        """Send a notification to the user."""
        # Placeholder for notification logic
        print(f"Notification: {message}")

# Example usage
if __name__ == "__main__":
    planner = TravelPlanner()
    planner.create_itinerary("Summer Vacation")
    itinerary = planner.get_itinerary("Summer Vacation")
    itinerary.add_destination("Paris")
    itinerary.add_flight("Flight 123")
    itinerary.add_hotel("Hotel de Paris")
    itinerary.add_activity("Visit Eiffel Tower")
    
    # Generate PDF
    pdf_file = itinerary.generate_pdf()
    print(f"Itinerary PDF generated: {pdf_file}")

# Testing suite (simplified for demonstration)
def test_add_destination():
    planner = TravelPlanner()
    planner.create_itinerary("Test Trip")
    itinerary = planner.get_itinerary("Test Trip")
    assert itinerary.add_destination("New York") == True
    assert itinerary.add_destination("New York") == False  # Duplicate

def test_fetch_flight_info():
    planner = TravelPlanner()
    flight_info = planner.fetch_flight_info("Flight 123")
    assert flight_info is not None  # Assuming the API is available

# More tests would be added here for other functionalities