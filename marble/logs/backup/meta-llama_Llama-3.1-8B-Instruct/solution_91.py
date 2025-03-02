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
        task.assigned_agent = self
        print(f"Task {task.name} assigned to agent {self.name}")

    def update_task_status(self, task, status):
        task.status = status
        print(f"Task {task.name} status updated to {status.name}")

    def become_unavailable(self):
        self.available = False
        print(f"Agent {self.name} became unavailable")

    def become_available(self):
        self.available = True
        print(f"Agent {self.name} became available")

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

    def start_execution(self):
        self.status = TaskStatus.IN_PROGRESS
        self.start_time = datetime.datetime.now()
        print(f"Task {self.name} started execution")

    def complete_execution(self):
        self.status = TaskStatus.COMPLETED
        self.end_time = datetime.datetime.now()
        print(f"Task {self.name} completed execution")

    def fail_execution(self):
        self.status = TaskStatus.FAILED
        print(f"Task {self.name} failed execution")

    def update_notes(self, notes):
        self.notes = notes
        print(f"Task {self.name} notes updated")

# MultiAgentTaskScheduler class
class MultiAgentTaskScheduler:
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

    def assign_task_to_agent(self, task, agent):
        if task.status == TaskStatus.PENDING and agent.available:
            agent.assign_task(task)
            task.start_execution()
        else:
            print("Task cannot be assigned to agent")

    def update_task_status(self, task, status):
        if task.status != TaskStatus.PENDING:
            task.assigned_agent.update_task_status(task, status)
        else:
            print("Task status cannot be updated")

    def reassign_task(self, task):
        for agent in self.agents:
            if agent.available:
                agent.assign_task(task)
                task.start_execution()
                break
        else:
            print("No available agent to reassign task")

    def update_agent_availability(self, agent, available):
        if available:
            agent.become_available()
        else:
            agent.become_unavailable()

    def get_task_status(self, task):
        return task.status

    def get_agent_status(self, agent):
        return agent.available

    def log_task_history(self, task):
        self.history_log.append({
            "task_name": task.name,
            "start_time": task.start_time,
            "end_time": task.end_time,
            "assigned_agent": task.assigned_agent.name,
            "notes": task.notes
        })

    def start_scheduler(self):
        while True:
            for task in self.tasks:
                if task.status == TaskStatus.PENDING and task.assigned_agent.available:
                    task.start_execution()
                    task.assigned_agent.assign_task(task)
                elif task.status == TaskStatus.IN_PROGRESS:
                    if task.end_time is not None:
                        task.complete_execution()
                    else:
                        task.assigned_agent.update_task_status(task, TaskStatus.FAILED)
                elif task.status == TaskStatus.FAILED:
                    task.assigned_agent.update_task_status(task, TaskStatus.PENDING)
            time.sleep(1)

# Create agents
agent1 = Agent("Agent1")
agent2 = Agent("Agent2")

# Create tasks
task1 = Task("Task1", "Task description 1", 1, ["Resource1", "Resource2"])
task2 = Task("Task2", "Task description 2", 2, ["Resource3", "Resource4"])

# Create task scheduler
scheduler = MultiAgentTaskScheduler()

# Add agents and tasks to scheduler
scheduler.add_agent(agent1)
scheduler.add_agent(agent2)
scheduler.add_task(task1)
scheduler.add_task(task2)

# Assign tasks to agents
scheduler.assign_task_to_agent(task1, agent1)
scheduler.assign_task_to_agent(task2, agent2)

# Start scheduler
threading.Thread(target=scheduler.start_scheduler).start()

# Simulate task completion
time.sleep(5)
task1.complete_execution()
task2.complete_execution()

# Log task history
scheduler.log_task_history(task1)
scheduler.log_task_history(task2)

# Print task history
for task in scheduler.history_log:
    print(task)