
# collaborative_analytics.py
import threading
import time

class CollaborativeAnalytics:
    def __init__(self):
        self.data = {}
        self.observers = []
        self.lock = threading.Lock()def update_data(self, key, value):
        with self.lock:if new_timestamp > current_timestamp:
            self.data[key] = value
            self.timestamps[key] = new_timestamp
            self.notify_observers()
        else:
            # Handle conflict by merging changes
            self.data[key] = self.merge_changes(self.data[key], value)
            self.timestamps[key] = new_timestamp
            self.notify_observers()    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.data)

    def resolve_conflicts(self):
        # Implement conflict resolution logic here
        pass# user_account_manager.py
import hashlib
import threading

class UserAccountManager:
    def __init__(self):
        self.users = {}
        self.lock = threading.Lock()

    def create_account(self, username, password):
        with self.lock:self.data[key] = value
self.resolve_conflicts()
self.timestamps[key] = time.time()self.notify_observers()

    def get_data(self):
        with self.lock:
            return self.data.copy()

    def generate_report(self):
        data = self.get_data()
        # Generate report using data
        print("Report:")
        for key, value in data.items():
            print(f"{key}: {value}")

    def visualize_data(self):
        data = self.get_data()
        # Visualize data using matplotlib
        plt.bar(data.keys(), data.values())
        plt.show()


# analyst.py
class Analyst:
    def __init__(self, name, collaborative_analytics):
        self.name = name
        self.collaborative_analytics = collaborative_analytics

    def update_data(self, key, value):
def merge_changes(self, existing_value, new_value):
        # Implement logic to merge changes
        # For example, if values are lists, merge them
        if isinstance(existing_value, list) and isinstance(new_value, list):
            return existing_value + new_value
        # If values are dictionaries, merge them recursively
        elif isinstance(existing_value, dict) and isinstance(new_value, dict):
            merged_dict = existing_value.copy()
            for key, value in new_value.items():
                if key in merged_dict:
                    merged_dict[key] = self.merge_changes(merged_dict[key], value)
                else:
                    merged_dict[key] = value
            return merged_dict
        # If values are not lists or dictionaries, return the new value
        else:
            return new_value
        print(f"{self.name} is updating data...")
        self.collaborative_analytics.update_data(key, value)

    def get_data(self):
        print(f"{self.name} is getting data...")
        return self.collaborative_analytics.get_data()

    def generate_report(self):
        print(f"{self.name} is generating report...")
        self.collaborative_analytics.generate_report()

    def visualize_data(self):
        print(f"{self.name} is visualizing data...")
        self.collaborative_analytics.visualize_data()

    def update(self, data):
        print(f"{self.name} received update: {data}")


# test_collaborative_analytics.py
import unittest
import threading
import time

class TestCollaborativeAnalytics(unittest.TestCase):
    def test_update_data(self):
        collaborative_analytics = CollaborativeAnalytics()
        analyst1 = Analyst("Analyst1", collaborative_analytics)
        analyst2 = Analyst("Analyst2", collaborative_analytics)
        collaborative_analytics.add_observer(analyst1)
        collaborative_analytics.add_observer(analyst2)

        analyst1.update_data("player1", 10)
        time.sleep(0.1)
        self.assertEqual(analyst2.get_data(), {"player1": 10})

    def test_generate_report(self):
        collaborative_analytics = CollaborativeAnalytics()
        analyst1 = Analyst("Analyst1", collaborative_analytics)
        analyst2 = Analyst("Analyst2", collaborative_analytics)
        collaborative_analytics.add_observer(analyst1)
        collaborative_analytics.add_observer(analyst2)

        analyst1.update_data("player1", 10)
        analyst2.generate_report()

    def test_visualize_data(self):
        collaborative_analytics = CollaborativeAnalytics()
        analyst1 = Analyst("Analyst1", collaborative_analytics)
        analyst2 = Analyst("Analyst2", collaborative_analytics)
        collaborative_analytics.add_observer(analyst1)
        collaborative_analytics.add_observer(analyst2)

        analyst1.update_data("player1", 10)
        analyst2.visualize_data()


# main.py
def main():
    user_account_manager = UserAccountManager()
    collaborative_analytics = CollaborativeAnalytics()

    while True:
        print("1. Create account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            if user_account_manager.create_account(username, password):
                print("Account created successfully!")
            else:
                print("Username already exists!")
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            if user_account_manager.authenticate(username, password):
                print("Login successful!")
                analyst = Analyst(username, collaborative_analytics)
                while True:
                    print("1. Update data")
                    print("2. Get data")
                    print("3. Generate report")
                    print("4. Visualize data")
                    print("5. Logout")
                    choice = input("Enter your choice: ")

                    if choice == "1":
                        key = input("Enter key: ")
                        value = input("Enter value: ")
                        analyst.update_data(key, value)
                    elif choice == "2":
                        print(analyst.get_data())
                    elif choice == "3":
                        analyst.generate_report()
                    elif choice == "4":
                        analyst.visualize_data()
                    elif choice == "5":
                        break
                    else:
                        print("Invalid choice!")
            else:
                print("Invalid username or password!")
        elif choice == "3":
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()