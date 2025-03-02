# solution.py

# Import necessary libraries
from datetime import datetime
from typing import List, Dict, Optional

# Define a class to represent an Agent in the event organizing system
class Agent:
    def __init__(self, name: str, role: str):
        self.name = name  # Agent's name
        self.role = role  # Agent's role (e.g., Coordinator, Budget Manager)

# Define a class to represent an Event
class Event:
    def __init__(self, title: str, location: str, date: str, time: str):
        self.title = title  # Title of the event
        self.location = location  # Location of the event
        self.date = datetime.strptime(date, "%Y-%m-%d")  # Event date
        self.time = time  # Event time
        self.guest_list: List[str] = []  # List of guests
        self.tasks: Dict[str, str] = {}  # Dictionary to hold tasks and their statuses
        self.budget: float = 0.0  # Total budget for the event
        self.expenses: float = 0.0  # Total expenses incurred
        self.notifications: List[str] = []  # Notifications for agents

    def add_guest(self, guest: str):
        """Add a guest to the event's guest list."""
        self.guest_list.append(guest)if guest not in self.guest_list:
            self.guest_list.append(guest)
            self.notify_agents(f"Guest {guest} added to the event.")
        else:
            self.notify_agents(f"Guest {guest} cannot be added again.")        self.notify_agents(f"Guest {guest} added to the event.")

    def assign_task(self, task: str, agent: str):
        """Assign a task to an agent."""
        self.tasks[task] = "Assigned to " + agent
        self.notify_agents(f"Task '{task}' assigned to {agent}.")

    def update_budget(self, amount: float):
        """Update the budget and track expenses."""
        self.budget += amount
        self.notify_agents(f"Budget updated. New budget: {self.budget}")

    def add_expense(self, amount: float):
        """Add an expense and check if it exceeds the budget."""
        self.expenses += amount
        if self.expenses > self.budget:
            self.notify_agents(f"Warning: Expenses exceeded budget! Current expenses: {self.expenses}")

    def notify_agents(self, message: str):
        """Notify all agents about changes."""
        self.notifications.append(message)

# Define a class to represent the Event Organizer Collaborative system
class EventOrganizerCollaborative:
    def __init__(self):
        self.agents: List[Agent] = []  # List of agents
        self.events: List[Event] = []  # List of events

    def add_agent(self, name: str, role: str):
        """Add a new agent to the system."""
        agent = Agent(name, role)
        self.agents.append(agent)

    def create_event(self, title: str, location: str, date: str, time: str):
        """Create a new event."""
        event = Event(title, location, date, time)
        self.events.append(event)
        self.notify_agents(f"New event '{title}' created.")

    def notify_agents(self, message: str):
        """Notify all agents about system-wide changes."""
        for agent in self.agents:
            print(f"Notification to {agent.name}: {message}")

    def display_dashboard(self):
        """Display the dashboard with ongoing events and their statuses."""
        print("Event Dashboard:")
        for event in self.events:
            print(f"Event: {event.title}, Location: {event.location}, Date: {event.date.date()}, Time: {event.time}")
            print(f"Guests: {', '.join(event.guest_list)}")
            print(f"Budget: {event.budget}, Expenses: {event.expenses}")
            print(f"Tasks: {event.tasks}")
            print(f"Notifications: {event.notifications}")

# Example usage of the Event Organizer Collaborative system
if __name__ == "__main__":
    # Create an instance of the Event Organizer Collaborative system
    organizer = EventOrganizerCollaborative()

    # Add agents to the system
    organizer.add_agent("Alice", "Coordinator")
    organizer.add_agent("Bob", "Budget Manager")

    # Create an event
    organizer.create_event("Annual Gala", "City Hall", "2023-12-15", "18:00")

    # Access the first event and manage it
    event = organizer.events[0]
    event.add_guest("John Doe")
    event.assign_task("Book catering", "Alice")
    event.update_budget(5000)
    event.add_expense(2000)

    # Display the dashboard
    organizer.display_dashboard()