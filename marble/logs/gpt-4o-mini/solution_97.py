# solution.py

import json
import requests
from fpdf import FPDF
from datetime import datetime
from threading import Lock

# Class to represent a travel itinerary
class Itinerary:
    def __init__(self, destination):
        self.destination = destination
        self.flights = []
        self.hotels = []
        self.activities = []
        self.lock = Lock()  # Lock for thread-safe operations

    def add_flight(self, flight):
        with self.lock:
            self.flights.append(flight)

    def remove_flight(self, flight):
        with self.lock:
            self.flights.remove(flight)

    def add_hotel(self, hotel):
        with self.lock:
            self.hotels.append(hotel)

    def remove_hotel(self, hotel):
        with self.lock:
            self.hotels.remove(hotel)

    def add_activity(self, activity):
        with self.lock:
            self.activities.append(activity)

    def remove_activity(self, activity):
        with self.lock:
            self.activities.remove(activity)

    def generate_pdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt=f"Itinerary for {self.destination}", ln=True, align='C')
        pdf.cell(200, 10, txt="Flights:", ln=True)
        for flight in self.flights:
            pdf.cell(200, 10, txt=flight, ln=True)

        pdf.cell(200, 10, txt="Hotels:", ln=True)
        for hotel in self.hotels:
            pdf.cell(200, 10, txt=hotel, ln=True)

        pdf.cell(200, 10, txt="Activities:", ln=True)
        for activity in self.activities:
            pdf.cell(200, 10, txt=activity, ln=True)

        pdf_file_name = f"{self.destination}_itinerary.pdf"
        pdf.output(pdf_file_name)
        return pdf_file_name

# Class to manage multiple itineraries
class TravelPlanner:
    def __init__(self):
        self.itineraries = {}

    def create_itinerary(self, destination):
        if destination not in self.itineraries:
            self.itineraries[destination] = Itinerary(destination)

    def get_itinerary(self, destination):
        return self.itineraries.get(destination)

    def delete_itinerary(self, destination):
        if destination in self.itineraries:
            del self.itineraries[destination]

# Function to fetch real-time flight information from an API
def fetch_flight_info(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()  # Return the JSON response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching flight information: {e}")
        return None

# Function to send notifications (placeholder for real implementation)
def send_notification(message):
    print(f"Notification: {message}")

# Example usage of the TravelPlanner
if __name__ == "__main__":
    planner = TravelPlanner()
    planner.create_itinerary("Paris")
    paris_itinerary = planner.get_itinerary("Paris")

    # Adding flights, hotels, and activities
    paris_itinerary.add_flight("Flight 123: NYC to Paris")
    paris_itinerary.add_hotel("Hotel de Paris")
    paris_itinerary.add_activity("Visit the Eiffel Tower")

    # Generate PDF itinerary
    pdf_file = paris_itinerary.generate_pdf()
    print(f"Itinerary PDF generated: {pdf_file}")

    # Fetch flight information (example API URL)
    flight_info = fetch_flight_info("https://api.example.com/flights")
    if flight_info:
        print("Fetched flight information:", flight_info)

    # Send a notification
    send_notification("Your flight to Paris is on time.")