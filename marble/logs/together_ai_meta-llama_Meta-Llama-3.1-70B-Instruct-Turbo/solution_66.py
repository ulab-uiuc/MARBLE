# task_chain.py

import datetime
import networkx as nx
import matplotlib.pyplot as plt
from enum import Enum

# Define an Enum for task status
class TaskStatus(Enum):
    NOT_STARTED = 1
    IN_PROGRESS = 2
    COMPLETED = 3

# Define a class for tasks
class Task:
    def __init__(self, name, description, start_time=None, end_time=None, status=TaskStatus.NOT_STARTED):
        self.name = name
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.dependencies = []
        self.comments = []

    def add_dependency(self, task):
        self.dependencies.append(task)

    def add_comment(self, comment):
        self.comments.append(comment)

    def update_status(self, status):
        self.status = status

    def __str__(self):
        return f'Task: {self.name}, Status: {self.status.name}'

# Define a class for TaskChain
class TaskChain:
    def __init__(self):
        self.tasks = []
        self.graph = nx.DiGraph()

    def add_task(self, task):
        self.tasks.append(task)
        self.graph.add_node(task.name)

    def add_dependency(self, task1, task2):def add_dependency(self, task1, task2):
        if task2.status == TaskStatus.COMPLETED:
            raise ValueError("Cannot add a completed task as a dependency")
        if task1 in task2.dependencies:
            raise ValueError("Circular dependency detected")
        task1.add_dependency(task2)
        self.graph.add_edge(task1.name, task2.name)
    def visualize_dependencies(self):
        nx.draw(self.graph, with_labels=True)
        plt.show()

    def track_progress(self):
        for task in self.tasks:
            print(task)
            if task.status == TaskStatus.COMPLETED:
                print('Task completed')
            elif task.status == TaskStatus.IN_PROGRESS:
                print('Task in progress')
            else:
                print('Task not started')

    def send_notifications(self):
        for task in self.tasks:
            if task.status == TaskStatus.COMPLETED:
                print(f'Task {task.name} completed')
            elif task.status == TaskStatus.IN_PROGRESS:
                print(f'Task {task.name} in progress')
            else:
                print(f'Task {task.name} not started')

    def generate_report(self):
        completed_tasks = [task for task in self.tasks if task.status == TaskStatus.COMPLETED]
        ongoing_tasks = [task for task in self.tasks if task.status == TaskStatus.IN_PROGRESS]
        delayed_tasks = [task for task in self.tasks if task.status == TaskStatus.NOT_STARTED]

        print('Completed Tasks:')
        for task in completed_tasks:
            print(task)

        print('Ongoing Tasks:')
        for task in ongoing_tasks:
            print(task)

        print('Delayed Tasks:')
        for task in delayed_tasks:
            print(task)

# Define a class for User
class User:
    def __init__(self, name):
        self.name = name

    def update_task_status(self, task, status):
        task.update_status(status)

    def add_comment(self, task, comment):
        task.add_comment(comment)

# Main function
def main():
    task_chain = TaskChain()

    task1 = Task('Task 1', 'This is task 1')
    task2 = Task('Task 2', 'This is task 2')
    task3 = Task('Task 3', 'This is task 3')

    task_chain.add_task(task1)
    task_chain.add_task(task2)
    task_chain.add_task(task3)

    task_chain.add_dependency(task1, task2)
    task_chain.add_dependency(task2, task3)

    task_chain.visualize_dependencies()

    user1 = User('User 1')
    user1.update_task_status(task1, TaskStatus.IN_PROGRESS)
    user1.add_comment(task1, 'This is a comment')

    task_chain.track_progress()

    task_chain.send_notifications()

    task_chain.generate_report()

if __name__ == '__main__':
    main()