# project_organizer.py

class Task:
    """Represents a task with description, due date, priority level, and assigned team members."""
    
    def __init__(self, description, due_date, priority_level, team_members):
        """
        Initializes a Task object.

        Args:
            description (str): Task description.
            due_date (str): Task due date.
            priority_level (str): Task priority level.
            team_members (list): List of team members assigned to the task.
        """
        self.description = description
        self.due_date = due_date
        self.priority_level = priority_level
        self.team_members = team_members
        self.status = "Not Started"

    def update_status(self, status):
        """Updates the task status."""
        self.status = status

    def __str__(self):
        return f"Task: {self.description}, Due Date: {self.due_date}, Priority Level: {self.priority_level}, Team Members: {', '.join(self.team_members)}, Status: {self.status}"


class TaskManager:
    """Manages tasks, including creation, editing, and deletion."""
    
    def __init__(self):
        self.tasks = {}

    def create_task(self, task_id, description, due_date, priority_level, team_members):
        """
        Creates a new task.

        Args:
            task_id (str): Unique task ID.
            description (str): Task description.
            due_date (str): Task due date.
            priority_level (str): Task priority level.
            team_members (list): List of team members assigned to the task.
        """
        self.tasks[task_id] = Task(description, due_date, priority_level, team_members)

    def edit_task(self, task_id, description=None, due_date=None, priority_level=None, team_members=None):
        """
        Edits an existing task.

        Args:
            task_id (str): Unique task ID.
            description (str, optional): New task description. Defaults to None.
            due_date (str, optional): New task due date. Defaults to None.
            priority_level (str, optional): New task priority level. Defaults to None.
            team_members (list, optional): New list of team members assigned to the task. Defaults to None.
        """
        if task_id in self.tasks:
            if description:
                self.tasks[task_id].description = description
            if due_date:
                self.tasks[task_id].due_date = due_date
            if priority_level:
                self.tasks[task_id].priority_level = priority_level
            if team_members:
                self.tasks[task_id].team_members = team_members
        else:
            print("Task not found.")

    def delete_task(self, task_id):
        """
        Deletes a task.

        Args:
            task_id (str): Unique task ID.
        """
        if task_id in self.tasks:
            del self.tasks[task_id]
        else:
            print("Task not found.")

    def __str__(self):
        task_list = "\n".join([str(task) for task in self.tasks.values()])
        return task_list


class TaskScheduler:
    """Schedules tasks based on dependencies and priority levels."""
    
    def __init__(self, task_manager):
        self.task_manager = task_manager
        self.scheduled_tasks = []

    def schedule_task(self, task_id, dependency=None):
        """
        Schedules a task.

        Args:
            task_id (str): Unique task ID.
            dependency (str, optional): ID of the task that this task depends on. Defaults to None.
        """
        if task_id in self.task_manager.tasks:
            self.scheduled_tasks.append((task_id, dependency))
        else:
            print("Task not found.")

    def update_schedule(self):
        """Updates the task schedule based on dependencies and priority levels."""
        # This is a simplified example and does not handle complex dependencies or priority levels.
        self.scheduled_tasks.sort(key=lambda x: self.task_manager.tasks[x[0]].priority_level)

    def __str__(self):
        scheduled_task_list = "\n".join([f"Task: {task_id}, Dependency: {dependency}" for task_id, dependency in self.scheduled_tasks])
        return scheduled_task_list


class ResourceAllocator:
    """Allocates resources to tasks."""
    
    def __init__(self, task_manager):
        self.task_manager = task_manager
        self.resources = {}

    def allocate_resource(self, task_id, resource_name, quantity):
        """
        Allocates a resource to a task.

        Args:
            task_id (str): Unique task ID.
            resource_name (str): Name of the resource.
            quantity (int): Quantity of the resource.
        """
        if task_id in self.task_manager.tasks:
            if resource_name in self.resources:
                if self.resources[resource_name] >= quantity:
                    self.resources[resource_name] -= quantity
                    print(f"Allocated {quantity} {resource_name} to task {task_id}.")
                else:
                    print(f"Not enough {resource_name} available.")
            else:
                print(f"{resource_name} not found.")
        else:
            print("Task not found.")

    def __str__(self):
        resource_list = "\n".join([f"{resource_name}: {quantity}" for resource_name, quantity in self.resources.items()])
        return resource_list


class RealTimeUpdater:
    """Provides real-time updates on task and resource status."""
    
    def __init__(self, task_manager, resource_allocator):
        self.task_manager = task_manager
        self.resource_allocator = resource_allocator

    def update_task_status(self, task_id, status):
        """
        Updates the status of a task.

        Args:
            task_id (str): Unique task ID.
            status (str): New task status.
        """
        if task_id in self.task_manager.tasks:
            self.task_manager.tasks[task_id].update_status(status)
            print(f"Task {task_id} status updated to {status}.")
        else:
            print("Task not found.")

    def update_resource_status(self, resource_name, quantity):
        """
        Updates the quantity of a resource.

        Args:
            resource_name (str): Name of the resource.
            quantity (int): New quantity of the resource.
        """
        if resource_name in self.resource_allocator.resources:
            self.resource_allocator.resources[resource_name] = quantity
            print(f"{resource_name} quantity updated to {quantity}.")
        else:
            print(f"{resource_name} not found.")

    def __str__(self):
        task_list = "\n".join([str(task) for task in self.task_manager.tasks.values()])
        resource_list = "\n".join([f"{resource_name}: {quantity}" for resource_name, quantity in self.resource_allocator.resources.items()])
        return task_list + "\n" + resource_list


class ProjectOrganizer:
    """Manages project tasks and resources."""
    
    def __init__(self):
        self.task_manager = TaskManager()
        self.task_scheduler = TaskScheduler(self.task_manager)
        self.resource_allocator = ResourceAllocator(self.task_manager)
        self.real_time_updater = RealTimeUpdater(self.task_manager, self.resource_allocator)

    def create_task(self, task_id, description, due_date, priority_level, team_members):
        self.task_manager.create_task(task_id, description, due_date, priority_level, team_members)

    def schedule_task(self, task_id, dependency=None):
        self.task_scheduler.schedule_task(task_id, dependency)

    def allocate_resource(self, task_id, resource_name, quantity):
        self.resource_allocator.allocate_resource(task_id, resource_name, quantity)

    def update_task_status(self, task_id, status):
        self.real_time_updater.update_task_status(task_id, status)

    def update_resource_status(self, resource_name, quantity):
        self.real_time_updater.update_resource_status(resource_name, quantity)

    def __str__(self):
        task_list = str(self.task_manager)
        scheduled_task_list = str(self.task_scheduler)
        resource_list = str(self.resource_allocator)
        return task_list + "\n" + scheduled_task_list + "\n" + resource_list


# Example usage
project_organizer = ProjectOrganizer()

project_organizer.create_task("T1", "Task 1", "2024-03-16", "High", ["John", "Alice"])
project_organizer.create_task("T2", "Task 2", "2024-03-17", "Medium", ["Bob", "Charlie"])
project_organizer.create_task("T3", "Task 3", "2024-03-18", "Low", ["David", "Eve"])

project_organizer.schedule_task("T1")
project_organizer.schedule_task("T2", "T1")
project_organizer.schedule_task("T3", "T2")

project_organizer.resource_allocator.resources["Personnel"] = 10
project_organizer.resource_allocator.resources["Equipment"] = 5
project_organizer.resource_allocator.resources["Budget"] = 1000

project_organizer.allocate_resource("T1", "Personnel", 2)
project_organizer.allocate_resource("T2", "Equipment", 1)
project_organizer.allocate_resource("T3", "Budget", 500)

project_organizer.update_task_status("T1", "In Progress")
project_organizer.update_task_status("T2", "Not Started")
project_organizer.update_task_status("T3", "Completed")

project_organizer.update_resource_status("Personnel", 8)
project_organizer.update_resource_status("Equipment", 4)
project_organizer.update_resource_status("Budget", 500)

print(project_organizer)