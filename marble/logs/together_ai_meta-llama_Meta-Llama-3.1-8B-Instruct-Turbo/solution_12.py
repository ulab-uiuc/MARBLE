# user.py
class User:
    def __init__(self, id, username, email, password, profile_picture, cultural_background, interests):
        """
        Initialize a User object.

        Args:
            id (int): Unique user ID.
            username (str): User's username.
            email (str): User's email address.
            password (str): User's password.
            profile_picture (str): Path to user's profile picture.
            cultural_background (str): User's cultural background.
            interests (list): User's interests.
        """
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.profile_picture = profile_picture
        self.cultural_background = cultural_background
        self.interests = interests

    def __str__(self):
        return f"User {self.username} ({self.id})"


# user_repository.py
class UserRepository:
    def __init__(self):
        """
        Initialize a UserRepository object.
        """
        self.users = {}

    def add_user(self, user):
        """
        Add a user to the repository.

        Args:
            user (User): User to add.
        """
        self.users[user.id] = user

    def get_user(self, id):
        """
        Get a user by ID.

        Args:
            id (int): User ID.

        Returns:
            User: User object if found, None otherwise.
        """
        return self.users.get(id)


# virtual_tour.py
class VirtualTour:
    def __init__(self, id, name, description, 3d_model):
        """
        Initialize a VirtualTour object.

        Args:
            id (int): Unique virtual tour ID.
            name (str): Virtual tour name.
            description (str): Virtual tour description.
            3d_model (str): Path to 3D model.
        """
        self.id = id
        self.name = name
        self.description = description
        self.3d_model = 3d_model

    def __str__(self):
        return f"Virtual Tour {self.name} ({self.id})"


# virtual_tour_repository.py
class VirtualTourRepository:
    def __init__(self):
        """
        Initialize a VirtualTourRepository object.
        """
        self.virtual_tours = {}

    def add_virtual_tour(self, virtual_tour):
        """
        Add a virtual tour to the repository.

        Args:
            virtual_tour (VirtualTour): Virtual tour to add.
        """
        self.virtual_tours[virtual_tour.id] = virtual_tour

    def get_virtual_tour(self, id):
        """
        Get a virtual tour by ID.

        Args:
            id (int): Virtual tour ID.

        Returns:
            VirtualTour: Virtual tour object if found, None otherwise.
        """
        return self.virtual_tours.get(id)


# language_exchange.py
class LanguageExchange:
    def __init__(self, id, user1, user2, language):
        """
        Initialize a LanguageExchange object.

        Args:
            id (int): Unique language exchange ID.
            user1 (User): First user in the exchange.
            user2 (User): Second user in the exchange.
            language (str): Language being exchanged.
        """
        self.id = id
        self.user1 = user1
        self.user2 = user2
        self.language = language

    def __str__(self):
        return f"Language Exchange {self.id} between {self.user1.username} and {self.user2.username}"


# language_exchange_repository.py
class LanguageExchangeRepository:
    def __init__(self):
        """
        Initialize a LanguageExchangeRepository object.
        """
        self.language_exchanges = {}

    def add_language_exchange(self, language_exchange):
        """
        Add a language exchange to the repository.

        Args:
            language_exchange (LanguageExchange): Language exchange to add.
        """
        self.language_exchanges[language_exchange.id] = language_exchange

    def get_language_exchange(self, id):
        """
        Get a language exchange by ID.

        Args:
            id (int): Language exchange ID.

        Returns:
            LanguageExchange: Language exchange object if found, None otherwise.
        """
        return self.language_exchanges.get(id)


# cultural_workshop.py
class CulturalWorkshop:
    def __init__(self, id, name, description, expert):
        """
        Initialize a CulturalWorkshop object.

        Args:
            id (int): Unique cultural workshop ID.
            name (str): Cultural workshop name.
            description (str): Cultural workshop description.
            expert (str): Expert leading the workshop.
        """
        self.id = id
        self.name = name
        self.description = description
        self.expert = expert

    def __str__(self):
        return f"Cultural Workshop {self.name} ({self.id})"


# cultural_workshop_repository.py
class CulturalWorkshopRepository:
    def __init__(self):
        """
        Initialize a CulturalWorkshopRepository object.
        """
        self.cultural_workshops = {}

    def add_cultural_workshop(self, cultural_workshop):
        """
        Add a cultural workshop to the repository.

        Args:
            cultural_workshop (CulturalWorkshop): Cultural workshop to add.
        """
        self.cultural_workshops[cultural_workshop.id] = cultural_workshop

    def get_cultural_workshop(self, id):
        """
        Get a cultural workshop by ID.

        Args:
            id (int): Cultural workshop ID.

        Returns:
            CulturalWorkshop: Cultural workshop object if found, None otherwise.
        """
        return self.cultural_workshops.get(id)


# solution.py
class CulturalExchangeHub:
    def __init__(self):
        """
        Initialize a CulturalExchangeHub object.
        """
        self.user_repository = UserRepository()
        self.virtual_tour_repository = VirtualTourRepository()
        self.language_exchange_repository = LanguageExchangeRepository()
        self.cultural_workshop_repository = CulturalWorkshopRepository()

    def register_user(self, user):
        """
        Register a user.

        Args:
            user (User): User to register.
        """
        self.user_repository.add_user(user)

    def add_virtual_tour(self, virtual_tour):
        """
        Add a virtual tour.

        Args:
            virtual_tour (VirtualTour): Virtual tour to add.
        """
        self.virtual_tour_repository.add_virtual_tour(virtual_tour)

    def add_language_exchange(self, language_exchange):
        """
        Add a language exchange.

        Args:
            language_exchange (LanguageExchange): Language exchange to add.
        """
        self.language_exchange_repository.add_language_exchange(language_exchange)

    def add_cultural_workshop(self, cultural_workshop):
        """
        Add a cultural workshop.

        Args:
            cultural_workshop (CulturalWorkshop): Cultural workshop to add.
        """
        self.cultural_workshop_repository.add_cultural_workshop(cultural_workshop)

    def get_user(self, id):
        """
        Get a user by ID.

        Args:
            id (int): User ID.

        Returns:
            User: User object if found, None otherwise.
        """
        return self.user_repository.get_user(id)

    def get_virtual_tour(self, id):
        """
        Get a virtual tour by ID.

        Args:
            id (int): Virtual tour ID.

        Returns:
            VirtualTour: Virtual tour object if found, None otherwise.
        """
        return self.virtual_tour_repository.get_virtual_tour(id)

    def get_language_exchange(self, id):
        """
        Get a language exchange by ID.

        Args:
            id (int): Language exchange ID.

        Returns:
            LanguageExchange: Language exchange object if found, None otherwise.
        """
        return self.language_exchange_repository.get_language_exchange(id)

    def get_cultural_workshop(self, id):
        """
        Get a cultural workshop by ID.

        Args:
            id (int): Cultural workshop ID.

        Returns:
            CulturalWorkshop: Cultural workshop object if found, None otherwise.
        """
        return self.cultural_workshop_repository.get_cultural_workshop(id)


# Example usage:
if __name__ == "__main__":
    hub = CulturalExchangeHub()

    user1 = User(1, "John", "john@example.com", "password", "profile_picture.jpg", "American", ["travel", "food"])
    hub.register_user(user1)

    virtual_tour1 = VirtualTour(1, "Eiffel Tower", "A virtual tour of the Eiffel Tower", "eiffel_tower_3d_model.obj")
    hub.add_virtual_tour(virtual_tour1)

    language_exchange1 = LanguageExchange(1, user1, User(2, "Jane", "jane@example.com", "password", "profile_picture.jpg", "French", ["language", "culture"]), "English")
    hub.add_language_exchange(language_exchange1)

    cultural_workshop1 = CulturalWorkshop(1, "French Cooking", "A cultural workshop on French cooking", "Chef Pierre")
    hub.add_cultural_workshop(cultural_workshop1)

    print(hub.get_user(1))
    print(hub.get_virtual_tour(1))
    print(hub.get_language_exchange(1))
    print(hub.get_cultural_workshop(1))