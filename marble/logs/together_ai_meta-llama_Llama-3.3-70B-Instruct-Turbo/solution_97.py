# solution.py
import os
import json
import requests
from fpdf import FPDF
from datetime import datetime
from threading import Thread
import unittest

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
        # Create a new itinerary with an empty list of destinations
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
        print(f"PDF itinerary '{itinerary_name}' generated successfully.")

    # Method to fetch real-time flight information
    def fetch_flight_info(self, flight):
        # API endpoint for flight information
        url = f"https://api.example.com/flights/{flight}"
        # Send a GET request to the API
        response = requests.get(url)
        # Check if the response was successful
        if response.status_code == 200:
            # Return the flight information
            return response.json()
        else:
            # Return an error message
            return "Failed to fetch flight information."

    # Method to send real-time notifications
    def send_notification(self, message):
        # API endpoint for sending notifications
        url = "https://api.example.com/notifications"
        # Send a POST request to the API
        response = requests.post(url, json={"message": message})
        # Check if the response was successful
        if response.status_code == 200:
            # Return a success message
            return "Notification sent successfully."
        else:
            # Return an error message
            return "Failed to send notification."

# Collaborative feature class
class CollaborativeFeature:
    def __init__(self):
        # Initialize an empty dictionary to store user roles
        self.user_roles = {}

    # Method to add a user to an itinerary
    def add_user(self, itinerary_name, user, role):
        # Check if the itinerary exists
        if itinerary_name not in self.user_roles:
            self.user_roles[itinerary_name] = {}
        # Add the user to the itinerary
        self.user_roles[itinerary_name][user] = role
        print(f"User '{user}' added to itinerary '{itinerary_name}' with role '{role}'.")

    # Method to remove a user from an itinerary
    def remove_user(self, itinerary_name, user):
        # Check if the itinerary exists
        if itinerary_name not in self.user_roles:
            print("Itinerary does not exist.")
            return
        # Remove the user from the itinerary
        if user in self.user_roles[itinerary_name]:
            del self.user_roles[itinerary_name][user]
            print(f"User '{user}' removed from itinerary '{itinerary_name}'.")
        else:
            print(f"User '{user}' not found in itinerary '{itinerary_name}'.")

    # Method to update a user's role in an itinerary
    def update_role(self, itinerary_name, user, role):
        # Check if the itinerary exists
        if itinerary_name not in self.user_roles:
            print("Itinerary does not exist.")
            return
        # Check if the user exists in the itinerary
        if user not in self.user_roles[itinerary_name]:
            print(f"User '{user}' not found in itinerary '{itinerary_name}'.")
            return
        # Update the user's role
        self.user_roles[itinerary_name][user] = role
        print(f"User '{user}' role updated to '{role}' in itinerary '{itinerary_name}'.")

# Test cases
class TestTravelPlanner(unittest.TestCase):
    def test_create_itinerary(self):
        travel_planner = TravelPlanner()
        travel_planner.create_itinerary("Test Itinerary")
        self.assertIn("Test Itinerary", travel_planner.itineraries)

    def test_add_destination(self):
        travel_planner = TravelPlanner()
        travel_planner.create_itinerary("Test Itinerary")
        travel_planner.add_destination("Test Itinerary", "Test Destination")
        self.assertIn("Test Destination", travel_planner.itineraries["Test Itinerary"]["destinations"])

    def test_remove_destination(self):
        travel_planner = TravelPlanner()
        travel_planner.create_itinerary("Test Itinerary")
        travel_planner.add_destination("Test Itinerary", "Test Destination")
        travel_planner.remove_destination("Test Itinerary", "Test Destination")
        self.assertNotIn("Test Destination", travel_planner.itineraries["Test Itinerary"]["destinations"])

    def test_fetch_flight_info(self):
        travel_planner = TravelPlanner()
        flight_info = travel_planner.fetch_flight_info("Test Flight")
        self.assertIsInstance(flight_info, dict)

    def test_send_notification(self):
        travel_planner = TravelPlanner()
        notification = travel_planner.send_notification("Test Notification")
        self.assertEqual(notification, "Notification sent successfully.")

    def test_collaborative_feature(self):
        collaborative_feature = CollaborativeFeature()
        collaborative_feature.add_user("Test Itinerary", "Test User", "Test Role")
        self.assertIn("Test Itinerary", collaborative_feature.user_roles)
        self.assertIn("Test User", collaborative_feature.user_roles["Test Itinerary"])

if __name__ == "__main__":
    travel_planner = TravelPlanner()
    collaborative_feature = CollaborativeFeature()
    while True:
        print("1. Create Itinerary")
        print("2. Add Destination")
        print("3. Remove Destination")
        print("4. Add Flight")
        print("5. Remove Flight")
        print("6. Add Hotel")
        print("7. Remove Hotel")
        print("8. Add Activity")
        print("9. Remove Activity")
        print("10. Generate PDF")
        print("11. Fetch Flight Info")
        print("12. Send Notification")
        print("13. Add User")
        print("14. Remove User")
        print("15. Update Role")
        print("16. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            name = input("Enter itinerary name: ")
            travel_planner.create_itinerary(name)
        elif choice == "2":
            itinerary_name = input("Enter itinerary name: ")
            destination = input("Enter destination: ")
            travel_planner.add_destination(itinerary_name, destination)
        elif choice == "3":
            itinerary_name = input("Enter itinerary name: ")
            destination = input("Enter destination: ")
            travel_planner.remove_destination(itinerary_name, destination)
        elif choice == "4":
            itinerary_name = input("Enter itinerary name: ")
            flight = input("Enter flight: ")
            travel_planner.add_flight(itinerary_name, flight)
        elif choice == "5":
            itinerary_name = input("Enter itinerary name: ")
            flight = input("Enter flight: ")
            travel_planner.remove_flight(itinerary_name, flight)
        elif choice == "6":
            itinerary_name = input("Enter itinerary name: ")
            hotel = input("Enter hotel: ")
            travel_planner.add_hotel(itinerary_name, hotel)
        elif choice == "7":
            itinerary_name = input("Enter itinerary name: ")
            hotel = input("Enter hotel: ")
            travel_planner.remove_hotel(itinerary_name, hotel)
        elif choice == "8":
            itinerary_name = input("Enter itinerary name: ")
            activity = input("Enter activity: ")
            travel_planner.add_activity(itinerary_name, activity)
        elif choice == "9":
            itinerary_name = input("Enter itinerary name: ")
            activity = input("Enter activity: ")
            travel_planner.remove_activity(itinerary_name, activity)
        elif choice == "10":
            itinerary_name = input("Enter itinerary name: ")
            travel_planner.generate_pdf(itinerary_name)
        elif choice == "11":
            flight = input("Enter flight: ")
            flight_info = travel_planner.fetch_flight_info(flight)
            print(flight_info)
        elif choice == "12":
            message = input("Enter message: ")
            notification = travel_planner.send_notification(message)
            print(notification)
        elif choice == "13":
            itinerary_name = input("Enter itinerary name: ")
            user = input("Enter user: ")
            role = input("Enter role: ")
            collaborative_feature.add_user(itinerary_name, user, role)
        elif choice == "14":
            itinerary_name = input("Enter itinerary name: ")
            user = input("Enter user: ")
            collaborative_feature.remove_user(itinerary_name, user)
        elif choice == "15":
            itinerary_name = input("Enter itinerary name: ")
            user = input("Enter user: ")
            role = input("Enter role: ")
            collaborative_feature.update_role(itinerary_name, user, role)
        elif choice == "16":
            break
        else:
            print("Invalid choice. Please try again.")