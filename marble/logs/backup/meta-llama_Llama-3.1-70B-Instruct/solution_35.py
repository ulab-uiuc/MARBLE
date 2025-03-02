# event_organizer_collaborative.py

class Agent:
    """Represents an agent with a distinct role and responsibilities."""
    
    def __init__(self, name, role):
        """
        Initializes an Agent object.

        Args:
            name (str): The agent's name.
            role (str): The agent's role.
        """
        self.name = name
        self.role = role

    def __str__(self):
        return f"{self.name} ({self.role})"


class Event:def __init__(self, name, location, date, time, guest_list, budget):self.guest_feedback = []
    self.budget = None
        """
        Initializes an Event object.

        Args:
            name (str): The event's name.
            location (str): The event's location.
            date (str): The event's date.
            time (str): The event's time.
            guest_list (list): The event's guest list.
        """
        self.name = name
        self.location = location
        self.date = date
        self.time = time
        self.guest_list = guest_list
        self.tasks = []

    def add_task(self, task):
        """
        Adds a task to the event.

        Args:
            task (Task): The task to add.
        """
        self.tasks.append(task)

    def __str__(self):
        return f"{self.name} at {self.location} on {self.date} at {self.time}"


class Task:
    """Represents a task with a deadline and assignee."""
    
    def __init__(self, name, deadline, assignee):
        """
        Initializes a Task object.

        Args:
            name (str): The task's name.
            deadline (str): The task's deadline.
            assignee (Agent): The task's assignee.
        """
        self.name = name
        self.deadline = deadline
        self.assignee = assignee
        self.status = "Not Started"

    def update_status(self, status):
        """
        Updates the task's status.

        Args:
            status (str): The new status.
        """
        self.status = status

    def __str__(self):
        return f"{self.name} (Deadline: {self.deadline}, Assignee: {self.assignee})"


class Budget:
    """Represents a budget with expenses and limits."""
    
    def __init__(self, limit):
        """
        Initializes a Budget object.

        Args:
            limit (float): The budget limit.
        """
        self.limit = limit
        self.expenses = []

    def add_expense(self, expense):
        """
        Adds an expense to the budget.

        Args:
            expense (float): The expense to add.
        """
        self.expenses.append(expense)

    def get_total_expenses(self):
        """
        Gets the total expenses.

        Returns:
            float: The total expenses.
        """
        return sum(self.expenses)

    def __str__(self):
        return f"Budget (Limit: {self.limit}, Total Expenses: {self.get_total_expenses()})"


class Dashboard:
    """Represents a dashboard with event metrics."""
    
    def __init__(self):
        """
        Initializes a Dashboard object.
        """
        self.events = []

    def add_event(self, event):
        """
        Adds an event to the dashboard.

        Args:
            event (Event): The event to add.
        """
        self.events.append(event)

    def get_event_metrics(self):
        """
        Gets the event metrics.

        Returns:
            dict: The event metrics.
        """
        metrics = {}
        for event in self.events:
            metrics[event.name] = {
                "Completion Status": self.get_completion_status(event),
                "Budget Adherence": self.get_budget_adherence(event),
                "Guest Satisfaction": self.get_guest_satisfaction(event)
            }
        return metrics

    def get_completion_status(self, event):completed_tasks = sum(1 for task in event.tasks if task.status == "Completed")
return f"{completed_tasks / len(event.tasks) * 100:.2f}%"# Calculate completion status based on task status
        return "In Progress"

    def get_budget_adherence(self, event):total_expenses = sum(expense for expense in event.budget.expenses)
if total_expenses > event.budget.limit:
    return "Over Budget"
else:
    return "Within Budget"# Calculate budget adherence based on expenses and limit
        return "Within Budget"

    def get_guest_satisfaction(self, event):guest_satisfaction = sum(feedback for feedback in event.guest_feedback) / len(event.guest_feedback)
if guest_satisfaction >= 4:
    return "Satisfied"
elif guest_satisfaction >= 2:
    return "Neutral"
else:
    return "Dissatisfied"# Calculate guest satisfaction based on guest feedback
        return "Satisfied"

    def __str__(self):
        return "Dashboard"


class EventOrganizerCollaborative:
    """Represents the Event Organizer Collaborative system."""
    
    def __init__(self):
        """
        Initializes the Event Organizer Collaborative system.
        """
        self.agents = []
        self.events = []
        self.dashboard = Dashboard()

    def add_agent(self, agent):
        """
        Adds an agent to the system.

        Args:
            agent (Agent): The agent to add.
        """
        self.agents.append(agent)

    def add_event(self, event):
        """
        Adds an event to the system.

        Args:
            event (Event): The event to add.
        """
        self.events.append(event)
        self.dashboard.add_event(event)

    def __str__(self):
        return "Event Organizer Collaborative"


# Example usage
if __name__ == "__main__":
    # Create agents
    agent1 = Agent("John Doe", "Event Manager")
    agent2 = Agent("Jane Doe", "Task Manager")

    # Create events
    event1 = Event("Wedding", "New York", "2024-07-26", "10:00 AM", ["Guest 1", "Guest 2"])
    event2 = Event("Conference", "Los Angeles", "2024-08-01", "9:00 AM", ["Guest 3", "Guest 4"])budget2 = Budget(5000.0)

    # Add expenses to budgets
    budget1.add_expense(5000.0)
    budget2.add_expense(2000.0)

    # Create Event Organizer Collaborative system
    eoc = EventOrganizerCollaborative()

    # Add agents to system
    eoc.add_agent(agent1)
    eoc.add_agent(agent2)

    # Add events to system
    eoc.add_event(event1)
    eoc.add_event(event2)

    # Print system information
    print(eoc)
    for agent in eoc.agents:
        print(agent)
    for event in eoc.events:
        print(event)
        for task in event.tasks:
            print(task)
    print(eoc.dashboard)
    print(eoc.dashboard.get_event_metrics())