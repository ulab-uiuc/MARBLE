# solution.py

# Importing necessary modules
import datetime
import calendar
from dataclasses import dataclass
from enum import Enum
from typing import List

# Enum for priority levels
class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

# Dataclass for Task
@dataclass
class Task:
    id: int
    description: str
    due_date: datetime.date
    priority: Priority
    assigned_members: List[str]

# Dataclass for Resource
@dataclass
class Resource:
    id: int
    name: str
    type: str
    allocated_tasks: List[Task]

# Dataclass for Project
@dataclass
class Project:
    id: int
    name: str
    tasks: List[Task]
    resources: List[Resource]

# Task Creation and Management Module
class TaskManager:
    def __init__(self):
        self.tasks = []

    def create_task(self, description: str, due_date: datetime.date, priority: Priority, assigned_members: List[str]):
        task = Task(len(self.tasks) + 1, description, due_date, priority, assigned_members)
        self.tasks.append(task)
        return task

    def edit_task(self, task_id: int, description: str = None, due_date: datetime.date = None, priority: Priority = None, assigned_members: List[str] = None):
        for task in self.tasks:
            if task.id == task_id:
                if description:
                    task.description = description
                if due_date:
                    task.due_date = due_date
                if priority:
                    task.priority = priority
                if assigned_members:
                    task.assigned_members = assigned_members
                return task
        return None

    def delete_task(self, task_id: int):
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                return True
        return False

# Task Scheduling Module
class TaskScheduler:
    def __init__(self, task_manager: TaskManager):
        self.task_manager = task_manager
        self.tasks = task_manager.tasks

    def schedule_tasks(self):
        # Sort tasks by due date and priority
        self.tasks.sort(key=lambda task: (task.due_date, task.priority.value))

        # Assign tasks to team members
        for task in self.tasks:
            task.assigned_members.sort()

        return self.tasks

# Resource Allocation Module
class ResourceAllocator:
    def __init__(self, task_scheduler: TaskScheduler):
        self.task_scheduler = task_scheduler
        self.resources = []
        self.tasks = task_scheduler.tasks

    def allocate_resources(self):
        # Create resources
        for task in self.tasks:
            resource = Resource(len(self.resources) + 1, task.description, task.priority.name, [task])
            self.resources.append(resource)

        # Allocate resources to tasks
        for resource in self.resources:
            for task in self.tasks:
                if task in resource.allocated_tasks:
                    continue
                if resource.type == task.priority.name:
                    resource.allocated_tasks.append(task)

        return self.resources

# Real-Time Updates and Notifications Module
class NotificationSystem:
    def __init__(self, resource_allocator: ResourceAllocator):
        self.resource_allocator = resource_allocator
        self.resources = resource_allocator.resources

    def send_notifications(self):
        # Send notifications for completed tasks
        for resource in self.resources:
            for task in resource.allocated_tasks:
                if task.due_date < datetime.date.today():
                    print(f"Task {task.id} completed!")

        # Send notifications for over-allocated resources
        for resource in self.resources:
            if len(resource.allocated_tasks) > 1:
                print(f"Resource {resource.id} is over-allocated!")

        # Send notifications for approaching due dates
        for task in self.tasks:
            if task.due_date - datetime.date.today() <= datetime.timedelta(days=7):
                print(f"Task {task.id} is approaching its due date!")

# User Interface Module
class ProjectManager:
    def __init__(self):
        self.task_manager = TaskManager()
        self.task_scheduler = TaskScheduler(self.task_manager)
        self.resource_allocator = ResourceAllocator(self.task_scheduler)
        self.notification_system = NotificationSystem(self.resource_allocator)

    def create_project(self, name: str):
        project = Project(len(self.projects) + 1, name, self.task_manager.tasks, self.resource_allocator.resources)
        self.projects.append(project)
        return project

    def display_project_info(self, project_id: int):
        for project in self.projects:
            if project.id == project_id:
                print(f"Project {project.id}: {project.name}")
                for task in project.tasks:
                    print(f"Task {task.id}: {task.description}, Due Date: {task.due_date}, Priority: {task.priority.name}, Assigned Members: {task.assigned_members}")
                for resource in project.resources:
                    print(f"Resource {resource.id}: {resource.name}, Type: {resource.type}, Allocated Tasks: {resource.allocated_tasks}")
                return

    def start_project(self, project_id: int):
        for project in self.projects:
            if project.id == project_id:
                self.task_scheduler.schedule_tasks()
                self.resource_allocator.allocate_resources()
                self.notification_system.send_notifications()
                return

# Main function
def main():
    project_manager = ProjectManager()
    project_manager.create_project("Project 1")
    task = project_manager.task_manager.create_task("Task 1", datetime.date(2024, 3, 15), Priority.HIGH, ["John", "Alice"])
    project_manager.display_project_info(1)
    project_manager.start_project(1)

if __name__ == "__main__":
    main()