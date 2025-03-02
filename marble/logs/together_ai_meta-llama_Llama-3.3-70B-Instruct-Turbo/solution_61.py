# solution.py
# Importing necessary libraries
from abc import ABC, abstractmethodclass User(ABC):
    def __init__(self, id: int, name: str, password: str):
        self.id = id
        self.name = name
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def login(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password)class Customer(User):
    """Class for customers"""
    def __init__(self, id: int, name: str, password: str):
        super().__init__(id, name)
        self.password = password.encode('utf-8')

    def place_order(self, restaurant_id: int, order_details: Dict) -> None:
        """Method for customer to place order"""
        print(f"Customer {self.name} placed an order at restaurant {restaurant_id} with details {order_details}")
        self.customers = []
        self.restaurants = []
        self.delivery_personnel = []
        self.orders = []

    def add_customer(self, customer: Customer) -> None:
        """Method to add customer"""
        self.customers.append(customer)

    def add_restaurant(self, restaurant: Restaurant) -> None:
        """Method to add restaurant"""
        self.restaurants.append(restaurant)

    def add_delivery_personnel(self, delivery_personnel: DeliveryPersonnel) -> None:
        """Method to add delivery personnel"""
        self.delivery_personnel.append(delivery_personnel)

    def place_order(self, customer_id: int, restaurant_id: int, order_details: Dict) -> None:
        """Method to place order"""
        customer = next((c for c in self.customers if c.id == customer_id), None)
        restaurant = next((r for r in self.restaurants if r.id == restaurant_id), None)
        if customer and restaurant:
            order = Order(len(self.orders) + 1, customer_id, restaurant_id, order_details)
            self.orders.append(order)
            customer.place_order(restaurant_id, order_details)
        else:
            print("Customer or restaurant not found")

    def manage_order(self, restaurant_id: int, order_id: int, status: OrderStatus) -> None:
        """Method to manage order"""
        restaurant = next((r for r in self.restaurants if r.id == restaurant_id), None)
        order = next((o for o in self.orders if o.id == order_id), None)
        if restaurant and order:
            restaurant.manage_order(order_id, status)
            order.update_status(status)
        else:
            print("Restaurant or order not found")

    def update_delivery_status(self, delivery_personnel_id: int, order_id: int, status: OrderStatus) -> None:
        """Method to update delivery status"""
        delivery_personnel = next((dp for dp in self.delivery_personnel if dp.id == delivery_personnel_id), None)
        order = next((o for o in self.orders if o.id == order_id), None)
        if delivery_personnel and order:
            delivery_personnel.update_delivery_status(order_id, status)
            order.update_status(status)
        else:
            print("Delivery personnel or order not found")

    def feedback(self, customer_id: int, order_id: int, rating: int, review: str) -> None:
        """Method for customer feedback"""
        customer = next((c for c in self.customers if c.id == customer_id), None)
        order = next((o for o in self.orders if o.id == order_id), None)
        if customer and order:
            print(f"Customer {customer.name} gave a rating of {rating} and review '{review}' for order {order_id}")
        else:
            print("Customer or order not found")

# Example usage
if __name__ == "__main__":
    food_chain = FoodChain()

    customer1 = Customer(1, "John Doe", "password123")
    restaurant1 = Restaurant(1, "Restaurant 1", "password123", [{"item": "Burger", "price": 10.99}, {"item": "Fries", "price": 4.99}])
    delivery_personnel1 = DeliveryPersonnel(1, "Jane Doe", "password123")

    food_chain.add_customer(customer1)
    food_chain.add_restaurant(restaurant1)
    food_chain.add_delivery_personnel(delivery_personnel1)

    food_chain.place_order(1, 1, {"item": "Burger", "quantity": 2})
    food_chain.manage_order(1, 1, OrderStatus.ACCEPTED)
    food_chain.update_delivery_status(1, 1, OrderStatus.DELIVERED)
    food_chain.feedback(1, 1, 5, "Excellent service and food quality")