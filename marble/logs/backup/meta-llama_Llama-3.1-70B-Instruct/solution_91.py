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
        self.assigned_agent = None
        self.status = "pending"
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
        self.available = True
        self.assigned_tasks = []

    def assign_task(self, task):
        """
        Assign a task to the agent.

        Args:
            task (Task): The task to assign.
        """
        self.assigned_tasks.append(task)
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
    def periodic_reassign(self):
        while True:
            time.sleep(self.reassign_interval)
            self.assign_tasks()
    def __init__(self):
        self.tasks = []
        self.agents = []
        self.history = []
        self.reassign_interval = 60  # seconds
        self.reassign_thread = threading.Thread(target=self.periodic_reassign)
        self.reassign_thread.daemon = True
        self.reassign_thread.start()
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
        Assign tasks to available agents based on priority and availability.
        """
        available_agents = [agent for agent in self.agents if agent.available]
        tasks_to_assign = sorted(self.tasks, key=lambda task: task.priority, reverse=True)

        for task in tasks_to_assign:
            if task.assigned_agent is None:
                for agent in available_agents:
                    if agent not in [task.assigned_agent for task in tasks_to_assign]:
                        agent.assign_task(task)
                        break

    def update_task_status(self, task, status):def update_agent_availability(self, agent, available):
    agent.update_availability(available)
    self.assign_tasks()    agent.update_availability(available)
        self.assign_tasks()


# multi_agent_task_scheduler.py
class MultiAgentTaskScheduler:
    def __init__(self):
        """
        Initialize a MultiAgentTaskScheduler object.
        """
        self.scheduler = TaskScheduler()

    def create_task(self, name, description, priority, required_resources):
        """
        Create a new task.

        Args:
            name (str): The name of the task.
            description (str): A brief description of the task.
            priority (int): The priority of the task (higher is more urgent).
            required_resources (list): A list of resources required to complete the task.

        Returns:
            Task: The created task.
        """
        task = Task(name, description, priority, required_resources)
        self.scheduler.add_task(task)
        return task

    def create_agent(self, name):
        """
        Create a new agent.

        Args:
            name (str): The name of the agent.

        Returns:
            Agent: The created agent.
        """
        agent = Agent(name)
        self.scheduler.add_agent(agent)
        return agent

    def assign_tasks(self):
        """
        Assign tasks to available agents based on priority and availability.
        """
        self.scheduler.assign_tasks()

    def update_task_status(self, task, status):
        """
        Update the status of a task.

        Args:
            task (Task): The task to update.
            status (str): The new status of the task.
        """
        self.scheduler.update_task_status(task, status)

    def update_agent_availability(self, agent, available):
        """
        Update the availability of an agent.

        Args:
            agent (Agent): The agent to update.
            available (bool): Whether the agent is available.
        """
        self.scheduler.update_agent_availability(agent, available)


# main.py
def main():
    scheduler = MultiAgentTaskScheduler()

    task1 = scheduler.create_task("Task 1", "This is task 1", 1, ["resource1", "resource2"])
    task2 = scheduler.create_task("Task 2", "This is task 2", 2, ["resource3", "resource4"])
    task3 = scheduler.create_task("Task 3", "This is task 3", 3, ["resource5", "resource6"])

    agent1 = scheduler.create_agent("Agent 1")
    agent2 = scheduler.create_agent("Agent 2")

    scheduler.assign_tasks()

    print("Task assignments:")
    for task in scheduler.scheduler.tasks:
        print(f"{task.name}: {task.assigned_agent.name if task.assigned_agent else 'None'}")

    scheduler.update_task_status(task1, "completed")
    scheduler.update_agent_availability(agent1, False)

    print("\nUpdated task assignments:")
    for task in scheduler.scheduler.tasks:
        print(f"{task.name}: {task.assigned_agent.name if task.assigned_agent else 'None'}")


if __name__ == "__main__":
    main()