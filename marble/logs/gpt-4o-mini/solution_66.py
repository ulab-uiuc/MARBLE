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

    def add_comment(self, comment):
        """Add a comment to the task."""
        self.comments.append(comment)

    def start(self):
        """Start the task and set the start time."""
        self.start_time = datetime.now()
        self.status = 'in progress'

    def complete(self):
        """Complete the task and set the end time."""
        self.end_time = datetime.now()
        self.status = 'completed'

    def is_ready(self):
        """Check if the task is ready to start based on its dependencies."""
        return all(dep.status == 'completed' for dep in self.dependencies)

class TaskChain:
    """Class representing the TaskChain project management system."""
    
    def __init__(self):
        self.tasks = {}  # Dictionary to hold tasks by name

    def add_task(self, name, dependencies=None):
        """Add a new task to the system."""
        dependencies = [self.tasks[dep] for dep in dependencies] if dependencies else []
        task = Task(name, dependencies)
        self.tasks[name] = task

    def start_task(self, name):
        """Start a task if its dependencies are completed."""
        task = self.tasks.get(name)
        if task and task.is_ready():
            task.start()
            self.notify_users(f'Task "{name}" has started.')
        else:
            print(f'Task "{name}" cannot be started. Dependencies not met.')

    def complete_task(self, name):
        """Complete a task and notify users."""
        task = self.tasks.get(name)
        if task:
            task.complete()
            self.notify_users(f'Task "{name}" has been completed.')
            self.check_dependencies(task)

    def check_dependencies(self, completed_task):
        """Check and start tasks that depend on the completed task."""
        for task in self.tasks.values():
            if completed_task in task.dependencies and task.is_ready():
                self.start_task(task.name)

    def notify_users(self, message):
        """Simulate sending a notification to users."""
        print(f'Notification: {message}')

    def generate_report(self):
        """Generate a report of the current project status."""
        report = {
            'completed_tasks': [],
            'ongoing_tasks': [],
            'not_started_tasks': [],
            'delayed_tasks': []
        }
        for task in self.tasks.values():
            if task.status == 'completed':
                report['completed_tasks'].append(task.name)
            elif task.status == 'in progress':
                report['ongoing_tasks'].append(task.name)
            elif task.status == 'not started':
                report['not_started_tasks'].append(task.name)
        
        # Here we could add logic to determine if any tasks are delayed
        # For simplicity, we will not implement that logic in this example

        return json.dumps(report, indent=4)

# Example usage
if __name__ == "__main__":
    task_chain = TaskChain()
    
    # Adding tasks with dependencies
    task_chain.add_task('Task A')
    task_chain.add_task('Task B', dependencies=['Task A'])
    task_chain.add_task('Task C', dependencies=['Task A'])
    
    # Starting and completing tasks
    task_chain.start_task('Task A')
    task_chain.complete_task('Task A')
    
    task_chain.start_task('Task B')
    task_chain.complete_task('Task B')
    
    task_chain.start_task('Task C')
    task_chain.complete_task('Task C')
    
    # Generating report
    print(task_chain.generate_report())