class Task:
    def __init__(self, name, description, priority, resources):
        self.name = name
        self.description = description
        self.priority = priority
        self.resources = resources
        self.status = "Pending"
        self.assigned_agent = None
        self.start_time = None
        self.end_time = None
        self.notes = ""

    def assign_task(self, agent):
        self.assigned_agent = agent

    def start_task(self):def start_task(self):
    import datetime
    self.start_time = datetime.datetime.now()
    self.status = "In Progress"    def complete_task(self):self.end_time = datetime.datetime.now()        self.status = "Completed"
        self.end_time = "Current Time"

    def add_notes(self, notes):
        self.notes += notes


class Agent:
    def __init__(self, name, availability):
        self.name = name
        self.availability = availability
        self.tasks_assigned = []

    def assign_task(self, task):
        self.tasks_assigned.append(task)


class MultiAgentTaskScheduler:
    def __init__(self):
        self.tasks = []
        self.agents = []

    def add_task(self, task):
        self.tasks.append(task)

    def add_agent(self, agent):
        self.agents.append(agent)

    def assign_tasks_to_agents(self):
        for task in self.tasks:
            available_agents = [agent for agent in self.agents if agent.availability]
            if available_agents:
                agent = min(available_agents, key=lambda x: len(x.tasks_assigned))
                agent.assign_task(task)
                task.assign_task(agent)
                agent.availability = False

    def reassign_tasks(self):
        for agent in self.agents:
            if agent.availability:
                for task in agent.tasks_assigned:
                    if task.priority == "High":
                        agent.availability = False
                        task.assigned_agent = None
                        self.assign_tasks_to_agents()
                        break

    def display_task_status(self):
        for task in self.tasks:
            print(f"Task: {task.name}, Status: {task.status}, Assigned Agent: {task.assigned_agent.name if task.assigned_agent else 'Unassigned'}")

    def display_agent_tasks(self, agent_name):
        for agent in self.agents:
            if agent.name == agent_name:
                print(f"Agent: {agent.name}")
                for task in agent.tasks_assigned:
                    print(f"Task: {task.name}, Status: {task.status}")

# Sample code to demonstrate the functionality
if __name__ == "__main__":
    task1 = Task("Task 1", "Description 1", "High", ["Resource 1", "Resource 2"])
    task2 = Task("Task 2", "Description 2", "Low", ["Resource 3"])
    
    agent1 = Agent("Agent 1", True)
    agent2 = Agent("Agent 2", True)
    
    scheduler = MultiAgentTaskScheduler()
    scheduler.add_task(task1)
    scheduler.add_task(task2)
    scheduler.add_agent(agent1)
    scheduler.add_agent(agent2)
    
    scheduler.assign_tasks_to_agents()
    scheduler.display_task_status()
    
    task1.start_task()
    task1.complete_task()
    task1.add_notes("Task completed successfully.")
    
    scheduler.reassign_tasks()
    scheduler.display_task_status()
    
    scheduler.display_agent_tasks("Agent 1")