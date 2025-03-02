class Task:
    def __init__(self, name, description, deadline):
        self.name = name
        self.description = description
        self.deadline = deadline
        self.dependencies = []
        self.status = "Pending"
    
    def add_dependency(self, task):
        self.dependencies.append(task)
    
    def get_dependencies(self):
        return self.dependencies
    
    def set_status(self, status):
        self.status = status
    
    def get_status(self):
        return self.status


class Project:
    def __init__(self, name):
        self.name = name
        self.tasks = []
    
    def add_task(self, task):
        self.tasks.append(task)
    
    def get_tasks(self):
        return self.tasks


class MultiAgentProjectManager:
    def __init__(self):
        self.projects = []
    
    def create_project(self, name):
        project = Project(name)
        self.projects.append(project)
        return project
    
    def get_projects(self):
        return self.projects
    
    def find_task(self, project_name, task_name):
        if not self.check_dependencies(task):
            return False

        for project in self.projects:
            if project.name == project_name:
                for task in project.tasks:
                    if task.name == task_name:
                        return task
        return None
    
    def assign_task(self, project_name, task_name, status):
        task = self.find_task(project_name, task_name)
        if task:self.check_dependencies(task)        return False
return False


# Example Usage
project_manager = MultiAgentProjectManager()

# Create a project
project = project_manager.create_project("Project 1")

# Create tasks
task1 = Task("Task 1", "Description for Task 1", "2022-12-31")
task2 = Task("Task 2", "Description for Task 2", "2022-12-31")
task3 = Task("Task 3", "Description for Task 3", "2022-12-31")

# Add dependencies
task3.add_dependency(task1)
task3.add_dependency(task2)

# Add tasks to the project
project.add_task(task1)
project.add_task(task2)
project.add_task(task3)

# Assign tasks
project_manager.assign_task("Project 1", "Task 1", "In Progress")
project_manager.assign_task("Project 1", "Task 2", "Completed")

# Get project tasks
tasks = project.get_tasks()
for task in tasks:
    print(f"Task: {task.name}, Status: {task.get_status()}, Dependencies: {[dep.name for dep in task.get_dependencies()]}")