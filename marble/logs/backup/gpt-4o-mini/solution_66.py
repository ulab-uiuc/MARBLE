# solution.py

from datetime import datetime, timedelta
from collections import defaultdict
import json

class Task:
    """Class representing a single task in the TaskChain system."""
    
    def __init__(self, name, dependencies=None):
        self.name = name  # Name of the task
        self.dependencies = dependencies if dependencies else []  # List of task names that this task depends on
        self.start_time = None  # Start time of the task
        self.end_time = None  # End time of the task
        self.status = 'not started'  # Current status of the task
        self.comments = []  # List of comments for the task

    def start(self):
        """Start the task and set the start time."""
        self.start_time = datetime.now()
        self.status = 'in progress'

    def complete(self):
        """Complete the task and set the end time."""
        self.end_time = datetime.now()
        self.status = 'completed'

    def add_comment(self, comment):
        """Add a comment to the task."""
        self.comments.append(comment)

    def to_dict(self):
        """Convert the task to a dictionary for easy serialization."""
        return {
            'name': self.name,
            'dependencies': self.dependencies,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'status': self.status,
            'comments': self.comments
        }

class TaskChain:
    """Class representing the TaskChain project management system."""
    
    def __init__(self):
        self.tasks = {}  # Dictionary to hold tasks by name
        self.notifications = []  # List to hold notifications

    def add_task(self, name, dependencies=None):
        """Add a new task to the system."""
        if name in self.tasks:
            raise ValueError(f"Task '{name}' already exists.")
        self.tasks[name] = Task(name, dependencies)

    def start_task(self, name):
        """Start a task and notify users if it has dependencies."""
        task = self.tasks.get(name)
        if not task:
            raise ValueError(f"Task '{name}' does not exist.")
        
        # Check if dependencies are completed
        for dep in task.dependencies:
            if self.tasks[dep].status != 'completed':
                raise ValueError(f"Cannot start task '{name}' because dependency '{dep}' is not completed.")
        
        task.start()
        self.notifications.append(f"Task '{name}' has started.")

    def complete_task(self, name):
        """Complete a task and notify users."""
        task = self.tasks.get(name)
        if not task:
            raise ValueError(f"Task '{name}' does not exist.")
        
        task.complete()
        self.notifications.append(f"Task '{name}' has been completed.")

    def add_comment_to_task(self, task_name, comment):
        """Add a comment to a specific task."""
        task = self.tasks.get(task_name)
        if not task:
            raise ValueError(f"Task '{task_name}' does not exist.")
        
        task.add_comment(comment)

    def generate_report(self):
        """Generate a report of the project's progress."""
        report = {
            'completed_tasks': [],
            'ongoing_tasks': [],
            'not_started_tasks': [],
            'delayed_tasks': []
        }def visualize_dependencies(self):
        """Visualize task dependencies using Matplotlib or Graphviz."""
        import matplotlib.pyplot as plt
        import networkx as nx

        G = nx.DiGraph()
        for task in self.tasks.values():
            G.add_node(task.name)
            for dep in task.dependencies:
                G.add_edge(dep, task.name)

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, arrows=True)
        plt.title('Task Dependencies')
        plt.show()    def save_to_file(self, filename):
        """Save the current state of tasks to a JSON file."""
        with open(filename, 'w') as f:
            json.dump({name: task.to_dict() for name, task in self.tasks.items()}, f, indent=4)

# Example usage
if __name__ == "__main__":
    task_chain = TaskChain()
    task_chain.add_task("Task A")
    task_chain.add_task("Task B", dependencies=["Task A"])
    task_chain.start_task("Task A")
    task_chain.complete_task("Task A")
    task_chain.start_task("Task B")
    task_chain.complete_task("Task B")
    task_chain.add_comment_to_task("Task A", "Started working on this task.")
    task_chain.add_comment_to_task("Task B", "Completed this task successfully.")
    
    report = task_chain.generate_report()
    print(json.dumps(report, indent=4))
    task_chain.visualize_dependencies()
    task_chain.save_to_file("tasks.json")