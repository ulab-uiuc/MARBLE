# Event_Organizer_Collaborative

class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.events = []

    def create_event(self, event_details):
        event = Event(event_details)
        self.events.append(event)
        return event

    def assign_task(self, event, task_details):
        task = Task(task_details)
        event.tasks.append(task)
        return task

    def communicate(self, message):
        print(f"{self.name} says: {message}")

class Event:
    def __init__(self, event_details):
        self.location = event_details.get('location', '')
        self.date = event_details.get('date', '')
        self.time = event_details.get('time', '')
        self.guest_list = event_details.get('guest_list', [])
        self.tasks = []

    def update_event_details(self, event_details):
        self.location = event_details.get('location', self.location)
        self.date = event_details.get('date', self.date)
        self.time = event_details.get('time', self.time)
        self.guest_list = event_details.get('guest_list', self.guest_list)

class Task:
    def __init__(self, task_details):
        self.description = task_details.get('description', '')
        self.deadline = task_details.get('deadline', '')
        self.completed = False

    def update_task_details(self, task_details):
        self.description = task_details.get('description', self.description)
        self.deadline = task_details.get('deadline', self.deadline)

class EventOrganizerCollaborative:
    def __init__(self):
        self.agents = []

    def add_agent(self, agent):
        self.agents.append(agent)

    def update_event(self, event, event_details):
        for agent in self.agents:'Event details updated'        task.update_task_details(task_details)

# Example Usage
if __name__ == "__main__":
    event_organizer = EventOrganizerCollaborative()

    agent1 = Agent("Alice", "Event Manager")
    agent2 = Agent("Bob", "Task Coordinator")

    event_organizer.add_agent(agent1)
    event_organizer.add_agent(agent2)

    event_details = {
        'location': 'ABC Hall',
        'date': '2022-12-31',
        'time': '20:00',
        'guest_list': ['John', 'Jane', 'Doe']
    }

    event = agent1.create_event(event_details)

    task_details = {
        'description': 'Send invitations',
        'deadline': '2022-11-30'
    }

    task = agent2.assign_task(event, task_details)

    agent1.communicate("Let's make this event a success!")
    agent2.communicate("I will take care of the tasks assigned to me.")

    print(event.location)
    print(task.description)