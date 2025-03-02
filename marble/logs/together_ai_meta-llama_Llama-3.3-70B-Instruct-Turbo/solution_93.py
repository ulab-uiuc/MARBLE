# solution.py
from datetime import datetime, timedelta
from typing import List, Dict

class Task:
    """Represents a task with description, due date, priority level, and assigned team members."""
    def __init__(self, description: str, due_date: datetime, priority_level: int, team_members: List[str]):
        self.description = description
        self.due_date = due_date
        self.priority_level = priority_level
        self.team_members = team_members
        self.status = "Not Started"

    def __str__(self):
        return f"Task: {self.description}, Due Date: {self.due_date}, Priority Level: {self.priority_level}, Team Members: {self.team_members}, Status: {self.status}"

class TaskManager:
    """Manages tasks, including creation, editing, and deletion."""
    def __init__(self):
        self.tasks = []

    def create_task(self, description: str, due_date: datetime, priority_level: int, team_members: List[str]):
        """Creates a new task."""
        task = Task(description, due_date, priority_level, team_members)
        self.tasks.append(task)
        print(f"Task created: {task}")

    def edit_task(self, task_index: int, description: str = None, due_date: datetime = None, priority_level: int = None, team_members: List[str] = None):
        """Edits an existing task."""
        if task_index < len(self.tasks):
            task = self.tasks[task_index]
            if description:
                task.description = description
            if due_date:
                task.due_date = due_date
            if priority_level:
                task.priority_level = priority_level
            if team_members:
                task.team_members = team_members
            print(f"Task updated: {task}")
        else:self.resources[task_index][resource_name] = quantityprint(f"Resource {resource_name} allocated to task {task.description}.")
self.total_resources[resource_name] = -quantity
                else:
                    print(f"Insufficient {resource_name} available.")
            else:
                self.resources[resource_name] = -quantity
                print(f"Resource {resource_name} allocated to task {task.description}.")
        else:
            print("Task not found.")

    def deallocate_resource(self, task_index: int, resource_name: str, quantity: int):self.total_resources[resource_name] += quantity; self.resources[task_index][resource_name] = 0print(f"Resource {resource_name} deallocated from task {task.description}.")
            else:
                print(f"Resource {resource_name} not allocated to task {task.description}.")
        else:
            print("Task not found.")

class RealTimeUpdater:
    """Provides real-time updates on task and resource status."""
    def __init__(self, task_manager: TaskManager, resource_allocator: ResourceAllocator):
        self.task_manager = task_manager
        self.resource_allocator = resource_allocator

    def update_task_status(self, task_index: int, status: str):
        """Updates the status of a task."""
        if task_index < len(self.task_manager.tasks):
            task = self.task_manager.tasks[task_index]
            task.status = status
            print(f"Task {task.description} status updated to {status}.")
        else:
            print("Task not found.")

    def check_resource_availability(self):
        """Checks the availability of resources."""
        for resource, quantity in self.resource_allocator.resources.items():
            if quantity < 0:
                print(f"Resource {resource} is over-allocated.")

class UserInterface:
    """Provides a user-friendly interface to interact with the system."""
    def __init__(self, task_manager: TaskManager, task_scheduler: TaskScheduler, resource_allocator: ResourceAllocator, real_time_updater: RealTimeUpdater):
        self.task_manager = task_manager
        self.task_scheduler = task_scheduler
        self.resource_allocator = resource_allocator
        self.real_time_updater = real_time_updater

    def display_menu(self):
        """Displays the main menu."""
        print("1. Create Task")
        print("2. Edit Task")
        print("3. Delete Task")
        print("4. Schedule Tasks")
        print("5. Allocate Resource")
        print("6. Deallocate Resource")
        print("7. Update Task Status")
        print("8. Check Resource Availability")
        print("9. Exit")

    def run(self):
        """Runs the user interface."""
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            if choice == "1":
                description = input("Enter task description: ")
                due_date = datetime.strptime(input("Enter task due date (YYYY-MM-DD): "), "%Y-%m-%d")
                priority_level = int(input("Enter task priority level: "))
                team_members = input("Enter task team members (comma-separated): ").split(",")
                self.task_manager.create_task(description, due_date, priority_level, team_members)
            elif choice == "2":
                task_index = int(input("Enter task index: "))
                description = input("Enter new task description: ")
                due_date = datetime.strptime(input("Enter new task due date (YYYY-MM-DD): "), "%Y-%m-%d")
                priority_level = int(input("Enter new task priority level: "))
                team_members = input("Enter new task team members (comma-separated): ").split(",")
                self.task_manager.edit_task(task_index, description, due_date, priority_level, team_members)
            elif choice == "3":
                task_index = int(input("Enter task index: "))
                self.task_manager.delete_task(task_index)
            elif choice == "4":
                self.task_scheduler.schedule_tasks()
            elif choice == "5":
                task_index = int(input("Enter task index: "))
                resource_name = input("Enter resource name: ")
                quantity = int(input("Enter resource quantity: "))
                self.resource_allocator.allocate_resource(task_index, resource_name, quantity)
            elif choice == "6":
                task_index = int(input("Enter task index: "))
                resource_name = input("Enter resource name: ")
                quantity = int(input("Enter resource quantity: "))
                self.resource_allocator.deallocate_resource(task_index, resource_name, quantity)
            elif choice == "7":
                task_index = int(input("Enter task index: "))
                status = input("Enter new task status: ")
                self.real_time_updater.update_task_status(task_index, status)
            elif choice == "8":
                self.real_time_updater.check_resource_availability()
            elif choice == "9":
                break
            else:
                print("Invalid choice. Please try again.")

def main():
    task_manager = TaskManager()
    task_scheduler = TaskScheduler(task_manager)
    resource_allocator = ResourceAllocator(task_manager)
    real_time_updater = RealTimeUpdater(task_manager, resource_allocator)
    user_interface = UserInterface(task_manager, task_scheduler, resource_allocator, real_time_updater)
    user_interface.run()

if __name__ == "__main__":
    main()