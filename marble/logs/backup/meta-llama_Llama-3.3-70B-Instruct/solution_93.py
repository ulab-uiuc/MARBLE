def __init__(self):
    self.tasks = []def create_task(self, description: str, due_date: datetime, priority_level: int, team_members: List[str]):
        """Creates a new task."""
        task = Task(description, due_date, priority_level, team_members)
        self.tasks.append(task)
        return task

    def edit_task(self, task: Task, description: str = None, due_date: datetime = None, priority_level: int = None, team_members: List[str] = None):
        """Edits an existing task."""
        if description:
            task.description = description
        if due_date:
            task.due_date = due_date
        if priority_level:
            task.priority_level = priority_level
        if team_members:
            task.team_members = team_members

    def delete_task(self, task: Task):
        """Deletes a task."""
        self.tasks.remove(task)

    def get_tasks(self):
        """Returns a list of all tasks."""
        return self.tasks


class TaskScheduler:
    """Schedules tasks based on dependencies and priority levels."""
    def __init__(self, task_manager: TaskManager):
        self.task_manager = task_manager
        self.scheduled_tasks = []

    def schedule_task(self, task: Task, dependencies: List[Task] = None):
        """Schedules a task."""
        if dependencies:
            for dependency in dependencies:
                if not dependency.completed:
                    raise ValueError("Cannot schedule task with uncompleted dependencies")
        self.scheduled_tasks.append(task)

    def adjust_schedule(self, task: Task):
        """Adjusts the schedule when a task is completed or when changes are made to the project plan."""
        # For simplicity, this example just removes the task from the schedule
        self.scheduled_tasks.remove(task)

    def get_scheduled_tasks(self):
        """Returns a list of scheduled tasks."""
        return self.scheduled_tasks


class ResourceAllocator:    def deallocate_resource(self, task: Task, resource_name: str):
        if task not in self.task_manager.get_tasks():
            raise ValueError('Task does not exist')
        if task not in self.allocated_resources or resource_name not in self.allocated_resources[task]:
            raise ValueError('Resource is not allocated to task')
        quantity = self.allocated_resources[task][resource_name]
        del self.allocated_resources[task][resource_name]
        if not self.allocated_resources[task]:
            del self.allocated_resources[task]
        self.resources[resource_name] += quantity        if task not in self.allocated_resources or resource_name not in self.allocated_resources[task]:
            raise ValueError("Resource is not allocated to task")
        quantity = self.allocated_resources[task][resource_name]
        del self.allocated_resources[task][resource_name]
        self.resources[resource_name] += quantity

    def get_allocated_resources(self, task: Task):
        """Returns the allocated resources for a task."""
        return self.allocated_resources.get(task, {})


class RealTimeUpdater:
    """Provides real-time updates on the status of tasks and resources."""
    def __init__(self, task_scheduler: TaskScheduler, resource_allocator: ResourceAllocator):
        self.task_scheduler = task_scheduler
        self.resource_allocator = resource_allocator

    def update_task_status(self, task: Task):
        """Updates the status of a task."""
        # For simplicity, this example just prints the task status
        print(f"Task {task.description} is {'completed' if task.completed else 'not completed'}")

    def update_resource_status(self, resource_name: str):
        """Updates the status of a resource."""
        # For simplicity, this example just prints the resource status
        print(f"Resource {resource_name} has {self.resource_allocator.resources[resource_name]} available quantity")

    def send_notification(self, message: str):
        """Sends a notification."""
        # For simplicity, this example just prints the notification
        print(f"Notification: {message}")


class UserInterface:
    """Provides a user-friendly interface to interact with the system."""
    def __init__(self, task_manager: TaskManager, task_scheduler: TaskScheduler, resource_allocator: ResourceAllocator, real_time_updater: RealTimeUpdater):
        self.task_manager = task_manager
        self.task_scheduler = task_scheduler
        self.resource_allocator = resource_allocator
        self.real_time_updater = real_time_updater

    def create_task(self):
        """Creates a new task."""
        description = input("Enter task description: ")
        due_date = datetime.strptime(input("Enter task due date (YYYY-MM-DD): "), "%Y-%m-%d")
        priority_level = int(input("Enter task priority level: "))
        team_members = input("Enter task team members (comma-separated): ").split(",")
        task = self.task_manager.create_task(description, due_date, priority_level, team_members)
        print(f"Task created: {task}")

    def schedule_task(self):
        """Schedules a task."""
        task_description = input("Enter task description: ")
        task = next((task for task in self.task_manager.get_tasks() if task.description == task_description), None)
        if task:
            dependencies = input("Enter task dependencies (comma-separated): ").split(",")
            dependencies = [next((t for t in self.task_manager.get_tasks() if t.description == d), None) for d in dependencies]
            self.task_scheduler.schedule_task(task, dependencies)
            print(f"Task scheduled: {task}")
        else:
            print("Task not found")

    def allocate_resource(self):
        """Allocates a resource to a task."""
        task_description = input("Enter task description: ")
        task = next((task for task in self.task_manager.get_tasks() if task.description == task_description), None)
        if task:
            resource_name = input("Enter resource name: ")
            quantity = int(input("Enter resource quantity: "))
            self.resource_allocator.allocate_resource(task, resource_name, quantity)
            print(f"Resource allocated to task: {task}")
        else:
            print("Task not found")

    def update_task_status(self):
        """Updates the status of a task."""
        task_description = input("Enter task description: ")
        task = next((task for task in self.task_manager.get_tasks() if task.description == task_description), None)
        if task:
            self.real_time_updater.update_task_status(task)
        else:
            print("Task not found")

    def update_resource_status(self):
        """Updates the status of a resource."""
        resource_name = input("Enter resource name: ")
        self.real_time_updater.update_resource_status(resource_name)

    def send_notification(self):
        """Sends a notification."""
        message = input("Enter notification message: ")
        self.real_time_updater.send_notification(message)


def main():
    task_manager = TaskManager()
    task_scheduler = TaskScheduler(task_manager)
    resource_allocator = ResourceAllocator(task_scheduler)
    real_time_updater = RealTimeUpdater(task_scheduler, resource_allocator)
    user_interface = UserInterface(task_manager, task_scheduler, resource_allocator, real_time_updater)

    while True:
        print("1. Create task")
        print("2. Schedule task")
        print("3. Allocate resource")
        print("4. Update task status")
        print("5. Update resource status")
        print("6. Send notification")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            user_interface.create_task()
        elif choice == "2":
            user_interface.schedule_task()
        elif choice == "3":
            user_interface.allocate_resource()
        elif choice == "4":
            user_interface.update_task_status()
        elif choice == "5":
            user_interface.update_resource_status()
        elif choice == "6":
            user_interface.send_notification()
        elif choice == "7":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()