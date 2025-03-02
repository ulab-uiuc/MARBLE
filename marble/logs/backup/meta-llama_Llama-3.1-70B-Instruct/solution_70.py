
        if task_type not in self.agents[agent_name].capabilities:
            print("Agent does not have the capability to perform the task.")
            return# science_collaboratory.py

import threading
from abc import ABC, abstractmethod
from typing import Dict, List
import tkinter as tk
from tkinter import ttk

# Agent Class
class Agent(ABC):
    """Abstract base class for AI agents."""
    
    def __init__(self, name: str, capabilities: List[str]):
        """
        Initialize an agent with a name and a list of capabilities.
        
        Args:
        name (str): The name of the agent.
        capabilities (List[str]): A list of capabilities the agent possesses.
        """
        self.name = name
        self.capabilities = capabilities
        self.tasks = []

    @abstractmethod
    def perform_task(self, task: str):
        """Perform a task assigned to the agent."""
        pass

    def report_progress(self, task: str, progress: str):
        """Report progress on a task."""
        print(f"{self.name} is working on {task}: {progress}")


# Data Analysis Agent
class DataAnalysisAgent(Agent):
    """Agent specialized in data analysis."""
    
    def __init__(self, name: str):
        super().__init__(name, ["data_analysis"])

    def perform_task(self, task: str):
        """Perform a data analysis task."""
        print(f"{self.name} is performing data analysis on {task}")


# Simulation Agent
class SimulationAgent(Agent):
    """Agent specialized in simulation."""
    
    def __init__(self, name: str):
        super().__init__(name, ["simulation"])

    def perform_task(self, task: str):
        """Perform a simulation task."""
        print(f"{self.name} is simulating {task}")


# Hypothesis Generation Agent
class HypothesisGenerationAgent(Agent):
    """Agent specialized in hypothesis generation."""
    
    def __init__(self, name: str):
        super().__init__(name, ["hypothesis_generation"])

    def perform_task(self, task: str):
        """Perform a hypothesis generation task."""
        print(f"{self.name} is generating hypotheses for {task}")


# Science Collaboratory Class
class ScienceCollaboratory:
    """A multi-agent system for collaborative scientific research."""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.tasks: Dict[str, str] = {}

    def add_agent(self, agent: Agent):
        """Add an agent to the collaboratory."""
        self.agents[agent.name] = agent

    def assign_task(self, task: str, agent_name: str):
        """Assign a task to an agent."""
        if agent_name in self.agents:
            self.tasks[task] = agent_name
            self.agents[agent_name].tasks.append(task)
        else:
            print("Agent not found.")

    def reassign_task(self, task: str, new_agent_name: str):
        """Reassign a task to a different agent."""
        if task in self.tasks:
            old_agent_name = self.tasks[task]
            self.agents[old_agent_name].tasks.remove(task)
            self.tasks[task] = new_agent_name
            self.agents[new_agent_name].tasks.append(task)
        else:
            print("Task not found.")

    def get_task_status(self, task: str):
        """Get the status of a task."""
        if task in self.tasks:
            agent_name = self.tasks[task]
            return self.agents[agent_name].tasks
        else:
            print("Task not found.")

    def start_collaboration(self):
        """Start the collaboration process."""
        for task, agent_name in self.tasks.items():
            agent = self.agents[agent_name]
            agent.perform_task(task)


# User Interface Class
class UserInterface:
    """A user-friendly interface for human researchers."""
    
    def __init__(self, collaboratory: ScienceCollaboratory):
        self.collaboratory = collaboratory
        self.root = tk.Tk()
        self.root.title("Science Collaboratory")

        # Create tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        self.agent_tab = ttk.Frame(self.notebook)
        self.task_tab = ttk.Frame(self.notebook)
        self.status_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.agent_tab, text="Agents")
        self.notebook.add(self.task_tab, text="Tasks")
        self.notebook.add(self.status_tab, text="Status")

        # Agent tab
        self.agent_label = ttk.Label(self.agent_tab, text="Agents:")
        self.agent_label.pack()

        self.agent_listbox = tk.Listbox(self.agent_tab)
        self.agent_listbox.pack()

        self.add_agent_button = ttk.Button(self.agent_tab, text="Add Agent", command=self.add_agent)
        self.add_agent_button.pack()

        # Task tabdef assign_task(self):
        task_type = input("Enter task type (data analysis, simulation, hypothesis generation): ")task = "Task " + str(len(self.collaboratory.tasks) + 1)self.collaboratory.assign_task(task, task_type, agent_name)self.task_listbox.insert(tk.END, task)

    def start_collaboration(self):
        # Start the collaboration process
        self.collaboratory.start_collaboration()

    def run(self):
        # Run the user interface
        self.root.mainloop()


# Main function
def main():
    collaboratory = ScienceCollaboratory()
    interface = UserInterface(collaboratory)
    interface.run()


if __name__ == "__main__":
    main()