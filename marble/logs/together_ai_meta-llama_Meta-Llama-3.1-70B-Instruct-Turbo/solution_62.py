# restaurant.py
class Restaurant:
    def __init__(self, name, menu):
        self.name = name
        self.menu = menu
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def update_order_status(self, order_id, status):
        for order in self.orders:
            if order.id == order_id:
                order.status = status
                break


# order.py
class Order:
    def __init__(self, id, items):
        self.id = id
        self.items = items
        self.status = "pending"


# delivery_agent.py
class DeliveryAgent:
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def update_task_status(self, task_id, status):
        for task in self.tasks:
            if task.id == task_id:
                task.status = status
                break


# task.py
class Task:
    def __init__(self, id, order_id, restaurant_name):
        self.id = id
        self.order_id = order_id
        self.restaurant_name = restaurant_name
        self.status = "pending"


# user.py
class User:
    def __init__(self, name):
        self.name = name
        self.cart = []

    def add_to_cart(self, item):
        self.cart.append(item)

    def place_order(self, restaurants):
        order = Order(len(restaurants.orders) + 1, self.cart)
        for restaurant in restaurants:
            restaurant.add_order(order)
        return order


# multiserve.py
class MultiServe:
    def __init__(self):
        self.restaurants = []
        self.delivery_agents = []
        self.orders = []

    def add_restaurant(self, restaurant):
        self.restaurants.append(restaurant)

    def add_delivery_agent(self, delivery_agent):
        self.delivery_agents.append(delivery_agent)

    def assign_delivery_tasks(self, order):
        tasks = []
        for restaurant in self.restaurants:
            for item in order.items:
                if item.restaurant_name == restaurant.name:
                    task = Task(len(self.delivery_agents[0].tasks) + 1, order.id, restaurant.name)
                    self.delivery_agents[0].add_task(task)
                    tasks.append(task)
        return tasks

    def update_order_status(self, order_id, status):
        for restaurant in self.restaurants:
            restaurant.update_order_status(order_id, status)

    def notify_user(self, order_id, status):
        print(f"Order {order_id} is {status}")


# solution.py
def main():
    # Create restaurants
    restaurant1 = Restaurant("Restaurant 1", ["item1", "item2"])
    restaurant2 = Restaurant("Restaurant 2", ["item3", "item4"])

    # Create delivery agents
    delivery_agent1 = DeliveryAgent("Delivery Agent 1")
    delivery_agent2 = DeliveryAgent("Delivery Agent 2")

    # Create user
    user = User("User 1")

    # Create multiserve system
    multiserve = MultiServe()
    multiserve.add_restaurant(restaurant1)
    multiserve.add_restaurant(restaurant2)
    multiserve.add_delivery_agent(delivery_agent1)
    multiserve.add_delivery_agent(delivery_agent2)

    # User adds items to cart
    user.add_to_cart({"name": "item1", "restaurant_name": "Restaurant 1"})
    user.add_to_cart({"name": "item3", "restaurant_name": "Restaurant 2"})

    # User places order
    order = user.place_order(multiserve.restaurants)

    # Assign delivery tasks
    tasks = multiserve.assign_delivery_tasks(order)

    # Update order status
    multiserve.update_order_status(order.id, "ready for pickup")

    # Notify user
    multiserve.notify_user(order.id, "ready for pickup")


if __name__ == "__main__":
    main()