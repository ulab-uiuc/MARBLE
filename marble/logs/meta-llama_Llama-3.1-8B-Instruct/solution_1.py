# Define a class called 'Employee' to represent an employee
class Employee:
    # Initialize the employee with a name and an ID
    def __init__(self, name, employee_id):
        self.name = name
        self.employee_id = employee_id
        self.projects = []  # List to store the projects assigned to the employee

    # Method to add a project to the employee's list of projects
    def add_project(self, project_name):
        self.projects.append(project_name)

    # Method to display the employee's details
    def display_details(self):
        print(f"Name: {self.name}")
        print(f"Employee ID: {self.employee_id}")
        print(f"Projects: {', '.join(self.projects)}")


# Define a class called 'Project' to represent a project
class Project:
    # Initialize the project with a name and a description
    def __init__(self, name, description):
        self.name = name
        self.description = description

    # Method to display the project's details
    def display_details(self):
        print(f"Name: {self.name}")
        print(f"Description: {self.description}")


# Define a class called 'ProjectManager' to manage projects and employees
class ProjectManager:
    # Initialize the project manager with a list of employees and projects
    def __init__(self):
        self.employees = []  # List to store the employees
        self.projects = []  # List to store the projects

    # Method to add an employee to the list of employees
    def add_employee(self, employee):
        self.employees.append(employee)

    # Method to add a project to the list of projects
    def add_project(self, project):
        self.projects.append(project)

    # Method to assign a project to an employee
    def assign_project(self, employee_id, project_name):
        for employee in self.employees:
            if employee.employee_id == employee_id:
                employee.add_project(project_name)
                print(f"Project '{project_name}' assigned to employee {employee_id}")
                return
        print(f"Employee with ID {employee_id} not found")

    # Method to display the details of all employees and projects
    def display_details(self):
        for employee in self.employees:
            employee.display_details()
            print()
        for project in self.projects:
            project.display_details()
            print()


# Create an instance of the ProjectManager class
project_manager = ProjectManager()

# Create instances of the Employee and Project classes
employee1 = Employee("John Doe", 1)
employee2 = Employee("Jane Doe", 2)
project1 = Project("Project A", "This is project A")
project2 = Project("Project B", "This is project B")

# Add employees and projects to the project manager
project_manager.add_employee(employee1)
project_manager.add_employee(employee2)
project_manager.add_project(project1)
project_manager.add_project(project2)

# Assign projects to employees
project_manager.assign_project(1, "Project A")
project_manager.assign_project(2, "Project B")

# Display the details of all employees and projects
project_manager.display_details()

# The task description is: Software Development Task: Please write a program called. Based on this task description, I have implemented the solution.