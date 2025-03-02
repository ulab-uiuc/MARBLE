# MultiAgentDine - Restaurant Delivery Coordination System

class DeliveryAgent:
    def __init__(self, agent_id, location, availability=True):
        self.agent_id = agent_id
        self.location = location
        self.availability = availability
        self.current_order = None

    def update_location(self, new_location):
        self.location = new_location

    def update_availability(self, availability):
        self.availability = availability

    def assign_order(self, order):
        self.current_order = order

    def complete_order(self):
        self.current_order = None


class Order:
    def __init__(self, order_id, restaurant, destination, items, customer_id):
        self.order_id = order_id
        self.restaurant = restaurant
        self.destination = destination
        self.items = items
        self.customer_id = customer_id
        self.assigned_agent = None

    def assign_agent(self, agent):
        self.assigned_agent = agent


class Restaurant:
    def __init__(self, name, location):
        self.name = name
        self.location = location

    def place_order(self, order_id, destination, items, customer_id):
        new_order = Order(order_id, self.name, destination, items, customer_id)
        return new_order


class Customer:
    def __init__(self, customer_id, location):
        self.customer_id = customer_id
        self.location = location

    def place_order(self, restaurant, order_id, items):
        destination = restaurant.location
        return restaurant.place_order(order_id, destination, items, self.customer_id)


# Sample Usage
if __name__ == "__main__":
    # Create Delivery Agents
    agent1 = DeliveryAgent(agent_id=1, location=(0, 0))
    agent2 = DeliveryAgent(agent_id=2, location=(3, 4))

    # Create Restaurants
    restaurant1 = Restaurant(name="Restaurant A", location=(2, 1))
    restaurant2 = Restaurant(name="Restaurant B", location=(5, 5))

    # Create Customers
    customer1 = Customer(customer_id=101, location=(1, 2))
    customer2 = Customer(customer_id=102, location=(4, 3))

    # Place Orders
    order1 = customer1.place_order(restaurant1, order_id=201, items=["Pizza", "Drink"])
    order2 = customer2.place_order(restaurant2, order_id=202, items=["Burger", "Fries"])

    # Assign Orders to Agents
    order1.assign_agent(agent1)
    agent1.assign_order(order1)

    order2.assign_agent(agent2)
    agent2.assign_order(order2)

    # Update Agent Locations
    agent1.update_location((1, 1))
    agent2.update_location((4, 4))

    # Complete Orders
    agent1.complete_order()
    agent2.complete_order()