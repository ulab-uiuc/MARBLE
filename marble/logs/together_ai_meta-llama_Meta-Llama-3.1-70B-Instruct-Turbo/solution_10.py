# models.py
from enum import Enum
from typing import List, Dict

class Role(Enum):
    ADMIN = 1
    MANAGER = 2
    MEMBER = 3

class User:
    def __init__(self, id: int, name: str, role: Role):
        self.id = id
        self.name = name
        self.role = role

class Task:
    def __init__(self, id: int, title: str, description: str, status: str, assigned_to: User):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.assigned_to = assigned_to

class Project:
    def __init__(self, id: int, title: str, tasks: List[Task]):
        self.id = id
        self.title = title
        self.tasks = tasks

# database.py
from typing import List, Dict
from models import User, Task, Project

class Database:
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.tasks: Dict[int, Task] = {}
        self.projects: Dict[int, Project] = {}

    def add_user(self, user: User):
        self.users[user.id] = user

    def add_task(self, task: Task):
        self.tasks[task.id] = task

    def add_project(self, project: Project):
        self.projects[project.id] = project

    def get_user(self, id: int) -> User:
        return self.users.get(id)

    def get_task(self, id: int) -> Task:
        return self.tasks.get(id)

    def get_project(self, id: int) -> Project:
        return self.projects.get(id)

# backend.py
from flask import Flask, jsonify, request
from models import User, Task, Project
from database import Database

app = Flask(__name__)

db = Database()

# Create some sample data
user1 = User(1, "John Doe", Role.ADMIN)
user2 = User(2, "Jane Doe", Role.MEMBER)
task1 = Task(1, "Task 1", "Description 1", "In Progress", user1)
task2 = Task(2, "Task 2", "Description 2", "Done", user2)
project1 = Project(1, "Project 1", [task1, task2])

db.add_user(user1)
db.add_user(user2)
db.add_task(task1)
db.add_task(task2)
db.add_project(project1)

# API Endpoints
@app.route('/users', methods=['GET'])
def get_users():
    users = list(db.users.values())
    return jsonify([user.__dict__ for user in users])

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = list(db.tasks.values())
    return jsonify([task.__dict__ for task in tasks])

@app.route('/projects', methods=['GET'])
def get_projects():
    projects = list(db.projects.values())
    return jsonify([project.__dict__ for project in projects])

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    user = db.get_user(user_id)
    if user:
        return jsonify(user.__dict__)
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id: int):
    task = db.get_task(task_id)
    if task:
        return jsonify(task.__dict__)
    else:
        return jsonify({"error": "Task not found"}), 404

@app.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id: int):
    project = db.get_project(project_id)
    if project:
        return jsonify(project.__dict__)
    else:
        return jsonify({"error": "Project not found"}), 404

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    task = Task(data['id'], data['title'], data['description'], data['status'], db.get_user(data['assigned_to']))
    db.add_task(task)
    return jsonify(task.__dict__), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id: int):
    task = db.get_task(task_id)
    if task:
        data = request.json
        task.title = data['title']
        task.description = data['description']
        task.status = data['status']
        task.assigned_to = db.get_user(data['assigned_to'])
        return jsonify(task.__dict__)
    else:
        return jsonify({"error": "Task not found"}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id: int):
    task = db.get_task(task_id)
    if task:
        del db.tasks[task_id]
        return jsonify({"message": "Task deleted"})
    else:
        return jsonify({"error": "Task not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)

# frontend.py
from flask import Flask, render_template, request, jsonify
from backend import app as backend_app

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    response = backend_app.test_client().get('/tasks')
    return jsonify(response.json)

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    response = backend_app.test_client().post('/tasks', json=data)
    return jsonify(response.json), response.status_code

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id: int):
    response = backend_app.test_client().get(f'/tasks/{task_id}')
    return jsonify(response.json)

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id: int):
    data = request.json
    response = backend_app.test_client().put(f'/tasks/{task_id}', json=data)
    return jsonify(response.json), response.status_code

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id: int):
    response = backend_app.test_client().delete(f'/tasks/{task_id}')
    return jsonify(response.json), response.status_code

if __name__ == '__main__':
    app.run(debug=True)

# reporting.py
from backend import app as backend_app
from flask import jsonify

def generate_project_report(project_id: int):
    project = backend_app.test_client().get(f'/projects/{project_id}').json
    tasks = project['tasks']
    report = {
        'project_id': project_id,
        'project_title': project['title'],
        'tasks': tasks,
        'total_tasks': len(tasks),
        'completed_tasks': sum(1 for task in tasks if task['status'] == 'Done')
    }
    return report

def generate_user_report(user_id: int):
    user = backend_app.test_client().get(f'/users/{user_id}').json
    tasks = backend_app.test_client().get('/tasks').json
    assigned_tasks = [task for task in tasks if task['assigned_to']['id'] == user_id]
    report = {
        'user_id': user_id,
        'user_name': user['name'],
        'tasks': assigned_tasks,
        'total_tasks': len(assigned_tasks),
        'completed_tasks': sum(1 for task in assigned_tasks if task['status'] == 'Done')
    }
    return report

# integration.py
from flask import Flask, jsonify
from backend import app as backend_app
from reporting import generate_project_report, generate_user_report

app = Flask(__name__)

@app.route('/projects/<int:project_id>/report', methods=['GET'])
def get_project_report(project_id: int):
    report = generate_project_report(project_id)
    return jsonify(report)

@app.route('/users/<int:user_id>/report', methods=['GET'])
def get_user_report(user_id: int):
    report = generate_user_report(user_id)
    return jsonify(report)

if __name__ == '__main__':
    app.run(debug=True)