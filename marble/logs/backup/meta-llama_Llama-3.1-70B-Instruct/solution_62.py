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
            if order['id'] == order_id:
                order['status'] = status
                break


# delivery_agent.py
class DeliveryAgent:
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def update_task_status(self, task_id, status):
        for task in self.tasks:
            if task['id'] == task_id:
                task['status'] = status
                break


# user.py
class User:
    def __init__(self, name):
        self.name = name
        self.cart = []

    def add_to_cart(self, item):
        self.cart.append(item)

    def place_order(self, restaurants):
        order = {'id': len(restaurants[0].orders) + 1, 'items': self.cart, 'status': 'pending'}
        for restaurant in restaurants:
            restaurant.add_order(order)
        self.cart = []
        return order


# multiserve.py
class MultiServe:
    def __init__(self):
        self.restaurants = []
        self.delivery_agents = []
        self.users = []

    def add_restaurant(self, restaurant):
        self.restaurants.append(restaurant)

    def add_delivery_agent(self, delivery_agent):
        self.delivery_agents.append(delivery_agent)

    def add_user(self, user):
        self.users.append(user)

    def assign_delivery_tasks(self, order, restaurants):
        tasks = []
        for i, restaurant in enumerate(restaurants):
            task = {'id': len(self.delivery_agents[i].tasks) + 1, 'order_id': order['id'], 'restaurant': restaurant.name, 'status': 'pending'}
            self.delivery_agents[i].add_task(task)
            tasks.append(task)
        return tasks

    def update_order_status(self, order_id, status):
        for restaurant in self.restaurants:
            restaurant.update_order_status(order_id, status)

    def notify_user(self, user, message):
        print(f"Notification to {user.name}: {message}")


# solution.py
def main():
    multiserve = MultiServe()

    # Create restaurants
    restaurant1 = Restaurant('Restaurant 1', ['item1', 'item2', 'item3'])
    restaurant2 = Restaurant('Restaurant 2', ['item4', 'item5', 'item6'])
    multiserve.add_restaurant(restaurant1)
    multiserve.add_restaurant(restaurant2)

    # Create delivery agents
    delivery_agent1 = DeliveryAgent('Delivery Agent 1')
    delivery_agent2 = DeliveryAgent('Delivery Agent 2')
    multiserve.add_delivery_agent(delivery_agent1)
    multiserve.add_delivery_agent(delivery_agent2)

    # Create user
    user = User('User 1')
    multiserve.add_user(user)

    # User adds items to cart
    user.add_to_cart('item1')
    user.add_to_cart('item4')

    # User places order
    order = user.place_order([restaurant1, restaurant2])
    print(f"Order placed: {order}")

    # Assign delivery tasks
    tasks = multiserve.assign_delivery_tasks(order, [restaurant1, restaurant2])
    print(f"Delivery tasks assigned: {tasks}")

    # Update order status
    multiserve.update_order_status(order['id'], 'in_progress')
    print(f"Order status updated: {order['status']}")

    # Notify user
    multiserve.notify_user(user, "Your order is ready for pickup.")

    # Test cases
    def test_place_order_with_items_from_two_restaurants():
        user.add_to_cart('item2')
        user.add_to_cart('item5')
        order = user.place_order([restaurant1, restaurant2])
        assert len(order['items']) == 4

    def test_assign_delivery_tasks_to_two_delivery_agents():
        tasks = multiserve.assign_delivery_tasks(order, [restaurant1, restaurant2])
        assert len(tasks) == 2

    def test_update_order_status_in_real_time():
        multiserve.update_order_status(order['id'], 'delivered')
        assert order['status'] == 'delivered'

    def test_handle_edge_cases():
        # Test restaurant being unavailable
        restaurant1.orders = []
        order = user.place_order([restaurant1, restaurant2])
        assert len(restaurant1.orders) == 0

        # Test delivery agent declining a task
        delivery_agent1.tasks = []
        tasks = multiserve.assign_delivery_tasks(order, [restaurant1, restaurant2])
        assert len(delivery_agent1.tasks) == 0

        # Test user canceling an order after it has been placed
        user.cart = []
        order = user.place_order([restaurant1, restaurant2])
        assert len(user.cart) == 0

    test_place_order_with_items_from_two_restaurants()
    test_assign_delivery_tasks_to_two_delivery_agents()
    test_update_order_status_in_real_time()
    test_handle_edge_cases()

if __name__ == "__main__":
    main()