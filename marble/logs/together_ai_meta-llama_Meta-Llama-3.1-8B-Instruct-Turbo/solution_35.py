# solution.py
# Importing necessary libraries
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

    # Method to create event
    def create_event(self, name, location, date, time, guest_list):
        event = Event(name, location, date, time, guest_list)
        self.events.append(event)

    # Method to assign task
    def assign_task(self, event_name, task_name, deadline, assigned_to):
        event = next((e for e in self.events if e.name == event_name), None)
        if event:
            task = Task(task_name, deadline, assigned_to)
            event.tasks.append(task)
            print(f"Task {task_name} assigned to {assigned_to} for event {event_name}")

    # Method to add comment
    def add_comment(self, event_name, comment):
        event = next((e for e in self.events if e.name == event_name), None)
        if event:
            event.comments.append(comment)
            print(f"Comment added to event {event_name}")

    # Method to add budget
    def add_budget(self, event_name, amount):
        event = next((e for e in self.events if e.name == event_name), None)
        if event:
            event.budget = Budget(amount)
            print(f"Budget added to event {event_name}")

    # Method to update expenses
    def update_expenses(self, event_name, amount):
        event = next((e for e in self.events if e.name == event_name), None)
        if event:
            event.budget.expenses += amount
            print(f"Expenses updated for event {event_name}")

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
                print(f"Task: {task.name}, Deadline: {task.deadline}, Assigned to: {task.assigned_to}")
            print(f"Comments:")
            for comment in event.comments:
                print(comment)
            print(f"Budget: {event.budget.amount}, Expenses: {event.budget.expenses}")
            print()

# Creating an instance of Event_Organizer_Collaborative
event_organizer = Event_Organizer_Collaborative()

# Adding agents
event_organizer.add_agent("John", "Event Coordinator")
event_organizer.add_agent("Jane", "Marketing Manager")
event_organizer.add_agent("Bob", "Logistics Manager")

# Creating events
event_organizer.create_event("Wedding", "Hotel", "2024-06-15", "10:00 AM", ["Guest 1", "Guest 2", "Guest 3"])
event_organizer.create_event("Conference", "Convention Center", "2024-06-20", "9:00 AM", ["Guest 4", "Guest 5", "Guest 6"])

# Assigning tasks
event_organizer.assign_task("Wedding", "Task 1", "2024-06-10", "John")
event_organizer.assign_task("Wedding", "Task 2", "2024-06-12", "Jane")
event_organizer.assign_task("Conference", "Task 3", "2024-06-18", "Bob")

# Adding comments
event_organizer.add_comment("Wedding", "This is a comment for the wedding event.")
event_organizer.add_comment("Conference", "This is a comment for the conference event.")

# Adding budget
event_organizer.add_budget("Wedding", 10000)
event_organizer.add_budget("Conference", 5000)

# Updating expenses
event_organizer.update_expenses("Wedding", 5000)
event_organizer.update_expenses("Conference", 2000)

# Viewing dashboard
event_organizer.view_dashboard()