# solution.py

# Importing necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from datetime import datetime
import numpy as np
import random

# User class to store user information and tasks
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.tasks = []
        self.availability = []

# Task class to store task information
class Task:
    def __init__(self, name, duration, priority, dependencies):
        self.name = name
        self.duration = duration
        self.priority = priority
        self.dependencies = dependencies

# CollaborativeSchedulePlanner class to manage the schedule
class CollaborativeSchedulePlanner:
    def __init__(self):
        self.users = {}
        self.schedule = {}

    # Method to add a new user
    def add_user(self, username, password):
        self.users[username] = User(username, password)

    # Method to add a new task
    def add_task(self, username, name, duration, priority, dependencies):
        if username in self.users:
            task = Task(name, duration, priority, dependencies)
            self.users[username].tasks.append(task)
            self.update_schedule(username, task)
        else:
            print("User not found.")

    # Method to update the schedule
    def update_schedule(self, username, task):
        if username in self.schedule:
            self.schedule[username].append(task)
        else:
            self.schedule[username] = [task]

    # Method to view the schedule
    def view_schedule(self, username):
        if username in self.schedule:
            print("Schedule for", username)
            for task in self.schedule[username]:
                print(task.name, task.duration, task.priority, task.dependencies)
        else:
            print("No schedule found for", username)

    # Method to analyze user patterns and preferences
    def analyze_user_patterns(self):
        # For simplicity, we will use a basic machine learning model
        # In a real-world application, you would use a more complex model
        # and train it on a larger dataset
        data = []
        for username, user in self.users.items():
            for task in user.tasks:
                data.append([username, task.duration, task.priority])
        X = np.array(data)[:, 1:]
        y = np.array(data)[:, 2]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        print("Mean Squared Error:", mean_squared_error(y_test, y_pred))

    # Method to generate reports and visual representations
    def generate_reports(self):
        # For simplicity, we will use a basic Gantt chart
        # In a real-world application, you would use a more complex library
        # such as Gantt or Plotly
        for username, user in self.users.items():
            tasks = []
            for task in user.tasks:
                tasks.append([task.name, task.duration])
            df = pd.DataFrame(tasks, columns=['Task', 'Duration'])
            plt.bar(df['Task'], df['Duration'])
            plt.xlabel('Task')
            plt.ylabel('Duration')
            plt.title('Gantt Chart for ' + username)
            plt.show()

# Main function
def main():
    planner = CollaborativeSchedulePlanner()
    while True:
        print("1. Add user")
        print("2. Add task")
        print("3. View schedule")
        print("4. Analyze user patterns")
        print("5. Generate reports")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            planner.add_user(username, password)
        elif choice == '2':
            username = input("Enter username: ")
            name = input("Enter task name: ")
            duration = int(input("Enter task duration: "))
            priority = int(input("Enter task priority: "))
            dependencies = input("Enter task dependencies: ")
            planner.add_task(username, name, duration, priority, dependencies)
        elif choice == '3':
            username = input("Enter username: ")
            planner.view_schedule(username)
        elif choice == '4':
            planner.analyze_user_patterns()
        elif choice == '5':
            planner.generate_reports()
        elif choice == '6':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()