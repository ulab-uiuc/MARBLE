
# Agent.py

class Agent:
    """Represents an agent with a name and role."""
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def __str__(self):
        return f"{self.name} ({self.role})"class Event:
    def __init__(self, name, location, date, time, guest_list, budget_amount):
        self.name = name
        self.location = location
        self.date = date
        self.time = time
        self.guest_list = guest_list
        self.tasks = []
        self.budget = Budget(budget_amount)    def __init__(self, name, location, date, time, guest_list):
        self.name = name
        self.location = location
        self.date = date
        self.time = time
        self.guest_list = guest_list
        self.tasks = []

    def add_task(self, task):
        """Adds a task to the event."""
        self.tasks.append(task)

    def __str__(self):
        return f"{self.name} at {self.location} on {self.date} at {self.time}"


class Task:
    """Represents a task with a deadline and status."""
    def __init__(self, name, deadline, status="Not Started"):
        self.name = name
        self.deadline = deadline
        self.status = status

    def update_status(self, status):
        """Updates the status of the task."""
        self.status = status

    def __str__(self):
        return f"{self.name} (Deadline: {self.deadline}, Status: {self.status})"


class Budget:
    """Represents a budget with expenses and alerts."""
    def __init__(self, amount):
        self.amount = amount
        self.expenses = []

    def add_expense(self, expense):
        """Adds an expense to the budget."""
        self.expenses.append(expense)
        if sum(self.expenses) > self.amount:
            print("Budget exceeded!")

    def __str__(self):
        return f"Budget: {self.amount}, Expenses: {sum(self.expenses)}"


class Dashboard:
    """Represents a dashboard with event metrics."""
    def __init__(self):
        self.events = []

    def add_event(self, event):
        """Adds an event to the dashboard."""
        self.events.append(event)

    def display_metrics(self):
        """Displays event metrics."""
        for event in self.events:
            print(f"Event: {event.name}")
            print(f"Completion Status: {len([task for task in event.tasks if task.status == 'Completed'])}/{len(event.tasks)}")
print(f"Budget Adherence: {sum(event.budget.expenses)}/{event.budget.amount}")print(f"Guest Satisfaction: 90%")
            print()


class CommunicationPlatform:
    """Represents a communication platform with chat, comments, and file sharing."""
    def __init__(self):
        self.chat_log = []
        self.comments = []
        self.files = []

    def send_message(self, message):
        """Sends a message to the chat log."""
        self.chat_log.append(message)

    def add_comment(self, comment):
        """Adds a comment to the comments list."""
        self.comments.append(comment)

    def share_file(self, file):
        """Shares a file."""
        self.files.append(file)

    def __str__(self):
        return f"Chat Log: {self.chat_log}, Comments: {self.comments}, Files: {self.files}"


class EventOrganizerCollaborative:
    """Represents the Event Organizer Collaborative system."""
    def __init__(self):
        self.agents = []
        self.events = []
        self.dashboard = Dashboard()
        self.communication_platform = CommunicationPlatform()

    def add_agent(self, agent):
        """Adds an agent to the system."""
        self.agents.append(agent)

    def create_event(self, event):
        """Creates an event."""
        self.events.append(event)
        self.dashboard.add_event(event)

    def display_dashboard(self):
        """Displays the dashboard."""
        self.dashboard.display_metrics()

    def display_communication_platform(self):
        """Displays the communication platform."""
        print(self.communication_platform)


# Example usage
event_organizer_collaborative = EventOrganizerCollaborative()

agent1 = Agent("John Doe", "Event Planner")
agent2 = Agent("Jane Doe", "Event Coordinator")

event_organizer_collaborative.add_agent(agent1)
event_organizer_collaborative.add_agent(agent2)

event = Event("Wedding", "New York", "2024-02-14", "10:00 AM", ["John Doe", "Jane Doe"], 1000)event.add_task(Task("Book venue", "2024-01-01"))
event.add_task(Task("Send invitations", "2024-01-15"))

event_organizer_collaborative.create_event(event)

budget = Budget(1000)
budget.add_expense(500)

event_organizer_collaborative.communication_platform.send_message("Hello, team!")
event_organizer_collaborative.communication_platform.add_comment("Great job on the event planning!")
event_organizer_collaborative.communication_platform.share_file("event_plan.pdf")

event_organizer_collaborative.display_dashboard()
event_organizer_collaborative.display_communication_platform()