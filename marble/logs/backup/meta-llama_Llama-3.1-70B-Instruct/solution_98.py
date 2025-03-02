# user_authentication.py
from datetime import datetime
from typing import Dict

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email
        self.profile = {}

    def create_profile(self, name: str, age: int, location: str):
        self.profile = {
            "name": name,
            "age": age,
            "location": location
        }

    def update_profile(self, name: str = None, age: int = None, location: str = None):
        if name:
            self.profile["name"] = name
        if age:
            self.profile["age"] = age
        if location:
            self.profile["location"] = location

    def __str__(self):
        return f"Username: {self.username}, Email: {self.email}, Profile: {self.profile}"


class UserAuthentication:
    def __init__(self):
        self.users = {}

    def register(self, username: str, password: str, email: str):
        if username in self.users:
            print("Username already exists.")
            return
        self.users[username] = User(username, password, email)
        print("User registered successfully.")

    def login(self, username: str, password: str):
        if username not in self.users:if not bcrypt.checkpw(password.encode('utf-8'), self.users[username].password):print("Incorrect password.")
            return
        print("User logged in successfully.")

    def get_user(self, username: str):
        return self.users.get(username)


# itinerary_creation.py
from datetime import datetime
from typing import Dict, List

class Itinerary:
    def __init__(self, name: str, user: 'User'):
        self.name = name
        self.user = user
        self.destinations = []
        self.activities = []
        self.accommodations = []

    def add_destination(self, name: str, date: datetime, time: str):
        self.destinations.append({
            "name": name,
            "date": date,
            "time": time
        })

    def add_activity(self, name: str, date: datetime, time: str):
        self.activities.append({
            "name": name,
            "date": date,
            "time": time
        })

    def add_accommodation(self, name: str, date: datetime, time: str):
        self.accommodations.append({
            "name": name,
            "date": date,
            "time": time
        })

    def __str__(self):
        return f"Itinerary: {self.name}, User: {self.user.username}, Destinations: {self.destinations}, Activities: {self.activities}, Accommodations: {self.accommodations}"


class ItineraryCreation:
    def __init__(self):
        self.itineraries = {}

    def create_itinerary(self, name: str, user: 'User'):
        if name in self.itineraries:
            print("Itinerary already exists.")
            return
        self.itineraries[name] = Itinerary(name, user)
        print("Itinerary created successfully.")

    def get_itinerary(self, name: str):
        return self.itineraries.get(name)


# collaboration.py
from typing import Dict, List

class Collaboration:
    def __init__(self):
        self.collaborators = {}

    def invite_collaborator(self, itinerary_name: str, user: 'User'):
        if itinerary_name not in self.collaborators:
            self.collaborators[itinerary_name] = []
        self.collaborators[itinerary_name].append(user)
        print("Collaborator invited successfully.")

    def get_collaborators(self, itinerary_name: str):
        return self.collaborators.get(itinerary_name, [])


# communication.py
from typing import Dict, List

class Communication:
    def __init__(self):
        self.messages = {}

    def send_message(self, itinerary_name: str, user: 'User', message: str):
        if itinerary_name not in self.messages:
            self.messages[itinerary_name] = []
        self.messages[itinerary_name].append({
            "user": user.username,
            "message": message
        })
        print("Message sent successfully.")

    def get_messages(self, itinerary_name: str):
        return self.messages.get(itinerary_name, [])


# synchronization.py
from typing import Dict, List

class Synchronization:
    def __init__(self):
        self.changes = {}

    def update_itinerary(self, itinerary_name: str, user: 'User', changes: Dict):
        if itinerary_name not in self.changes:
            self.changes[itinerary_name] = []
        self.changes[itinerary_name].append({
            "user": user.username,
            "changes": changes
        })
        print("Itinerary updated successfully.")

    def get_changes(self, itinerary_name: str):
        return self.changes.get(itinerary_name, [])


# review.py
from typing import Dict, List

class Review:
    def __init__(self):
        self.reviews = {}

    def add_review(self, itinerary_name: str, user: 'User', review: str):
        if itinerary_name not in self.reviews:
            self.reviews[itinerary_name] = []
        self.reviews[itinerary_name].append({
            "user": user.username,
            "review": review
        })
        print("Review added successfully.")

    def get_reviews(self, itinerary_name: str):
        return self.reviews.get(itinerary_name, [])


# main.py
from user_authentication import UserAuthentication, User
from itinerary_creation import ItineraryCreation, Itinerary
from collaboration import Collaboration
from communication import Communication
from synchronization import Synchronization
from review import Review

def main():
    user_auth = UserAuthentication()
    itinerary_creation = ItineraryCreation()
    collaboration = Collaboration()
    communication = Communication()
    synchronization = Synchronization()
    review = Review()

    while True:
        print("1. Register")
        print("2. Login")
        print("3. Create Itinerary")
        print("4. Invite Collaborator")
        print("5. Send Message")
        print("6. Update Itinerary")
        print("7. Add Review")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            email = input("Enter email: ")
            user_auth.register(username, password, email)
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            user_auth.login(username, password)
        elif choice == "3":
            name = input("Enter itinerary name: ")
            username = input("Enter username: ")
            user = user_auth.get_user(username)
            if user:
                itinerary_creation.create_itinerary(name, user)
        elif choice == "4":
            itinerary_name = input("Enter itinerary name: ")
            username = input("Enter username: ")
            user = user_auth.get_user(username)
            if user:
                collaboration.invite_collaborator(itinerary_name, user)
        elif choice == "5":
            itinerary_name = input("Enter itinerary name: ")
            username = input("Enter username: ")
            user = user_auth.get_user(username)
            if user:
                message = input("Enter message: ")
                communication.send_message(itinerary_name, user, message)
        elif choice == "6":
            itinerary_name = input("Enter itinerary name: ")
            username = input("Enter username: ")
            user = user_auth.get_user(username)
            if user:
                changes = input("Enter changes: ")
                synchronization.update_itinerary(itinerary_name, user, changes)
        elif choice == "7":
            itinerary_name = input("Enter itinerary name: ")
            username = input("Enter username: ")
            user = user_auth.get_user(username)
            if user:
                review_text = input("Enter review: ")
                review.add_review(itinerary_name, user, review_text)
        elif choice == "8":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()