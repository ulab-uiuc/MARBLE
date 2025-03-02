# solution.py
import datetime
from typing import List, Dict

class Task:
    """Represents a task with its properties."""
    def __init__(self, name: str, description: str, priority: int, required_resources: List[str]):
        # Initialize task properties
        self.name = name
        self.description = description
        self.priority = priority
        self.required_resources = required_resources
        self.assigned_agents = []
        self.start_time = None
        self.end_time = None
        self.status = "Not Started"
        self.notes = []

    def assign_agent(self, agent_name: str):
        # Assign an agent to the task
        self.assigned_agents.append(agent_name)

    def update_status(self, status: str):
        # Update the task status
        self.status = status

    def add_note(self, note: str):
        # Add a note to the task
        self.notes.append(note)

    def start_task(self):
        # Start the task
        self.start_time = datetime.datetime.now()
        self.update_status("In Progress")

    def complete_task(self):
        # Complete the task
        self.end_time = datetime.datetime.now()
        self.update_status("Completed")


class Agent:
    """Represents an agent with its properties."""
    def __init__(self, name: str):
        # Initialize agent properties
        self.name = name
        self.available = True
        self.assigned_tasks = []

    def assign_task(self, task: Task):
        # Assign a task to the agent
        self.assigned_tasks.append(task)
        task.assign_agent(self.name)

    def update_availability(self, available: bool):
        # Update the agent's availability
        self.available = available


class MultiAgentTaskScheduler:
    """Manages tasks and agents."""
    def __init__(self):
    def reassign_tasks(self):
        for task_name, task in self.tasks.items():
            for agent_name in task.assigned_agents:
                if not self.agents[agent_name].available:
                    available_agents = [agent for agent in self.agents.values() if agent.available]
                    if available_agents:
                        new_agent = available_agents[0]
                        new_agent.assign_task(task)
                        task.assigned_agents.remove(agent_name)
                        print(f'Task {task_name} reassigned to agent {new_agent.name}.')
                    else:
                        print(f'No available agents to reassign task {task_name}.')
        # Initialize the task scheduler
        self.tasks: Dict[str, Task] = {}
        self.agents: Dict[str, Agent] = {}

    def create_task(self, name: str, description: str, priority: int, required_resources: List[str]):
        # Create a new task
        task = Task(name, description, priority, required_resources)
        self.tasks[name] = task

    def create_agent(self, name: str):
        # Create a new agent
        agent = Agent(name)
        self.agents[name] = agentdef assign_task_to_agent(self, task_name: str, agent_name: str):
    if task_name in self.tasks and agent_name in self.agents and agent_name not in self.tasks[task_name].assigned_agents:
        task = self.tasks[task_name]
        agent = self.agents[agent_name]
        if agent.available:
            agent.assign_task(task)
        else:
            print(f"Agent {agent_name} is not available.")
    elif agent_name in self.tasks[task_name].assigned_agents:
        print(f'Task {task_name} is already assigned to agent {agent_name}.')
        reassign = input('Do you want to reassign the task? (yes/no): ')
        if reassign.lower() == 'yes':
            for existing_agent in self.tasks[task_name].assigned_agents:
                self.agents[existing_agent].assigned_tasks.remove(task)
                self.tasks[task_name].assigned_agents.remove(existing_agent)
            agent.assign_task(task)
        else:
            print('Task assignment cancelled.')
    else:
        print("Task or agent not found.")    def update_task_status(self, task_name: str, status: str):
        # Update the status of a task
        if task_name in self.tasks:
            task = self.tasks[task_name]
            task.update_status(status)
        else:
            print("Task not found.")

    def add_note_to_task(self, task_name: str, note: str):
        # Add a note to a task
        if task_name in self.tasks:
            task = self.tasks[task_name]
            task.add_note(note)
        else:
            print("Task not found.")

    def start_task(self, task_name: str):
        # Start a task
        if task_name in self.tasks:
            task = self.tasks[task_name]
            task.start_task()
        else:
            print("Task not found.")

    def complete_task(self, task_name: str):
        # Complete a task
        if task_name in self.tasks:
            task = self.tasks[task_name]
            task.complete_task()
        else:
            print("Task not found.")

    def update_agent_availability(self, agent_name: str, available: bool):
        # Update the availability of an agent
        if agent_name in self.agents:
            agent = self.agents[agent_name]
            agent.update_availability(available)
        else:
            print("Agent not found.")

    def display_tasks(self):
        # Display all tasks
        for task_name, task in self.tasks.items():
            print(f"Task Name: {task_name}")
            print(f"Description: {task.description}")
            print(f"Priority: {task.priority}")
            print(f"Required Resources: {task.required_resources}")
            print(f"Assigned Agents: {task.assigned_agents}")
            print(f"Status: {task.status}")
            print(f"Notes: {task.notes}")
            print()

    def display_agents(self):
        # Display all agents
        for agent_name, agent in self.agents.items():
            print(f"Agent Name: {agent_name}")
            print(f"Available: {agent.available}")
            print(f"Assigned Tasks: {[task.name for task in agent.assigned_tasks]}")
            print()


def main():
    # Create a task scheduler
    scheduler = MultiAgentTaskScheduler()

    # Create tasks
    scheduler.create_task("Task 1", "This is task 1", 1, ["Resource 1", "Resource 2"])
    scheduler.create_task("Task 2", "This is task 2", 2, ["Resource 3", "Resource 4"])

    # Create agents
    scheduler.create_agent("Agent 1")
    scheduler.create_agent("Agent 2")

    # Assign tasks to agents
    scheduler.assign_task_to_agent("Task 1", "Agent 1")
    scheduler.assign_task_to_agent("Task 2", "Agent 2")

    # Start tasks
    scheduler.start_task("Task 1")
    scheduler.start_task("Task 2")

    # Update task status
    scheduler.update_task_status("Task 1", "In Progress")
    scheduler.update_task_status("Task 2", "Completed")

    # Add notes to tasks
    scheduler.add_note_to_task("Task 1", "This is a note for task 1")
    scheduler.add_note_to_task("Task 2", "This is a note for task 2")

    # Complete tasks
    scheduler.complete_task("Task 1")
    scheduler.complete_task("Task 2")

    # Update agent availability
    scheduler.update_agent_availability("Agent 1", False)
    scheduler.update_agent_availability("Agent 2", True)

    # Display tasks and agents
    scheduler.display_tasks()
    scheduler.display_agents()


if __name__ == "__main__":
    main()