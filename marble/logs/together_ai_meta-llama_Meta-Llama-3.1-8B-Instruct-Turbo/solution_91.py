# solution.py

# Importing required libraries
import datetime
import threading
import time
from enum import Enum
from typing import Dict, List

# Enum for task status
class TaskStatus(Enum):
    PENDING = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    FAILED = 4

# Agent class
class Agent:
    def __init__(self, name: str):
        self.name = name
        self.available = True
        self.tasks = []

    def assign_task(self, task):
        self.tasks.append(task)
        print(f"Task {task.name} assigned to agent {self.name}")

    def update_task_status(self, task, status):
        for t in self.tasks:
            if t.name == task.name:
                t.status = status
                print(f"Task {task.name} status updated to {status.name}")

    def is_available(self):
        return self.available

# Task class
class Task:
    def __init__(self, name: str, description: str, priority: int, required_resources: List[str]):
        self.name = name
        self.description = description
        self.priority = priority
        self.required_resources = required_resources
        self.status = TaskStatus.PENDING
        self.assigned_agent = None
        self.start_time = None
        self.end_time = None
        self.notes = ""

    def assign_agent(self, agent):
        self.assigned_agent = agent
        agent.assign_task(self)

    def update_status(self, status):
        self.status = status
        if status == TaskStatus.COMPLETED:
            self.end_time = datetime.datetime.now()
        print(f"Task {self.name} status updated to {status.name}")

    def add_note(self, note):
        self.notes += note + "\n"

# TaskScheduler class
class TaskScheduler:
    def __init__(self):
        self.tasks = []
        self.agents = []
        self.history_log = []

    def add_task(self, task):
        self.tasks.append(task)
        print(f"Task {task.name} added")

    def add_agent(self, agent):
        self.agents.append(agent)
        print(f"Agent {agent.name} added")

    def assign_task(self, task, agent):
        task.assign_agent(agent)
        print(f"Task {task.name} assigned to agent {agent.name}")

    def update_task_status(self, task, status):
        task.update_status(status)
        print(f"Task {task.name} status updated to {status.name}")

    def get_task_status(self, task):
        return task.status

    def get_agent_status(self, agent):
        for task in agent.tasks:
            print(f"Task {task.name} status: {task.status.name}")

    def start_task(self, task):
        task.start_time = datetime.datetime.now()
        print(f"Task {task.name} started")

    def end_task(self, task):
        task.end_time = datetime.datetime.now()
        print(f"Task {task.name} ended")

    def add_note(self, task, note):
        task.add_note(note)
        print(f"Note added to task {task.name}")

    def log_task_history(self, task):
        self.history_log.append({
            "task_name": task.name,
            "start_time": task.start_time,
            "end_time": task.end_time,
            "assigned_agent": task.assigned_agent.name,
            "notes": task.notes
        })
        print(f"Task history logged for task {task.name}")

# Main function
def main():
    scheduler = TaskScheduler()

    # Create agents
    agent1 = Agent("Agent 1")
    agent2 = Agent("Agent 2")
    scheduler.add_agent(agent1)
    scheduler.add_agent(agent2)

    # Create tasks
    task1 = Task("Task 1", "This is task 1", 1, ["Resource 1", "Resource 2"])
    task2 = Task("Task 2", "This is task 2", 2, ["Resource 3", "Resource 4"])
    scheduler.add_task(task1)
    scheduler.add_task(task2)

    # Assign tasks to agents
    scheduler.assign_task(task1, agent1)
    scheduler.assign_task(task2, agent2)

    # Start tasks
    scheduler.start_task(task1)
    scheduler.start_task(task2)

    # Update task status
    scheduler.update_task_status(task1, TaskStatus.IN_PROGRESS)
    scheduler.update_task_status(task2, TaskStatus.IN_PROGRESS)

    # Add notes to tasks
    scheduler.add_note(task1, "Note 1")
    scheduler.add_note(task2, "Note 2")

    # End tasks
    scheduler.end_task(task1)
    scheduler.end_task(task2)

    # Log task history
    scheduler.log_task_history(task1)
    scheduler.log_task_history(task2)

    # Print task status
    print("Task 1 status:", scheduler.get_task_status(task1))
    print("Task 2 status:", scheduler.get_task_status(task2))

    # Print agent status
    scheduler.get_agent_status(agent1)
    scheduler.get_agent_status(agent2)

# Run the main function
if __name__ == "__main__":
    main()