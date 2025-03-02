# solution.py
from datetime import datetime
from enum import Enum
import networkx as nx
import matplotlib.pyplot as plt

# Define the status of a task
class TaskStatus(Enum):
    NOT_STARTED = 1
    IN_PROGRESS = 2
    COMPLETED = 3

# Define a class for tasks
class Task:
    def __init__(self, name, description, start_time=None, end_time=None, status=TaskStatus.NOT_STARTED):
        """
        Initialize a task.

        Args:
        name (str): The name of the task.
        description (str): The description of the task.
        start_time (datetime): The start time of the task.
        end_time (datetime): The end time of the task.
        status (TaskStatus): The status of the task.
        """
        self.name = name
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.dependencies = []
        self.comments = []

    def add_dependency(self, task):
        """
        Add a dependency to the task.

        Args:
        task (Task): The task that this task depends on.
        """
        self.dependencies.append(task)

    def add_comment(self, comment):
        """
        Add a comment to the task.

        Args:
        comment (str): The comment to add.
        """
        self.comments.append(comment)

    def update_status(self, status):
        """
        Update the status of the task.

        Args:
        status (TaskStatus): The new status of the task.
        """
        self.status = status

# Define a class for the task chain
class TaskChain:
    def __init__(self):
        """
        Initialize the task chain.
        """
        self.tasks = []
        self.graph = nx.DiGraph()

    def add_task(self, task):
        """
        Add a task to the task chain.

        Args:
        task (Task): The task to add.
        """
        self.tasks.append(task)
        self.graph.add_node(task.name)

    def add_dependency(self, task1, task2):
        """
        Add a dependency between two tasks.

        Args:
        task1 (Task): The task that depends on task2.
        task2 (Task): The task that task1 depends on.
        """
        task1.add_dependency(task2)
        self.graph.add_edge(task2.name, task1.name)

    def visualize_dependencies(self):
        """
        Visualize the task dependencies using a directed graph.
        """
        nx.draw(self.graph, with_labels=True)
        plt.show()

    def track_progress(self):
        """
        Track the progress of each task.
        """
        for task in self.tasks:
            print(f"Task: {task.name}, Status: {task.status.name}")

    def send_notifications(self):
        """
        Send notifications to users when a task is completed or when a task is about to start.
        """
        for task in self.tasks:
            if task.status == TaskStatus.COMPLETED:
                print(f"Task {task.name} is completed.")
            elif task.status == TaskStatus.IN_PROGRESS:
                print(f"Task {task.name} is in progress.")
            else:
                print(f"Task {task.name} is not started.")

    def generate_report(self):
        """
        Generate a report that summarizes the project's progress.
        """
        completed_tasks = [task for task in self.tasks if task.status == TaskStatus.COMPLETED]
        ongoing_tasks = [task for task in self.tasks if task.status == TaskStatus.IN_PROGRESS]
        delayed_tasks = [task for task in self.tasks if task.status == TaskStatus.NOT_STARTED]

        print("Completed Tasks:")
        for task in completed_tasks:
            print(task.name)

        print("Ongoing Tasks:")
        for task in ongoing_tasks:
            print(task.name)

        print("Delayed Tasks:")
        for task in delayed_tasks:
            print(task.name)

# Example usage
task_chain = TaskChain()

task1 = Task("Task 1", "This is task 1")
task2 = Task("Task 2", "This is task 2")
task3 = Task("Task 3", "This is task 3")

task_chain.add_task(task1)
task_chain.add_task(task2)
task_chain.add_task(task3)

task_chain.add_dependency(task2, task1)
task_chain.add_dependency(task3, task2)

task_chain.visualize_dependencies()

task1.update_status(TaskStatus.COMPLETED)
task_chain.track_progress()

task_chain.send_notifications()

task_chain.generate_report()