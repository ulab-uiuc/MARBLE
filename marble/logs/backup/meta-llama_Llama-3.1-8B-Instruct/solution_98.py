# user.py
class User:
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.profile = Profile()

    def __str__(self):
        return f"User {self.username} ({self.email})"


class Profile:
    def __init__(self):
        self.name = None
        self.birthdate = None
        self.privacy_settings = {"public": False, "private": False}

    def update_name(self, name):
        self.name = name

    def update_birthdate(self, birthdate):
        self.birthdate = birthdate

    def update_privacy_settings(self, public, private):
        self.privacy_settings["public"] = public
        self.privacy_settings["private"] = private


# user_manager.py
class UserManager:
    def __init__(self):
        self.users = {}

    def register_user(self, username, email, password):
        if username in self.users:
            raise ValueError("Username already exists")
        user = User(len(self.users) + 1, username, email, password)
        self.users[username] = user
        return user

    def login_user(self, username, password):
        if username not in self.users:
            raise ValueError("Username does not exist")
        user = self.users[username]
        if user.password != password:
            raise ValueError("Incorrect password")
        return user

    def get_user(self, username):
        return self.users.get(username)


# itinerary.py
class Itinerary:
    def __init__(self, id, title, user):
        self.id = id
        self.title = title
        self.user = user
        self.destinations = []
        self.activities = []
        self.accommodations = []

    def add_destination(self, destination):
        self.destinations.append(destination)

    def add_activity(self, activity):
        self.activities.append(activity)

    def add_accommodation(self, accommodation):
        self.accommodations.append(accommodation)

    def __str__(self):
        return f"Itinerary {self.title} ({self.user.username})"


class Destination:
    def __init__(self, id, name, location):
        self.id = id
        self.name = name
        self.location = location

    def __str__(self):
        return f"Destination {self.name} ({self.location})"


class Activity:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    def __str__(self):
        return f"Activity {self.name} ({self.description})"


class Accommodation:
    def __init__(self, id, name, location):
        self.id = id
        self.name = name
        self.location = location

    def __str__(self):
        return f"Accommodation {self.name} ({self.location})"


# itinerary_manager.py
class ItineraryManager:
    def __init__(self):
        self.itineraries = {}

    def create_itinerary(self, title, user):
        if title in self.itineraries:
            raise ValueError("Itinerary already exists")
        itinerary = Itinerary(len(self.itineraries) + 1, title, user)
        self.itineraries[title] = itinerary
        return itinerary

    def get_itinerary(self, title):
        return self.itineraries.get(title)


# invitation.py
class Invitation:
    def __init__(self, id, itinerary, user):
        self.id = id
        self.itinerary = itinerary
        self.user = user

    def __str__(self):
        return f"Invitation to {self.itinerary.title} for {self.user.username}"


# invitation_manager.py
class InvitationManager:
    def __init__(self):
        self.invitations = {}

    def send_invitation(self, itinerary, user):
        if itinerary not in self.invitations:
            self.invitations[itinerary] = []
        invitation = Invitation(len(self.invitations[itinerary]) + 1, itinerary, user)
        self.invitations[itinerary].append(invitation)
        return invitation

    def get_invitations(self, itinerary):
        return self.invitations.get(itinerary)


# chat.py
class Chat:
    def __init__(self, id, itinerary):
        self.id = id
        self.itinerary = itinerary
        self.messages = []

    def send_message(self, message):
        self.messages.append(message)

    def __str__(self):
        return f"Chat for {self.itinerary.title}"


# chat_manager.py
class ChatManager:
    def __init__(self):
        self.chats = {}

    def create_chat(self, itinerary):
        if itinerary not in self.chats:
            self.chats[itinerary] = []
        chat = Chat(len(self.chats[itinerary]) + 1, itinerary)
        self.chats[itinerary].append(chat)
        return chat

    def get_chat(self, itinerary):
        return self.chats.get(itinerary)


# solution.py
class TravelCollaborator:
    def __init__(self):
        self.user_manager = UserManager()
        self.itinerary_manager = ItineraryManager()
        self.invitation_manager = InvitationManager()
        self.chat_manager = ChatManager()

    def run(self):
        while True:
            print("1. Register user")
            print("2. Login user")
            print("3. Create itinerary")
            print("4. Invite user to itinerary")
            print("5. Send message in chat")
            print("6. Exit")
            choice = input("Choose an option: ")
            if choice == "1":
                username = input("Enter username: ")
                email = input("Enter email: ")
                password = input("Enter password: ")
                self.user_manager.register_user(username, email, password)
            elif choice == "2":
                username = input("Enter username: ")
                password = input("Enter password: ")
                try:
                    user = self.user_manager.login_user(username, password)
                    print(f"Logged in as {user.username}")
                except ValueError as e:
                    print(e)
            elif choice == "3":
                title = input("Enter itinerary title: ")
                user = self.user_manager.get_user(input("Enter username: "))
                itinerary = self.itinerary_manager.create_itinerary(title, user)
                print(f"Itinerary {title} created")
            elif choice == "4":
                title = input("Enter itinerary title: ")
                user = self.user_manager.get_user(input("Enter username: "))
                invitation = self.invitation_manager.send_invitation(self.itinerary_manager.get_itinerary(title), user)
                print(f"Invitation sent to {user.username}")
            elif choice == "5":
                title = input("Enter itinerary title: ")
                chat = self.chat_manager.get_chat(self.itinerary_manager.get_itinerary(title))
                message = input("Enter message: ")
                chat.send_message(message)
                print(f"Message sent in chat")
            elif choice == "6":
                break
            else:
                print("Invalid option")

if __name__ == "__main__":
    travel_collaborator = TravelCollaborator()
    travel_collaborator.run()