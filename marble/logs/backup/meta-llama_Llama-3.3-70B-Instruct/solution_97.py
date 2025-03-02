# solution.py
import os
import json
from datetime import datetime
from fpdf import FPDF
import requests
from unittest import TestCase, main

# TravelPlanner class
class TravelPlanner:
    def __init__(self):
        # Initialize an empty dictionary to store itineraries
        self.itineraries = {}

    # Method to create a new itinerary
    def create_itinerary(self, name):
        # Check if the itinerary already exists
        if name in self.itineraries:
            print("Itinerary already exists.")
            return
        # Create a new itinerary with an empty dictionary
        self.itineraries[name] = {
            "destinations": [],
            "flights": [],
            "hotels": [],
            "activities": []
        }
        print(f"Itinerary '{name}' created successfully.")

    # Method to add a destination to an itinerary
    def add_destination(self, itinerary_name, destination):
        # Check if the itinerary exists
        if itinerary_name not in self.itineraries:
            print("Itinerary does not exist.")
            return
        # Add the destination to the itinerary
        self.itineraries[itinerary_name]["destinations"].append(destination)
        print(f"Destination '{destination}' added to itinerary '{itinerary_name}'.")

    # Method to remove a destination from an itinerary
    def remove_destination(self, itinerary_name, destination):
        # Check if the itinerary exists
        if itinerary_name not in self.itineraries:
            print("Itinerary does not exist.")
            return
        # Remove the destination from the itinerary
        if destination in self.itineraries[itinerary_name]["destinations"]:
            self.itineraries[itinerary_name]["destinations"].remove(destination)
            print(f"Destination '{destination}' removed from itinerary '{itinerary_name}'.")
        else:
            print(f"Destination '{destination}' not found in itinerary '{itinerary_name}'.")

    # Method to add a flight to an itinerary
    def add_flight(self, itinerary_name, flight):
        # Check if the itinerary exists
        if itinerary_name not in self.itineraries:
            print("Itinerary does not exist.")
            return
        # Add the flight to the itinerary
        self.itineraries[itinerary_name]["flights"].append(flight)
        print(f"Flight '{flight}' added to itinerary '{itinerary_name}'.")

    # Method to remove a flight from an itinerary
    def remove_flight(self, itinerary_name, flight):
        # Check if the itinerary exists
        if itinerary_name not in self.itineraries:
            print("Itinerary does not exist.")
            return
        # Remove the flight from the itinerary
        if flight in self.itineraries[itinerary_name]["flights"]:
            self.itineraries[itinerary_name]["flights"].remove(flight)
            print(f"Flight '{flight}' removed from itinerary '{itinerary_name}'.")
        else:
            print(f"Flight '{flight}' not found in itinerary '{itinerary_name}'.")

    # Method to add a hotel to an itinerary
    def add_hotel(self, itinerary_name, hotel):
        # Check if the itinerary exists
        if itinerary_name not in self.itineraries:
            print("Itinerary does not exist.")
            return
        # Add the hotel to the itinerary
        self.itineraries[itinerary_name]["hotels"].append(hotel)
        print(f"Hotel '{hotel}' added to itinerary '{itinerary_name}'.")

    # Method to remove a hotel from an itinerary
    def remove_hotel(self, itinerary_name, hotel):
        # Check if the itinerary exists
        if itinerary_name not in self.itineraries:
            print("Itinerary does not exist.")
            return
        # Remove the hotel from the itinerary
        if hotel in self.itineraries[itinerary_name]["hotels"]:
            self.itineraries[itinerary_name]["hotels"].remove(hotel)
            print(f"Hotel '{hotel}' removed from itinerary '{itinerary_name}'.")
        else:
            print(f"Hotel '{hotel}' not found in itinerary '{itinerary_name}'.")

    # Method to add an activity to an itinerary
    def add_activity(self, itinerary_name, activity):
        # Check if the itinerary exists
        if itinerary_name not in self.itineraries:
            print("Itinerary does not exist.")
            return
        # Add the activity to the itinerary
        self.itineraries[itinerary_name]["activities"].append(activity)
        print(f"Activity '{activity}' added to itinerary '{itinerary_name}'.")

    # Method to remove an activity from an itinerary
    def remove_activity(self, itinerary_name, activity):
        # Check if the itinerary exists
        if itinerary_name not in self.itineraries:
            print("Itinerary does not exist.")
            return
        # Remove the activity from the itinerary
        if activity in self.itineraries[itinerary_name]["activities"]:
            self.itineraries[itinerary_name]["activities"].remove(activity)
            print(f"Activity '{activity}' removed from itinerary '{itinerary_name}'.")
        else:
            print(f"Activity '{activity}' not found in itinerary '{itinerary_name}'.")

    # Method to generate a PDF itinerary
    def generate_pdf(self, itinerary_name):
        # Check if the itinerary exists
        if itinerary_name not in self.itineraries:
            print("Itinerary does not exist.")
            return
        # Create a PDF object
        pdf = FPDF()
        # Add a page to the PDF
        pdf.add_page()
        # Set the font of the PDF
        pdf.set_font("Arial", size=15)
        # Add the itinerary name to the PDF
        pdf.cell(200, 10, txt=f"Itinerary: {itinerary_name}", ln=True, align='C')
        # Add the destinations to the PDF
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Destinations:", ln=True, align='L')
        for destination in self.itineraries[itinerary_name]["destinations"]:
            pdf.cell(200, 10, txt=destination, ln=True, align='L')
        # Add the flights to the PDF
        pdf.cell(200, 10, txt="Flights:", ln=True, align='L')
        for flight in self.itineraries[itinerary_name]["flights"]:
            pdf.cell(200, 10, txt=flight, ln=True, align='L')
        # Add the hotels to the PDF
        pdf.cell(200, 10, txt="Hotels:", ln=True, align='L')
        for hotel in self.itineraries[itinerary_name]["hotels"]:
            pdf.cell(200, 10, txt=hotel, ln=True, align='L')
        # Add the activities to the PDF
        pdf.cell(200, 10, txt="Activities:", ln=True, align='L')
        for activity in self.itineraries[itinerary_name]["activities"]:
            pdf.cell(200, 10, txt=activity, ln=True, align='L')
        # Save the PDF
        pdf.output(f"{itinerary_name}.pdf")
        print(f"PDF itinerary '{itinerary_name}.pdf' generated successfully.")

    # Method to fetch real-time flight information
    def fetch_flight_info(self, flight_number):url = f"https://api.skyscanner.net/api/flight/search?api_key=YOUR_API_KEY&flight_number={flight_number}"try:
    response = requests.get(url, timeout=10)
except requests.exceptions.Timeout:
    print("Timeout error: Failed to fetch flight information")
    returnif response.status_code == 200:try:
    flight_info = response.json()
except ValueError:
    print("Invalid JSON response: Failed to parse flight information")
    returnprint(f"Flight {flight_number} information:")
            print(f"Departure: {flight_info['departure']}")
            print(f"Arrival: {flight_info['arrival']}")
            print(f"Status: {flight_info['status']}")
        else:
            print(f"Failed to fetch flight information for {flight_number}.")

    # Method to send real-time notifications
    def send_notification(self, message):url = "https://api.pushover.net/1/messages.json"        # Send a POST request to the API
ACTUAL_PUSHOVER_API_KEY = "your_actual_pushover_api_key"ACTUAL_PUSHOVER_API_KEYurl = f"https://api.pushover.net/1/messages.json?token={ACTUAL_PUSHOVER_API_KEY}"try:
    response = requests.post(url, json={"message": message}, timeout=10)
except requests.exceptions.Timeout:
    print("Timeout error: Failed to send notification")
    returnif response.status_code == 200:
except requests.exceptions.RequestException as e:    print(f"Error sending notification: {e}")
        try:
            response = requests.post(url, json={"message": message}, timeout=10)
        except requests.exceptions.Timeout:
            print("Timeout error: Failed to send notification")
            return
            print(f"Notification sent successfully: {message}")
        else:
            print(f"Failed to send notification: {message}")


# Test cases for the TravelPlanner class
class TestTravelPlanner(TestCase):
    def setUp(self):
        self.travel_planner = TravelPlanner()

    def test_create_itinerary(self):
        self.travel_planner.create_itinerary("Test Itinerary")
        self.assertIn("Test Itinerary", self.travel_planner.itineraries)

    def test_add_destination(self):
        self.travel_planner.create_itinerary("Test Itinerary")
        self.travel_planner.add_destination("Test Itinerary", "New York")
        self.assertIn("New York", self.travel_planner.itineraries["Test Itinerary"]["destinations"])

    def test_remove_destination(self):
        self.travel_planner.create_itinerary("Test Itinerary")
        self.travel_planner.add_destination("Test Itinerary", "New York")
        self.travel_planner.remove_destination("Test Itinerary", "New York")
        self.assertNotIn("New York", self.travel_planner.itineraries["Test Itinerary"]["destinations"])

    def test_add_flight(self):
        self.travel_planner.create_itinerary("Test Itinerary")
        self.travel_planner.add_flight("Test Itinerary", "AA123")
        self.assertIn("AA123", self.travel_planner.itineraries["Test Itinerary"]["flights"])

    def test_remove_flight(self):
        self.travel_planner.create_itinerary("Test Itinerary")
        self.travel_planner.add_flight("Test Itinerary", "AA123")
        self.travel_planner.remove_flight("Test Itinerary", "AA123")
        self.assertNotIn("AA123", self.travel_planner.itineraries["Test Itinerary"]["flights"])

    def test_add_hotel(self):
        self.travel_planner.create_itinerary("Test Itinerary")
        self.travel_planner.add_hotel("Test Itinerary", "Hotel A")
        self.assertIn("Hotel A", self.travel_planner.itineraries["Test Itinerary"]["hotels"])

    def test_remove_hotel(self):
        self.travel_planner.create_itinerary("Test Itinerary")
        self.travel_planner.add_hotel("Test Itinerary", "Hotel A")
        self.travel_planner.remove_hotel("Test Itinerary", "Hotel A")
        self.assertNotIn("Hotel A", self.travel_planner.itineraries["Test Itinerary"]["hotels"])

    def test_add_activity(self):
        self.travel_planner.create_itinerary("Test Itinerary")
        self.travel_planner.add_activity("Test Itinerary", "Activity A")
        self.assertIn("Activity A", self.travel_planner.itineraries["Test Itinerary"]["activities"])

    def test_remove_activity(self):
        self.travel_planner.create_itinerary("Test Itinerary")
        self.travel_planner.add_activity("Test Itinerary", "Activity A")
        self.travel_planner.remove_activity("Test Itinerary", "Activity A")
        self.assertNotIn("Activity A", self.travel_planner.itineraries["Test Itinerary"]["activities"])

    def test_generate_pdf(self):
        self.travel_planner.create_itinerary("Test Itinerary")
        self.travel_planner.add_destination("Test Itinerary", "New York")
        self.travel_planner.add_flight("Test Itinerary", "AA123")
        self.travel_planner.add_hotel("Test Itinerary", "Hotel A")
        self.travel_planner.add_activity("Test Itinerary", "Activity A")
        self.travel_planner.generate_pdf("Test Itinerary")
        self.assertTrue(os.path.exists("Test Itinerary.pdf"))

    def test_fetch_flight_info(self):
        self.travel_planner.fetch_flight_info("AA123")

    def test_send_notification(self):
        self.travel_planner.send_notification("Test notification")


if __name__ == "__main__":
    main()