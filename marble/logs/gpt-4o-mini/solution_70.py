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

    def report_progress(self, task, result):
        """Report the progress of a task."""
        if task in self.tasks:
            self.progress[task] = result  # Update task progress
        else:
            raise ValueError("Task not assigned to this agent.")

    def get_status(self):
        """Return the current status of the agent's tasks."""
        return {self.name: self.progress}


class ScienceCollaboratory:
    """
    A class representing the Science Collaboratory system that manages multiple AI agents.
    It facilitates collaborative scientific research by dynamically allocating tasks and collecting feedback.
    """
    def __init__(self):
        self.agents = []  # List of AI agents
        self.tasks = []  # List of tasks to be assigned

    def add_agent(self, agent):
        """Add an AI agent to the collaboratory."""
        self.agents.append(agent)

    def add_task(self, task):
        """Add a task to the collaboratory."""
        self.tasks.append(task)

    def allocate_tasks(self):
        """Dynamically allocate tasks to agents based on their specialization."""def allocate_tasks(self):
        """Dynamically allocate tasks to agents based on their strengths and performance."""
        for task in self.tasks:
            best_agent = self.evaluate_agents_for_task(task)
            if best_agent:
                best_agent.assign_task(task)

    def evaluate_agents_for_task(self, task):
        """Evaluate agents based on their past performance and current workload for task allocation."""
        suitable_agents = []
        for agent in self.agents:
            if agent.specialization in task:
                performance_score = self.calculate_performance(agent)
                workload = len(agent.tasks)
                suitable_agents.append((agent, performance_score, workload))
        # Sort agents by performance score and workload
        suitable_agents.sort(key=lambda x: (x[1], -x[2]), reverse=True)
        return suitable_agents[0][0] if suitable_agents else None

    def calculate_performance(self, agent):
        """Calculate the performance score of an agent based on their completed tasks."""
        completed_tasks = sum(1 for result in agent.progress.values() if result == 'Completed')
        return completed_tasks    def find_best_agent(self, task):
        """Find the best agent for a given task based on specialization."""
        for agent in self.agents:
            if agent.specialization in task:  # Simple matching logic
                return agent
        return None

    def collect_feedback(self):
        """Collect feedback from all agents and adjust tasks accordingly."""
        for agent in self.agents:
            status = agent.get_status()
            print(status)  # Print the status for monitoring

    def run(self):
        """Run the collaboratory process."""
        self.allocate_tasks()  # Allocate tasks to agents
        self.collect_feedback()  # Collect feedback from agents


# Example usage
if __name__ == "__main__":
    # Create the collaboratory
    collaboratory = ScienceCollaboratory()

    # Create AI agents with different specializations
    agent1 = AIAgent("Agent A", "data analysis")
    agent2 = AIAgent("Agent B", "simulation")
    agent3 = AIAgent("Agent C", "hypothesis generation")

    # Add agents to the collaboratory
    collaboratory.add_agent(agent1)
    collaboratory.add_agent(agent2)
    collaboratory.add_agent(agent3)

    # Add tasks to the collaboratory
    collaboratory.add_task("Analyze data from experiment 1")
    collaboratory.add_task("Simulate experiment 2")
    collaboratory.add_task("Generate hypothesis for experiment 3")

    # Run the collaboratory process
    collaboratory.run()