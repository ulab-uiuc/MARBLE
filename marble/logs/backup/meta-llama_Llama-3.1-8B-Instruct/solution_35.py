# solution.py

# Importing required libraries
import datetime
import random

# Defining a class for Agent
class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.tasks = []
        self.comments = []

# Defining a class for Event
class Event:
    def __init__(self, name, location, date, time, guest_list):
        self.name = name
        self.location = location
        self.date = date
        self.time = time
        self.guest_list = guest_list
        self.tasks = []
        self.comments = []
        self.budget = 0
        self.expenses = 0

# Defining a class for Task
class Task:
    def __init__(self, name, deadline, assigned_to):
        self.name = name
        self.deadline = deadline
        self.assigned_to = assigned_to
        self.status = "Not Started"

# Defining a class for Budget
class Budget:
    def __init__(self, amount):
        self.amount = amount
        self.expenses = 0

# Defining a class for Dashboard
class Dashboard:
    def __init__(self):
        self.events = []

# Defining a class for Event_Organizer_Collaborative
class Event_Organizer_Collaborative:
    def __init__(self):
        self.agents = []
        self.events = []
        self.dashboard = Dashboard()

    # Method to add agent
    def add_agent(self, name, role):
        agent = Agent(name, role)
        self.agents.append(agent)
        print(f"Agent {name} added with role {role}")

    # Method to create event
    def create_event(self, name, location, date, time, guest_list):
        event = Event(name, location, date, time, guest_list)
        self.events.append(event)
        print(f"Event {name} created")

    # Method to assign task
    def assign_task(self, event_name, task_name, deadline, assigned_to):
        event = next((e for e in self.events if e.name == event_name), None)
        if event:
            task = Task(task_name, deadline, assigned_to)
            event.tasks.append(task)
            print(f"Task {task_name} assigned to {assigned_to} for event {event_name}")
        else:
            print(f"Event {event_name} not found")

    # Method to add comment
    def add_comment(self, event_name, comment):
        event = next((e for e in self.events if e.name == event_name), None)
        if event:
            event.comments.append(comment)
            print(f"Comment added to event {event_name}")
        else:
            print(f"Event {event_name} not found")

    # Method to update budget
    def update_budget(self, event_name, amount):
        event = next((e for e in self.events if e.name == event_name), None)
        if event:
            event.budget = amount
            print(f"Budget updated for event {event_name}")
        else:
            print(f"Event {event_name} not found")

    # Method to add expense
    def add_expense(self, event_name, amount):
        event = next((e for e in self.events if e.name == event_name), None)
        if event:
            event.expenses += amount
            print(f"Expense added to event {event_name}")
        else:
            print(f"Event {event_name} not found")

    # Method to view dashboard
    def view_dashboard(self):
        print("Dashboard:")
        for event in self.events:
            print(f"Event: {event.name}")
            print(f"Location: {event.location}")
            print(f"Date: {event.date}")
            print(f"Time: {event.time}")
            print(f"Guest List: {event.guest_list}")
            print(f"Tasks:")
            for task in event.tasks:
                print(f"Task: {task.name}, Deadline: {task.deadline}, Assigned To: {task.assigned_to}")
            print(f"Comments:")
            for comment in event.comments:
                print(comment)
            print(f"Budget: {event.budget}, Expenses: {event.expenses}")

# Creating an instance of Event_Organizer_Collaborative
collaborative = Event_Organizer_Collaborative()

# Adding agents
collaborative.add_agent("John", "Project Manager")
collaborative.add_agent("Jane", "Designer")
collaborative.add_agent("Bob", "Developer")

# Creating events
collaborative.create_event("Event 1", "New York", "2024-07-26", "10:00 AM", ["John", "Jane", "Bob"])
collaborative.create_event("Event 2", "Los Angeles", "2024-07-27", "11:00 AM", ["John", "Jane", "Bob"])

# Assigning tasks
collaborative.assign_task("Event 1", "Task 1", "2024-07-25", "John")
collaborative.assign_task("Event 1", "Task 2", "2024-07-26", "Jane")
collaborative.assign_task("Event 2", "Task 3", "2024-07-28", "Bob")

# Adding comments
collaborative.add_comment("Event 1", "This is a comment for Event 1")
collaborative.add_comment("Event 2", "This is a comment for Event 2")

# Updating budget
collaborative.update_budget("Event 1", 10000)
collaborative.update_budget("Event 2", 20000)

# Adding expenses
collaborative.add_expense("Event 1", 5000)
collaborative.add_expense("Event 2", 10000)

# Viewing dashboard
collaborative.view_dashboard()