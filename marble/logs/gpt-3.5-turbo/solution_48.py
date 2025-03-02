class Task:
    def __init__(self, task_id, title, description, assignee, deadline, priority):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.assignee = assignee
        self.deadline = deadline
        self.priority = priority
        self.status = "Not Started"
        self.comments = []
        self.attachments = []

    def update_status(self, new_status):self.status = new_status        self.deadline = deadline

class User:
    def __init__(self, user_id, name, role):
        self.user_id = user_id
        self.name = name
        self.role = role


class OfficeTaskCollaborationManager:
    def __init__(self):
        self.tasks = {}
        self.users = {}

    def create_task(self, task_id, title, description, assignee, deadline, priority):
        if assignee not in self.users:
            return "Assignee not found. Please add the user first."
        task = Task(task_id, title, description, assignee, deadline, priority)
        self.tasks[task_id] = task
        return "Task created successfully."

    def assign_task(self, task_id, assignee_id):
        if task_id not in self.tasks:
            return "Task not found. Please create the task first."
        if assignee_id not in self.users:
            return "Assignee not found. Please add the user first."
        self.tasks[task_id].assignee = assignee_id
        return "Task assigned successfully."

    def update_task_status(self, task_id, new_status):
        if task_id not in self.tasks:
            return "Task not found."
        self.tasks[task_id].update_status(new_status)
        return "Task status updated successfully."

    def add_comment_to_task(self, task_id, comment):
        if task_id not in self.tasks:
            return "Task not found."
        self.tasks[task_id].add_comment(comment)
        return "Comment added successfully."

    def add_attachment_to_task(self, task_id, attachment):
        if task_id not in self.tasks:
            return "Task not found."
        self.tasks[task_id].add_attachment(attachment)
        return "Attachment added successfully."

    def generate_task_report(self):
        completed_tasks = []
        pending_tasks = []
        overdue_tasks = []
        for task_id, task in self.tasks.items():
            if task.status == "Completed":
                completed_tasks.append(task)
            elif task.status == "Not Started":
                if task.deadline < datetime.now():
                    overdue_tasks.append(task)
                else:
                    pending_tasks.append(task)
            elif task.status == "In Progress":
                if task.deadline < datetime.now():
                    overdue_tasks.append(task)
                else:
                    pending_tasks.append(task)
        return {
            "Completed Tasks": completed_tasks,
            "Pending Tasks": pending_tasks,
            "Overdue Tasks": overdue_tasks
        }

    def add_user(self, user_id, name, role):
        user = User(user_id, name, role)
        self.users[user_id] = user
        return "User added successfully."


# Test cases
if __name__ == "__main__":
    office_manager = OfficeTaskCollaborationManager()

    # Add users
    print(office_manager.add_user(1, "Alice", "Manager"))
    print(office_manager.add_user(2, "Bob", "Developer"))

    # Create tasks
    print(office_manager.create_task(1, "Task 1", "Description 1", 2, datetime(2022, 12, 31), "High"))
    print(office_manager.create_task(2, "Task 2", "Description 2", 2, datetime(2022, 11, 30), "Medium"))

    # Assign tasks
    print(office_manager.assign_task(1, 1))

    # Update task status
    print(office_manager.update_task_status(1, "In Progress"))

    # Add comments
    print(office_manager.add_comment_to_task(1, "Work in progress..."))

    # Add attachments
    print(office_manager.add_attachment_to_task(1, "file.txt"))

    # Generate task report
    print(office_manager.generate_task_report())