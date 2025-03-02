# solution.py

# This module handles task creation and management
class Task:
    def __init__(self, description, due_date, priority, assigned_members):
        """
        Initializes a new task with the given parameters.
        
        :param description: Description of the task
        :param due_date: Due date of the task
        :param priority: Priority level of the task (e.g., low, medium, high)
        :param assigned_members: List of team members assigned to the task
        """
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.assigned_members = assigned_members
        self.completed = False

    def mark_completed(self):
        """Marks the task as completed."""
        self.completed = True

    def edit_task(self, description=None, due_date=None, priority=None, assigned_members=None):
        """
        Edits the task details.
        
        :param description: New description of the task
        :param due_date: New due date of the task
        :param priority: New priority level of the task
        :param assigned_members: New list of assigned team members
        """
        if description:
            self.description = description
        if due_date:
            self.due_date = due_date
        if priority:
            self.priority = priority
        if assigned_members:
            self.assigned_members = assigned_members

# This module handles task scheduling based on dependencies and priority levels
class TaskScheduler:
    def __init__(self):
        """Initializes the task scheduler with an empty task list."""
        self.tasks = []

    def add_task(self, task):
        """Adds a new task to the scheduler."""
        self.tasks.append(task)        self.tasks.append(task)

    def schedule_tasks(self):    def complete_task(self, task):
        """Marks a task as completed and reschedules tasks if necessary."""
        task.mark_completed()
        self.schedule_tasks()

# This module handles resource allocation to tasks
class ResourceAllocator:
    def __init__(self):
        """Initializes the resource allocator with an empty resource list."""
        self.resources = {}
        self.task_resources = {}

    def allocate_resource(self, task, resource):
        """
        Allocates a resource to a task.
        
        :param task: The task to which the resource is allocated
        :param resource: The resource being allocated
        """
        if resource not in self.resources:
            self.resources[resource] = 0
        self.resources[resource] += 1
        self.task_resources.setdefault(task, []).append(resource)

    def check_over_allocation(self):
        """Checks for over-allocated resources and returns a list of them."""
        over_allocated = [resource for resource, count in self.resources.items() if count > 1]
        return over_allocated

# This module handles real-time updates and notifications
class NotificationSystem:
    def notify_task_completed(self, task):
        """Notifies users when a task is completed."""
        print(f"Task '{task.description}' has been completed.")

    def notify_resource_over_allocated(self, resource):
        """Notifies users when a resource is over-allocated."""
        print(f"Resource '{resource}' is over-allocated.")

    def notify_due_date_approaching(self, task):
        """Notifies users when a task is approaching its due date."""
        print(f"Task '{task.description}' is approaching its due date.")

# Example usage of the ProjectOrganizer system
if __name__ == "__main__":
    # Create tasks
    task1 = Task("Design the project architecture", "2023-10-15", "high", ["Alice", "Bob"])
    task2 = Task("Implement the user interface", "2023-10-20", "medium", ["Charlie"])
    
    # Manage tasks
    scheduler = TaskScheduler()
    scheduler.add_task(task1)
    scheduler.add_task(task2)
    scheduler.schedule_tasks()

    # Allocate resources
    allocator = ResourceAllocator()
    allocator.allocate_resource(task1, "Developer A")
    allocator.allocate_resource(task1, "Developer B")
    allocator.allocate_resource(task2, "Developer C")

    # Check for over-allocated resources
    over_allocated_resources = allocator.check_over_allocation()
    for resource in over_allocated_resources:
        NotificationSystem().notify_resource_over_allocated(resource)

    # Complete a task and notify
    scheduler.complete_task(task1)
    NotificationSystem().notify_task_completed(task1)