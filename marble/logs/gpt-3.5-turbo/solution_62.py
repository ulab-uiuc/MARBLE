# MultiServe - Collaborative Food Ordering and Delivery System

class Restaurant:
    def __init__(self, name, menu):
        self.name = name
        self.menu = menu

class User:    def __init__(self, name):
        self.name = name
        self.status = 'Pending'
        pass

    def receive_task(self, order_details):
        self.status = 'Pending'
        passdef update_status(self, status):
        # Update delivery status
        pass

# Test Cases
def test_place_order():
    r1 = Restaurant("Restaurant A", ["Pizza", "Pasta"])
    r2 = Restaurant("Restaurant B", ["Burger", "Fries"])
    user = User("Alice")
    user.add_to_cart({"restaurant": "Restaurant A", "item": "Pizza"})
    user.add_to_cart({"restaurant": "Restaurant B", "item": "Burger"})
    order_details = user.place_order()
    assert len(order_details) == 2
    assert len(order_details["Restaurant A"]) == 1
    assert len(order_details["Restaurant B"]) == 1

def test_delivery_agents():
    agent1 = DeliveryAgent("Agent 1")
    agent2 = DeliveryAgent("Agent 2")
    order_details = {"Restaurant A": [{"item": "Pizza"}], "Restaurant B": [{"item": "Burger"}]}
    agent1.receive_task(order_details["Restaurant A"])
    agent2.receive_task(order_details["Restaurant B"])
    assert agent1.name == "Agent 1"
    assert agent2.name == "Agent 2"

def test_update_status():
    agent = DeliveryAgent("Agent 1")
    agent.update_status("Delivered")
    assert agent.status == "Delivered"

# Run test cases
test_place_order()
test_delivery_agents()
test_update_status()