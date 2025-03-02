# solution.py

class AIAgent:
    """
    A class representing an AI agent with specialized capabilities.
    Each agent can perform tasks based on its specialization and report progress.
    """
    def __init__(self, name, specialization):
        self.name = name  # Name of the agent
        self.specialization = specialization  # Area of expertise
        self.tasks = []  # List of tasks assigned to the agent
        self.progress = {}  # Dictionary to track progress of tasks

    def assign_task(self, task):
        """Assign a task to the agent."""
        self.tasks.append(task)
        self.progress[task] = "In Progress"  # Initialize task progress

    def report_progress(self):
        """Report the progress of assigned tasks."""
        return {task: self.progress[task] for task in self.tasks}

    def complete_task(self, task):
        """Mark a task as completed."""
        if task in self.tasks:
            self.progress[task] = "Completed"

class Task:
    """
    A class representing a scientific task that needs to be performed.
    Each task has a description and a required specialization.
    """
    def __init__(self, description, required_specialization):
        self.description = description  # Description of the task
        self.required_specialization = required_specialization  # Required expertise

class ScienceCollaboratory:
    """
    A class representing the Science Collaboratory system.
    It manages AI agents, task allocation, and feedback mechanisms.
    """
    def __init__(self):
        self.agents = []  # List of AI agents
        self.tasks = []  # List of tasks to be performed

    def add_agent(self, agent):
        """Add an AI agent to the collaboratory."""
        self.agents.append(agent)

    def add_task(self, task):
        """Add a task to the collaboratory."""
        self.tasks.append(task)

    def allocate_tasks(self):
        """Allocate tasks to agents based on their specialization."""def allocate_tasks(self):
        """Allocate tasks to agents based on their specialization and current workload."""
        for task in self.tasks:
            suitable_agents = [agent for agent in self.agents if agent.specialization == task.required_specialization]
            if suitable_agents:
                # Sort agents by the number of tasks they have
                suitable_agents.sort(key=lambda x: len(x.tasks))
                # Assign task to the agent with the least workload
                suitable_agents[0].assign_task(task.description)
                
                # Check if any agent is overloaded and redistribute tasks if necessary
                self.reassign_tasks()

    def reassign_tasks(self):
        """Reassign tasks if any agent is overloaded."""
        task_threshold = 3  # Example threshold for maximum tasks
        for agent in self.agents:
            if len(agent.tasks) > task_threshold:
                # Logic to redistribute tasks from overloaded agent
                # This is a placeholder for the actual redistribution logic
                pass    def collect_feedback(self):
        """Collect feedback from agents about their progress."""
        feedback = {}
        for agent in self.agents:
            feedback[agent.name] = agent.report_progress()
        return feedback

    def display_progress(self):
        """Display the progress of all agents."""
        for agent in self.agents:
            print(f"Agent: {agent.name}, Progress: {agent.report_progress()}")

# Example usage
if __name__ == "__main__":
    # Create agents with different specializations
    agent1 = AIAgent("Agent A", "Data Analysis")
    agent2 = AIAgent("Agent B", "Simulation")
    agent3 = AIAgent("Agent C", "Hypothesis Generation")

    # Create a collaboratory and add agents
    collaboratory = ScienceCollaboratory()
    collaboratory.add_agent(agent1)
    collaboratory.add_agent(agent2)
    collaboratory.add_agent(agent3)

    # Create tasks and add them to the collaboratory
    task1 = Task("Analyze dataset A", "Data Analysis")
    task2 = Task("Simulate experiment B", "Simulation")
    task3 = Task("Generate hypothesis C", "Hypothesis Generation")
    collaboratory.add_task(task1)
    collaboratory.add_task(task2)
    collaboratory.add_task(task3)

    # Allocate tasks to agents
    collaboratory.allocate_tasks()

    # Display progress of agents
    collaboratory.display_progress()

    # Simulate task completion
    agent1.complete_task("Analyze dataset A")
    agent2.complete_task("Simulate experiment B")

    # Display updated progress
    print("\nUpdated Progress:")
    collaboratory.display_progress()

    # Collect feedback from agents
    feedback = collaboratory.collect_feedback()
    print("\nFeedback from Agents:")
    print(feedback)