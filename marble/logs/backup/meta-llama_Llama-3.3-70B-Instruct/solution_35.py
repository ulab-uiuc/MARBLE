# solution.py
# Event Organizer Collaborative System

# Import required libraries
import datetime
import threading

# Define a class for Agent
class Agent:
    def __init__(self, name, role):
        """
        Initialize an Agent object.

        Args:
        name (str): The name of the agent.
        role (str): The role of the agent.
        """
        self.name = name
        self.role = role

# Define a class for Event
class Event:
    def __init__(self, name, location, date, time, guest_list):
        """
        Initialize an Event object.

        Args:
        name (str): The name of the event.
        location (str): The location of the event.
        date (str): The date of the event.
        time (str): The time of the event.
        guest_list (list): The list of guests for the event.
        """
        self.name = name
        self.location = location
        self.date = date
        self.time = time
        self.guest_list = guest_list
        self.tasks = []
        self.budget = 0
        self.expenses = 0

    def add_task(self, task):
        """
        Add a task to the event.

        Args:
        task (Task): The task to be added.
        """
        self.tasks.append(task)

    def update_budget(self, amount):
        """
        Update the budget of the event.

        Args:
        amount (float): The amount to be added to the budget.
        """
        self.budget += amount

    def add_expense(self, amount):
        """
        Add an expense to the event.

        Args:
        amount (float): The amount of the expense.
        """
        self.expenses += amount

# Define a class for Task
class Task:
    def __init__(self, name, deadline, assigned_to):
        """
        Initialize a Task object.

        Args:
        name (str): The name of the task.
        deadline (str): The deadline of the task.
        assigned_to (Agent): The agent assigned to the task.
        """
        self.name = name
        self.deadline = deadline
        self.assigned_to = assigned_to
        self.status = "Not Started"

    def update_status(self, status):
        """
        Update the status of the task.

        Args:
        status (str): The new status of the task.
        """
        self.status = status

# Define a class for CommunicationPlatform
class CommunicationPlatform:
    def __init__(self):
        """
        Initialize a CommunicationPlatform object.
        """
        self.messages = []

    def send_message(self, message):
        """
        Send a message on the communication platform.

        Args:
        message (str): The message to be sent.
        """
        self.messages.append(message)

# Define a class for Dashboard
class Dashboard:
    def __init__(self):
    def notify_observers(self, message):
        with self.lock:
            for observer in self.observers:
                observer.update(message)
    def register_observer(self, observer):
        with self.lock:
            self.observers.append(observer)
        self.observers = []
        self.lock = threading.Lock()
        """
        Initialize a Dashboard object.
        """
        self.events = []

    def add_event(self, event):
        """
        Add an event to the dashboard.

        Args:
        event (Event): The event to be added.
        """
        self.events.append(event)

    def update_event(self, event):
        """
        Update an event on the dashboard.

        Args:
        event (Event): The event to be updated.
        """
        for i, e in enumerate(self.events):
            if e.name == event.name:
                self.events[i] = event
                break

# Define a class for EventOrganizerCollaborative
class EventOrganizerCollaborative:
    def __init__(self):
        """
        Initialize an EventOrganizerCollaborative object.
        """
        self.agents = []
        self.events = []
        self.communication_platform = CommunicationPlatform()
        self.dashboard = Dashboard()

    def add_agent(self, agent):
        """
        Add an agent to the system.

        Args:
        agent (Agent): The agent to be added.
        """
        self.agents.append(agent)

    def create_event(self, name, location, date, time, guest_list):def assign_task(self, event_name, task_name, deadline, agent_name):
        event = next((e for e in self.events if e.name == event_name), None)
        if event:
            agent = next((a for a in self.agents if a.name == agent_name), None)
            if agent:
                task = Task(task_name, deadline, agent)
                event.add_task(task)
                self.notify_observers(f'Task {task_name} assigned to {agent_name}')
            else:
                print(f"Agent {agent_name} not found")
        else:
            print(f"Event {event_name} not found")    def update_task_status(self, event_name, task_name, status):
        event = next((e for e in self.events if e.name == event_name), None)
        if event:
            task = next((t for t in event.tasks if t.name == task_name), None)
            if task:
                task.update_status(status)
                self.notify_observers(f'Task {task_name} updated to {status}')    def send_message(self, message):
        """
        Send a message on the communication platform.

        Args:
        message (str): The message to be sent.
        """
        self.communication_platform.send_message(message)

    def update_budget(self, event_name, amount):    def add_expense(self, event_name, amount):
        event = next((e for e in self.events if e.name == event_name), None)
        if event:
            event.add_expense(amount)
            self.notify_observers(f'Expense added to {event_name}: {amount}')    def display_dashboard(self):
        """
        Display the dashboard.
        """
        for event in self.dashboard.events:
            print(f"Event: {event.name}")
            print(f"Location: {event.location}")
            print(f"Date: {event.date}")
            print(f"Time: {event.time}")
            print(f"Guest List: {event.guest_list}")
            print(f"Tasks: {[t.name for t in event.tasks]}")
            print(f"Budget: {event.budget}")
            print(f"Expenses: {event.expenses}")
            print("")

# Create an instance of EventOrganizerCollaborative
event_organizer = EventOrganizerCollaborative()

# Create agents
agent1 = Agent("John", "Organizer")
agent2 = Agent("Jane", "Assistant")

# Add agents to the system
event_organizer.add_agent(agent1)
event_organizer.add_agent(agent2)

# Create an event
event_organizer.create_event("Wedding", "New York", "2024-09-16", "10:00 AM", ["Guest1", "Guest2"])

# Assign tasks
event_organizer.assign_task("Wedding", "Task1", "2024-09-10", "John")
event_organizer.assign_task("Wedding", "Task2", "2024-09-12", "Jane")

# Update task status
event_organizer.update_task_status("Wedding", "Task1", "In Progress")

# Send a message
event_organizer.send_message("Hello, team!")

# Update budget
event_organizer.update_budget("Wedding", 1000.0)

# Add an expense
event_organizer.add_expense("Wedding", 500.0)

# Display the dashboard
event_organizer.display_dashboard()