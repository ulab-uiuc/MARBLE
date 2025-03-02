# food_chain.py

class User:import bcrypt
self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())self.username = username
        self.password = password

class Customer(User):
    """Class representing a customer in the FoodChain system."""
    def __init__(self, username, password):
import bcrypt

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password)
        super().__init__(username, password)
        self.orders = []

    def place_order(self, restaurant, order):
        """Place an order at a restaurant."""
        self.orders.append((restaurant, order))
        print(f"Order placed at {restaurant.name}.")

    def rate_experience(self, restaurant, rating):
        """Rate the experience with a restaurant."""
        print(f"Rated {restaurant.name} {rating} stars.")

class Restaurant(User):
    """Class representing a restaurant in the FoodChain system."""
    def __init__(self, username, password, name, menu):
        super().__init__(username, password)
        self.name = name
        self.menu = menu
        self.orders = []

    def accept_order(self, order):
        """Accept an order."""
        self.orders.append(order)
        print(f"Order accepted: {order}.")

    def reject_order(self, order):
        """Reject an order."""
        self.orders.remove(order)
        print(f"Order rejected: {order}.")

    def modify_order(self, order, modification):
        """Modify an order."""
        print(f"Order modified: {order} -> {modification}.")

class DeliveryPersonnel(User):
    """Class representing a delivery personnel in the FoodChain system."""
    def __init__(self, username, password):
        super().__init__(username, password)
        self.deliveries = []

    def pick_up_order(self, order):
        """Pick up an order."""
        self.deliveries.append(order)
        print(f"Order picked up: {order}.")

    def deliver_order(self, order):
        """Deliver an order."""
        self.deliveries.remove(order)
        print(f"Order delivered: {order}.")

class FoodChain:
    """Class representing the FoodChain system."""
    def __init__(self):
        self.customers = []
        self.restaurants = []
        self.delivery_personnel = []

    def add_customer(self, customer):
        """Add a customer to the system."""
        self.customers.append(customer)

    def add_restaurant(self, restaurant):
        """Add a restaurant to the system."""
        self.restaurants.append(restaurant)

    def add_delivery_personnel(self, delivery_personnel):
        """Add a delivery personnel to the system."""
        self.delivery_personnel.append(delivery_personnel)

    def display_restaurants(self):
        """Display all restaurants in the system."""
        for restaurant in self.restaurants:
            print(restaurant.name)

    def display_menu(self, restaurant):
        """Display the menu of a restaurant."""
        for item in restaurant.menu:
            print(item)

def main():
    # Create a FoodChain system
    food_chain = FoodChain()

    # Create customerscustomer1 = Customer("customer1", "password1")
print(customer1.check_password("password1"))  # Should print: Truecustomer2 = Customer("customer2", "password2")

    # Create restaurantsrestaurant1 = Restaurant("restaurant1", "password1", "Restaurant 1", ["Item 1", "Item 2", "Item 3"])
print(restaurant1.check_password("password1"))  # Should print: Truerestaurant2 = Restaurant("restaurant2", "password2", "Restaurant 2", ["Item 4", "Item 5", "Item 6"])

    # Create delivery personneldelivery_personnel1 = DeliveryPersonnel("delivery_personnel1", "password1")
print(delivery_personnel1.check_password("password1"))  # Should print: True
    delivery_personnel1 = DeliveryPersonnel("delivery_personnel1", "password1")

    # Add customers, restaurants, and delivery personnel to the system
    food_chain.add_customer(customer1)
    food_chain.add_customer(customer2)
    food_chain.add_restaurant(restaurant1)
    food_chain.add_restaurant(restaurant2)
    food_chain.add_delivery_personnel(delivery_personnel1)

    # Display restaurants
    print("Restaurants:")
    food_chain.display_restaurants()

    # Display menu of a restaurant
    print("\nMenu of Restaurant 1:")
    food_chain.display_menu(restaurant1)

    # Place an order
    customer1.place_order(restaurant1, "Item 1")

    # Accept an order
    restaurant1.accept_order("Item 1")

    # Pick up an order
    delivery_personnel1.pick_up_order("Item 1")

    # Deliver an order
    delivery_personnel1.deliver_order("Item 1")

    # Rate the experience
    customer1.rate_experience(restaurant1, 5)

if __name__ == "__main__":
    main()