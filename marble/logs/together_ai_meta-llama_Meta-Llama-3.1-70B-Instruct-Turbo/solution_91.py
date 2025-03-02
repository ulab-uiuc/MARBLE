# task.py
class Task:
    def __init__(self, name, description, priority, required_resources):
        """
        Initialize a Task object.

        Args:
            name (str): The name of the task.
            description (str): A brief description of the task.
            priority (int): The priority of the task (higher is more urgent).
            required_resources (list): A list of resources required to complete the task.
        """
        self.name = name
        self.description = description
        self.priority = priority
        self.required_resources = required_resources
        self.status = "pending"
        self.assigned_agent = None
        self.start_time = None
        self.end_time = None
        self.notes = []

    def assign_agent(self, agent):
        """
        Assign an agent to the task.

        Args:
            agent (Agent): The agent to assign to the task.
        """
        self.assigned_agent = agent

    def update_status(self, status):
        """
        Update the status of the task.

        Args:
            status (str): The new status of the task.
        """
        self.status = status

    def add_note(self, note):
        """
        Add a note to the task.

        Args:
            note (str): The note to add.
        """
        self.notes.append(note)


# agent.py
class Agent:
    def __init__(self, name):
        """
        Initialize an Agent object.

        Args:
            name (str): The name of the agent.
        """
        self.name = name
        self.tasks = []
        self.available = True

    def assign_task(self, task):
        """
        Assign a task to the agent.

        Args:
            task (Task): The task to assign.
        """
        self.tasks.append(task)
        task.assign_agent(self)

    def update_availability(self, available):
        """
        Update the availability of the agent.

        Args:
            available (bool): Whether the agent is available.
        """
        self.available = available


# task_scheduler.py
class TaskScheduler:
    def __init__(self):
        """
        Initialize a TaskScheduler object.
        """
        self.tasks = []
        self.agents = []
        self.history = []

    def add_task(self, task):
        """
        Add a task to the scheduler.

        Args:
            task (Task): The task to add.
        """
        self.tasks.append(task)

    def add_agent(self, agent):
        """
        Add an agent to the scheduler.

        Args:
            agent (Agent): The agent to add.
        """
        self.agents.append(agent)

    def assign_tasks(self):
        """
        Assign tasks to available agents.
        """
        available_agents = [agent for agent in self.agents if agent.available]
        tasks = sorted(self.tasks, key=lambda task: task.priority, reverse=True)
        for task in tasks:
            if task.assigned_agent is None:
                for agent in available_agents:
                    if agent.available:
                        agent.assign_task(task)
                        break

    def update_task_status(self, task, status):
        """
        Update the status of a task.

        Args:
            task (Task): The task to update.
            status (str): The new status of the task.
        """
        task.update_status(status)
        if status == "completed":
            self.history.append(task)
            self.tasks.remove(task)

    def update_agent_availability(self, agent, available):
        """
        Update the availability of an agent.

        Args:
            agent (Agent): The agent to update.
            available (bool): Whether the agent is available.
        """
        agent.update_availability(available)


# main.py
def main():
    scheduler = TaskScheduler()

    # Create tasks
    task1 = Task("Task 1", "This is task 1", 1, ["resource 1", "resource 2"])
    task2 = Task("Task 2", "This is task 2", 2, ["resource 3", "resource 4"])
    task3 = Task("Task 3", "This is task 3", 3, ["resource 5", "resource 6"])

    # Create agents
    agent1 = Agent("Agent 1")
    agent2 = Agent("Agent 2")

    # Add tasks and agents to scheduler
    scheduler.add_task(task1)
    scheduler.add_task(task2)
    scheduler.add_task(task3)
    scheduler.add_agent(agent1)
    scheduler.add_agent(agent2)

    # Assign tasks to agents
    scheduler.assign_tasks()

    # Update task status
    scheduler.update_task_status(task1, "in_progress")
    scheduler.update_task_status(task2, "completed")

    # Update agent availability
    scheduler.update_agent_availability(agent1, False)

    # Print task status
    for task in scheduler.tasks:
        print(f"Task: {task.name}, Status: {task.status}, Assigned Agent: {task.assigned_agent.name if task.assigned_agent else None}")

    # Print agent status
    for agent in scheduler.agents:
        print(f"Agent: {agent.name}, Available: {agent.available}")


if __name__ == "__main__":
    main()