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

    def edit_task(self, description=None, due_date=None, priority=None, assigned_members=None):
        """
        Edits the task details.
        
        :param description: New description of the task
        :param due_date: New due date of the task
        :param priority: New priority level of the task
        :param assigned_members: New list of team members assigned to the task
        """
        if description:
            self.description = description
        if due_date:
            self.due_date = due_date
        if priority:
            self.priority = priority
        if assigned_members:
            self.assigned_members = assigned_members

    def mark_completed(self):
        """Marks the task as completed."""
        self.completed = True


class TaskManager:
    def __init__(self):
        """Initializes the task manager with an empty task list."""
        self.tasks = []

    def create_task(self, description, due_date, priority, assigned_members):
        """
        Creates a new task and adds it to the task list.
        
        :param description: Description of the task
        :param due_date: Due date of the task
        :param priority: Priority level of the task
        :param assigned_members: List of team members assigned to the task
        """        if not description:
            raise ValueError('Description cannot be empty.')
        if not isinstance(due_date, str):
            raise ValueError('Due date must be a string.')
        if not assigned_members or not isinstance(assigned_members, list):
            raise ValueError('Assigned members must be a non-empty list.')
        if priority not in ['low', 'medium', 'high']:
            raise ValueError('Priority must be one of: low, medium, high.')
        new_task = Task(description, due_date, priority, assigned_members)        self.tasks.append(new_task)

    def delete_task(self, task):
        """
        Deletes a task from the task list.
        
        :param task: The task to be deleted
        """
        self.tasks.remove(task)

    def get_all_tasks(self):
        """Returns a list of all tasks."""
        return self.tasks


# This module handles task scheduling based on dependencies and priority levels
class TaskScheduler:
    def __init__(self, task_manager):
        """
        Initializes the task scheduler with a reference to the task manager.
        
        :param task_manager: An instance of TaskManager
        """
        self.task_manager = task_manager

    def schedule_tasks(self):
        """
        Schedules tasks based on their priority and due date.
        This is a simple implementation that sorts tasks by priority and due date.
        """
        self.task_manager.tasks.sort(key=lambda x: (x.priority, x.due_date))

    def complete_task(self, task):
        """
        Marks a task as completed and reschedules tasks if necessary.
        
        :param task: The task to be marked as completed
        """
        task.mark_completed()
        self.schedule_tasks()


# This module handles resource allocation to tasks
class ResourceAllocator:
    def __init__(self):
        """Initializes the resource allocator with an empty resource allocation dictionary."""
        self.resource_allocation = {}

    def allocate_resource(self, task, resource):
        """
        Allocates a resource to a task.
        
        :param task: The task to which the resource is allocated
        :param resource: The resource being allocated
        """
        if task not in self.resource_allocation:
            self.resource_allocation[task] = []
        self.resource_allocation[task].append(resource)

    def check_over_allocation(self):
        """
        Checks for over-allocated resources and returns a list of alerts.
        
        :return: List of alerts for over-allocated resources
        """
        alerts = []
        for task, resources in self.resource_allocation.items():
            if len(resources) > 1:  # Example condition for over-allocation
                alerts.append(f"Task '{task.description}' has over-allocated resources: {resources}")
        return alerts


# This module handles real-time updates and notifications
class NotificationSystem:
    def __init__(self):
        """Initializes the notification system."""
        self.notifications = []

    def notify_task_completed(self, task):
        """Sends a notification when a task is completed."""
        self.notifications.append(f"Task '{task.description}' has been completed.")

    def notify_resource_over_allocation(self, alerts):
        """Sends notifications for over-allocated resources."""
        for alert in alerts:
            self.notifications.append(alert)

    def notify_due_date_approaching(self, task):
        """Sends a notification when a task's due date is approaching."""
        self.notifications.append(f"Task '{task.description}' is approaching its due date.")


# Example usage of the ProjectOrganizer system
if __name__ == "__main__":
    # Create instances of the managers
    task_manager = TaskManager()
    task_scheduler = TaskScheduler(task_manager)
    resource_allocator = ResourceAllocator()
    notification_system = NotificationSystem()

    # Create some tasks
    task_manager.create_task("Design the project architecture", "2023-10-15", "high", ["Alice", "Bob"])
    task_manager.create_task("Implement the user interface", "2023-10-20", "medium", ["Charlie"])
    
    # Schedule tasks
    task_scheduler.schedule_tasks()

    # Allocate resources
    task = task_manager.tasks[0]
    resource_allocator.allocate_resource(task, "Development Team")
    
    # Check for over-allocation
    alerts = resource_allocator.check_over_allocation()
    notification_system.notify_resource_over_allocation(alerts)

    # Complete a task and notify
    task_scheduler.complete_task(task)
    notification_system.notify_task_completed(task)

    # Print notifications
    for notification in notification_system.notifications:
        print(notification)