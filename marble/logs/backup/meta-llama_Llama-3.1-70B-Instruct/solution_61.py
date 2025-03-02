# food_chain.py

class User:
    """Base class for all users in the FoodChain system."""
    
    def __init__(self, username, password):self.password = self._hash_password(password)self.username = username
def _hash_password(self, password):
        import bcrypt
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)
        self.password = password

    def login(self, password):return bcrypt.checkpw(password.encode('utf-8'), self.password)import bcrypt
        return bcrypt.checkpw(password.encode('utf-8'), self.password)
        """
        Check if the provided password matches the user's password.

        Args:
            password (str): The password to check.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return self.password == password


class Customer(User):
    """Class representing a customer in the FoodChain system."""
    
    def __init__(self, username, password):
        """
        Initialize a Customer object.

        Args:
            username (str): The username chosen by the customer.
            password (str): The password chosen by the customer.
        """
        super().__init__(username, password)
        self.orders = []

    def place_order(self, restaurant, order):
        """
        Place an order at a restaurant.

        Args:
            restaurant (Restaurant): The restaurant where the order is placed.
            order (str): The order details.
        """
        self.orders.append((restaurant, order))
        restaurant.receive_order(order)


class Restaurant(User):
    """Class representing a restaurant in the FoodChain system."""
    
    def __init__(self, username, password):
        """
        Initialize a Restaurant object.

        Args:
            username (str): The username chosen by the restaurant.
            password (str): The password chosen by the restaurant.
        """
        super().__init__(username, password)
        self.menu = []
        self.orders = []

    def add_to_menu(self, item):
        """
        Add an item to the restaurant's menu.

        Args:
            item (str): The item to add.
        """
        self.menu.append(item)

    def receive_order(self, order):
        """
        Receive an order from a customer.

        Args:
            order (str): The order details.
        """
        self.orders.append(order)

    def accept_order(self, order):
        """
        Accept an order.

        Args:
            order (str): The order details.
        """
        self.orders.remove(order)
        print(f"Order '{order}' accepted.")

    def reject_order(self, order):
        """
        Reject an order.

        Args:
            order (str): The order details.
        """
        self.orders.remove(order)
        print(f"Order '{order}' rejected.")


class DeliveryPersonnel(User):
    """Class representing a delivery personnel in the FoodChain system."""
    
    def __init__(self, username, password):
        """
        Initialize a DeliveryPersonnel object.

        Args:
            username (str): The username chosen by the delivery personnel.
            password (str): The password chosen by the delivery personnel.
        """
        super().__init__(username, password)
        self.deliveries = []

    def assign_delivery(self, order):
        """
        Assign a delivery to the personnel.

        Args:
            order (str): The order details.
        """
        self.deliveries.append(order)

    def update_delivery_status(self, order, status):
        """
        Update the status of a delivery.

        Args:
            order (str): The order details.
            status (str): The new status of the delivery.
        """
        if order in self.deliveries:
            print(f"Delivery status of '{order}' updated to '{status}'.")
        else:
            print(f"Delivery '{order}' not found.")


class FoodChain:
    """Class representing the FoodChain system."""
    
    def __init__(self):
        """
        Initialize a FoodChain object.
        """
        self.customers = []
        self.restaurants = []
        self.delivery_personnel = []

    def add_customer(self, customer):
        """
        Add a customer to the system.

        Args:
            customer (Customer): The customer to add.
        """
        self.customers.append(customer)

    def add_restaurant(self, restaurant):
        """
        Add a restaurant to the system.

        Args:
            restaurant (Restaurant): The restaurant to add.
        """
        self.restaurants.append(restaurant)

    def add_delivery_personnel(self, personnel):
        """
        Add a delivery personnel to the system.

        Args:
            personnel (DeliveryPersonnel): The personnel to add.
        """
        self.delivery_personnel.append(personnel)

    def display_restaurants(self):
        """
        Display a list of all restaurants in the system.
        """
        print("Restaurants:")
        for i, restaurant in enumerate(self.restaurants):
            print(f"{i+1}. {restaurant.username}")

    def display_menu(self, restaurant):
        """
        Display the menu of a restaurant.

        Args:
            restaurant (Restaurant): The restaurant whose menu to display.
        """
        print(f"Menu of {restaurant.username}:")
        for i, item in enumerate(restaurant.menu):
            print(f"{i+1}. {item}")


def main():
    food_chain = FoodChain()

    customer1 = Customer("customer1", "password1")
    food_chain.add_customer(customer1)

    restaurant1 = Restaurant("restaurant1", "password1")
    restaurant1.add_to_menu("Pizza")
    restaurant1.add_to_menu("Burger")
    food_chain.add_restaurant(restaurant1)

    delivery_personnel1 = DeliveryPersonnel("delivery1", "password1")
    food_chain.add_delivery_personnel(delivery_personnel1)

    food_chain.display_restaurants()
    food_chain.display_menu(restaurant1)

    customer1.place_order(restaurant1, "Pizza")
    restaurant1.accept_order("Pizza")
    delivery_personnel1.assign_delivery("Pizza")
    delivery_personnel1.update_delivery_status("Pizza", "Delivered")


if __name__ == "__main__":
    main()