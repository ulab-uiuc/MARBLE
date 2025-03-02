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
        self.tasks: Dict[str, str] = {}  # Dictionary to hold tasks and their assignees
        self.budget: float = 0.0  # Total budget for the event
        self.expenses: float = 0.0  # Total expenses incurred
        self.notifications: List[str] = []  # List of notifications for agents

    def add_guest(self, guest: str):
        """Add a guest to the event's guest list."""
        self.guest_list.append(guest)if guest not in self.guest_list:
            self.guest_list.append(guest)
            self.notify_agents(f"Guest {guest} added to {self.title}.")
        else:
            self.notify_agents(f"Guest {guest} is already on the list for {self.title}.")        self.notify_agents(f"Guest {guest} added to {self.title}.")

    def assign_task(self, task: str, agent_name: str):
        """Assign a task to an agent."""
        self.tasks[task] = agent_name
        self.notify_agents(f"Task '{task}' assigned to {agent_name}.")

    def set_budget(self, budget: float):
        """Set the budget for the event."""
        self.budget = budget
        self.notify_agents(f"Budget set to ${budget} for {self.title}.")

    def add_expense(self, amount: float):
        """Add an expense to the event."""
        self.expenses += amount
        self.notify_agents(f"Expense of ${amount} added to {self.title}.")
        if self.expenses > self.budget:
            self.notify_agents(f"Warning: Expenses exceeded budget for {self.title}.")

    def notify_agents(self, message: str):
        """Notify all agents about changes."""
        self.notifications.append(message)

# Define a class to represent the Event Organizer Collaborative system
class EventOrganizerCollaborative:
    def __init__(self):
        self.agents: List[Agent] = []  # List of agents
        self.events: List[Event] = []  # List of events

    def add_agent(self, agent: Agent):
        """Add an agent to the system."""
        self.agents.append(agent)

    def create_event(self, title: str, location: str, date: str, time: str) -> Event:
        """Create a new event and add it to the system."""
        new_event = Event(title, location, date, time)
        self.events.append(new_event)
        return new_event

    def get_dashboard(self) -> Dict[str, Optional[Dict]]:
        """Generate a dashboard overview of all events."""
        dashboard = {}
        for event in self.events:
            dashboard[event.title] = {
                "Location": event.location,
                "Date": event.date.strftime("%Y-%m-%d"),
                "Time": event.time,
                "Guests": event.guest_list,
                "Budget": event.budget,
                "Expenses": event.expenses,
                "Status": "Under Budget" if event.expenses <= event.budget else "Over Budget",
                "Notifications": event.notifications
            }
        return dashboard

# Example usage of the Event Organizer Collaborative system
if __name__ == "__main__":
    # Create an instance of the event organizer system
    organizer = EventOrganizerCollaborative()

    # Add agents to the system
    agent1 = Agent("Alice", "Coordinator")
    agent2 = Agent("Bob", "Budget Manager")
    organizer.add_agent(agent1)
    organizer.add_agent(agent2)

    # Create an event
    event = organizer.create_event("Annual Gala", "City Hall", "2023-12-15", "18:00")

    # Manage event details
    event.add_guest("John Doe")
    event.assign_task("Book catering", "Alice")
    event.set_budget(5000)
    event.add_expense(2000)

    # Print the dashboard overview
    dashboard = organizer.get_dashboard()
    for event_title, details in dashboard.items():
        print(f"Event: {event_title}")
        for key, value in details.items():
            print(f"  {key}: {value}")