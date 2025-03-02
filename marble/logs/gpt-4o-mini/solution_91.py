# solution.py

class Task:
    """Class representing a task with its details."""
    
    def __init__(self, name, description, priority, resources):
        self.name = name  # Name of the task
        self.description = description  # Description of the task
        self.priority = priority  # Priority of the task (higher number means higher priority)
        self.resources = resources  # Resources required for the task
        self.assigned_agents = []  # List of agents assigned to this task
        self.status = 'Pending'  # Current status of the task
        self.start_time = None  # Start time of the task
        self.end_time = None  # End time of the task
        self.notes = []  # Log of notes or feedback during task execution

    def assign_agent(self, agent):
        """Assign an agent to the task."""
        self.assigned_agents.append(agent)
        agent.assign_task(self)

    def complete_task(self):
        """Mark the task as completed."""
        self.status = 'Completed'
        self.end_time = self.get_current_time()

    def get_current_time(self):
        """Get the current time (placeholder for actual implementation)."""
        from datetime import datetime
        return datetime.now()

    def add_note(self, note):
        """Add a note to the task's log."""
        self.notes.append(note)

class Agent:
    """Class representing an agent that can perform tasks."""
    
    def __init__(self, name):
        self.name = name  # Name of the agent
        self.tasks = []  # List of tasks assigned to the agent

    def assign_task(self, task):
        """Assign a task to the agent."""
        self.tasks.append(task)

    def complete_task(self, task):
        """Complete a task assigned to the agent."""
        if task in self.tasks:
            task.complete_task()
            self.tasks.remove(task)

class TaskScheduler:
    """Class to manage the scheduling and execution of tasks among agents."""
    
    def __init__(self):
        self.tasks = []  # List of all tasks
        self.agents = []  # List of all agents

    def add_task(self, task):
        """Add a new task to the scheduler."""
        self.tasks.append(task)

    def add_agent(self, agent):
        """Add a new agent to the scheduler."""
        self.agents.append(agent)

    def assign_tasks(self):
        """Assign tasks to agents based on priority and availability."""def assign_tasks(self):
        """Assign tasks to agents based on urgency and availability."""
        # Sort tasks by urgency and priority
        sorted_tasks = sorted(self.tasks, key=lambda x: (x.priority, x.status == 'Pending'), reverse=True)
        for task in sorted_tasks:
            for agent in self.agents:
                if len(agent.tasks) < 3 and task.status == 'Pending':  # Check agent capacity and task status
                    task.assign_agent(agent)
                    break
        # Reassign tasks if agents become available or tasks are overdue
        for agent in self.agents:
            if len(agent.tasks) < 3:
                for task in sorted_tasks:
                    if task.status == 'Pending' and task.priority > 1:  # Example condition for urgency
                        task.assign_agent(agent)
                        break    def get_task_status(self):
        """Get the status of all tasks."""
        return {task.name: task.status for task in self.tasks}

    def log_history(self):
        """Log the history of all tasks."""
        history = []
        for task in self.tasks:
            history.append({
                'name': task.name,
                'status': task.status,
                'start_time': task.start_time,
                'end_time': task.end_time,
                'notes': task.notes
            })
        return history

# Example usage
if __name__ == "__main__":
    # Create a task scheduler
    scheduler = TaskScheduler()

    # Create agents
    agent1 = Agent("Agent A")
    agent2 = Agent("Agent B")

    # Add agents to the scheduler
    scheduler.add_agent(agent1)
    scheduler.add_agent(agent2)

    # Create tasks
    task1 = Task("Task 1", "Description of Task 1", 1, ["Resource 1"])
    task2 = Task("Task 2", "Description of Task 2", 2, ["Resource 2"])
    task3 = Task("Task 3", "Description of Task 3", 3, ["Resource 3"])

    # Add tasks to the scheduler
    scheduler.add_task(task1)
    scheduler.add_task(task2)
    scheduler.add_task(task3)

    # Assign tasks to agents
    scheduler.assign_tasks()

    # Print task status
    print(scheduler.get_task_status())

    # Complete a task
    agent1.complete_task(task1)

    # Print task history
    print(scheduler.log_history())