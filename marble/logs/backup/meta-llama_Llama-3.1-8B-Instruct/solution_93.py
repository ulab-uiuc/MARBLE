# task.py
class Task:
    def __init__(self, description, due_date, priority, team_members):
        """
        Initialize a Task object.

        Args:
            description (str): Task description.
            due_date (str): Task due date in YYYY-MM-DD format.
            priority (str): Task priority level (High, Medium, Low).
            team_members (list): List of team members assigned to the task.
        """
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.team_members = team_members
        self.status = "Not Started"
        self.completed = False

    def start_task(self):
        """
        Mark the task as started.
        """
        self.status = "In Progress"

    def complete_task(self):
        """
        Mark the task as completed.
        """
        self.status = "Completed"
        self.completed = True

    def __str__(self):
        return f"Task: {self.description}\nDue Date: {self.due_date}\nPriority: {self.priority}\nTeam Members: {', '.join(self.team_members)}\nStatus: {self.status}"


# task_manager.py
class TaskManager:
    def __init__(self):
        """
        Initialize a TaskManager object.
        """
        self.tasks = {}

    def create_task(self, task_id, description, due_date, priority, team_members):
        """
        Create a new task.

        Args:
            task_id (str): Unique task ID.
            description (str): Task description.
            due_date (str): Task due date in YYYY-MM-DD format.
            priority (str): Task priority level (High, Medium, Low).
            team_members (list): List of team members assigned to the task.

        Returns:
            Task: The created task object.
        """
        task = Task(description, due_date, priority, team_members)
        self.tasks[task_id] = task
        return task

    def get_task(self, task_id):
        """
        Get a task by its ID.

        Args:
            task_id (str): Unique task ID.

        Returns:
            Task: The task object if found, otherwise None.
        """
        return self.tasks.get(task_id)

    def update_task(self, task_id, description=None, due_date=None, priority=None, team_members=None):
        """
        Update a task.

        Args:
            task_id (str): Unique task ID.
            description (str, optional): Task description. Defaults to None.
            due_date (str, optional): Task due date in YYYY-MM-DD format. Defaults to None.
            priority (str, optional): Task priority level (High, Medium, Low). Defaults to None.
            team_members (list, optional): List of team members assigned to the task. Defaults to None.

        Returns:
            Task: The updated task object.
        """
        task = self.get_task(task_id)
        if task:
            if description:
                task.description = description
            if due_date:
                task.due_date = due_date
            if priority:
                task.priority = priority
            if team_members:
                task.team_members = team_members
        return task

    def delete_task(self, task_id):
        """
        Delete a task.

        Args:
            task_id (str): Unique task ID.
        """
        if task_id in self.tasks:
            del self.tasks[task_id]


# solution.py
class ProjectOrganizer:
    def __init__(self):
        """
        Initialize a ProjectOrganizer object.
        """
        self.task_manager = TaskManager()

    def create_task(self, task_id, description, due_date, priority, team_members):
        """
        Create a new task.

        Args:
            task_id (str): Unique task ID.
            description (str): Task description.
            due_date (str): Task due date in YYYY-MM-DD format.
            priority (str): Task priority level (High, Medium, Low).
            team_members (list): List of team members assigned to the task.

        Returns:
            Task: The created task object.
        """
        return self.task_manager.create_task(task_id, description, due_date, priority, team_members)

    def get_task(self, task_id):
        """
        Get a task by its ID.

        Args:
            task_id (str): Unique task ID.

        Returns:
            Task: The task object if found, otherwise None.
        """
        return self.task_manager.get_task(task_id)

    def update_task(self, task_id, description=None, due_date=None, priority=None, team_members=None):
        """
        Update a task.

        Args:
            task_id (str): Unique task ID.
            description (str, optional): Task description. Defaults to None.
            due_date (str, optional): Task due date in YYYY-MM-DD format. Defaults to None.
            priority (str, optional): Task priority level (High, Medium, Low). Defaults to None.
            team_members (list, optional): List of team members assigned to the task. Defaults to None.

        Returns:
            Task: The updated task object.
        """
        return self.task_manager.update_task(task_id, description, due_date, priority, team_members)

    def delete_task(self, task_id):
        """
        Delete a task.

        Args:
            task_id (str): Unique task ID.
        """
        self.task_manager.delete_task(task_id)


# main.py
if __name__ == "__main__":
    organizer = ProjectOrganizer()

    task1 = organizer.create_task("T1", "Task 1", "2024-07-31", "High", ["John", "Alice"])
    print(task1)

    task2 = organizer.create_task("T2", "Task 2", "2024-08-15", "Medium", ["Bob", "Charlie"])
    print(task2)

    updated_task = organizer.update_task("T1", description="Updated Task 1")
    print(updated_task)

    organizer.delete_task("T2")
    print(organizer.get_task("T2"))