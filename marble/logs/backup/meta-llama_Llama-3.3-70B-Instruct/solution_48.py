def __init__(self):def create_user(self, id: int, name: str, role: str):
    self.users[id] = User(id, name, role)
    # Generate a token for the user
    token = str(uuid.uuid4())
    self.tokens[id] = tokendef create_task(self, token: str, id: int, title: str, description: str, deadline: datetime.date, priority: str, assigned_to_id: int):
        if not self.authenticate(token):
            print("Authentication failed")
            return
        assigned_to = self.users.get(assigned_to_id)
        if assigned_to and assigned_to.role in ['admin', 'user']:
            self.tasks[id] = Task(id, title, description, deadline, priority, "Not Started", assigned_to)
        else:
            print("User not found or does not have the necessary role")        if not self.authenticate(token):
            print("Authentication failed")
            return
        assigned_to = self.users.get(assigned_to_id)
        if assigned_to:
            self.tasks[id] = Task(id, title, description, deadline, priority, "Not Started", assigned_to)
        else:
            print("User not found")        assigned_to = self.users.get(assigned_to_id)
        if assigned_to:
            self.tasks[id] = Task(id, title, description, deadline, priority, "Not Started", assigned_to)
        else:
            print("User not found")

    def assign_task(self, task_id: int, user_id: int):def update_task_status(self, token: str, task_id: int, status: str):
        if not self.authenticate(token):
            print("Authentication failed")
            return
        task = self.tasks.get(task_id)
        if task:
            task.update_status(status)
        else:
            print("Task not found")        task.update_status(status)
        else:
            print("Task not found")

    def add_comment_to_task(self, task_id: int, comment: str):def add_attachment_to_task(self, token: str, task_id: int, attachment: str):
        if not self.authenticate(token):
            print("Authentication failed")
            return
        task = self.tasks.get(task_id)
        if task:
            task.add_attachment(attachment)
        else:
            print("Task not found")        task.add_attachment(attachment)
        else:
            print("Task not found")

    def generate_report(self):
        """
        Generate a report on task progress.
        """
        report = {}
        for task in self.tasks.values():
            if task.status not in report:
                report[task.status] = []
            report[task.status].append(task.title)
        return report

# Define test cases
class TestOfficeTaskCollaborationManager(unittest.TestCase):
    def test_create_user(self):
        manager = OfficeTaskCollaborationManager()
        manager.create_user(1, "John Doe", "admin")
        self.assertIn(1, manager.users)

    def test_create_task(self):
        manager = OfficeTaskCollaborationManager()
        manager.create_user(1, "John Doe", "admin")
        manager.create_task(1, "Task 1", "Description 1", datetime.date(2024, 9, 16), "high", 1)
        self.assertIn(1, manager.tasks)

    def test_assign_task(self):
        manager = OfficeTaskCollaborationManager()
        manager.create_user(1, "John Doe", "admin")
        manager.create_task(1, "Task 1", "Description 1", datetime.date(2024, 9, 16), "high", 1)
        manager.assign_task(1, 1)
        self.assertEqual(manager.tasks[1].assigned_to.id, 1)

    def test_update_task_status(self):
        manager = OfficeTaskCollaborationManager()
        manager.create_user(1, "John Doe", "admin")
        manager.create_task(1, "Task 1", "Description 1", datetime.date(2024, 9, 16), "high", 1)
        manager.update_task_status(1, "In Progress")
        self.assertEqual(manager.tasks[1].status, "In Progress")

    def test_add_comment_to_task(self):
        manager = OfficeTaskCollaborationManager()
        manager.create_user(1, "John Doe", "admin")
        manager.create_task(1, "Task 1", "Description 1", datetime.date(2024, 9, 16), "high", 1)
        manager.add_comment_to_task(1, "Comment 1")
        self.assertIn("Comment 1", manager.tasks[1].comments)

    def test_add_attachment_to_task(self):
        manager = OfficeTaskCollaborationManager()
        manager.create_user(1, "John Doe", "admin")
        manager.create_task(1, "Task 1", "Description 1", datetime.date(2024, 9, 16), "high", 1)
        manager.add_attachment_to_task(1, "Attachment 1")
        self.assertIn("Attachment 1", manager.tasks[1].attachments)

    def test_generate_report(self):
        manager = OfficeTaskCollaborationManager()
        manager.create_user(1, "John Doe", "admin")
        manager.create_task(1, "Task 1", "Description 1", datetime.date(2024, 9, 16), "high", 1)
        manager.create_task(2, "Task 2", "Description 2", datetime.date(2024, 9, 16), "low", 1)
        manager.update_task_status(1, "In Progress")
        manager.update_task_status(2, "Completed")
        report = manager.generate_report()
        self.assertIn("In Progress", report)
        self.assertIn("Completed", report)

if __name__ == "__main__":
    unittest.main()